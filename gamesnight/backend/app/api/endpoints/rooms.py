from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_active_user, get_current_paid_user
from app.models import Room, RoomParticipant, User, GameSession
from app.schemas.room import RoomCreate, RoomResponse, RoomJoin, ParticipantResponse
from app.core.redis_client import redis_client

router = APIRouter()


@router.post("/", response_model=RoomResponse)
async def create_room(
    room_data: RoomCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Validate game slug
    valid_games = ["would_you_rather", "truth_or_dare", "sixty_seconds", "hot_seat", "draw_guess"]
    if room_data.game_slug not in valid_games:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid game slug"
        )
    
    # Create room
    db_room = Room(
        host_id=current_user.id,
        game_slug=room_data.game_slug
    )
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    
    # Add host as participant
    db_participant = RoomParticipant(
        room_id=db_room.id,
        user_id=current_user.id,
        is_approved=True
    )
    db.add(db_participant)
    
    # Create game session
    db_session = GameSession(
        room_id=db_room.id,
        game_state={"themes": room_data.theme_ids, "status": "waiting"}
    )
    db.add(db_session)
    
    await db.commit()
    
    # Initialize room in Redis
    await redis_client.hset(
        f"room:{db_room.id}",
        "status",
        "waiting"
    )
    
    return RoomResponse(
        **db_room.__dict__,
        participant_count=1
    )


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.participants))
    )
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    return RoomResponse(
        **room.__dict__,
        participant_count=len(room.participants)
    )


@router.get("/invite/{invite_code}", response_model=RoomResponse)
async def get_room_by_invite(
    invite_code: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Room)
        .where(Room.invite_code == invite_code)
        .options(selectinload(Room.participants))
    )
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invite code"
        )
    
    if room.status == "closed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This room is closed"
        )
    
    return RoomResponse(
        **room.__dict__,
        participant_count=len(room.participants)
    )


@router.post("/{room_id}/join", response_model=ParticipantResponse)
async def join_room(
    room_id: int,
    join_data: RoomJoin,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Get room
    result = await db.execute(
        select(Room)
        .where(Room.id == room_id)
        .options(selectinload(Room.participants))
    )
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user already in room
    existing = next(
        (p for p in room.participants if p.user_id == current_user.id),
        None
    )
    if existing:
        return ParticipantResponse.from_orm(existing)
    
    # Add participant
    db_participant = RoomParticipant(
        room_id=room_id,
        user_id=current_user.id,
        is_approved=room.host_id == current_user.id  # Auto-approve host
    )
    db.add(db_participant)
    await db.commit()
    await db.refresh(db_participant)
    
    return ParticipantResponse.from_orm(db_participant)


@router.post("/{room_id}/join-guest", response_model=ParticipantResponse)
async def join_room_as_guest(
    room_id: int,
    join_data: RoomJoin,
    db: AsyncSession = Depends(get_db)
):
    if not join_data.guest_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Guest name is required"
        )
    
    # Get room
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if host is paid user (only paid users can invite guests)
    host_result = await db.execute(select(User).where(User.id == room.host_id))
    host = host_result.scalar_one()
    
    if not host.is_paid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only paid users can invite guests"
        )
    
    # Add guest participant
    db_participant = RoomParticipant(
        room_id=room_id,
        guest_name=join_data.guest_name,
        is_guest=True,
        is_approved=False  # Guests need host approval
    )
    db.add(db_participant)
    await db.commit()
    await db.refresh(db_participant)
    
    return ParticipantResponse.from_orm(db_participant)


@router.put("/{room_id}/participants/{participant_id}/approve")
async def approve_participant(
    room_id: int,
    participant_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify user is host
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    
    if not room or room.host_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the host can approve participants"
        )
    
    # Update participant
    result = await db.execute(
        select(RoomParticipant)
        .where(RoomParticipant.id == participant_id)
        .where(RoomParticipant.room_id == room_id)
    )
    participant = result.scalar_one_or_none()
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found"
        )
    
    participant.is_approved = True
    await db.commit()
    
    return {"message": "Participant approved"}


@router.get("/{room_id}/participants", response_model=List[ParticipantResponse])
async def get_room_participants(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(RoomParticipant)
        .where(RoomParticipant.room_id == room_id)
        .order_by(RoomParticipant.joined_at)
    )
    participants = result.scalars().all()
    
    return [ParticipantResponse.from_orm(p) for p in participants]