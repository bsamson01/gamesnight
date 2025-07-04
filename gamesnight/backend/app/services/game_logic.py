import random
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.sql.expression import func

from app.models import (
    WouldYouRatherPrompt,
    TruthOrDarePrompt,
    SixtySecondsPrompt,
    HotSeatPrompt,
    DrawGuessPrompt,
    Theme
)
from app.core.redis_client import redis_client


class GameLogicService:
    def __init__(self):
        self.game_handlers = {
            "would_you_rather": self._handle_would_you_rather,
            "truth_or_dare": self._handle_truth_or_dare,
            "sixty_seconds": self._handle_sixty_seconds,
            "hot_seat": self._handle_hot_seat,
            "draw_guess": self._handle_draw_guess
        }
    
    async def load_prompts_for_session(
        self,
        db: AsyncSession,
        game_slug: str,
        theme_ids: List[int],
        room_id: int
    ) -> List[int]:
        """Load 50 random prompt IDs for a session"""
        prompt_model = self._get_prompt_model(game_slug)
        if not prompt_model:
            return []
        
        # Build query with theme filter
        query = select(prompt_model.id).where(prompt_model.is_safe == True)
        
        if theme_ids:
            # Join with themes
            query = query.join(prompt_model.themes).where(Theme.id.in_(theme_ids))
        
        # Order randomly and limit to 50
        query = query.order_by(func.random()).limit(50)
        
        result = await db.execute(query)
        prompt_ids = [row[0] for row in result.fetchall()]
        
        # Store in Redis
        key = f"room:{room_id}:prompts"
        if prompt_ids:
            await redis_client.delete(key)  # Clear existing
            await redis_client.lpush(key, *[str(id) for id in prompt_ids])
            await redis_client.expire(key, 86400)  # 24 hours
        
        return prompt_ids
    
    async def get_next_prompt(
        self,
        db: AsyncSession,
        room_id: int,
        game_slug: str
    ) -> Optional[Dict[str, Any]]:
        """Get the next prompt for a room"""
        key = f"room:{room_id}:prompts"
        
        # Pop a prompt ID from the list
        prompt_id_str = await redis_client.lpop(key)
        if not prompt_id_str:
            return None
        
        prompt_id = int(prompt_id_str)
        
        # Get the prompt from database
        prompt_model = self._get_prompt_model(game_slug)
        if not prompt_model:
            return None
        
        result = await db.execute(
            select(prompt_model).where(prompt_model.id == prompt_id)
        )
        prompt = result.scalar_one_or_none()
        
        if not prompt:
            return None
        
        # Format prompt based on game type
        return self._format_prompt(game_slug, prompt)
    
    def _get_prompt_model(self, game_slug: str):
        """Get the appropriate prompt model for a game"""
        models = {
            "would_you_rather": WouldYouRatherPrompt,
            "truth_or_dare": TruthOrDarePrompt,
            "sixty_seconds": SixtySecondsPrompt,
            "hot_seat": HotSeatPrompt,
            "draw_guess": DrawGuessPrompt
        }
        return models.get(game_slug)
    
    def _format_prompt(self, game_slug: str, prompt) -> Dict[str, Any]:
        """Format a prompt for API response"""
        if game_slug == "would_you_rather":
            return {
                "id": prompt.id,
                "option_a": prompt.option_a,
                "option_b": prompt.option_b
            }
        elif game_slug == "truth_or_dare":
            return {
                "id": prompt.id,
                "type": prompt.prompt_type,
                "text": prompt.text
            }
        elif game_slug == "sixty_seconds":
            return {
                "id": prompt.id,
                "category": prompt.category
            }
        elif game_slug == "hot_seat":
            return {
                "id": prompt.id,
                "question": prompt.question
            }
        elif game_slug == "draw_guess":
            return {
                "id": prompt.id,
                "word": prompt.word,
                "difficulty": prompt.difficulty
            }
        return {}
    
    async def process_game_action(
        self,
        room_id: int,
        game_slug: str,
        action: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a game action and return the result"""
        handler = self.game_handlers.get(game_slug)
        if not handler:
            return {"error": "Unknown game type"}
        
        return await handler(room_id, action, data)
    
    async def _handle_would_you_rather(
        self,
        room_id: int,
        action: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle Would You Rather game logic"""
        if action == "vote":
            user_id = data.get("user_id")
            choice = data.get("choice")  # "a" or "b"
            prompt_id = data.get("prompt_id")
            
            if not all([user_id, choice, prompt_id]):
                return {"error": "Missing required data"}
            
            # Store vote in Redis
            vote_key = f"room:{room_id}:votes:{prompt_id}"
            await redis_client.hset(vote_key, str(user_id), choice)
            await redis_client.expire(vote_key, 300)  # 5 minutes
            
            # Get current vote counts
            all_votes = await redis_client.hgetall(vote_key)
            vote_counts = {"a": 0, "b": 0}
            for vote in all_votes.values():
                if vote in vote_counts:
                    vote_counts[vote] += 1
            
            return {
                "success": True,
                "vote_counts": vote_counts,
                "total_votes": len(all_votes)
            }
        
        return {"error": "Unknown action"}
    
    async def _handle_truth_or_dare(
        self,
        room_id: int,
        action: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle Truth or Dare game logic"""
        if action == "complete":
            user_id = data.get("user_id")
            prompt_id = data.get("prompt_id")
            result = data.get("result")  # "completed" or "skipped"
            
            # Store result
            result_key = f"room:{room_id}:tod_results"
            await redis_client.hset(
                result_key,
                f"{user_id}:{prompt_id}",
                result
            )
            await redis_client.expire(result_key, 3600)  # 1 hour
            
            return {"success": True, "result": result}
        
        elif action == "select_player":
            player_id = data.get("player_id")
            prompt_type = data.get("type")  # "truth" or "dare"
            
            # Store current player
            await redis_client.hset(
                f"room:{room_id}",
                "current_player",
                str(player_id)
            )
            await redis_client.hset(
                f"room:{room_id}",
                "current_type",
                prompt_type
            )
            
            return {"success": True, "player_id": player_id, "type": prompt_type}
        
        return {"error": "Unknown action"}
    
    async def _handle_sixty_seconds(
        self,
        room_id: int,
        action: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle 60 Seconds game logic"""
        if action == "submit_answers":
            user_id = data.get("user_id")
            answers = data.get("answers", [])
            prompt_id = data.get("prompt_id")
            
            # Store answers
            answer_key = f"room:{room_id}:answers:{prompt_id}:{user_id}"
            await redis_client.delete(answer_key)
            if answers:
                await redis_client.lpush(answer_key, *answers)
            await redis_client.expire(answer_key, 300)  # 5 minutes
            
            return {"success": True, "answer_count": len(answers)}
        
        elif action == "calculate_scores":
            prompt_id = data.get("prompt_id")
            
            # Get all answers for this prompt
            pattern = f"room:{room_id}:answers:{prompt_id}:*"
            all_answers = {}
            unique_answers = set()
            
            # This is a simplified version - in production you'd use SCAN
            # For now, we'll assume we know the user IDs
            user_ids = data.get("user_ids", [])
            
            for user_id in user_ids:
                key = f"room:{room_id}:answers:{prompt_id}:{user_id}"
                user_answers = await redis_client.lrange(key, 0, -1)
                all_answers[user_id] = user_answers
                unique_answers.update(answer.lower() for answer in user_answers)
            
            # Calculate scores based on unique answers
            scores = {}
            for user_id, answers in all_answers.items():
                unique_count = len(set(answer.lower() for answer in answers))
                scores[user_id] = unique_count
            
            return {
                "success": True,
                "scores": scores,
                "total_unique": len(unique_answers)
            }
        
        return {"error": "Unknown action"}
    
    async def _handle_hot_seat(
        self,
        room_id: int,
        action: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle Hot Seat game logic"""
        if action == "set_hot_seat":
            player_id = data.get("player_id")
            
            # Store current hot seat player
            await redis_client.hset(
                f"room:{room_id}",
                "hot_seat_player",
                str(player_id)
            )
            
            return {"success": True, "player_id": player_id}
        
        elif action == "submit_question":
            user_id = data.get("user_id")
            question = data.get("question")
            
            # Store question
            question_key = f"room:{room_id}:hot_seat_questions"
            await redis_client.lpush(
                question_key,
                f"{user_id}:{question}"
            )
            await redis_client.expire(question_key, 600)  # 10 minutes
            
            return {"success": True}
        
        return {"error": "Unknown action"}
    
    async def _handle_draw_guess(
        self,
        room_id: int,
        action: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle Draw & Guess game logic"""
        if action == "set_drawer":
            drawer_id = data.get("drawer_id")
            word = data.get("word")
            
            # Store drawer and word
            await redis_client.hset(
                f"room:{room_id}",
                "drawer_id",
                str(drawer_id)
            )
            await redis_client.hset(
                f"room:{room_id}",
                "current_word",
                word
            )
            
            return {"success": True, "drawer_id": drawer_id}
        
        elif action == "submit_guess":
            user_id = data.get("user_id")
            guess = data.get("guess")
            
            # Get current word
            current_word = await redis_client.hget(f"room:{room_id}", "current_word")
            
            if not current_word:
                return {"error": "No active drawing"}
            
            # Check if guess is correct
            is_correct = guess and guess.lower().strip() == current_word.lower().strip()
            
            if is_correct:
                # Store winner
                await redis_client.hset(
                    f"room:{room_id}",
                    "round_winner",
                    str(user_id)
                )
                
                return {"success": True, "correct": True, "winner_id": user_id}
            
            return {"success": True, "correct": False}
        
        elif action == "clear_canvas":
            # Clear drawing data
            await redis_client.delete(f"room:{room_id}:strokes")
            return {"success": True}
        
        return {"error": "Unknown action"}


game_logic_service = GameLogicService()