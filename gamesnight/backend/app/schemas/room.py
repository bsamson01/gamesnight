from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class RoomCreate(BaseModel):
    game_slug: str
    theme_ids: List[int]


class RoomResponse(BaseModel):
    id: int
    host_id: int
    game_slug: str
    invite_code: str
    status: str
    created_at: datetime
    participant_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


class RoomJoin(BaseModel):
    guest_name: Optional[str] = None


class ParticipantResponse(BaseModel):
    id: int
    user_id: Optional[int]
    guest_name: Optional[str]
    is_guest: bool
    is_approved: bool
    joined_at: datetime
    
    class Config:
        from_attributes = True


class GameStateUpdate(BaseModel):
    action: str
    data: Dict[str, Any]


class TimerSync(BaseModel):
    t0: float  # Unix timestamp when timer started
    duration: int  # Duration in seconds