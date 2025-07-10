"""
Lesson Flow Logic for Akash Gurukul
Manages lesson progression, state tracking, and query path management
"""

from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from datetime import datetime
import json
from pathlib import Path

class LessonState(Enum):
    """Lesson completion states"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"

class QueryPath(Enum):
    """Different types of learning interactions"""
    CONCEPTUAL = "conceptual"      # Tree agent - understanding concepts
    PRACTICAL = "practical"       # Seed agent - practicing skills
    REFLECTIVE = "reflective"     # Sky agent - deep reflection
    ASSESSMENT = "assessment"     # Quiz and evaluation
    REVIEW = "review"            # Reviewing previous content

class LessonFlowManager:
    """Manages lesson progression and state tracking"""
    
    def __init__(self, student_id: str, storage_path: str = "./student_data"):
        self.student_id = student_id
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Load or initialize student progress
        self.progress_file = self.storage_path / f"{student_id}_progress.json"
        self.student_progress = self._load_progress()
        
    def _load_progress(self) -> Dict[str, Any]:
        """Load student progress from storage"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "student_id": self.student_id,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "lessons": {},
                "current_lesson": None,
                "learning_path": [],
                "preferences": {
                    "preferred_agent": None,
                    "learning_style": None,
                    "pace": "medium"
                }
            }
    
    def _save_progress(self):
        """Save student progress to storage"""
        self.student_progress["last_updated"] = datetime.now().isoformat()
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.student_progress, f, indent=2, ensure_ascii=False)
    
    def start_lesson(self, lesson_id: str, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new lesson and return initial context"""
        # Initialize lesson progress
        if lesson_id not in self.student_progress["lessons"]:
            self.student_progress["lessons"][lesson_id] = {
                "state": LessonState.NOT_STARTED.value,
                "started_at": None,
                "completed_at": None,
                "attempts": 0,
                "quiz_scores": [],
                "agent_interactions": {
                    "seed": 0,
                    "tree": 0,
                    "sky": 0
                },
                "time_spent": 0,
                "query_paths_used": [],
                "mastery_indicators": {}
            }
        
        # Update lesson state
        lesson_progress = self.student_progress["lessons"][lesson_id]
        lesson_progress["state"] = LessonState.IN_PROGRESS.value
        lesson_progress["started_at"] = datetime.now().isoformat()
        lesson_progress["attempts"] += 1
        
        # Set as current lesson
        self.student_progress["current_lesson"] = lesson_id
        
        self._save_progress()
        
        # Return lesson context for agents
        return {
            "lesson_id": lesson_id,
            "lesson_data": lesson_data,
            "progress": lesson_progress,
            "recommended_agent": self._get_recommended_agent(lesson_data, lesson_progress),
            "query_path": self._get_initial_query_path(lesson_data),
            "context": self._build_lesson_context(lesson_id, lesson_data)
        }
    
    def _get_recommended_agent(self, lesson_data: Dict[str, Any], progress: Dict[str, Any]) -> str:
        """Determine which agent should handle the initial interaction"""
        # Check student preferences
        preferred = self.student_progress["preferences"].get("preferred_agent")
        if preferred:
            return preferred
        
        # Based on lesson level and student history
        level = lesson_data.get("level", "Seed")
        interactions = progress.get("agent_interactions", {})
        
        if level == "Seed" or sum(interactions.values()) == 0:
            return "seed"  # Start with practice for beginners
        elif level == "Tree":
            return "tree"  # Conceptual understanding for intermediate
        else:
            return "sky"   # Philosophical for advanced
    
    def _get_initial_query_path(self, lesson_data: Dict[str, Any]) -> str:
        """Determine initial query path based on lesson content"""
        level = lesson_data.get("level", "Seed")
        
        if level == "Seed":
            return QueryPath.PRACTICAL.value
        elif level == "Tree":
            return QueryPath.CONCEPTUAL.value
        else:
            return QueryPath.REFLECTIVE.value
    
    def _build_lesson_context(self, lesson_id: str, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive context for agent interactions"""
        return {
            "current_lesson": lesson_data,
            "student_progress": self.student_progress,
            "lesson_objectives": lesson_data.get("learning_objectives", []),
            "lesson_level": lesson_data.get("level", "Seed"),
            "estimated_duration": lesson_data.get("estimated_duration", 30),
            "prerequisites_met": self._check_prerequisites(lesson_data),
            "learning_path_position": self._get_path_position(lesson_id)
        }
    
    def record_interaction(self, lesson_id: str, agent_type: str, query_path: str, 
                          user_input: str, agent_response: str, quality_score: float = 1.0):
        """Record an agent interaction"""
        if lesson_id not in self.student_progress["lessons"]:
            return
        
        lesson_progress = self.student_progress["lessons"][lesson_id]
        
        # Update interaction counts
        lesson_progress["agent_interactions"][agent_type] += 1
        
        # Track query paths used
        if query_path not in lesson_progress["query_paths_used"]:
            lesson_progress["query_paths_used"].append(query_path)
        
        # Store interaction details (keep last 10)
        if "interactions" not in lesson_progress:
            lesson_progress["interactions"] = []
        
        lesson_progress["interactions"].append({
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,
            "query_path": query_path,
            "user_input": user_input[:100],  # Truncate for storage
            "response_length": len(agent_response),
            "quality_score": quality_score
        })
        
        # Keep only last 10 interactions
        lesson_progress["interactions"] = lesson_progress["interactions"][-10:]
        
        self._save_progress()
    
    def suggest_next_agent(self, lesson_id: str, current_agent: str,
                          user_input: str) -> Tuple[str, str]:
        """Enhanced agent suggestion with refined query path logic"""
        lesson_progress = self.student_progress["lessons"].get(lesson_id, {})
        interactions = lesson_progress.get("agent_interactions", {"seed": 0, "tree": 0, "sky": 0})

        # Analyze user input with enhanced keyword detection
        user_lower = user_input.lower().strip()

        # If input is empty or very short, suggest tree agent as default
        if len(user_lower) < 3:
            return "tree", QueryPath.CONCEPTUAL.value

        # Enhanced keyword mapping with more nuanced detection
        practical_keywords = {
            "primary": ["how", "practice", "do", "steps", "exercise", "try", "apply", "use", "implement", "show", "guide"],
            "secondary": ["daily", "routine", "habit", "action", "technique", "method", "way", "start", "begin"]
        }

        conceptual_keywords = {
            "primary": ["why", "what", "explain", "understand", "concept", "meaning", "principle", "because"],
            "secondary": ["reason", "theory", "idea", "knowledge", "wisdom", "connection", "relationship", "framework"]
        }

        reflective_keywords = {
            "primary": ["soul", "spirit", "divine", "deeper", "purpose", "meaning", "spiritual", "consciousness"],
            "secondary": ["feel", "think", "believe", "reflect", "contemplate", "meditate", "inner", "philosophical"]
        }

        # Calculate keyword scores with higher weights
        practical_score = self._calculate_keyword_score(user_lower, practical_keywords) * 2.0
        conceptual_score = self._calculate_keyword_score(user_lower, conceptual_keywords) * 2.0
        reflective_score = self._calculate_keyword_score(user_lower, reflective_keywords) * 2.0

        # Base scores for each agent
        scores = {
            "seed": practical_score + 0.1,  # Small base score
            "tree": conceptual_score + 0.2,  # Slightly higher base (default)
            "sky": reflective_score + 0.1
        }

        # Add significant bonus for agent diversity (encourage trying different agents)
        total_interactions = sum(interactions.values())
        if total_interactions > 0:
            for agent, interaction_count in interactions.items():
                if interaction_count == 0:
                    scores[agent] += 1.0  # Large bonus for unused agents
                else:
                    # Penalty for overused agents
                    usage_ratio = interaction_count / total_interactions
                    if usage_ratio > 0.6:  # If agent used more than 60% of time
                        scores[agent] -= 0.8
                    elif usage_ratio > 0.4:  # If agent used more than 40% of time
                        scores[agent] -= 0.4

        # Discourage consecutive same agent unless score is very high
        if current_agent in scores and scores[current_agent] < 1.5:
            scores[current_agent] -= 0.6

        # Ensure we have valid scores
        if all(score <= 0 for score in scores.values()):
            # Fallback: suggest least used agent
            least_used_agent = min(interactions.items(), key=lambda x: x[1])[0]
            return least_used_agent, self._get_default_path_for_agent(least_used_agent)

        # Select agent with highest score
        suggested_agent = max(scores.items(), key=lambda x: x[1])[0]
        suggested_path = self._get_default_path_for_agent(suggested_agent)

        return suggested_agent, suggested_path

    def _calculate_keyword_score(self, text: str, keyword_dict: dict) -> float:
        """Calculate keyword match score with weighted importance"""
        score = 0.0

        # Primary keywords have higher weight
        for keyword in keyword_dict["primary"]:
            if keyword in text:
                score += 1.0

        # Secondary keywords have lower weight
        for keyword in keyword_dict["secondary"]:
            if keyword in text:
                score += 0.5

        return score
    
    def _get_default_path_for_agent(self, agent_type: str) -> str:
        """Get default query path for agent type"""
        defaults = {
            "seed": QueryPath.PRACTICAL.value,
            "tree": QueryPath.CONCEPTUAL.value,
            "sky": QueryPath.REFLECTIVE.value
        }
        return defaults.get(agent_type, QueryPath.CONCEPTUAL.value)
    
    def complete_lesson(self, lesson_id: str, quiz_score: float = None, 
                       mastery_indicators: Dict[str, Any] = None) -> Dict[str, Any]:
        """Mark lesson as completed and determine mastery level"""
        if lesson_id not in self.student_progress["lessons"]:
            return {"error": "Lesson not found"}
        
        lesson_progress = self.student_progress["lessons"][lesson_id]
        lesson_progress["completed_at"] = datetime.now().isoformat()
        
        if quiz_score is not None:
            lesson_progress["quiz_scores"].append(quiz_score)
        
        if mastery_indicators:
            lesson_progress["mastery_indicators"].update(mastery_indicators)
        
        # Determine completion state
        avg_quiz_score = sum(lesson_progress["quiz_scores"]) / len(lesson_progress["quiz_scores"]) if lesson_progress["quiz_scores"] else 0
        
        if avg_quiz_score >= 0.9 and len(lesson_progress["query_paths_used"]) >= 2:
            lesson_progress["state"] = LessonState.MASTERED.value
        else:
            lesson_progress["state"] = LessonState.COMPLETED.value
        
        # Clear current lesson
        if self.student_progress["current_lesson"] == lesson_id:
            self.student_progress["current_lesson"] = None
        
        self._save_progress()
        
        return {
            "lesson_id": lesson_id,
            "final_state": lesson_progress["state"],
            "quiz_score": quiz_score,
            "mastery_achieved": lesson_progress["state"] == LessonState.MASTERED.value,
            "next_recommendations": self._get_next_lesson_recommendations(lesson_id)
        }
    
    def _check_prerequisites(self, lesson_data: Dict[str, Any]) -> bool:
        """Check if lesson prerequisites are met"""
        prerequisites = lesson_data.get("prerequisites", [])
        for prereq in prerequisites:
            if prereq not in self.student_progress["lessons"]:
                return False
            if self.student_progress["lessons"][prereq]["state"] == LessonState.NOT_STARTED.value:
                return False
        return True
    
    def _get_path_position(self, lesson_id: str) -> Dict[str, Any]:
        """Get position in learning path"""
        # This would integrate with curriculum structure
        return {
            "current": lesson_id,
            "position": 1,
            "total": 10,
            "path_name": "Dharma Foundation"
        }
    
    def _get_next_lesson_recommendations(self, completed_lesson_id: str) -> List[str]:
        """Get recommendations for next lessons"""
        # This would integrate with curriculum dependency graph
        return ["next_lesson_001", "alternative_lesson_002"]
    
    def get_student_summary(self) -> Dict[str, Any]:
        """Get comprehensive student progress summary"""
        total_lessons = len(self.student_progress["lessons"])
        completed = sum(1 for lesson in self.student_progress["lessons"].values() 
                       if lesson["state"] in [LessonState.COMPLETED.value, LessonState.MASTERED.value])
        mastered = sum(1 for lesson in self.student_progress["lessons"].values() 
                      if lesson["state"] == LessonState.MASTERED.value)
        
        return {
            "student_id": self.student_id,
            "total_lessons_attempted": total_lessons,
            "lessons_completed": completed,
            "lessons_mastered": mastered,
            "completion_rate": completed / total_lessons if total_lessons > 0 else 0,
            "mastery_rate": mastered / total_lessons if total_lessons > 0 else 0,
            "current_lesson": self.student_progress["current_lesson"],
            "preferences": self.student_progress["preferences"],
            "last_updated": self.student_progress["last_updated"]
        }
