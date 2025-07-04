import socketio
import json
from typing import Dict, Optional
from datetime import datetime

from app.core.redis_client import redis_client
from app.core.security import decode_token

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",  # Configure based on your needs
    logger=True,
    engineio_logger=True
)

# Store user sessions
user_sessions: Dict[str, dict] = {}


@sio.event
async def connect(sid, environ, auth):
    """Handle client connection"""
    print(f"Client {sid} connected")
    
    # Verify authentication
    if auth and 'token' in auth:
        payload = decode_token(auth['token'])
        if payload:
            user_id = payload.get('sub')
            user_sessions[sid] = {
                'user_id': user_id,
                'room_id': None,
                'connected_at': datetime.utcnow()
            }
            await sio.emit('connected', {'message': 'Connected successfully'}, to=sid)
        else:
            await sio.disconnect(sid)
    else:
        # Allow guest connections but mark them
        user_sessions[sid] = {
            'user_id': None,
            'room_id': None,
            'is_guest': True,
            'connected_at': datetime.utcnow()
        }


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client {sid} disconnected")
    
    if sid in user_sessions:
        session = user_sessions[sid]
        if session.get('room_id'):
            await leave_room(sid, {'room_id': session['room_id']})
        del user_sessions[sid]


@sio.event
async def join_room(sid, data):
    """Join a game room"""
    room_id = data.get('room_id')
    if not room_id:
        return {'error': 'Room ID required'}
    
    room_key = f"room:{room_id}"
    
    # Check if room exists
    exists = await redis_client.exists(room_key)
    if not exists:
        return {'error': 'Room not found'}
    
    # Join Socket.IO room
    await sio.enter_room(sid, room_key)
    
    # Update session
    if sid in user_sessions:
        user_sessions[sid]['room_id'] = room_id
    
    # Notify others
    await sio.emit(
        'user_joined',
        {
            'user_id': user_sessions[sid].get('user_id'),
            'timestamp': datetime.utcnow().isoformat()
        },
        room=room_key,
        skip_sid=sid
    )
    
    return {'success': True, 'room_id': room_id}


@sio.event
async def leave_room(sid, data):
    """Leave a game room"""
    room_id = data.get('room_id')
    if not room_id:
        return {'error': 'Room ID required'}
    
    room_key = f"room:{room_id}"
    
    # Leave Socket.IO room
    await sio.leave_room(sid, room_key)
    
    # Update session
    if sid in user_sessions:
        user_sessions[sid]['room_id'] = None
    
    # Notify others
    await sio.emit(
        'user_left',
        {
            'user_id': user_sessions[sid].get('user_id'),
            'timestamp': datetime.utcnow().isoformat()
        },
        room=room_key,
        skip_sid=sid
    )
    
    return {'success': True}


@sio.event
async def game_action(sid, data):
    """Handle game actions"""
    if sid not in user_sessions:
        return {'error': 'Not authenticated'}
    
    session = user_sessions[sid]
    room_id = session.get('room_id')
    
    if not room_id:
        return {'error': 'Not in a room'}
    
    room_key = f"room:{room_id}"
    action_type = data.get('type')
    action_data = data.get('data', {})
    
    # Broadcast to all users in room
    await sio.emit(
        'game_update',
        {
            'type': action_type,
            'data': action_data,
            'user_id': session.get('user_id'),
            'timestamp': datetime.utcnow().isoformat()
        },
        room=room_key
    )
    
    # Store in Redis for persistence
    await redis_client.lpush(
        f"room:{room_id}:actions",
        json.dumps({
            'type': action_type,
            'data': action_data,
            'user_id': session.get('user_id'),
            'timestamp': datetime.utcnow().isoformat()
        })
    )
    
    return {'success': True}


@sio.event
async def start_timer(sid, data):
    """Start a synchronized timer"""
    if sid not in user_sessions:
        return {'error': 'Not authenticated'}
    
    session = user_sessions[sid]
    room_id = session.get('room_id')
    
    if not room_id:
        return {'error': 'Not in a room'}
    
    duration = data.get('duration', 60)  # Default 60 seconds
    t0 = datetime.utcnow().timestamp()
    
    # Store timer info in Redis
    await redis_client.hset(
        f"room:{room_id}",
        "timer_start",
        str(t0)
    )
    await redis_client.hset(
        f"room:{room_id}",
        "timer_duration",
        str(duration)
    )
    
    # Broadcast timer sync
    await sio.emit(
        'timer_sync',
        {
            't0': t0,
            'duration': duration
        },
        room=f"room:{room_id}"
    )
    
    return {'success': True, 't0': t0, 'duration': duration}


@sio.event
async def drawing_stroke(sid, data):
    """Handle drawing strokes for Draw & Guess game"""
    if sid not in user_sessions:
        return {'error': 'Not authenticated'}
    
    session = user_sessions[sid]
    room_id = session.get('room_id')
    
    if not room_id:
        return {'error': 'Not in a room'}
    
    # Broadcast stroke to all other users in room
    await sio.emit(
        'stroke_update',
        {
            'stroke': data.get('stroke'),
            'user_id': session.get('user_id')
        },
        room=f"room:{room_id}",
        skip_sid=sid
    )
    
    return {'success': True}


def create_socketio_app():
    """Create the Socket.IO ASGI app"""
    return socketio.ASGIApp(sio, other_asgi_app=None)