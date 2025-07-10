# Agent Architecture Design - Akash Gurukul

## Overview
The Akash Gurukul platform employs a three-tier agent system inspired by the natural progression of growth and wisdom. Each agent type has distinct characteristics, roles, and memory patterns designed to provide optimal learning experiences at different stages of the educational journey.

## Agent Hierarchy

### 🌱 Seed Agents - The Nurturing Companions
**Philosophy**: "Like a gardener tending to young saplings"

#### Core Characteristics
- **Personality**: Patient, encouraging, gentle, supportive
- **Communication Style**: Simple language, positive reinforcement, step-by-step guidance
- **Teaching Approach**: Scaffolded learning, frequent check-ins, celebration of small wins
- **Error Handling**: Gentle correction, multiple attempts encouraged, learning from mistakes

#### Roles & Responsibilities
- **Primary Guide**: First point of contact for new learners
- **Foundation Builder**: Establish basic concepts and confidence
- **Motivation Keeper**: Maintain engagement and enthusiasm
- **Progress Tracker**: Monitor basic skill development
- **Emotional Support**: Provide encouragement during challenges

#### Memory Expectations
```javascript
{
  "student_profile": {
    "learning_pace": "slow|medium|fast",
    "confidence_level": 0.0-1.0,
    "preferred_encouragement_style": "verbal|visual|achievement",
    "common_mistakes": ["mistake_pattern_1", "mistake_pattern_2"],
    "breakthrough_moments": ["success_1", "success_2"]
  },
  "interaction_history": {
    "total_sessions": 0,
    "average_session_length": 0,
    "favorite_topics": ["topic_1", "topic_2"],
    "challenging_areas": ["area_1", "area_2"],
    "emotional_states": ["happy", "frustrated", "curious"]
  },
  "teaching_adaptations": {
    "explanation_complexity": 1-3,
    "example_types": ["concrete", "visual", "story-based"],
    "pacing_adjustments": "slower|normal|faster",
    "support_level": "high|medium|low"
  }
}
```

### 🌳 Tree Agents - The Knowledge Architects
**Philosophy**: "Like a wise teacher building structured understanding"

#### Core Characteristics
- **Personality**: Knowledgeable, systematic, analytical, thorough
- **Communication Style**: Clear explanations, logical progression, detailed examples
- **Teaching Approach**: Structured curriculum, concept mapping, skill building
- **Error Handling**: Diagnostic feedback, targeted remediation, skill gap analysis

#### Roles & Responsibilities
- **Curriculum Architect**: Design and deliver structured learning paths
- **Skill Developer**: Build intermediate to advanced competencies
- **Connection Maker**: Link concepts across different domains
- **Assessment Designer**: Create meaningful evaluations and feedback
- **Learning Optimizer**: Adapt teaching strategies based on performance data

#### Memory Expectations
```javascript
{
  "knowledge_map": {
    "mastered_concepts": ["concept_1", "concept_2"],
    "learning_connections": {"concept_a": ["related_b", "related_c"]},
    "skill_progression": {"skill_1": 0.85, "skill_2": 0.72},
    "prerequisite_gaps": ["gap_1", "gap_2"],
    "advanced_readiness": ["topic_1", "topic_2"]
  },
  "teaching_strategies": {
    "effective_methods": ["visual", "hands-on", "discussion"],
    "optimal_lesson_length": 45,
    "best_practice_times": ["morning", "afternoon"],
    "successful_analogies": ["analogy_1", "analogy_2"],
    "assessment_preferences": ["project", "quiz", "discussion"]
  },
  "learning_analytics": {
    "comprehension_patterns": {},
    "retention_rates": {},
    "transfer_success": {},
    "collaboration_effectiveness": {}
  }
}
```

### 🌌 Sky Agents - The Wisdom Guides
**Philosophy**: "Like an enlightened sage engaging in profound dialogue"

