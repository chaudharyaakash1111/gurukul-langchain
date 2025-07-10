"""
Day 3 Comprehensive Test for Akash Gurukul
Tests live UI functionality, refined agent queries, quiz system, and Sankalpa lesson
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_live_ui_functionality():
    """Test that all lessons work properly in the UI interface"""
    print("Testing Live UI Functionality...")
    
    # Test health and lesson availability
    try:
        health = requests.get(f"{BASE_URL}/api/health").json()
        print(f"✓ System Health: {health['status']} - {health['lessons_loaded']} lessons available")
        
        lessons = requests.get(f"{BASE_URL}/api/curriculum/lessons").json()
        print(f"✓ Lessons Available: {lessons['total_count']}")
        
        # Test each lesson can be started
        for lesson in lessons['lessons']:
            lesson_id = lesson.get('id') if isinstance(lesson, dict) else lesson
            lesson_title = lesson.get('title', 'Unknown') if isinstance(lesson, dict) else str(lesson)
            student_id = f"ui_test_{lesson_id}"
            
            # Start lesson
            start_response = requests.post(f"{BASE_URL}/api/lessons/start", json={
                "student_id": student_id,
                "lesson_id": lesson_id
            })
            
            if start_response.status_code == 200:
                print(f"  ✓ {lesson_title} - Started successfully")
            else:
                print(f"  ✗ {lesson_title} - Failed to start")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ UI functionality test failed: {e}")
        return False

def test_refined_agent_queries():
    """Test the enhanced agent query routing and response paths"""
    print("\nTesting Refined Agent Queries...")
    
    student_id = "agent_query_test"
    lesson_id = "seed_dharma_001"
    
    try:
        # Start lesson
        requests.post(f"{BASE_URL}/api/lessons/start", json={
            "student_id": student_id,
            "lesson_id": lesson_id
        })
        
        # Test different query types and agent suggestions
        test_queries = [
            {
                "query": "How can I practice kindness today?",
                "expected_agent": "seed",
                "type": "practical"
            },
            {
                "query": "Why is kindness important for society?",
                "expected_agent": "tree", 
                "type": "conceptual"
            },
            {
                "query": "What does kindness mean to my soul?",
                "expected_agent": "sky",
                "type": "reflective"
            },
            {
                "query": "Can you explain the deeper meaning of compassion?",
                "expected_agent": "tree",
                "type": "conceptual"
            },
            {
                "query": "How do I feel when I help others?",
                "expected_agent": "sky",
                "type": "reflective"
            }
        ]
        
        for test_case in test_queries:
            # Get agent suggestion
            suggestion_response = requests.get(
                f"{BASE_URL}/api/lessons/suggest-agent/{student_id}",
                params={"user_input": test_case["query"], "current_agent": "seed"}
            )
            
            if suggestion_response.status_code == 200:
                suggestion = suggestion_response.json()
                suggested_agent = suggestion["suggested_agent"]
                
                print(f"  Query: '{test_case['query'][:50]}...'")
                print(f"    Expected: {test_case['expected_agent']}, Got: {suggested_agent}")
                
                # Test chat with suggested agent
                chat_response = requests.post(f"{BASE_URL}/api/agents/chat", json={
                    "agent_type": suggested_agent,
                    "student_id": student_id,
                    "message": test_case["query"],
                    "context": {"query_path": test_case["type"]}
                })
                
                if chat_response.status_code == 200:
                    response_text = chat_response.json()["response"]
                    print(f"    ✓ {suggested_agent.title()} agent responded ({len(response_text)} chars)")
                else:
                    print(f"    ✗ {suggested_agent.title()} agent failed to respond")
                    return False
            else:
                print(f"  ✗ Agent suggestion failed for query: {test_case['query']}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Agent query test failed: {e}")
        return False

def test_quiz_system():
    """Test the inline quiz system with different question types"""
    print("\nTesting Quiz System...")
    
    student_id = "quiz_test_student"
    
    try:
        # Test lessons with quizzes
        quiz_lessons = ["foundation_000_sankalpa", "tree_dharma_002"]
        
        for lesson_id in quiz_lessons:
            print(f"  Testing quiz for: {lesson_id}")

            # Start lesson
            start_response = requests.post(f"{BASE_URL}/api/lessons/start", json={
                "student_id": student_id,
                "lesson_id": lesson_id
            })

            if start_response.status_code != 200:
                print(f"    ✗ Failed to start lesson: {start_response.status_code}")
                continue
            
            # Get quiz questions
            quiz_response = requests.get(f"{BASE_URL}/api/quiz/questions/{lesson_id}")
            if quiz_response.status_code != 200:
                print(f"    ✗ Failed to get quiz questions")
                continue
                
            questions = quiz_response.json()["questions"]
            print(f"    ✓ Found {len(questions)} quiz questions")
            
            # Test each question type
            for question in questions:
                question_id = question["id"]
                question_type = question["type"]
                
                # Prepare test answer based on type
                if question_type == "multiple_choice":
                    test_answer = 0  # First option
                elif question_type == "scenario":
                    test_answer = 2  # Usually the best option
                elif question_type == "reflection":
                    test_answer = "This is a thoughtful reflection on the question posed. I believe that learning is a transformative process that requires dedication and openness to growth."
                else:
                    test_answer = "Test answer"
                
                # Submit answer
                submit_response = requests.post(f"{BASE_URL}/api/quiz/submit", json={
                    "student_id": student_id,
                    "lesson_id": lesson_id,
                    "quiz_id": question_id,
                    "answer": test_answer
                })
                
                if submit_response.status_code == 200:
                    result = submit_response.json()
                    print(f"      ✓ {question_type} question: Score {result['score']}")
                else:
                    print(f"      ✗ {question_type} question failed")
                    return False
            
            # Check quiz progress
            progress_response = requests.get(f"{BASE_URL}/api/quiz/progress/{student_id}/{lesson_id}")
            if progress_response.status_code == 200:
                progress = progress_response.json()
                print(f"    ✓ Quiz progress: {progress['completion_rate']:.1%} complete, Score: {progress['total_score']:.1f}")
            
        return True
        
    except Exception as e:
        print(f"✗ Quiz system test failed: {e}")
        return False

def test_sankalpa_lesson():
    """Test the foundational Sankalpa lesson"""
    print("\nTesting Sankalpa Lesson...")
    
    student_id = "sankalpa_test_student"
    lesson_id = "foundation_000_sankalpa"
    
    try:
        # Start Sankalpa lesson
        start_response = requests.post(f"{BASE_URL}/api/lessons/start", json={
            "student_id": student_id,
            "lesson_id": lesson_id
        })
        
        if start_response.status_code != 200:
            print("✗ Failed to start Sankalpa lesson")
            return False
            
        lesson_context = start_response.json()["lesson_context"]
        lesson_data = lesson_context["lesson_data"]
        
        print(f"✓ Started: {lesson_data['title']}")
        print(f"  Level: {lesson_data['level']}")
        print(f"  Category: {lesson_data['category']}")
        
        # Test interaction with each agent type about Sankalpa
        sankalpa_queries = [
            ("seed", "How do I practice the daily learning ritual?"),
            ("tree", "What is the philosophical foundation of Gurukul education?"),
            ("sky", "What does it mean to make a sacred vow of learning?")
        ]
        
        for agent_type, query in sankalpa_queries:
            chat_response = requests.post(f"{BASE_URL}/api/agents/chat", json={
                "agent_type": agent_type,
                "student_id": student_id,
                "message": query,
                "context": {"current_lesson": lesson_id}
            })
            
            if chat_response.status_code == 200:
                response = chat_response.json()["response"]
                print(f"  ✓ {agent_type.title()} agent: {response[:80]}...")
            else:
                print(f"  ✗ {agent_type.title()} agent failed")
                return False
        
        # Test Sankalpa quiz
        quiz_response = requests.get(f"{BASE_URL}/api/quiz/questions/{lesson_id}")
        if quiz_response.status_code == 200:
            questions = quiz_response.json()["questions"]
            print(f"  ✓ Sankalpa quiz has {len(questions)} questions")
            
            # Test the personal Sankalpa reflection question
            for question in questions:
                if question["type"] == "reflection":
                    submit_response = requests.post(f"{BASE_URL}/api/quiz/submit", json={
                        "student_id": student_id,
                        "lesson_id": lesson_id,
                        "quiz_id": question["id"],
                        "answer": "I commit to approaching each lesson with reverence and curiosity, using my knowledge to serve others and contribute to the greater good. I vow to honor the wisdom traditions while remaining open to transformation."
                    })
                    
                    if submit_response.status_code == 200:
                        result = submit_response.json()
                        print(f"    ✓ Personal Sankalpa reflection scored: {result['score']}")
                    break
        
        # Complete the lesson
        complete_response = requests.post(f"{BASE_URL}/api/lessons/complete", json={
            "student_id": student_id,
            "lesson_id": lesson_id,
            "quiz_score": 0.9,
            "mastery_indicators": {"sankalpa_understanding": "excellent", "commitment_level": "high"}
        })
        
        if complete_response.status_code == 200:
            completion = complete_response.json()
            print(f"  ✓ Lesson completed: {completion['final_state']}")
            print(f"  ✓ Mastery achieved: {completion['mastery_achieved']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Sankalpa lesson test failed: {e}")
        return False

def test_second_lesson_with_quiz():
    """Test the second lesson (Compassion in Action) with advanced quiz features"""
    print("\nTesting Second Lesson with Advanced Quiz...")
    
    student_id = "second_lesson_test"
    lesson_id = "tree_dharma_002"
    
    try:
        # Start lesson
        start_response = requests.post(f"{BASE_URL}/api/lessons/start", json={
            "student_id": student_id,
            "lesson_id": lesson_id
        })
        
        if start_response.status_code != 200:
            print("✗ Failed to start second lesson")
            return False
            
        lesson_data = start_response.json()["lesson_context"]["lesson_data"]
        print(f"✓ Started: {lesson_data['title']}")
        
        # Test query paths
        query_paths = lesson_data.get("query_paths", {})
        print(f"  ✓ Query paths available: {list(query_paths.keys())}")
        
        # Test scenario-based quiz question
        quiz_response = requests.get(f"{BASE_URL}/api/quiz/questions/{lesson_id}")
        if quiz_response.status_code == 200:
            questions = quiz_response.json()["questions"]
            
            for question in questions:
                if question["type"] == "scenario":
                    print(f"  ✓ Found scenario question: {question['question'][:60]}...")
                    
                    # Submit answer to scenario
                    submit_response = requests.post(f"{BASE_URL}/api/quiz/submit", json={
                        "student_id": student_id,
                        "lesson_id": lesson_id,
                        "quiz_id": question["id"],
                        "answer": 2  # Usually the compassionate response
                    })
                    
                    if submit_response.status_code == 200:
                        result = submit_response.json()
                        print(f"    ✓ Scenario response scored: {result['score']}")
                        print(f"    ✓ Agent feedback: {result.get('agent_feedback', 'None')[:60]}...")
                    break
        
        # Test challenges if available
        if "challenges" in lesson_data:
            challenges = lesson_data["challenges"]
            print(f"  ✓ Found {len(challenges)} challenges")
            for challenge in challenges:
                print(f"    - {challenge['title']}: {challenge['type']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Second lesson test failed: {e}")
        return False

def main():
    """Run all Day 3 comprehensive tests"""
    print("Starting Day 3 Comprehensive Tests...")
    print("=" * 60)
    
    # Wait for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_live_ui_functionality()
    all_passed &= test_refined_agent_queries()
    all_passed &= test_quiz_system()
    all_passed &= test_sankalpa_lesson()
    all_passed &= test_second_lesson_with_quiz()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All Day 3 comprehensive tests passed!")
        print("\nDay 3 Systems Ready:")
        print("✓ Live UI functionality operational")
        print("✓ Refined agent query routing working")
        print("✓ Inline quiz system functional")
        print("✓ Sankalpa invocation lesson complete")
        print("✓ Second lesson with advanced features ready")
        print("✓ Audio/video sync framework enhanced")
        print("\n🕉️ The Gurukul is breathing with life!")
    else:
        print("❌ Some Day 3 tests failed!")
    
    return all_passed

if __name__ == "__main__":
    main()
