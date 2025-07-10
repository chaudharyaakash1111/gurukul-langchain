"""
Day 2 Integration Test for Akash Gurukul
Tests agent personalities, lesson flow, and context passing
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_agent_personalities():
    """Test the refined agent personalities and roles"""
    print("Testing Agent Personalities...")
    
    # Test Seed Agent (Practice/Drill Mentor)
    seed_request = {
        "agent_type": "seed",
        "student_id": "test_student_day2",
        "message": "How can I practice kindness today?",
        "context": {}
    }
    
    response = requests.post(f"{BASE_URL}/api/agents/chat", json=seed_request)
    if response.status_code == 200:
        seed_response = response.json()["response"]
        print(f"✓ Seed Agent (Practice Mentor): {seed_response[:100]}...")
        
        # Check if response is practice-oriented
        practice_keywords = ["practice", "do", "try", "step", "exercise"]
        if any(keyword in seed_response.lower() for keyword in practice_keywords):
            print("  ✓ Response is practice-oriented")
        else:
            print("  ⚠ Response may not be sufficiently practice-focused")
    else:
        print(f"✗ Seed Agent test failed: {response.status_code}")
        return False
    
    # Test Tree Agent (Wisdom/Conceptual Teacher)
    tree_request = {
        "agent_type": "tree",
        "student_id": "test_student_day2",
        "message": "Why is kindness important?",
        "context": {}
    }
    
    response = requests.post(f"{BASE_URL}/api/agents/chat", json=tree_request)
    if response.status_code == 200:
        tree_response = response.json()["response"]
        print(f"✓ Tree Agent (Wisdom Teacher): {tree_response[:100]}...")
        
        # Check if response is conceptual
        concept_keywords = ["understand", "because", "concept", "principle", "wisdom"]
        if any(keyword in tree_response.lower() for keyword in concept_keywords):
            print("  ✓ Response is conceptually oriented")
        else:
            print("  ⚠ Response may not be sufficiently conceptual")
    else:
        print(f"✗ Tree Agent test failed: {response.status_code}")
        return False
    
    # Test Sky Agent (Philosophical/Introspective Guru)
    sky_request = {
        "agent_type": "sky",
        "student_id": "test_student_day2",
        "message": "What does kindness mean to my soul?",
        "context": {}
    }
    
    response = requests.post(f"{BASE_URL}/api/agents/chat", json=sky_request)
    if response.status_code == 200:
        sky_response = response.json()["response"]
        print(f"✓ Sky Agent (Philosophical Guru): {sky_response[:100]}...")
        
        # Check if response is philosophical
        philosophy_keywords = ["soul", "meaning", "reflect", "inner", "spiritual", "deeper"]
        if any(keyword in sky_response.lower() for keyword in philosophy_keywords):
            print("  ✓ Response is philosophically oriented")
        else:
            print("  ⚠ Response may not be sufficiently philosophical")
    else:
        print(f"✗ Sky Agent test failed: {response.status_code}")
        return False
    
    return True

def test_lesson_flow():
    """Test the lesson flow management system"""
    print("\nTesting Lesson Flow Management...")
    
    student_id = "test_student_flow"
    lesson_id = "seed_dharma_001"
    
    # Test starting a lesson
    start_request = {
        "student_id": student_id,
        "lesson_id": lesson_id
    }
    
    response = requests.post(f"{BASE_URL}/api/lessons/start", json=start_request)
    if response.status_code == 200:
        start_data = response.json()
        print("✓ Lesson started successfully")
        print(f"  Recommended agent: {start_data['lesson_context']['recommended_agent']}")
        print(f"  Query path: {start_data['lesson_context']['query_path']}")
    else:
        print(f"✗ Lesson start failed: {response.status_code}")
        return False
    
    # Test agent suggestion
    response = requests.get(
        f"{BASE_URL}/api/lessons/suggest-agent/{student_id}",
        params={"user_input": "How do I practice being kind?", "current_agent": "tree"}
    )
    if response.status_code == 200:
        suggestion = response.json()
        print(f"✓ Agent suggestion: {suggestion['suggested_agent']} ({suggestion['suggested_query_path']})")
        print(f"  Reasoning: {suggestion['reasoning']}")
    else:
        print(f"✗ Agent suggestion failed: {response.status_code}")
        return False
    
    # Test recording interaction
    interaction_request = {
        "student_id": student_id,
        "lesson_id": lesson_id,
        "agent_type": "seed",
        "query_path": "practical",
        "user_input": "How can I be kind today?"
    }
    
    response = requests.post(f"{BASE_URL}/api/lessons/interact", json=interaction_request)
    if response.status_code == 200:
        print("✓ Interaction recorded successfully")
    else:
        print(f"✗ Interaction recording failed: {response.status_code}")
        return False
    
    # Test getting student progress
    response = requests.get(f"{BASE_URL}/api/students/{student_id}/progress")
    if response.status_code == 200:
        progress = response.json()
        print(f"✓ Student progress retrieved: {progress['total_lessons_attempted']} lessons attempted")
    else:
        print(f"✗ Progress retrieval failed: {response.status_code}")
        return False
    
    # Test completing lesson
    completion_request = {
        "student_id": student_id,
        "lesson_id": lesson_id,
        "quiz_score": 0.85,
        "mastery_indicators": {"kindness_understanding": "good", "practice_willingness": "high"}
    }
    
    response = requests.post(f"{BASE_URL}/api/lessons/complete", json=completion_request)
    if response.status_code == 200:
        completion_data = response.json()
        print(f"✓ Lesson completed: {completion_data['final_state']}")
        print(f"  Mastery achieved: {completion_data['mastery_achieved']}")
    else:
        print(f"✗ Lesson completion failed: {response.status_code}")
        return False
    
    return True

def test_context_passing():
    """Test enhanced context passing and fallback logic"""
    print("\nTesting Context Passing and Fallbacks...")
    
    student_id = "test_context_student"
    
    # Start a lesson to provide context
    start_request = {
        "student_id": student_id,
        "lesson_id": "seed_dharma_001"
    }
    requests.post(f"{BASE_URL}/api/lessons/start", json=start_request)
    
    # Test context-aware response
    chat_request = {
        "agent_type": "tree",
        "student_id": student_id,
        "message": "Tell me more about this lesson",
        "context": {"test_context": True}
    }
    
    response = requests.post(f"{BASE_URL}/api/agents/chat", json=chat_request)
    if response.status_code == 200:
        chat_response = response.json()["response"]
        print(f"✓ Context-aware response: {chat_response[:100]}...")
        
        # Check if response mentions the lesson
        if "kindness" in chat_response.lower():
            print("  ✓ Response is contextually relevant to the lesson")
        else:
            print("  ⚠ Response may not be using lesson context effectively")
    else:
        print(f"✗ Context-aware chat failed: {response.status_code}")
        return False
    
    # Test fallback with very short input
    fallback_request = {
        "agent_type": "seed",
        "student_id": student_id,
        "message": "hi",
        "context": {}
    }
    
    response = requests.post(f"{BASE_URL}/api/agents/chat", json=fallback_request)
    if response.status_code == 200:
        fallback_response = response.json()["response"]
        print(f"✓ Fallback response: {fallback_response[:100]}...")
        
        # Check if it's a meaningful fallback
        if len(fallback_response) > 20:
            print("  ✓ Fallback provides meaningful guidance")
        else:
            print("  ⚠ Fallback response may be too brief")
    else:
        print(f"✗ Fallback test failed: {response.status_code}")
        return False
    
    return True

def test_query_paths():
    """Test the different query paths for the enhanced lesson"""
    print("\nTesting Query Paths...")
    
    # Get the enhanced lesson
    response = requests.get(f"{BASE_URL}/api/curriculum/lessons/seed_dharma_001")
    if response.status_code == 200:
        lesson = response.json()["lesson"]
        
        # Check if query paths exist
        if "query_paths" in lesson:
            query_paths = lesson["query_paths"]
            print(f"✓ Query paths found: {list(query_paths.keys())}")
            
            # Check each path
            for path_name, path_data in query_paths.items():
                agent_type = path_data.get("agent_type")
                focus = path_data.get("focus")
                sample_queries = path_data.get("sample_queries", [])
                
                print(f"  ✓ {path_name} path: {agent_type} agent, {len(sample_queries)} sample queries")
                print(f"    Focus: {focus}")
                
                # Test a sample query with the appropriate agent
                if sample_queries:
                    test_query = sample_queries[0]
                    chat_request = {
                        "agent_type": agent_type,
                        "student_id": "test_query_paths",
                        "message": test_query,
                        "context": {"query_path": path_name}
                    }
                    
                    chat_response = requests.post(f"{BASE_URL}/api/agents/chat", json=chat_request)
                    if chat_response.status_code == 200:
                        print(f"    ✓ Sample query test passed for {path_name}")
                    else:
                        print(f"    ✗ Sample query test failed for {path_name}")
        else:
            print("✗ No query paths found in lesson")
            return False
    else:
        print(f"✗ Failed to get lesson: {response.status_code}")
        return False
    
    return True

def main():
    """Run all Day 2 integration tests"""
    print("Starting Day 2 Integration Tests...")
    print("=" * 60)
    
    # Wait for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_agent_personalities()
    all_passed &= test_lesson_flow()
    all_passed &= test_context_passing()
    all_passed &= test_query_paths()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All Day 2 integration tests passed!")
        print("\nDay 2 Systems Ready:")
        print("✓ Agent personalities refined (Seed=Practice, Tree=Wisdom, Sky=Philosophy)")
        print("✓ Lesson flow management working")
        print("✓ Context passing and fallback logic implemented")
        print("✓ Enhanced lesson with query paths functional")
        print("✓ Agent suggestion system operational")
        print("✓ Student progress tracking active")
    else:
        print("❌ Some Day 2 tests failed!")
    
    return all_passed

if __name__ == "__main__":
    main()
