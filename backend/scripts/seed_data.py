import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import engine, Base
from app.models import (
    Theme,
    WouldYouRatherPrompt,
    TruthOrDarePrompt,
    SixtySecondsPrompt,
    HotSeatPrompt,
    DrawGuessPrompt,
    User
)
from app.core.security import get_password_hash
from app.core.config import settings


async def seed_themes(session: AsyncSession):
    """Seed themes"""
    themes_data = [
        {"label": "General", "is_safe": True},
        {"label": "Funny", "is_safe": True},
        {"label": "Deep", "is_safe": True},
        {"label": "Family Friendly", "is_safe": True},
        {"label": "Party", "is_safe": True},
        {"label": "Icebreaker", "is_safe": True},
    ]
    
    themes = []
    for theme_data in themes_data:
        theme = Theme(**theme_data)
        session.add(theme)
        themes.append(theme)
    
    await session.flush()
    return themes


async def seed_would_you_rather(session: AsyncSession, themes):
    """Seed Would You Rather prompts"""
    prompts_data = [
        {
            "option_a": "Have the ability to fly",
            "option_b": "Have the ability to be invisible",
            "themes": ["General", "Icebreaker"]
        },
        {
            "option_a": "Always have to sing instead of speaking",
            "option_b": "Always have to dance while walking",
            "themes": ["Funny", "Party"]
        },
        {
            "option_a": "Know when you're going to die",
            "option_b": "Know how you're going to die",
            "themes": ["Deep"]
        },
        {
            "option_a": "Have a rewind button for your life",
            "option_b": "Have a pause button for your life",
            "themes": ["Deep", "General"]
        },
        {
            "option_a": "Be able to talk to animals",
            "option_b": "Be able to speak all human languages",
            "themes": ["General", "Family Friendly"]
        }
    ]
    
    theme_map = {t.label: t for t in themes}
    
    for prompt_data in prompts_data:
        theme_labels = prompt_data.pop("themes")
        prompt = WouldYouRatherPrompt(**prompt_data, is_safe=True)
        for label in theme_labels:
            if label in theme_map:
                prompt.themes.append(theme_map[label])
        session.add(prompt)


async def seed_truth_or_dare(session: AsyncSession, themes):
    """Seed Truth or Dare prompts"""
    prompts_data = [
        {
            "prompt_type": "truth",
            "text": "What's the most embarrassing thing that's happened to you?",
            "themes": ["General", "Icebreaker"]
        },
        {
            "prompt_type": "truth",
            "text": "What's your biggest fear?",
            "themes": ["Deep", "Icebreaker"]
        },
        {
            "prompt_type": "dare",
            "text": "Do your best impression of another player",
            "themes": ["Funny", "Party"]
        },
        {
            "prompt_type": "dare",
            "text": "Sing the chorus of your favorite song",
            "themes": ["Party", "Family Friendly"]
        },
        {
            "prompt_type": "truth",
            "text": "What's the best compliment you've ever received?",
            "themes": ["Deep", "Family Friendly"]
        }
    ]
    
    theme_map = {t.label: t for t in themes}
    
    for prompt_data in prompts_data:
        theme_labels = prompt_data.pop("themes")
        prompt = TruthOrDarePrompt(**prompt_data, is_safe=True)
        for label in theme_labels:
            if label in theme_map:
                prompt.themes.append(theme_map[label])
        session.add(prompt)


async def seed_sixty_seconds(session: AsyncSession, themes):
    """Seed 60 Seconds prompts"""
    prompts_data = [
        {"category": "Things you find at the beach", "themes": ["General", "Family Friendly"]},
        {"category": "Pizza toppings", "themes": ["General", "Family Friendly"]},
        {"category": "Superheroes", "themes": ["General", "Party"]},
        {"category": "Things that make you happy", "themes": ["Deep", "Icebreaker"]},
        {"category": "Animals that start with 'B'", "themes": ["Family Friendly", "Icebreaker"]}
    ]
    
    theme_map = {t.label: t for t in themes}
    
    for prompt_data in prompts_data:
        theme_labels = prompt_data.pop("themes")
        prompt = SixtySecondsPrompt(**prompt_data, is_safe=True)
        for label in theme_labels:
            if label in theme_map:
                prompt.themes.append(theme_map[label])
        session.add(prompt)


async def seed_hot_seat(session: AsyncSession, themes):
    """Seed Hot Seat prompts"""
    prompts_data = [
        {"question": "What's your dream vacation destination?", "themes": ["General", "Icebreaker"]},
        {"question": "If you could have dinner with anyone, who would it be?", "themes": ["Deep", "Icebreaker"]},
        {"question": "What's your hidden talent?", "themes": ["Funny", "Party"]},
        {"question": "What's the best advice you've ever received?", "themes": ["Deep", "Family Friendly"]},
        {"question": "What's your favorite childhood memory?", "themes": ["Family Friendly", "Icebreaker"]}
    ]
    
    theme_map = {t.label: t for t in themes}
    
    for prompt_data in prompts_data:
        theme_labels = prompt_data.pop("themes")
        prompt = HotSeatPrompt(**prompt_data, is_safe=True)
        for label in theme_labels:
            if label in theme_map:
                prompt.themes.append(theme_map[label])
        session.add(prompt)


async def seed_draw_guess(session: AsyncSession, themes):
    """Seed Draw & Guess prompts"""
    prompts_data = [
        {"word": "cat", "difficulty": "easy", "themes": ["General", "Family Friendly"]},
        {"word": "bicycle", "difficulty": "easy", "themes": ["General", "Family Friendly"]},
        {"word": "rainbow", "difficulty": "medium", "themes": ["General", "Family Friendly"]},
        {"word": "astronaut", "difficulty": "medium", "themes": ["General", "Party"]},
        {"word": "democracy", "difficulty": "hard", "themes": ["Deep"]}
    ]
    
    theme_map = {t.label: t for t in themes}
    
    for prompt_data in prompts_data:
        theme_labels = prompt_data.pop("themes")
        prompt = DrawGuessPrompt(**prompt_data, is_safe=True)
        for label in theme_labels:
            if label in theme_map:
                prompt.themes.append(theme_map[label])
        session.add(prompt)


async def seed_admin_user(session: AsyncSession):
    """Create admin user"""
    admin = User(
        email=settings.ADMIN_EMAIL,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        role="admin",
        is_paid=True
    )
    session.add(admin)


async def main():
    """Main seed function"""
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Seeding data...")
    async with AsyncSession(engine) as session:
        # Seed themes
        themes = await seed_themes(session)
        print(f"Created {len(themes)} themes")
        
        # Seed game prompts
        await seed_would_you_rather(session, themes)
        print("Created Would You Rather prompts")
        
        await seed_truth_or_dare(session, themes)
        print("Created Truth or Dare prompts")
        
        await seed_sixty_seconds(session, themes)
        print("Created 60 Seconds prompts")
        
        await seed_hot_seat(session, themes)
        print("Created Hot Seat prompts")
        
        await seed_draw_guess(session, themes)
        print("Created Draw & Guess prompts")
        
        # Create admin user
        await seed_admin_user(session)
        print("Created admin user")
        
        # Commit all changes
        await session.commit()
    
    print("Seeding completed!")


if __name__ == "__main__":
    asyncio.run(main())