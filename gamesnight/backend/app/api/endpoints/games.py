from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.models import User, Room, GameSession
from app.services.game_logic import game_logic_service
from app.schemas.room import GameStateUpdate

router = APIRouter()


@router.post("/rooms/{room_id}/start")
async def start_game(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Start a game session"""
    # Verify user is host
    room = await db.get(Room, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if room.host_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the host can start the game"
        )
    
    # Get game session
    session = await db.get(GameSession, {"room_id": room_id})
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game session not found"
        )
    
    # Load prompts for the session
    theme_ids = session.game_state.get("themes", [])
    prompt_ids = await game_logic_service.load_prompts_for_session(
        db, room.game_slug, theme_ids, room_id
    )
    
    if not prompt_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No prompts available for selected themes"
        )
    
    # Update room status
    room.status = "active"
    session.game_state["status"] = "active"
    session.game_state["prompt_count"] = len(prompt_ids)
    
    await db.commit()
    
    return {
        "success": True,
        "prompt_count": len(prompt_ids),
        "game_slug": room.game_slug
    }


@router.get("/rooms/{room_id}/next-prompt")
async def get_next_prompt(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get the next prompt for the game"""
    # Get room
    room = await db.get(Room, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Get next prompt
    prompt = await game_logic_service.get_next_prompt(
        db, room_id, room.game_slug
    )
    
    if not prompt:
        return {"success": False, "message": "No more prompts available"}
    
    return {
        "success": True,
        "prompt": prompt,
        "game_slug": room.game_slug
    }


@router.post("/rooms/{room_id}/action")
async def process_game_action(
    room_id: int,
    action_data: GameStateUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Process a game action"""
    # Get room
    room = await db.get(Room, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Add user ID to data
    data = action_data.data
    data["user_id"] = current_user.id
    
    # Process action
    result = await game_logic_service.process_game_action(
        room_id,
        room.game_slug,
        action_data.action,
        data
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result


@router.post("/rooms/{room_id}/end")
async def end_game(
    room_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """End a game session"""
    # Verify user is host
    room = await db.get(Room, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if room.host_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the host can end the game"
        )
    
    # Update room status
    room.status = "closed"
    
    # Get session and update
    session = await db.get(GameSession, {"room_id": room_id})
    if session:
        session.game_state["status"] = "ended"
    
    await db.commit()
    
    return {"success": True, "message": "Game ended"}