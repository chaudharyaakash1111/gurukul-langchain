# 👨‍💻 Akash Gurukul - Developer Guide

## 🚀 **Quick Start for New Developers**

### **Prerequisites**
- Python 3.8+
- Git
- Basic understanding of FastAPI and LangChain

### **5-Minute Setup**
```bash
# 1. Clone the repository
git clone https://github.com/chaudharyaakash1111/gurukul-langchain.git
cd gurukul-langchain

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the development server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 5. Verify installation
curl http://localhost:8000/api/health
```

### **First API Call**
```bash
curl -X POST "http://localhost:8000/api/ask-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "dev_test",
    "message": "Hello, I want to learn about kindness",
    "use_memory": true
  }'
```

---

## 🏗️ **Architecture Overview**

### **System Components**
```
┌─────────────────────────────────────────────────────────────┐
│                    AKASH GURUKUL SYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│  🌱 Seed Agent (Practice Mentor)                            │
│  🌳 Tree Agent (Wisdom Teacher)                             │
│  🌌 Sky Agent (Philosophical Guru)                          │
├─────────────────────────────────────────────────────────────┤
│  📚 Curriculum System (6 Lessons)                           │
│  🧠 Memory System (FAISS + LangChain)                       │
│  🔗 Agent Chaining (Intelligent Routing)                    │
│  🕉️ Sacred Ceremony (Agent Puja)                            │
├─────────────────────────────────────────────────────────────┤
│  ⚙️ FastAPI Backend                                          │
│  🌐 Web Interface                                            │
│  📊 Monitoring & Logging                                     │
│  🧪 Test Suite                                               │
└─────────────────────────────────────────────────────────────┘
```

### **Directory Structure**
```
akash-gurukul/
├── 📁 agents/                    # AI agent implementations
│   ├── base_agent.py            # Core agent framework
│   ├── memory_system.py         # LangChain memory + FAISS
│   └── agent_chaining.py        # Intelligent routing
├── 📁 backend/                   # FastAPI server
│   └── main.py                  # Main API server
├── 📁 curriculum/                # Learning content
│   ├── lessons/                 # JSON lesson files
│   ├── ingestion.py            # Content loading
│   └── agent_puja_ceremony.py  # Sacred onboarding
├── 📁 monitoring/                # Enterprise monitoring
│   └── logging_config.py       # Logging & metrics
├── 📁 tests/                     # Test suite
├── 📁 static/                    # Web interface
├── 📁 memory/                    # Persistent storage
└── 📁 logs/                      # Application logs
```

---

## 🤖 **Working with Agents**

### **Creating a New Agent**
```python
from agents.base_agent import create_agent

# Create agent instance
agent = create_agent('seed', 'student_123')

# Get response
response = agent.respond("How can I practice kindness?", {
    'current_lesson': 'seed_dharma_001'
})

print(response)
```

### **Agent Types and Personalities**
```python
AGENT_PERSONALITIES = {
    'seed': {
        'role': 'Practice Mentor',
        'focus': 'Hands-on learning and skill building',
        'style': 'Encouraging, practical, action-oriented',
        'keywords': ['how', 'practice', 'do', 'steps', 'exercise']
    },
    'tree': {
        'role': 'Wisdom Teacher',
        'focus': 'Conceptual understanding and principles',
        'style': 'Wise, explanatory, connecting ideas',
        'keywords': ['why', 'meaning', 'understand', 'explain', 'concept']
    },
    'sky': {
        'role': 'Philosophical Guru',
        'focus': 'Spiritual insights and deeper meaning',
        'style': 'Reflective, profound, spiritually-oriented',
        'keywords': ['purpose', 'soul', 'spiritual', 'consciousness']
    }
}
```

### **Memory System Usage**
```python
from agents.memory_system import AgentMemorySystem

# Initialize memory
memory = AgentMemorySystem('seed', 'student_123')

# Add memory
memory.add_memory(
    content="Student learned about daily kindness practices",
    metadata={'lesson': 'seed_dharma_001', 'type': 'learning'}
)

# Search memory
results = memory.search_memory("kindness practices", limit=5)
for result in results:
    print(result.page_content)
```

---

## 🔗 **API Development**

### **Main Production Endpoint**
```python
@app.post("/api/ask-agent", response_model=AskAgentResponse)
async def ask_agent(request: AskAgentRequest):
    """
    Production endpoint with:
    - Intelligent agent routing
    - Memory retrieval and storage
    - Conversation tracking
    - Confidence scoring
    """
```

### **Request/Response Models**
```python
class AskAgentRequest(BaseModel):
    student_id: str
    message: str
    preferred_agent: Optional[str] = None  # "seed", "tree", "sky"
    context: Optional[Dict[str, Any]] = None
    use_memory: bool = True
    memory_limit: int = 5

class AskAgentResponse(BaseModel):
    response: str
    agent_used: str
    routing_reason: str
    memory_retrieved: List[str]
    confidence_score: float
    suggested_next_agent: Optional[str]
    conversation_id: str
    timestamp: str
```

