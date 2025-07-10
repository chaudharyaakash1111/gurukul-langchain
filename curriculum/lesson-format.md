# Curriculum Lesson Format Specification

## Overview
This document defines the standardized format for curriculum lessons in the Akash Gurukul platform. Each lesson follows a structured JSON format that enables seamless integration with AI agents and the learning management system.

## Lesson Structure

### Core Format
```json
{
  "id": "unique-lesson-identifier",
  "title": "Lesson Title",
  "level": "Seed|Tree|Sky",
  "category": "dharma|artha|kama|moksha",
  "prerequisites": ["lesson-id-1", "lesson-id-2"],
  "learning_objectives": [
    "Objective 1",
    "Objective 2"
  ],
  "estimated_duration": 30,
  "content": {
    "text": "Main lesson content in markdown format...",
    "media": {
      "images": ["path/to/image1.jpg"],
      "videos": ["path/to/video1.mp4"],
      "audio": ["path/to/audio1.mp3"]
    }
  },
  "quiz": [
    {
      "id": "q1",
      "type": "multiple_choice",
      "question": "What is the primary concept discussed?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Explanation for the correct answer"
    }
  ],
  "tts": true,
  "metadata": {
    "created_by": "author-name",
    "created_date": "2025-01-01",
    "last_modified": "2025-01-01",
    "version": "1.0",
    "tags": ["philosophy", "ethics", "beginner"],
    "difficulty": 1
  }
}
```

## Level Definitions

### Seed Level
- **Target**: Beginners, foundational concepts
- **Characteristics**: Simple language, basic concepts, guided learning
- **Agent Role**: Nurturing companion, patient guidance

### Tree Level  
- **Target**: Intermediate learners, structured knowledge
- **Characteristics**: Deeper concepts, interconnected topics, analytical thinking
- **Agent Role**: Knowledgeable teacher, systematic instruction

### Sky Level
- **Target**: Advanced learners, philosophical depth
- **Characteristics**: Complex concepts, abstract thinking, wisdom traditions
- **Agent Role**: Wise mentor, philosophical dialogue

## Content Categories

### Dharma (Righteousness)
- Ethics and moral philosophy
- Duty and responsibility
- Social harmony and justice

### Artha (Prosperity)
- Practical skills and knowledge
- Economic understanding
- Resource management

### Kama (Fulfillment)
- Emotional intelligence
- Relationships and communication
- Creative expression

### Moksha (Liberation)
- Spiritual wisdom
- Self-realization
- Ultimate truth and freedom

## Quiz Types

### Multiple Choice
```json
{
  "type": "multiple_choice",
  "question": "Question text",
  "options": ["A", "B", "C", "D"],
  "correct_answer": 0
}
```

### True/False
```json
{
  "type": "true_false",
  "question": "Statement to evaluate",
  "correct_answer": true
}
```

### Short Answer
```json
{
  "type": "short_answer",
  "question": "Question requiring brief response",
  "sample_answers": ["Expected answer 1", "Expected answer 2"]
}
```

### Reflection
```json
{
  "type": "reflection",
  "question": "Deep thinking prompt",
  "guidance": "Reflection guidelines for the student"
}
```

## File Naming Convention
- Format: `{level}_{category}_{sequence}_{slug}.json`
- Example: `seed_dharma_001_introduction-to-ethics.json`

## Validation Rules
1. All required fields must be present
2. Level must be one of: Seed, Tree, Sky
3. Category must be one of: dharma, artha, kama, moksha
4. Prerequisites must reference existing lesson IDs
5. Quiz must have at least one question
6. TTS flag determines audio generation requirement