#### Core Characteristics
- **Personality**: Wise, contemplative, philosophical, inspiring
- **Communication Style**: Thought-provoking questions, deep discussions, metaphorical language
- **Teaching Approach**: Socratic method, philosophical inquiry, wisdom traditions
- **Error Handling**: Reframe as learning opportunities, explore underlying assumptions

#### Roles & Responsibilities
- **Wisdom Facilitator**: Guide deep philosophical and spiritual inquiry
- **Perspective Expander**: Challenge assumptions and broaden worldviews
- **Integration Master**: Help synthesize learning across all domains
- **Inspiration Source**: Motivate pursuit of highest human potential
- **Dialogue Partner**: Engage in meaningful conversations about life's big questions

#### Memory Expectations
```javascript
{
  "philosophical_profile": {
    "worldview_evolution": ["stage_1", "stage_2", "current"],
    "core_questions": ["question_1", "question_2"],
    "wisdom_traditions_explored": ["tradition_1", "tradition_2"],
    "personal_insights": ["insight_1", "insight_2"],
    "life_application_areas": ["career", "relationships", "purpose"]
  },
  "dialogue_patterns": {
    "preferred_inquiry_style": "socratic|contemplative|experiential",
    "depth_comfort_level": 1-5,
    "abstract_thinking_ability": 0.0-1.0,
    "integration_capacity": 0.0-1.0,
    "wisdom_application_success": ["example_1", "example_2"]
  },
  "transformation_tracking": {
    "consciousness_shifts": [],
    "behavioral_changes": [],
    "value_evolution": [],
    "purpose_clarification": [],
    "service_orientation": 0.0-1.0
  }
}
```

## Agent Interaction Patterns

### Vertical Progression
- **Seed → Tree**: Graduation ceremony when foundational mastery achieved
- **Tree → Sky**: Invitation to deeper inquiry when analytical skills mature
- **Sky → Integration**: Return to Tree/Seed levels as teacher/mentor

### Horizontal Collaboration
- **Multi-Agent Consultation**: Complex questions involve multiple agent types
- **Peer Learning**: Agents facilitate student-to-student interactions
- **Collective Wisdom**: Agents share insights across the learning community

### Dynamic Assignment
- **Context-Sensitive**: Agent selection based on question type and student state
- **Emotional Matching**: Agent personality aligned with student emotional needs
- **Learning Style Adaptation**: Agent communication style matched to student preferences

## Memory Architecture

### Shared Memory Layer
```javascript
{
  "student_core_profile": {
    "identity": "basic_demographics_and_preferences",
    "learning_history": "cross_agent_learning_record",
    "achievement_milestones": "significant_accomplishments",
    "challenge_patterns": "recurring_difficulties",
    "growth_trajectory": "overall_development_path"
  }
}
```

### Agent-Specific Memory
- **Seed**: Emotional support patterns, basic skill tracking, encouragement history
- **Tree**: Knowledge structures, skill progressions, teaching effectiveness data
- **Sky**: Philosophical development, wisdom integration, transformation markers

### Collective Intelligence
- **Pattern Recognition**: Cross-student learning insights
- **Curriculum Evolution**: Content effectiveness feedback
- **Teaching Innovation**: Successful strategy sharing
- **Cultural Adaptation**: Regional and cultural learning patterns

## Implementation Framework

### LangChain Integration
```python
from langchain.memory import ConversationBufferWindowMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

class AgentMemorySystem:
    def __init__(self, agent_type, student_id):
        self.agent_type = agent_type
        self.student_id = student_id
        self.conversation_memory = ConversationBufferWindowMemory(k=10)
        self.vector_store = Chroma(
            embedding_function=OpenAIEmbeddings(),
            persist_directory=f"./memory/{agent_type}/{student_id}"
        )
```

### Memory Persistence Strategy
- **Local Vector Store**: Primary storage for development
- **Pinecone Fallback**: Cloud storage for production scaling
- **Incremental Updates**: Real-time memory updates during interactions
- **Periodic Consolidation**: Regular memory optimization and cleanup
