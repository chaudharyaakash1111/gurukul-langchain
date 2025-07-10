# 🕉️ Akash Gurukul - Digital Wisdom Learning System

> *"Gurur Brahma Gurur Vishnu Gurur Devo Maheshwarah"*  
> *The Guru is the creator, sustainer, and transformer*

A sacred digital learning platform that embodies the ancient Gurukul tradition through AI-powered teaching agents, providing personalized wisdom education for the modern age.

## 🌟 Overview

**Akash Gurukul** is a revolutionary learning system that combines ancient Indian wisdom traditions with cutting-edge AI technology. The platform features three distinct AI agents representing different aspects of learning, comprehensive curriculum covering life's essential wisdom, and a sacred onboarding experience that honors the teacher-student relationship.

### ✨ Key Features

- **🤖 Three AI Teaching Agents** with distinct personalities and teaching styles
- **📚 Complete Curriculum** covering Dharma, Artha, Kama, and Moksha
- **🕉️ Sacred Agent Puja Ceremony** for meaningful onboarding
- **🔗 Intelligent Agent Chaining** with context-aware transitions
- **🧠 Memory-Enabled Conversations** that remember student preferences
- **📝 Interactive Quizzes** with personalized feedback
- **⚙️ Production-Ready API** with comprehensive endpoints

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AKASH GURUKUL SYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│  🌱 Seed Agent (Practice Mentor)                            │
│  🌳 Tree Agent (Wisdom Teacher)                             │
│  🌌 Sky Agent (Philosophical Guru)                          │
├─────────────────────────────────────────────────────────────┤
│  📚 Curriculum System                                       │
│  ├─ 6 Complete Lessons                                      │
│  ├─ Interactive Quizzes                                     │
│  ├─ Progress Tracking                                       │
│  └─ Learning Path Management                                │
├─────────────────────────────────────────────────────────────┤
│  ⚙️ Backend Infrastructure                                   │
│  ├─ FastAPI Server                                          │
│  ├─ LangChain Memory System                                 │
│  ├─ Agent Chaining Engine                                   │
│  └─ RESTful API Endpoints                                   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Git (for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Akash Gurukul Deployment Ready Sprint"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

4. **Verify installation**
   ```bash
   curl http://localhost:8000/api/health
   ```

### 🌐 Access the System

- **Main Server**: `http://localhost:8000`
- **Health Check**: `http://localhost:8000/api/health`
- **API Documentation**: `http://localhost:8000/docs`

## 🤖 The Three AI Agents

### 🌱 Seed Agent - The Practice Mentor
- **Role**: Hands-on learning and skill building
- **Personality**: Encouraging, practical, action-oriented
- **Best for**: "How do I practice this?", "What steps should I take?"
- **Teaching Style**: Step-by-step guidance, exercises, daily practices

### 🌳 Tree Agent - The Wisdom Teacher  
- **Role**: Conceptual understanding and principles
- **Personality**: Wise, explanatory, connecting ideas
- **Best for**: "Why is this important?", "How does this connect?"
- **Teaching Style**: Deep explanations, frameworks, wisdom connections

### 🌌 Sky Agent - The Philosophical Guru
- **Role**: Spiritual insights and deeper meaning
- **Personality**: Reflective, profound, spiritually-oriented
- **Best for**: "What does this mean?", "How does this serve my soul?"
- **Teaching Style**: Contemplative questions, spiritual insights, purpose exploration

## 📚 Curriculum Overview

### Foundation Level
- **Sankalpa**: The Sacred Vow of Learning

### Seed Level (Practice-Oriented)
- **Introduction to Kindness** - Basic dharma practices
- **Joyful Living Practices** - Kama wisdom for daily happiness

### Tree Level (Understanding-Oriented)  
- **Understanding Value Creation** - Artha principles and economics
- **Compassion in Action** - Advanced dharma with wisdom

### Sky Level (Meaning-Oriented)
- **Inner Wisdom Awakening** - Moksha and consciousness exploration

## 🔗 API Endpoints

### Core Endpoints

#### Health & Status
```http
GET /api/health
```
Returns system health and status information.

#### Curriculum Management
```http
GET /api/curriculum/lessons
GET /api/curriculum/lessons/{lesson_id}
```

#### Lesson Management
```http
POST /api/lessons/start
POST /api/lessons/complete
GET /api/lessons/progress/{student_id}
```

#### Agent Interactions
```http
POST /api/agents/chat
GET /api/agents/chain-suggestion/{student_id}
GET /api/agents/chain-summary/{student_id}
```

#### Quiz System
```http
GET /api/quiz/questions/{lesson_id}
POST /api/quiz/submit
```

### Example API Usage

#### Chat with an Agent
```bash
curl -X POST "http://localhost:8000/api/agents/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "seed",
    "student_id": "student_123",
    "message": "How can I practice kindness daily?",
    "context": {"current_lesson": "seed_dharma_001"}
  }'
```

#### Start a Lesson
```bash
curl -X POST "http://localhost:8000/api/lessons/start" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "student_123",
    "lesson_id": "foundation_000_sankalpa"
  }'
```

## 🕉️ Agent Puja Ceremony

The sacred onboarding experience that introduces students to their three AI guides:

```python
from curriculum.agent_puja_ceremony import AgentPujaCeremony

# Create ceremony for new student
ceremony = AgentPujaCeremony("Student Name")

# Run the complete ceremony
opening = ceremony.begin_ceremony()
seed_invocation = ceremony.invoke_seed_agent()
tree_invocation = ceremony.invoke_tree_agent()
sky_invocation = ceremony.invoke_sky_agent()
completion = ceremony.complete_ceremony()
```

## 🧪 Testing

### Run System Verification
```bash
python SYSTEM_VERIFICATION.py
```

### Run Integration Tests
```bash
python tests/day4_final_integration_test.py
python tests/test_agent_chaining.py
```

### Test Individual Components
```bash
# Test curriculum loading
python -c "from curriculum.ingestion import CurriculumIngestion; c=CurriculumIngestion(); c.load_all_lessons(); print(f'Loaded {len(c.lessons)} lessons')"

# Test agent creation
python -c "from agents.base_agent import create_agent; agent=create_agent('seed', 'test'); print(f'Created {agent.agent_type} agent')"
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: OpenAI API for production LLM
export OPENAI_API_KEY="your-api-key-here"

# Optional: Pinecone for production vector storage
export PINECONE_API_KEY="your-pinecone-key"
export PINECONE_ENVIRONMENT="your-environment"
```

### Fallback Systems
The system includes robust fallback mechanisms:
- **LLM Fallback**: Uses test responses when OpenAI API unavailable
- **Vector Storage Fallback**: FAISS when Pinecone/Chroma unavailable
- **Memory Fallback**: In-memory storage when external systems unavailable

## 📁 Project Structure

```
Akash Gurukul Deployment Ready Sprint/
├── 📁 agents/                    # AI agent implementations
│   ├── base_agent.py            # Core agent framework
│   ├── memory_system.py         # LangChain memory integration
│   └── agent_chaining.py        # Intelligent agent transitions
├── 📁 backend/                   # FastAPI server
│   └── main.py                  # Main API server
├── 📁 curriculum/                # Learning content system
│   ├── lessons/                 # JSON lesson files
│   ├── ingestion.py            # Curriculum loading
│   ├── lesson_flow.py          # Learning progression
│   └── agent_puja_ceremony.py  # Sacred onboarding
├── 📁 tests/                     # Comprehensive test suite
├── 📁 docs/                      # Documentation
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## 🤝 Team Integration

### For Frontend Developers
- Connect to agent chat API: `POST /api/agents/chat`
- Implement lesson display from: `GET /api/curriculum/lessons`
- Add quiz integration: `GET /api/quiz/questions/{lesson_id}`
- Use Agent Puja ceremony for onboarding

### For Backend Developers
- Implement student progress storage
- Add lesson scoring system
- Set up agent memory persistence
- Create analytics dashboard

### For UI/UX Designers
- Apply agent personality themes (Seed=Green, Tree=Brown, Sky=Blue)
- Implement responsive design
- Add transition animations
- Create quiz UI components

### For Content Creators
- Follow JSON lesson format in `curriculum/lessons/`
- Provide audio files with sync maps
- Create video assets with chapter markers
- Add meditation and practice audio

## 🚀 Deployment

### Development
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 System Status

### ✅ Completed Features
- [x] 6 Complete lessons with interactive content
- [x] 3 AI agents with distinct personalities
- [x] Agent chaining with intelligent transitions
- [x] Memory system with conversation persistence
- [x] Quiz system with personalized feedback
- [x] Agent Puja sacred ceremony
- [x] Complete REST API
- [x] Comprehensive testing framework

### 🔄 Integration Ready
- [ ] Frontend UI implementation
- [ ] Production database setup
- [ ] Audio/video asset integration
- [ ] User authentication system
- [ ] Analytics and reporting

## 🐛 Troubleshooting

### Common Issues

**Server won't start**
```bash
# Check if port is in use
netstat -an | grep 8000

# Try different port
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8001
```

**Agents not responding**
```bash
# Verify agent creation
python -c "from agents.base_agent import create_agent; create_agent('seed', 'test')"
```

**Lessons not loading**
```bash
# Check curriculum
python -c "from curriculum.ingestion import CurriculumIngestion; c=CurriculumIngestion(); c.load_all_lessons()"
```

## 📄 License

This project embodies sacred wisdom traditions and is intended for educational and spiritual growth purposes.

## 🙏 Acknowledgments

- Ancient Gurukul tradition and wisdom keepers
- Modern AI and machine learning communities
- All contributors to this sacred digital learning project

## 📞 Support

For technical support or integration questions:
- Check the comprehensive documentation in `/docs/`
- Review API examples in this README
- Run system verification: `python SYSTEM_VERIFICATION.py`

---

## 🕉️ Sacred Completion

*"Sarve bhavantu sukhinah, sarve santu niramayah"*  
*May all beings be happy, may all beings be healthy*

The **Akash Gurukul** stands ready to serve students on their journey of wisdom and transformation. The digital Gurukul breathes with life, honoring the ancient tradition while embracing modern technology.

**Om Shanti Shanti Shanti** 🙏

---

*Built with reverence for the ancient Gurukul tradition and dedication to the awakening of consciousness in the digital age.*
