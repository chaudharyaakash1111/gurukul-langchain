"""
Test script for Akash Gurukul API
Tests basic functionality of all endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_curriculum_endpoints():
    """Test curriculum-related endpoints"""
    print("\nTesting curriculum endpoints...")
    
    # Test get all lessons
    try:
        response = requests.get(f"{BASE_URL}/api/curriculum/lessons")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get all lessons: {data['total_count']} lessons found")
        else:
            print(f"✗ Get all lessons failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Get all lessons error: {e}")
        return False
    
    # Test get lessons by level
    try:
        response = requests.get(f"{BASE_URL}/api/curriculum/lessons/level/Seed")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get Seed lessons: {data['count']} lessons found")
        else:
            print(f"✗ Get Seed lessons failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Get Seed lessons error: {e}")
        return False
    
    # Test get specific lesson
    try:
        response = requests.get(f"{BASE_URL}/api/curriculum/lessons/seed_dharma_001")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get specific lesson: {data['lesson']['title']}")
        else:
            print(f"✗ Get specific lesson failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Get specific lesson error: {e}")
        return False
    
    # Test learning paths
    try:
        response = requests.get(f"{BASE_URL}/api/curriculum/learning-paths")
        if response.status_code == 200:
            data = response.json()
            print("✓ Get learning paths successful")
        else:
            print(f"✗ Get learning paths failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Get learning paths error: {e}")
        return False
    
    return True

def test_agent_endpoints():
    """Test agent-related endpoints"""
    print("\nTesting agent endpoints...")
    
    # Test chat with Seed agent
    try:
        payload = {
            "agent_type": "seed",
            "student_id": "test_student_001",
            "message": "What is kindness?",
            "context": {}
        }
        response = requests.post(f"{BASE_URL}/api/agents/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Seed agent chat: {data['response'][:50]}...")
        else:
            print(f"✗ Seed agent chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Seed agent chat error: {e}")
        return False
    
    # Test chat with Tree agent
    try:
        payload = {
            "agent_type": "tree",
            "student_id": "test_student_002",
            "message": "How do I create value?",
            "context": {}
        }
        response = requests.post(f"{BASE_URL}/api/agents/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Tree agent chat: {data['response'][:50]}...")
        else:
            print(f"✗ Tree agent chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Tree agent chat error: {e}")
        return False
    
    # Test chat with Sky agent
    try:
        payload = {
            "agent_type": "sky",
            "student_id": "test_student_003",
            "message": "What is the meaning of life?",
            "context": {}
        }
        response = requests.post(f"{BASE_URL}/api/agents/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Sky agent chat: {data['response'][:50]}...")
        else:
            print(f"✗ Sky agent chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Sky agent chat error: {e}")
        return False
    
    # Test get agent profile
    try:
        response = requests.get(f"{BASE_URL}/api/agents/seed/test_student_001/profile")
        if response.status_code == 200:
            data = response.json()
            print("✓ Get agent profile successful")
        else:
            print(f"✗ Get agent profile failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Get agent profile error: {e}")
        return False
    
    # Test progress update
    try:
        payload = {
            "student_id": "test_student_001",
            "lesson_id": "seed_dharma_001",
            "performance": 0.85,
            "insights": {"mastered_concepts": ["kindness", "empathy"]}
        }
        response = requests.post(f"{BASE_URL}/api/agents/progress", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✓ Progress update successful")
        else:
            print(f"✗ Progress update failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Progress update error: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("Starting Akash Gurukul API Tests...")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_health_check()
    all_passed &= test_curriculum_endpoints()
    all_passed &= test_agent_endpoints()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    main()