### **Adding New Endpoints**
```python
@app.post("/api/your-new-endpoint")
async def your_new_endpoint(request: YourRequest):
    """
    1. Add request/response models
    2. Implement business logic
    3. Add error handling
    4. Add logging
    5. Add tests
    """
    try:
        # Your logic here
        result = process_request(request)
        
        # Log the operation
        gurukul_logger.log_api_request(
            endpoint="/api/your-new-endpoint",
            method="POST",
            status_code=200,
            response_time=0.1
        )
        
        return result
        
    except Exception as e:
        gurukul_logger.log_error(e, {'endpoint': '/api/your-new-endpoint'})
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📚 **Curriculum Development**

### **Lesson Structure**
```json
{
  "id": "lesson_id",
  "title": "Lesson Title",
  "level": "seed|tree|sky|foundation",
  "category": "dharma|artha|kama|moksha",
  "prerequisites": ["prerequisite_lesson_ids"],
  "content": {
    "introduction": "...",
    "main_content": "...",
    "conclusion": "...",
    "key_points": ["point1", "point2"]
  },
  "quiz": [
    {
      "id": "q1",
      "question": "Question text?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0,
      "explanation": "Why this is correct"
    }
  ],
  "metadata": {
    "estimated_duration": 15,
    "difficulty": "beginner|intermediate|advanced",
    "tags": ["kindness", "practice", "daily"]
  }
}
```

### **Adding New Lessons**
```python
# 1. Create lesson JSON file in curriculum/lessons/
# 2. Follow naming convention: {level}_{category}_{number}_{slug}.json
# 3. Validate structure
from curriculum.ingestion import CurriculumIngestion

ingestion = CurriculumIngestion()
ingestion.validate_lesson("your_lesson.json")

# 4. Test lesson loading
ingestion.load_all_lessons()
```

---

## 🧪 **Testing**

### **Running Tests**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python tests/test_production_ready.py

# Run with coverage
python -m pytest tests/ --cov=agents --cov=backend --cov-report=html
```

### **Writing New Tests**
```python
import pytest
from agents.base_agent import create_agent

class TestYourFeature:
    def test_agent_creation(self):
        """Test agent creation"""
        agent = create_agent('seed', 'test_student')
        assert agent is not None
        assert agent.agent_type == 'seed'
    
    def test_agent_response(self):
        """Test agent response generation"""
        agent = create_agent('seed', 'test_student')
        response = agent.respond("Test message", {})
        assert len(response) > 0
        assert isinstance(response, str)
```

### **Test Categories**
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **Production Tests**: End-to-end system testing
- **Performance Tests**: Response time and load testing

---

## 📊 **Monitoring and Logging**

### **Using the Logging System**
```python
from monitoring.logging_config import gurukul_logger, log_performance

# Log agent interactions
gurukul_logger.log_agent_interaction(
    agent_type='seed',
    student_id='student_123',
    message='User message',
    response='Agent response',
    conversation_id='conv_123',
    response_time=0.5,
    confidence_score=0.85
)

# Use performance decorator
@log_performance
def your_function():
    # Function implementation
    pass
```

### **Metrics Collection**
```python
from monitoring.logging_config import metrics_collector

# Record metrics
metrics_collector.record_agent_interaction(
    agent_type='seed',
    student_id='student_123',
    response_time=0.5,
    confidence_score=0.85,
    success=True
)

# Get metrics summary
summary = metrics_collector.get_metrics_summary()
print(summary)
```

---

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Core Configuration
AKASH_GURUKUL_ENV=development
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# AI Services (Optional)
OPENAI_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here

# Database (Future)
DATABASE_URL=postgresql://user:pass@localhost/gurukul

# Monitoring (Optional)
SENTRY_DSN=your_sentry_dsn
POSTHOG_API_KEY=your_posthog_key
```

### **Development vs Production**
```python
# Development
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Production
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🚀 **Deployment**

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Production Checklist**
- [ ] Environment variables configured
- [ ] Database setup (if using external DB)
- [ ] SSL certificates installed
- [ ] Monitoring configured
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Security review completed

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Server Won't Start**
```bash
# Check port availability
netstat -an | grep 8000

# Check Python path
python -c "import sys; print(sys.path)"

# Check dependencies
pip list | grep fastapi
```

#### **Agents Not Responding**
```bash
# Test agent creation
python -c "from agents.base_agent import create_agent; print(create_agent('seed', 'test'))"

# Check memory system
python -c "from agents.memory_system import AgentMemorySystem; print('Memory OK')"
```

#### **Memory Issues**
```bash
# Check memory directory
ls -la memory/

# Test FAISS
python -c "import faiss; print('FAISS OK')"
```

### **Debug Mode**
```python
# Enable debug logging
import logging
logging.getLogger("akash_gurukul").setLevel(logging.DEBUG)

# Test with verbose output
python -c "
from agents.base_agent import create_agent
import logging
logging.basicConfig(level=logging.DEBUG)
agent = create_agent('seed', 'debug_test')
response = agent.respond('test', {})
print(response)
"
```

---

## 🤝 **Contributing**

### **Development Workflow**
1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/your-feature`
3. **Implement** changes with tests
4. **Run** test suite: `python -m pytest`
5. **Commit** with clear message
6. **Push** and create pull request

### **Code Standards**
- Follow PEP 8 for Python code
- Add docstrings to all functions
- Include type hints where possible
- Write tests for new features
- Update documentation

### **Pull Request Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

---

## 📞 **Support**

### **Getting Help**
- **Documentation**: Check this guide and README.md
- **Issues**: Create GitHub issue with detailed description
- **Tests**: Run `python tests/test_production_ready.py`
- **Logs**: Check `logs/` directory for error details

### **Contact**
- **Repository**: https://github.com/chaudharyaakash1111/gurukul-langchain
- **Issues**: https://github.com/chaudharyaakash1111/gurukul-langchain/issues

---

## 🕉️ **Philosophy**

Remember that Akash Gurukul is more than code—it's a sacred digital space for learning and transformation. Approach development with:

- **Reverence** for the learning process
- **Attention** to student experience
- **Commitment** to quality and reliability
- **Respect** for the ancient Gurukul tradition

**Om Shanti Shanti Shanti** 🙏
