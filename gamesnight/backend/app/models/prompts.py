from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

# Association tables for many-to-many relationships
would_you_rather_themes = Table(
    'would_you_rather_themes',
    Base.metadata,
    Column('prompt_id', Integer, ForeignKey('prompts_would_you_rather.id')),
    Column('theme_id', Integer, ForeignKey('themes.id'))
)

truth_or_dare_themes = Table(
    'truth_or_dare_themes',
    Base.metadata,
    Column('prompt_id', Integer, ForeignKey('prompts_truth_or_dare.id')),
    Column('theme_id', Integer, ForeignKey('themes.id'))
)

sixty_seconds_themes = Table(
    'sixty_seconds_themes',
    Base.metadata,
    Column('prompt_id', Integer, ForeignKey('prompts_sixty_seconds.id')),
    Column('theme_id', Integer, ForeignKey('themes.id'))
)

hot_seat_themes = Table(
    'hot_seat_themes',
    Base.metadata,
    Column('prompt_id', Integer, ForeignKey('prompts_hot_seat.id')),
    Column('theme_id', Integer, ForeignKey('themes.id'))
)

draw_guess_themes = Table(
    'draw_guess_themes',
    Base.metadata,
    Column('prompt_id', Integer, ForeignKey('prompts_draw_guess.id')),
    Column('theme_id', Integer, ForeignKey('themes.id'))
)


class WouldYouRatherPrompt(Base):
    __tablename__ = "prompts_would_you_rather"
    
    id = Column(Integer, primary_key=True, index=True)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    is_safe = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    themes = relationship("Theme", secondary=would_you_rather_themes)


class TruthOrDarePrompt(Base):
    __tablename__ = "prompts_truth_or_dare"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_type = Column(String, nullable=False)  # truth or dare
    text = Column(Text, nullable=False)
    is_safe = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    themes = relationship("Theme", secondary=truth_or_dare_themes)


class SixtySecondsPrompt(Base):
    __tablename__ = "prompts_sixty_seconds"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(Text, nullable=False)
    is_safe = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    themes = relationship("Theme", secondary=sixty_seconds_themes)


class HotSeatPrompt(Base):
    __tablename__ = "prompts_hot_seat"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    is_safe = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    themes = relationship("Theme", secondary=hot_seat_themes)


class DrawGuessPrompt(Base):
    __tablename__ = "prompts_draw_guess"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False)
    difficulty = Column(String, default="medium")  # easy, medium, hard
    is_safe = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    themes = relationship("Theme", secondary=draw_guess_themes)