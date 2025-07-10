# Akash Gurukul Backend Deployment Guide

## 🚀 Backend-Only Deployment Package

This package contains only the backend components needed to run the Akash Gurukul API server.

## 📁 Backend Structure

```
akash-gurukul-backend/
├── backend/
│   ├── main.py              # FastAPI application
│   └── test_api.py          # API testing script
├── agents/
│   ├── __init__.py
│   ├── base_agent.py        # Core agent logic
│   └── memory_system.py     # Agent memory management
├── curriculum/
│   ├── __init__.py
│   ├── ingestion.py         # Lesson loading system
│   ├── lesson_flow.py       # Lesson progression logic
│   └── lessons/             # Lesson content files
│       ├── foundation_000_sankalpa-invocation.json
│       ├── seed_dharma_001_introduction-to-kindness.json
│       ├── tree_artha_001_understanding-value-creation.json
│       └── tree_dharma_002_compassion-in-action.json
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 3. Verify Installation
```bash
python backend/test_api.py
```

## 📡 API Endpoints

### Health & System
- `GET /api/health` - System health check
- `GET /docs` - Interactive API documentation

### Curriculum Management
- `GET /api/curriculum/lessons` - Get all lessons
- `GET /api/curriculum/lessons/{lesson_id}` - Get specific lesson
- `GET /api/curriculum/learning-paths` - Get learning paths by category

### Agent Interaction
- `POST /api/agents/chat` - Chat with agents (Seed, Tree, Sky)
- `GET /api/agents/{agent_type}/profile` - Get agent profile
- `POST /api/agents/update-progress` - Update learning progress

### Lesson Flow Management
- `POST /api/lessons/start` - Start a lesson
- `POST /api/lessons/interact` - Record lesson interaction
- `GET /api/lessons/suggest-agent/{student_id}` - Get agent suggestion
- `POST /api/lessons/complete` - Complete a lesson

### Quiz System
- `GET /api/quiz/questions/{lesson_id}` - Get quiz questions
- `POST /api/quiz/submit` - Submit quiz answer
- `GET /api/quiz/progress/{student_id}/{lesson_id}` - Get quiz progress

### Student Progress
- `GET /api/students/{student_id}/progress` - Get student progress

## 🤖 Agent Types

### Seed Agent - Practice/Drill Mentor
- **Focus**: Hands-on practice and skill building
- **Use Case**: "How can I practice kindness?"
- **Response Style**: Step-by-step guidance, practical exercises

### Tree Agent - Wisdom Teacher
- **Focus**: Conceptual understanding and deeper meaning
- **Use Case**: "Why is compassion important?"
- **Response Style**: Explanations, principles, connections

### Sky Agent - Philosophical Guru
- **Focus**: Spiritual inquiry and introspection
- **Use Case**: "What does kindness mean to my soul?"
- **Response Style**: Reflective questions, philosophical insights

## 📚 Lesson Categories

### Foundation
- Introductory spiritual and philosophical concepts
- Gurukul principles and sacred learning

### Dharma (Righteousness)
- Ethical principles and moral development
- Character building and virtue cultivation

### Artha (Prosperity)
- Value creation and meaningful work
- Resource management and abundance

### Kama (Fulfillment)
- Healthy desires and relationships
- Emotional intelligence and joy

### Moksha (Liberation)
- Spiritual growth and transcendence
- Self-realization and freedom

## 🔄 API Usage Examples

### Start a Lesson
```python
import requests

response = requests.post("http://localhost:8000/api/lessons/start", json={
    "student_id": "student_123",
    "lesson_id": "foundation_000_sankalpa"
})
```

### Chat with Agent
```python
response = requests.post("http://localhost:8000/api/agents/chat", json={
    "agent_type": "seed",
    "student_id": "student_123",
    "message": "How can I practice kindness today?"
})
```

### Submit Quiz Answer
```python
response = requests.post("http://localhost:8000/api/quiz/submit", json={
    "student_id": "student_123",
    "lesson_id": "foundation_000_sankalpa",
    "quiz_id": "sankalpa_meaning",
    "answer": 1
})
```

## 🛠️ Configuration

### Environment Variables (Optional)
```bash
OPENAI_API_KEY=your_openai_key_here  # For production LLM
PINECONE_API_KEY=your_pinecone_key   # For production vector store
```

### Fallback Behavior
- **LLM**: Uses fake LLM for testing when OpenAI key not provided
- **Vector Store**: Uses FAISS with dummy embeddings when Pinecone not available
- **Memory**: Local file-based storage for agent memories

## 📊 System Features

### Agent Memory System
- Conversation history tracking
- Context-aware responses
- Student progress memory
- Vector-based knowledge retrieval

### Lesson Flow Management
- State tracking (not_started → in_progress → completed)
- Agent interaction recording
- Progress analytics
- Mastery assessment

### Quiz System
- Multiple question types (multiple choice, scenario, reflection)
- Real-time scoring
- Agent-specific feedback
- Progress tracking

### Curriculum Engine
- JSON-based lesson format
- Dependency validation
- Learning path generation
- Category-based organization

## 🔒 Security Notes

- No authentication required for development
- Student IDs are used for session management
- All data stored locally during development
- Production deployment should add proper authentication

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Port Conflicts**: Change port in uvicorn command if 8000 is busy
3. **Memory Warnings**: LangChain deprecation warnings are normal
4. **Lesson Loading**: Check JSON format if lessons fail to load

### Debug Mode
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## 📈 Performance

- **Startup Time**: ~3-5 seconds
- **Response Time**: <200ms for most endpoints
- **Memory Usage**: ~100-200MB base
- **Concurrent Users**: Supports 50+ concurrent connections

## 🔄 Development Workflow

1. **Start Server**: `uvicorn backend.main:app --reload`
2. **Test APIs**: Use `/docs` for interactive testing
3. **Add Lessons**: Place JSON files in `curriculum/lessons/`
4. **Test Changes**: Run `python backend/test_api.py`

## 📞 Support

For backend-specific issues:
- Check server logs for detailed error messages
- Use `/api/health` endpoint to verify system status
- Test individual endpoints using `/docs` interface
- Review lesson JSON format in `curriculum/lesson-format.md`

## 🎯 Production Deployment

For production deployment:
1. Set environment variables for OpenAI and Pinecone
2. Configure proper authentication
3. Set up database for persistent storage
4. Add monitoring and logging
5. Configure CORS for frontend domains
6. Set up SSL/TLS certificates

---

**The Akash Gurukul backend is ready to serve wisdom through APIs!** 🕉️
