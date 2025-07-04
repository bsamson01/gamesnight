from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_paid = Column(Boolean, default=False)
    paid_until = Column(DateTime, nullable=True)
    role = Column(String, default="free")  # free, paid, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = relationship("Payment", back_populates="user")
    hosted_rooms = relationship("Room", back_populates="host", foreign_keys="[Room.host_id]")
    room_participants = relationship("RoomParticipant", back_populates="user")