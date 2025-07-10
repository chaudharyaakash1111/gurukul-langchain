"""
Agent Chaining System for Akash Gurukul
Enables seamless transitions between Tree, Seed, and Sky agents
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

class AgentType(Enum):
    SEED = "seed"
    TREE = "tree" 
    SKY = "sky"

class TransitionTrigger(Enum):
    STUDENT_REQUEST = "student_request"
    NATURAL_FLOW = "natural_flow"
    LEARNING_OBJECTIVE = "learning_objective"
    AGENT_RECOMMENDATION = "agent_recommendation"

class AgentTransitionResult:
    """Result of agent transition analysis"""

    def __init__(self, should_transition: bool, recommended_agent: str,
                 confidence: float, reason: str, context_data: Dict[str, Any] = None):
        self.should_transition = should_transition
        self.recommended_agent = recommended_agent
        self.confidence = confidence
        self.reason = reason
        self.context_data = context_data or {}

class AgentChainContext:
    """Shared context that travels between agents"""
    
    def __init__(self, student_id: str, lesson_id: str = None):
        self.student_id = student_id
        self.lesson_id = lesson_id
        self.chain_id = str(uuid.uuid4())
        self.conversation_history = []
        self.agent_insights = {}
        self.learning_progress = {}
        self.student_preferences = {}
        self.unresolved_questions = []
        self.key_concepts_covered = []
        self.emotional_state = "neutral"
        self.engagement_level = "medium"
        
    def add_agent_insight(self, agent_type: str, insight: Dict[str, Any]):
        """Add insight from an agent to shared context"""
        if agent_type not in self.agent_insights:
            self.agent_insights[agent_type] = []
        
        insight["timestamp"] = datetime.now().isoformat()
        self.agent_insights[agent_type].append(insight)
    
    def get_context_for_agent(self, agent_type: str) -> Dict[str, Any]:
        """Get relevant context for a specific agent"""
        return {
            "student_id": self.student_id,
            "lesson_id": self.lesson_id,
            "chain_id": self.chain_id,
            "conversation_history": self.conversation_history[-5:],  # Last 5 exchanges
            "other_agent_insights": {k: v for k, v in self.agent_insights.items() if k != agent_type},
            "learning_progress": self.learning_progress,
            "student_preferences": self.student_preferences,
            "unresolved_questions": self.unresolved_questions,
            "concepts_covered": self.key_concepts_covered,
            "emotional_state": self.emotional_state,
            "engagement_level": self.engagement_level
        }

class AgentTransitionRule:
    """Defines when and how to transition between agents"""
    
    def __init__(self, from_agent: AgentType, to_agent: AgentType, 
                 triggers: List[str], context_keys: List[str], 
                 confidence_threshold: float = 0.7):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.triggers = triggers
        self.context_keys = context_keys
        self.confidence_threshold = confidence_threshold
    
    def should_transition(self, user_input: str, context: AgentChainContext) -> Tuple[bool, float]:
        """Determine if transition should occur based on input and context"""
        user_lower = user_input.lower()
        
        # Check for trigger words
        trigger_score = sum(1 for trigger in self.triggers if trigger in user_lower)
        trigger_confidence = trigger_score / len(self.triggers) if self.triggers else 0
        
        # Check context factors
        context_score = 0
        if self.from_agent.value in context.agent_insights:
            recent_interactions = len(context.agent_insights[self.from_agent.value])
            if recent_interactions >= 3:  # After 3+ interactions, consider transition
                context_score += 0.3
        
        # Check for unresolved questions that other agent might handle better
        if context.unresolved_questions:
            context_score += 0.2
        
        total_confidence = (trigger_confidence * 0.7) + (context_score * 0.3)
        should_transition = total_confidence >= self.confidence_threshold
        
        return should_transition, total_confidence

class AgentChainManager:
    """Manages the chaining and transitions between agents"""
    
    def __init__(self):
        self.active_chains: Dict[str, AgentChainContext] = {}
        self.transition_rules = self._initialize_transition_rules()
        
    def _initialize_transition_rules(self) -> List[AgentTransitionRule]:
        """Initialize the rules for agent transitions"""
        return [
            # Seed to Tree transitions (practice to understanding)
            AgentTransitionRule(
                from_agent=AgentType.SEED,
                to_agent=AgentType.TREE,
                triggers=["why", "explain", "understand", "principle", "concept", "theory", "because"],
                context_keys=["practice_attempts", "skill_questions", "conceptual_gaps"],
                confidence_threshold=0.6
            ),
            
            # Tree to Sky transitions (understanding to meaning)
            AgentTransitionRule(
                from_agent=AgentType.TREE,
                to_agent=AgentType.SKY,
                triggers=["meaning", "purpose", "spiritual", "soul", "deeper", "divine", "consciousness"],
                context_keys=["philosophical_questions", "meaning_seeking", "spiritual_curiosity"],
                confidence_threshold=0.6
            ),
            
            # Sky to Seed transitions (insight to application)
            AgentTransitionRule(
                from_agent=AgentType.SKY,
                to_agent=AgentType.SEED,
                triggers=["how", "practice", "apply", "implement", "daily", "routine", "habit"],
                context_keys=["insights_to_apply", "practical_needs", "implementation_questions"],
                confidence_threshold=0.6
            ),
            
            # Tree to Seed transitions (understanding to practice)
            AgentTransitionRule(
                from_agent=AgentType.TREE,
                to_agent=AgentType.SEED,
                triggers=["practice", "try", "do", "exercise", "apply", "implement", "steps"],
                context_keys=["ready_for_practice", "concept_understood"],
                confidence_threshold=0.7
            ),
            
            # Seed to Sky transitions (practice to reflection)
            AgentTransitionRule(
                from_agent=AgentType.SEED,
                to_agent=AgentType.SKY,
                triggers=["feel", "experience", "meaning", "why", "purpose", "spiritual"],
                context_keys=["experiential_questions", "deeper_inquiry"],
                confidence_threshold=0.7
            ),
            
            # Sky to Tree transitions (insight to understanding)
            AgentTransitionRule(
                from_agent=AgentType.SKY,
                to_agent=AgentType.TREE,
                triggers=["understand", "explain", "how", "what", "principle", "concept"],
                context_keys=["need_framework", "conceptual_clarity"],
                confidence_threshold=0.7
            )
        ]
    
    def get_or_create_chain(self, student_id: str, lesson_id: str = None) -> AgentChainContext:
        """Get existing chain or create new one for student"""
        chain_key = f"{student_id}_{lesson_id}" if lesson_id else student_id
        
        if chain_key not in self.active_chains:
            self.active_chains[chain_key] = AgentChainContext(student_id, lesson_id)
        
        return self.active_chains[chain_key]
    
    def suggest_agent_transition(self, current_agent: str, user_input: str, 
                               student_id: str, lesson_id: str = None) -> Dict[str, Any]:
        """Suggest if agent transition should occur"""
        context = self.get_or_create_chain(student_id, lesson_id)
        current_agent_type = AgentType(current_agent)
        
        best_transition = None
        best_confidence = 0
        
        # Check all possible transitions from current agent
        for rule in self.transition_rules:
            if rule.from_agent == current_agent_type:
                should_transition, confidence = rule.should_transition(user_input, context)
                
                if should_transition and confidence > best_confidence:
                    best_transition = rule
                    best_confidence = confidence
        
        if best_transition:
            return {
                "should_transition": True,
                "recommended_agent": best_transition.to_agent.value,
                "confidence": best_confidence,
                "reason": f"Detected transition triggers: {best_transition.triggers}",
                "transition_context": self._prepare_transition_context(
                    context, current_agent, best_transition.to_agent.value
                )
            }
        else:
            return {
                "should_transition": False,
                "recommended_agent": current_agent,
                "confidence": 1.0,
                "reason": "No strong transition signals detected"
            }
    
    def _prepare_transition_context(self, context: AgentChainContext, 
                                  from_agent: str, to_agent: str) -> Dict[str, Any]:
        """Prepare context for smooth agent transition"""
        return {
            "handoff_summary": f"Transitioning from {from_agent} to {to_agent}",
            "previous_agent_insights": context.agent_insights.get(from_agent, []),
            "student_state": {
                "engagement": context.engagement_level,
                "emotional_state": context.emotional_state,
                "learning_progress": context.learning_progress
            },
            "conversation_context": context.conversation_history[-3:],
            "unresolved_questions": context.unresolved_questions,
            "recommended_approach": self._get_transition_approach(from_agent, to_agent)
        }
    
    def _get_transition_approach(self, from_agent: str, to_agent: str) -> str:
        """Get recommended approach for specific agent transition"""
        transitions = {
            ("seed", "tree"): "Build on practical experience to explore underlying principles",
            ("tree", "sky"): "Deepen conceptual understanding into spiritual insight",
            ("sky", "seed"): "Ground spiritual insights in practical application",
            ("tree", "seed"): "Transform understanding into actionable practice",
            ("seed", "sky"): "Reflect on the deeper meaning of practical experience",
            ("sky", "tree"): "Clarify insights through conceptual frameworks"
        }
        
        return transitions.get((from_agent, to_agent), "Smooth transition between perspectives")
    
    def record_agent_interaction(self, agent_type: str, user_input: str, 
                               agent_response: str, student_id: str, 
                               lesson_id: str = None, insights: Dict[str, Any] = None):
        """Record interaction in the chain context"""
        context = self.get_or_create_chain(student_id, lesson_id)
        
        # Add to conversation history
        context.conversation_history.append({
            "agent": agent_type,
            "user_input": user_input,
            "agent_response": agent_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Add agent insights if provided
        if insights:
            context.add_agent_insight(agent_type, insights)
        
        # Update engagement and emotional state based on interaction
        self._update_student_state(context, user_input, agent_response)
    
    def _update_student_state(self, context: AgentChainContext, 
                            user_input: str, agent_response: str):
        """Update student emotional and engagement state"""
        # Simple heuristics for engagement
        if len(user_input) > 50:  # Longer inputs suggest higher engagement
            context.engagement_level = "high"
        elif len(user_input) < 10:
            context.engagement_level = "low"
        else:
            context.engagement_level = "medium"
        
        # Simple emotional state detection
        positive_words = ["thank", "great", "love", "amazing", "wonderful", "helpful"]
        negative_words = ["confused", "difficult", "hard", "frustrated", "stuck"]
        
        user_lower = user_input.lower()
        if any(word in user_lower for word in positive_words):
            context.emotional_state = "positive"
        elif any(word in user_lower for word in negative_words):
            context.emotional_state = "challenged"
        else:
            context.emotional_state = "neutral"
    
    def get_chain_summary(self, student_id: str, lesson_id: str = None) -> Dict[str, Any]:
        """Get summary of the current agent chain"""
        context = self.get_or_create_chain(student_id, lesson_id)
        
        return {
            "chain_id": context.chain_id,
            "total_interactions": len(context.conversation_history),
            "agents_used": list(context.agent_insights.keys()),
            "current_state": {
                "engagement": context.engagement_level,
                "emotional_state": context.emotional_state
            },
            "learning_progress": context.learning_progress,
            "unresolved_questions": len(context.unresolved_questions)
        }

    def should_transition(self, current_agent: str, student_message: str,
                         agent_response: str, conversation_context: Dict[str, Any]) -> AgentTransitionResult:
        """
        Determine if we should transition to a different agent based on the conversation
        """
        # Analyze the student message for transition indicators
        message_lower = student_message.lower()

        # Keywords that suggest different agent types
        practice_keywords = ["how", "practice", "do", "steps", "exercise", "daily", "routine"]
        wisdom_keywords = ["why", "meaning", "understand", "explain", "concept", "principle"]
        philosophy_keywords = ["purpose", "soul", "spiritual", "deeper", "consciousness", "meaning of life"]

        # Count keyword matches
        practice_score = sum(1 for keyword in practice_keywords if keyword in message_lower)
        wisdom_score = sum(1 for keyword in wisdom_keywords if keyword in message_lower)
        philosophy_score = sum(1 for keyword in philosophy_keywords if keyword in message_lower)

        # Determine best agent
        scores = {
            "seed": practice_score,
            "tree": wisdom_score,
            "sky": philosophy_score
        }

        best_agent = max(scores, key=scores.get)
        best_score = scores[best_agent]

        # Only suggest transition if there's a clear better match and it's different from current
        should_transition = (best_agent != current_agent and best_score > 0)
        confidence = min(best_score / 3.0, 1.0)  # Normalize to 0-1

        reason = f"Message contains {best_score} keywords suggesting {best_agent} agent expertise"

        return AgentTransitionResult(
            should_transition=should_transition,
            recommended_agent=best_agent,
            confidence=confidence,
            reason=reason,
            context_data={
                "keyword_scores": scores,
                "current_agent": current_agent,
                "message_analysis": {
                    "practice_score": practice_score,
                    "wisdom_score": wisdom_score,
                    "philosophy_score": philosophy_score
                }
            }
        )

    def route_to_best_agent(self, student_message: str, conversation_context: Dict[str, Any]) -> AgentTransitionResult:
        """
        Route to the best agent for initial message (no current agent)
        """
        message_lower = student_message.lower()

        # Enhanced keyword analysis for routing
        practice_keywords = ["how", "practice", "do", "steps", "exercise", "daily", "routine", "action", "implement"]
        wisdom_keywords = ["why", "meaning", "understand", "explain", "concept", "principle", "learn", "teach"]
        philosophy_keywords = ["purpose", "soul", "spiritual", "deeper", "consciousness", "meaning of life", "reflect"]

        # Advanced scoring with weights
        practice_score = sum(2 if keyword in message_lower else 0 for keyword in practice_keywords)
        wisdom_score = sum(2 if keyword in message_lower else 0 for keyword in wisdom_keywords)
        philosophy_score = sum(2 if keyword in message_lower else 0 for keyword in philosophy_keywords)

        # Question type analysis
        if message_lower.startswith("how"):
            practice_score += 3
        elif message_lower.startswith("why"):
            wisdom_score += 3
        elif message_lower.startswith("what") and ("meaning" in message_lower or "purpose" in message_lower):
            philosophy_score += 3

        # Determine best agent
        scores = {
            "seed": practice_score,
            "tree": wisdom_score,
            "sky": philosophy_score
        }

        best_agent = max(scores, key=scores.get)
        best_score = scores[best_agent]

        # Default to seed if no clear preference
        if best_score == 0:
            best_agent = "seed"
            reason = "Default routing to seed agent for general guidance"
            confidence = 0.5
        else:
            reason = f"Routed to {best_agent} agent based on message analysis (score: {best_score})"
            confidence = min(best_score / 6.0, 1.0)

        return AgentTransitionResult(
            should_transition=True,  # Always true for initial routing
            recommended_agent=best_agent,
            confidence=confidence,
            reason=reason,
            context_data={
                "keyword_scores": scores,
                "routing_type": "initial",
                "message_analysis": {
                    "practice_score": practice_score,
                    "wisdom_score": wisdom_score,
                    "philosophy_score": philosophy_score
                }
            }
        )

# Global instance for the application
agent_chain_manager = AgentChainManager()
