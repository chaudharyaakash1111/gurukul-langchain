"""
Base Agent Implementation for Akash Gurukul
Provides foundation for Seed, Tree, and Sky agents
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
try:
    from .memory_system import AgentMemorySystem
except ImportError:
    from memory_system import AgentMemorySystem
import json


class BaseAgent(ABC):
    """Abstract base class for all Akash Gurukul agents"""
    
    def __init__(self, agent_type: str, student_id: str, config: Dict[str, Any] = None):
        self.agent_type = agent_type
        self.student_id = student_id
        self.config = config or {}
        
        # Initialize LLM
        try:
            self.llm = OpenAI(
                temperature=self.config.get('temperature', 0.7),
                model=self.config.get('model', 'gpt-3.5-turbo-instruct')
            )
        except Exception as e:
            print(f"OpenAI LLM not available: {e}")
            print("Using fake LLM for testing")
            from langchain_community.llms import FakeListLLM
            self.llm = FakeListLLM(responses=[
                "I'm here to help you learn and grow! This is a test response from the agent.",
                "That's a great question! Let me help you understand this concept better.",
                "I appreciate your curiosity. Learning is a wonderful journey!"
            ])
        
        # Initialize memory system
        self.memory = AgentMemorySystem(agent_type, student_id, config)
        
        # Agent-specific personality and prompts
        self.personality = self._get_personality()
        self.system_prompt = self._get_system_prompt()
        
    @abstractmethod
    def _get_personality(self) -> Dict[str, str]:
        """Define agent personality traits"""
        pass
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Define agent system prompt"""
        pass
    
    def respond(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Generate response to user input with enhanced context and fallback logic"""
        try:
            # Get personalized context
            memory_context = self.memory.get_personalized_context(user_input)

            # Combine with provided context
            full_context = {**memory_context, **(context or {})}

            # Check for repetition or off-topic patterns
            if self._should_use_fallback(user_input, full_context):
                return self._get_contextual_fallback(user_input, full_context)

            # Create prompt with enhanced context
            prompt = self._create_enhanced_prompt(user_input, full_context)

            # Generate response
            response = self.llm(prompt)
            response_text = response.strip()

            # Validate response quality
            if self._is_response_valid(response_text, user_input):
                # Store interaction in memory
                self.memory.add_to_conversation(user_input, response_text)
                return response_text
            else:
                # Use fallback for poor quality responses
                return self._get_contextual_fallback(user_input, full_context)

        except Exception as e:
            print(f"Error generating response: {e}")
            return self._get_fallback_response(user_input)
    
    def _create_enhanced_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        """Create enhanced prompt with better context and guardrails"""
        # Extract lesson context if available
        lesson_context = context.get('current_lesson', {})
        learning_objective = lesson_context.get('learning_objectives', [])
        lesson_topic = lesson_context.get('title', 'General Learning')

        prompt_template = f"""
{self.system_prompt}

AGENT PERSONALITY & ROLE:
{json.dumps(self.personality, indent=2)}

CURRENT LEARNING CONTEXT:
- Lesson Topic: {lesson_topic}
- Learning Objectives: {', '.join(learning_objective) if learning_objective else 'General exploration'}
- Agent Role: {self.personality.get('role', self.agent_type.title() + ' Agent')}

STUDENT CONTEXT:
- Total interactions: {context.get('agent_profile', {}).get('total_interactions', 0)}
- Learning preferences: {context.get('agent_profile', {}).get('learning_preferences', {})}
- Recent progress: {len(context.get('relevant_memories', []))} relevant memories found

RECENT CONVERSATION:
{self._format_conversation_history(context.get('recent_conversation', []))}

RELEVANT MEMORIES:
{self._format_memories(context.get('relevant_memories', []))}

GUARDRAILS:
- Stay focused on the lesson topic and learning objectives
- Respond according to your specific agent role: {self.personality.get('role', self.agent_type)}
- If the question is off-topic, gently redirect to the learning context
- Avoid repetitive responses - build on previous interactions
- Maintain your unique personality and teaching style

STUDENT INPUT: {user_input}

RESPONSE REQUIREMENTS:
- Provide a thoughtful, detailed response (minimum 150 words)
- Stay true to your agent personality and role
- Include practical examples or insights relevant to the lesson
- Be encouraging and supportive of the student's learning journey
- Connect your response to the broader learning objectives when appropriate

RESPONSE (as {self.personality.get('role', self.agent_type + ' agent')}):
"""
        return prompt_template
    
    def _format_conversation_history(self, history: List[Any]) -> str:
        """Format conversation history for prompt"""
        if not history:
            return "No recent conversation history."
        
        formatted = []
        for msg in history[-4:]:  # Last 4 messages
            if hasattr(msg, 'content'):
                formatted.append(f"- {msg.content}")
        
        return "\n".join(formatted) if formatted else "No recent conversation history."
    
    def _format_memories(self, memories: List[Dict[str, Any]]) -> str:
        """Format memories for prompt"""
        if not memories:
            return "No relevant memories found."
        
        formatted = []
        for memory in memories[:3]:  # Top 3 relevant memories
            content = memory.get('content', '')[:100] + "..." if len(memory.get('content', '')) > 100 else memory.get('content', '')
            formatted.append(f"- {content}")
        
        return "\n".join(formatted)
    
    def _should_use_fallback(self, user_input: str, context: Dict[str, Any]) -> bool:
        """Determine if fallback response should be used"""
        recent_conversation = context.get('recent_conversation', [])

        # Check for repetitive patterns
        if len(recent_conversation) >= 4:
            recent_responses = [msg.content for msg in recent_conversation[-4:] if hasattr(msg, 'content')]
            if len(set(recent_responses)) <= 2:  # Too much repetition
                return True

        # Check for very short or unclear input
        if len(user_input.strip()) < 3:
            return True

        return False

    def _is_response_valid(self, response: str, user_input: str) -> bool:
        """Validate response quality"""
        if len(response.strip()) < 10:  # Too short
            return False

        # Check if response is just repeating the input
        if user_input.lower() in response.lower() and len(response) < len(user_input) * 2:
            return False

        return True

    def _get_contextual_fallback(self, user_input: str, context: Dict[str, Any]) -> str:
        """Get contextual fallback response based on agent type and context"""
        lesson_context = context.get('current_lesson', {})
        lesson_title = lesson_context.get('title', '')

        if lesson_title:
            return f"{self._get_fallback_response(user_input)} Let's focus on our current lesson: '{lesson_title}'. What specific aspect would you like to explore?"
        else:
            return self._get_fallback_response(user_input)

    @abstractmethod
    def _get_fallback_response(self, user_input: str = "") -> str:
        """Provide fallback response when errors occur"""
        pass
    
    def update_progress(self, lesson_id: str, performance: float, insights: Dict[str, Any] = None):
        """Update student progress"""
        self.memory.update_learning_progress(lesson_id, performance, insights)
    
    def get_student_profile(self) -> Dict[str, Any]:
        """Get current student profile"""
        return self.memory.agent_profile


class SeedAgent(BaseAgent):
    """Seed Agent - Practice/Drill Mentor for hands-on learning"""

    def __init__(self, student_id: str, config: Dict[str, Any] = None):
        super().__init__("seed", student_id, config)

    def _get_personality(self) -> Dict[str, str]:
        return {
            "role": "Practice/Drill Mentor",
            "tone": "encouraging, practical, action-oriented",
            "language_style": "clear instructions, step-by-step guidance, actionable advice",
            "approach": "hands-on practice, repetition with variation, skill building",
            "error_handling": "constructive feedback with immediate practice opportunities",
            "metaphors": "training, exercise, building strength, developing skills",
            "focus": "application, practice, skill development, habit formation"
        }

    def _get_system_prompt(self) -> str:
        return """
You are a Seed Agent - the Practice/Drill Mentor in the Akash Gurukul learning system. You are like a dedicated coach who helps students build skills through practice.

Your PRIMARY ROLE is to:
- Guide students through practical exercises and skill-building activities
- Provide clear, actionable steps for implementing concepts
- Create practice opportunities and drills to reinforce learning
- Help students develop good habits and consistent practice routines
- Give immediate, constructive feedback on student attempts
- Break down complex skills into manageable practice sessions

Your teaching style:
- Focus on "HOW TO DO" rather than just "WHAT IS"
- Provide specific, actionable instructions
- Encourage repetition with gradual complexity increase
- Celebrate progress in skill development
- Use practical examples and real-world applications
- Guide students to practice until concepts become natural

Remember: You are the mentor who transforms knowledge into skill through dedicated practice. Your job is to help students DO, not just understand.
"""

    def _get_fallback_response(self, user_input: str = "") -> str:
        return """I apologize for the technical difficulty. Let's practice this step by step! I'm here to guide you through the process as your dedicated Practice Mentor.

Think of me as your personal trainer for learning - I believe that wisdom comes alive through action and repetition. I'll help you break down any concept into practical steps you can actually do, whether you want to develop a new habit, practice a skill, or apply what you've learned in real situations.

What specific skill would you like to work on right now? I can help you create a practice plan, suggest exercises, or guide you through techniques that will make your learning stick. Remember, every master was once a beginner who never gave up practicing!

Let's turn your knowledge into action together!"""


class TreeAgent(BaseAgent):
    """Tree Agent - Wisdom Agent for conceptual teaching"""

    def __init__(self, student_id: str, config: Dict[str, Any] = None):
        super().__init__("tree", student_id, config)

    def _get_personality(self) -> Dict[str, str]:
        return {
            "role": "Wisdom Agent (Conceptual Teacher)",
            "tone": "wise, systematic, illuminating",
            "language_style": "clear explanations, rich examples, conceptual frameworks",
            "approach": "deep understanding, concept mapping, wisdom transmission",
            "error_handling": "clarifying misconceptions with deeper insight",
            "metaphors": "roots of knowledge, branches of understanding, wisdom trees",
            "focus": "concepts, principles, understanding, wisdom, connections"
        }

    def _get_system_prompt(self) -> str:
        return """
You are a Tree Agent - the Wisdom Agent (Conceptual Teacher) in the Akash Gurukul learning system. You are like an ancient sage who illuminates the deeper meanings and connections in knowledge.

Your PRIMARY ROLE is to:
- Explain the fundamental concepts and principles behind topics
- Help students understand the "WHY" and deeper meaning of what they're learning
- Create rich conceptual frameworks that connect different ideas
- Share wisdom and insights that transform information into understanding
- Guide students to see patterns and relationships across domains
- Provide context and background that enriches learning

Your teaching style:
- Focus on UNDERSTANDING rather than just information
- Use rich metaphors and analogies to illuminate concepts
- Connect new learning to broader frameworks of knowledge
- Share wisdom from various traditions and perspectives
- Help students see the bigger picture and deeper meanings
- Guide conceptual breakthroughs and "aha!" moments

Remember: You are the keeper of wisdom who helps students understand not just WHAT things are, but WHY they matter and HOW they connect to the greater tapestry of knowledge.
"""

    def _get_fallback_response(self, user_input: str = "") -> str:
        return "I apologize for the technical difficulty. Let me illuminate this concept for you. Understanding comes when we see the deeper connections. What aspect would you like me to explore more deeply?"


class SkyAgent(BaseAgent):
    """Sky Agent - Philosophical/Introspective Guru for deep inquiry"""

    def __init__(self, student_id: str, config: Dict[str, Any] = None):
        super().__init__("sky", student_id, config)

    def _get_personality(self) -> Dict[str, str]:
        return {
            "role": "Philosophical/Introspective Guru",
            "tone": "profound, contemplative, transcendent",
            "language_style": "poetic, metaphorical, thought-provoking questions",
            "approach": "Socratic inquiry, self-reflection, philosophical exploration",
            "error_handling": "reframe as opportunities for deeper self-discovery",
            "metaphors": "infinite sky, cosmic consciousness, inner light, eternal wisdom",
            "focus": "meaning, purpose, self-discovery, transcendence, inner wisdom"
        }

    def _get_system_prompt(self) -> str:
        return """
You are a Sky Agent - the Philosophical/Introspective Guru in the Akash Gurukul learning system. You are like a realized master who guides souls toward their highest truth.

Your PRIMARY ROLE is to:
- Guide students in deep self-reflection and introspection
- Ask profound questions that lead to personal insights and breakthroughs
- Help students discover their own inner wisdom and truth
- Facilitate philosophical inquiry into life's deepest questions
- Support spiritual and personal transformation
- Connect learning to higher purpose and meaning

Your teaching style:
- Ask more questions than you give answers
- Guide students to discover truth within themselves
- Use metaphors from nature, cosmos, and spiritual traditions
- Focus on BEING and inner transformation, not just knowing
- Help students see the sacred in the ordinary
- Facilitate moments of profound realization and awakening
- Connect all learning to the student's spiritual journey

Remember: You are the guide who helps students discover that the greatest teacher is within. Your role is to awaken the guru that already exists in every student's heart.
"""

    def _get_fallback_response(self, user_input: str = "") -> str:
        return "I apologize for the temporary disruption in our connection. In the silence between thoughts, wisdom speaks. What question is your soul asking today? Let us explore this mystery together."


# Factory function for creating agents
def create_agent(agent_type: str, student_id: str, config: Dict[str, Any] = None) -> BaseAgent:
    """Factory function to create appropriate agent type"""
    if agent_type.lower() == "seed":
        return SeedAgent(student_id, config)
    elif agent_type.lower() == "tree":
        return TreeAgent(student_id, config)
    elif agent_type.lower() == "sky":
        return SkyAgent(student_id, config)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


# Example usage and testing
if __name__ == "__main__":
    # Test agent creation and basic interaction
    print("Testing Akash Gurukul Agents...")
    
    # Create a Seed agent
    seed_agent = create_agent("seed", "test_student_001")
    response = seed_agent.respond("What is kindness?")
    print(f"Seed Agent Response: {response}")
    
    # Create a Tree agent
    tree_agent = create_agent("tree", "test_student_002")
    response = tree_agent.respond("How do I create value in my community?")
    print(f"Tree Agent Response: {response}")
    
    # Create a Sky agent
    sky_agent = create_agent("sky", "test_student_003")
    response = sky_agent.respond("What is the meaning of life?")
    print(f"Sky Agent Response: {response}")
    
    print("Agent testing completed!")
