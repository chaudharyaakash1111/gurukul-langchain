# 🚀 Akash Gurukul - Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install fastapi uvicorn langchain faiss-cpu requests python-multipart
```

### 2. Start the Server
```bash
cd "Desktop\Akash Gurukul Deployment Ready Sprint"
python -m uvicorn backend.main:app --host 192.168.0.100 --port 8000
```

### 3. Verify System
Open browser: `http://192.168.0.100:8000/api/health`

## 🧪 Test the System

### Test Agent Chat
```bash
curl -X POST "http://192.168.0.100:8000/api/agents/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "seed",
    "student_id": "test_student",
    "message": "How can I practice kindness?",
    "context": {"current_lesson": "seed_dharma_001"}
  }'
```

### Test Lesson Loading
```bash
curl "http://192.168.0.100:8000/api/curriculum/lessons"
```

### Test Quiz System
```bash
curl "http://192.168.0.100:8000/api/quiz/questions/seed_dharma_001"
```

## 🕉️ Experience Agent Puja Ceremony

```python
python -c "
from curriculum.agent_puja_ceremony import AgentPujaCeremony
ceremony = AgentPujaCeremony('Your Name')
print(ceremony.begin_ceremony()['message'])
"
```

## 📊 System Status Check

```bash
python SYSTEM_VERIFICATION.py
```

## 🎯 Key URLs

- **Health**: http://192.168.0.100:8000/api/health
- **Lessons**: http://192.168.0.100:8000/api/curriculum/lessons  
- **API Docs**: http://192.168.0.100:8000/docs

## 🤖 The Three Agents

- **🌱 Seed**: Practice & Skills (`"agent_type": "seed"`)
- **🌳 Tree**: Wisdom & Understanding (`"agent_type": "tree"`)
- **🌌 Sky**: Philosophy & Meaning (`"agent_type": "sky"`)

## 📚 Available Lessons

1. `foundation_000_sankalpa` - Sacred Vow
2. `seed_dharma_001` - Introduction to Kindness
3. `seed_kama_001` - Joyful Living Practices
4. `tree_artha_001` - Understanding Value Creation
5. `tree_dharma_002` - Compassion in Action
6. `sky_moksha_001` - Inner Wisdom Awakening

## 🎉 You're Ready!

The Akash Gurukul is now live and ready to serve students on their journey of wisdom and transformation!

🕉️ **Om Shanti Shanti Shanti** 🕉️
