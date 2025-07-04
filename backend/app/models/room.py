from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
import secrets

from app.db.base import Base


class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_slug = Column(String, nullable=False)  # would_you_rather, truth_or_dare, etc.
    invite_code = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="open")  # open, locked, active, closed
    game_state = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    host = relationship("User", back_populates="hosted_rooms", foreign_keys=[host_id])
    participants = relationship("RoomParticipant", back_populates="room")
    session = relationship("GameSession", back_populates="room", uselist=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
    
    @staticmethod
    def generate_invite_code():
        return secrets.token_urlsafe(8)


class RoomParticipant(Base):
    __tablename__ = "room_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for guests
    guest_name = Column(String, nullable=True)  # For guest users
    is_guest = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    room = relationship("Room", back_populates="participants")
    user = relationship("User", back_populates="room_participants")