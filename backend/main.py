"""
FastAPI Backend for Akash Gurukul
Provides API endpoints for agent interactions, lesson management, and curriculum ingestion
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.base_agent import create_agent
from curriculum.ingestion import CurriculumIngestion
from curriculum.lesson_flow import LessonFlowManager
from agents.agent_chaining import agent_chain_manager, AgentChainContext

app = FastAPI(
    title="Akash Gurukul API",
    description="AI-Powered Educational Platform with Intelligent Agents",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global instances
curriculum_ingestion = CurriculumIngestion()
active_agents: Dict[str, Any] = {}
lesson_flow_managers: Dict[str, LessonFlowManager] = {}

@app.on_event("startup")
async def startup_event():
    """Load curriculum on startup"""
    try:
        curriculum_ingestion.load_all_lessons()
        print(f"Loaded {len(curriculum_ingestion.lessons)} lessons successfully")
    except Exception as e:
        print(f"Error loading curriculum on startup: {e}")

# Pydantic models for API requests/responses
class AgentRequest(BaseModel):
    agent_type: str  # "seed", "tree", or "sky"
    student_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    response: str
    agent_type: str
    student_id: str
    context: Optional[Dict[str, Any]] = None

class LessonRequest(BaseModel):
    lesson_id: str

class LessonResponse(BaseModel):
    lesson: Dict[str, Any]

class ProgressUpdate(BaseModel):
    student_id: str
    lesson_id: str
    performance: float
    insights: Optional[Dict[str, Any]] = None

class LessonStartRequest(BaseModel):
    student_id: str
    lesson_id: str

class LessonInteractionRequest(BaseModel):
    student_id: str
    lesson_id: str
    agent_type: str
    query_path: str
    user_input: str

class LessonCompletionRequest(BaseModel):
    student_id: str
    lesson_id: str
    quiz_score: Optional[float] = None
    mastery_indicators: Optional[Dict[str, Any]] = None

class AgentSuggestionResponse(BaseModel):
    suggested_agent: str
    suggested_query_path: str
    reasoning: str

class QuizSubmissionRequest(BaseModel):
    student_id: str
    lesson_id: str
    quiz_id: str
    answer: Any  # Can be int, str, list, etc.
    time_taken: Optional[float] = None

class QuizSubmissionResponse(BaseModel):
    correct: bool
    score: float
    explanation: str
    agent_feedback: Optional[str] = None
    next_question: Optional[Dict[str, Any]] = None

class QuizProgressRequest(BaseModel):
    student_id: str
    lesson_id: str

# Initialize curriculum on module load
try:
    curriculum_ingestion.load_all_lessons()
    try:
        curriculum_ingestion.validate_dependencies()
    except ValueError as e:
        print(f"Warning: Dependency validation issues: {e}")
    curriculum_ingestion.generate_learning_paths()
    print(f"Loaded {len(curriculum_ingestion.lessons)} lessons successfully")
except Exception as e:
    print(f"Error loading curriculum: {e}")

# Agent endpoints
@app.post("/api/agents/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """Chat with a specific agent type with enhanced lesson context"""
    try:
        # Get or create lesson flow manager
        if request.student_id not in lesson_flow_managers:
            lesson_flow_managers[request.student_id] = LessonFlowManager(request.student_id)

        flow_manager = lesson_flow_managers[request.student_id]

        # Create or get existing agent
        agent_key = f"{request.agent_type}_{request.student_id}"

        if agent_key not in active_agents:
            active_agents[agent_key] = create_agent(
                request.agent_type,
                request.student_id
            )

        agent = active_agents[agent_key]

        # Enhance context with lesson flow information
        enhanced_context = request.context or {}
        current_lesson_id = None
        if flow_manager.student_progress.get("current_lesson"):
            current_lesson_id = flow_manager.student_progress["current_lesson"]
            lesson_data = curriculum_ingestion.get_lesson(current_lesson_id)
            if lesson_data:
                enhanced_context.update(flow_manager._build_lesson_context(current_lesson_id, lesson_data))

        # Check for potential agent transitions using chaining system
        transition_suggestion = agent_chain_manager.suggest_agent_transition(
            current_agent=request.agent_type,
            user_input=request.message,
            student_id=request.student_id,
            lesson_id=current_lesson_id
        )

        # Add chain context to enhanced context
        chain_context = agent_chain_manager.get_or_create_chain(request.student_id, current_lesson_id)
        enhanced_context.update({
            "chain_context": chain_context.get_context_for_agent(request.agent_type),
            "transition_suggestion": transition_suggestion
        })

        # Generate response
        response = agent.respond(request.message, enhanced_context)

        # Record the interaction in the chain
        agent_chain_manager.record_agent_interaction(
            agent_type=request.agent_type,
            user_input=request.message,
            agent_response=response,
            student_id=request.student_id,
            lesson_id=current_lesson_id,
            insights={"response_length": len(response)}
        )

        return AgentResponse(
            response=response,
            agent_type=request.agent_type,
            student_id=request.student_id,
            context={
                "agent_profile": agent.get_student_profile(),
                "transition_suggestion": transition_suggestion,
                "chain_summary": agent_chain_manager.get_chain_summary(request.student_id, current_lesson_id)
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing agent request: {str(e)}")

@app.get("/api/agents/chain-suggestion/{student_id}")
async def get_agent_chain_suggestion(student_id: str, current_agent: str, user_input: str, lesson_id: str = None):
    """Get intelligent agent chaining suggestion"""
    try:
        suggestion = agent_chain_manager.suggest_agent_transition(
            current_agent=current_agent,
            user_input=user_input,
            student_id=student_id,
            lesson_id=lesson_id
        )

        return {
            "student_id": student_id,
            "current_agent": current_agent,
            "suggestion": suggestion,
            "chain_summary": agent_chain_manager.get_chain_summary(student_id, lesson_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chain suggestion: {str(e)}")

@app.get("/api/agents/chain-summary/{student_id}")
async def get_agent_chain_summary(student_id: str, lesson_id: str = None):
    """Get summary of current agent chain for student"""
    try:
        summary = agent_chain_manager.get_chain_summary(student_id, lesson_id)
        return {
            "student_id": student_id,
            "lesson_id": lesson_id,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chain summary: {str(e)}")

@app.get("/api/agents/{agent_type}/{student_id}/profile")
async def get_agent_profile(agent_type: str, student_id: str):
    """Get student profile from agent memory"""
    try:
        agent_key = f"{agent_type}_{student_id}"
        
        if agent_key not in active_agents:
            active_agents[agent_key] = create_agent(agent_type, student_id)
        
        agent = active_agents[agent_key]
        return {"profile": agent.get_student_profile()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving profile: {str(e)}")

@app.post("/api/agents/progress")
async def update_progress(progress: ProgressUpdate):
    """Update student progress across all agent types"""
    try:
        # Update progress for all agent types for this student
        for agent_type in ["seed", "tree", "sky"]:
            agent_key = f"{agent_type}_{progress.student_id}"
            
            if agent_key not in active_agents:
                active_agents[agent_key] = create_agent(agent_type, progress.student_id)
            
            agent = active_agents[agent_key]
            agent.update_progress(progress.lesson_id, progress.performance, progress.insights)
        
        return {"status": "success", "message": "Progress updated for all agents"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating progress: {str(e)}")

# Lesson Flow endpoints
@app.post("/api/lessons/start")
async def start_lesson(request: LessonStartRequest):
    """Start a new lesson with proper flow management"""
    try:
        # Get or create lesson flow manager
        if request.student_id not in lesson_flow_managers:
            lesson_flow_managers[request.student_id] = LessonFlowManager(request.student_id)

        flow_manager = lesson_flow_managers[request.student_id]

        # Get lesson data
        lesson_data = curriculum_ingestion.get_lesson(request.lesson_id)
        if not lesson_data:
            raise HTTPException(status_code=404, detail="Lesson not found")

        # Start lesson
        lesson_context = flow_manager.start_lesson(request.lesson_id, lesson_data)

        return {
            "status": "lesson_started",
            "lesson_context": lesson_context,
            "message": f"Started lesson: {lesson_data['title']}"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting lesson: {str(e)}")

@app.post("/api/lessons/interact")
async def record_lesson_interaction(request: LessonInteractionRequest):
    """Record an interaction during a lesson"""
    try:
        # Get lesson flow manager
        if request.student_id not in lesson_flow_managers:
            raise HTTPException(status_code=404, detail="No active lesson session found")

        flow_manager = lesson_flow_managers[request.student_id]

        # Record interaction (we'll get the agent response from the chat endpoint)
        flow_manager.record_interaction(
            request.lesson_id,
            request.agent_type,
            request.query_path,
            request.user_input,
            "Response recorded",  # Placeholder - actual response comes from chat endpoint
            1.0  # Default quality score
        )

        return {"status": "interaction_recorded"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording interaction: {str(e)}")

@app.get("/api/lessons/suggest-agent/{student_id}")
async def suggest_next_agent(student_id: str, user_input: str, current_agent: str = "seed"):
    """Suggest the best agent for the next interaction"""
    try:
        # Get lesson flow manager
        if student_id not in lesson_flow_managers:
            lesson_flow_managers[student_id] = LessonFlowManager(student_id)

        flow_manager = lesson_flow_managers[student_id]
        current_lesson = flow_manager.student_progress.get("current_lesson")

        if not current_lesson:
            # Default suggestion if no active lesson
            return AgentSuggestionResponse(
                suggested_agent="seed",
                suggested_query_path="practical",
                reasoning="Starting with practical guidance for new learners"
            )

        suggested_agent, suggested_path = flow_manager.suggest_next_agent(
            current_lesson, current_agent, user_input
        )

        # Create reasoning based on suggestion
        reasoning_map = {
            "seed": "Your question suggests you want to practice and apply concepts",
            "tree": "Your question indicates you want to understand concepts more deeply",
            "sky": "Your question shows you're ready for philosophical reflection"
        }

        return AgentSuggestionResponse(
            suggested_agent=suggested_agent,
            suggested_query_path=suggested_path,
            reasoning=reasoning_map.get(suggested_agent, "Based on your learning pattern")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error suggesting agent: {str(e)}")

@app.post("/api/lessons/complete")
async def complete_lesson(request: LessonCompletionRequest):
    """Mark a lesson as completed"""
    try:
        # Get lesson flow manager
        if request.student_id not in lesson_flow_managers:
            raise HTTPException(status_code=404, detail="No lesson session found")

        flow_manager = lesson_flow_managers[request.student_id]

        # Complete lesson
        completion_result = flow_manager.complete_lesson(
            request.lesson_id,
            request.quiz_score,
            request.mastery_indicators
        )

        return completion_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error completing lesson: {str(e)}")

@app.get("/api/students/{student_id}/progress")
async def get_student_progress(student_id: str):
    """Get comprehensive student progress summary"""
    try:
        # Get or create lesson flow manager
        if student_id not in lesson_flow_managers:
            lesson_flow_managers[student_id] = LessonFlowManager(student_id)

        flow_manager = lesson_flow_managers[student_id]
        return flow_manager.get_student_summary()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving progress: {str(e)}")

# Quiz endpoints
@app.post("/api/quiz/submit", response_model=QuizSubmissionResponse)
async def submit_quiz_answer(request: QuizSubmissionRequest):
    """Submit an answer to a quiz question"""
    try:
        # Get lesson data to access quiz
        lesson_data = curriculum_ingestion.get_lesson(request.lesson_id)
        if not lesson_data:
            raise HTTPException(status_code=404, detail="Lesson not found")

        # Find the specific quiz question
        quiz_questions = lesson_data.get("quiz", [])
        quiz_question = None
        for q in quiz_questions:
            if q["id"] == request.quiz_id:
                quiz_question = q
                break

        if not quiz_question:
            raise HTTPException(status_code=404, detail="Quiz question not found")

        # Evaluate the answer
        correct = False
        score = 0.0
        explanation = quiz_question.get("explanation", "")

        if quiz_question["type"] == "multiple_choice":
            correct = request.answer == quiz_question["correct_answer"]
            score = 1.0 if correct else 0.0
        elif quiz_question["type"] == "scenario":
            correct = request.answer == quiz_question["correct_answer"]
            score = 1.0 if correct else 0.0
        elif quiz_question["type"] == "true_false":
            correct = request.answer == quiz_question["correct_answer"]
            score = 1.0 if correct else 0.0
        elif quiz_question["type"] == "reflection":
            # For reflection questions, we give partial credit based on length and effort
            answer_length = len(str(request.answer)) if request.answer else 0
            if answer_length > 50:
                score = 1.0
                correct = True
            elif answer_length > 20:
                score = 0.7
                correct = True
            else:
                score = 0.3
                correct = False

        # Get agent-specific feedback if available
        agent_feedback = None
        if "agent_specific_feedback" in quiz_question:
            # For now, default to seed agent feedback
            agent_feedback = quiz_question["agent_specific_feedback"].get("seed", "")

        # Store the quiz result
        if request.student_id not in lesson_flow_managers:
            lesson_flow_managers[request.student_id] = LessonFlowManager(request.student_id)

        flow_manager = lesson_flow_managers[request.student_id]

        # Record quiz interaction
        flow_manager.record_interaction(
            request.lesson_id,
            "quiz",
            "assessment",
            f"Quiz: {request.quiz_id}",
            f"Score: {score}",
            score
        )

        # Find next question if available
        next_question = None
        current_index = next((i for i, q in enumerate(quiz_questions) if q["id"] == request.quiz_id), -1)
        if current_index >= 0 and current_index + 1 < len(quiz_questions):
            next_question = quiz_questions[current_index + 1]

        return QuizSubmissionResponse(
            correct=correct,
            score=score,
            explanation=explanation,
            agent_feedback=agent_feedback,
            next_question=next_question
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting quiz answer: {str(e)}")

@app.get("/api/quiz/progress/{student_id}/{lesson_id}")
async def get_quiz_progress(student_id: str, lesson_id: str):
    """Get student's quiz progress for a lesson"""
    try:
        if student_id not in lesson_flow_managers:
            return {"quiz_attempts": [], "total_score": 0.0, "completion_rate": 0.0}

        flow_manager = lesson_flow_managers[student_id]
        lesson_progress = flow_manager.student_progress["lessons"].get(lesson_id, {})

        # Filter quiz interactions
        quiz_interactions = []
        for interaction in lesson_progress.get("interactions", []):
            if interaction.get("agent_type") == "quiz":
                quiz_interactions.append(interaction)

        # Calculate total score and completion rate
        lesson_data = curriculum_ingestion.get_lesson(lesson_id)
        total_questions = len(lesson_data.get("quiz", [])) if lesson_data else 0

        total_score = sum(interaction.get("quality_score", 0) for interaction in quiz_interactions)
        completion_rate = len(quiz_interactions) / total_questions if total_questions > 0 else 0.0

        return {
            "quiz_attempts": quiz_interactions,
            "total_score": total_score,
            "completion_rate": completion_rate,
            "total_questions": total_questions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quiz progress: {str(e)}")

@app.get("/api/quiz/questions/{lesson_id}")
async def get_quiz_questions(lesson_id: str):
    """Get all quiz questions for a lesson"""
    try:
        lesson_data = curriculum_ingestion.get_lesson(lesson_id)
        if not lesson_data:
            raise HTTPException(status_code=404, detail="Lesson not found")

        quiz_questions = lesson_data.get("quiz", [])

        # Remove correct answers from the response for security
        safe_questions = []
        for q in quiz_questions:
            safe_q = {k: v for k, v in q.items() if k != "correct_answer"}
            safe_questions.append(safe_q)

        return {"questions": safe_questions, "total_count": len(safe_questions)}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quiz questions: {str(e)}")

# Curriculum endpoints
@app.get("/api/curriculum/lessons")
async def get_all_lessons():
    """Get all available lessons"""
    try:
        return {
            "lessons": curriculum_ingestion.lessons,
            "total_count": len(curriculum_ingestion.lessons)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving lessons: {str(e)}")

@app.get("/api/curriculum/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: str):
    """Get a specific lesson by ID"""
    try:
        lesson = curriculum_ingestion.get_lesson(lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        return LessonResponse(lesson=lesson)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving lesson: {str(e)}")

@app.get("/api/curriculum/lessons/level/{level}")
async def get_lessons_by_level(level: str, category: Optional[str] = None):
    """Get lessons by level and optionally by category"""
    try:
        lessons = curriculum_ingestion.get_lessons_by_level(level, category)
        return {
            "lessons": lessons,
            "level": level,
            "category": category,
            "count": len(lessons)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving lessons: {str(e)}")

@app.get("/api/curriculum/learning-paths")
async def get_learning_paths():
    """Get all learning paths organized by category and level"""
    try:
        return {
            "learning_paths": curriculum_ingestion.learning_paths,
            "metadata": {
                "categories": ["dharma", "artha", "kama", "moksha"],
                "levels": ["Seed", "Tree", "Sky"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving learning paths: {str(e)}")

@app.post("/api/curriculum/reload")
async def reload_curriculum():
    """Reload curriculum data (useful for development)"""
    try:
        curriculum_ingestion.lessons.clear()
        curriculum_ingestion.learning_paths.clear()
        
        curriculum_ingestion.load_all_lessons()
        try:
            curriculum_ingestion.validate_dependencies()
        except ValueError as e:
            print(f"Warning: Dependency validation issues: {e}")
        curriculum_ingestion.generate_learning_paths()
        
        return {
            "status": "success",
            "message": f"Reloaded {len(curriculum_ingestion.lessons)} lessons"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading curriculum: {str(e)}")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Akash Gurukul API",
        "version": "1.0.0",
        "agents_active": len(active_agents),
        "lessons_loaded": len(curriculum_ingestion.lessons)
    }

# Root endpoint
@app.get("/")
async def root():
    """Serve the main web interface"""
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
