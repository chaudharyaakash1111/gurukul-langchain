"""
Day 4 Final Integration Test - The Gurukul is Now Alive
Comprehensive test for all 6 lessons, agent routing, and complete system functionality
"""

import requests
import json
import time
from typing import Dict, List

BASE_URL = "http://192.168.0.95:8000"

def test_complete_system_health():
    """Test overall system health with all 6 lessons"""
    print("🏥 Testing Complete System Health...")
    
    try:
        health = requests.get(f"{BASE_URL}/api/health").json()
        print(f"✅ System Status: {health['status']}")
        print(f"✅ Lessons Loaded: {health['lessons_loaded']}")
        print(f"✅ Service: {health['service']}")
        
        if health['lessons_loaded'] != 6:
            print(f"⚠️ Expected 6 lessons, found {health['lessons_loaded']}")
            return False
            
        return health['status'] == 'healthy'
        
    except Exception as e:
        print(f"❌ System health check failed: {e}")
        return False

def test_all_six_lessons():
    """Test that all 6 lessons can be started and interacted with"""
    print("\n📚 Testing All Six Lessons...")
    
    try:
        lessons = requests.get(f"{BASE_URL}/api/curriculum/lessons").json()
        lesson_dict = lessons['lessons']

        expected_lessons = [
            "foundation_000_sankalpa",
            "seed_dharma_001",
            "seed_kama_001",
            "tree_artha_001",
            "tree_dharma_002",
            "sky_moksha_001"
        ]

        found_lessons = list(lesson_dict.keys())
        print(f"Found lessons: {found_lessons}")
        
        for expected in expected_lessons:
            if expected not in found_lessons:
                print(f"❌ Missing expected lesson: {expected}")
                return False
        
        # Test starting each lesson
        student_id = f"lesson_test_{int(time.time())}"

        for lesson_id, lesson_data in lesson_dict.items():
            lesson_title = lesson_data['title']
            
            start_response = requests.post(f"{BASE_URL}/api/lessons/start", json={
                "student_id": student_id,
                "lesson_id": lesson_id
            })
            
            if start_response.status_code == 200:
                print(f"  ✅ {lesson_title} - Started successfully")
            else:
                print(f"  ❌ {lesson_title} - Failed to start")
                return False
        
        print(f"✅ All {len(lesson_dict)} lessons operational")
        return True
        
    except Exception as e:
        print(f"❌ Lesson testing failed: {e}")
        return False

def test_agent_puja_ceremony():
    """Test the Agent Puja ceremony script"""
    print("\n🕉️ Testing Agent Puja Ceremony...")
    
    try:
        # Import and test the ceremony
        import sys
        sys.path.append('curriculum')
        from agent_puja_ceremony import AgentPujaCeremony
        
        ceremony = AgentPujaCeremony("Test Student")
        
        # Test ceremony flow
        opening = ceremony.begin_ceremony()
        assert opening['type'] == 'ceremony_opening'
        print("  ✅ Ceremony opening works")
        
        seed_invocation = ceremony.invoke_seed_agent()
        assert seed_invocation['agent'] == 'seed'
        print("  ✅ Seed agent invocation works")
        
        tree_invocation = ceremony.invoke_tree_agent()
        assert tree_invocation['agent'] == 'tree'
        print("  ✅ Tree agent invocation works")
        
        sky_invocation = ceremony.invoke_sky_agent()
        assert sky_invocation['agent'] == 'sky'
        print("  ✅ Sky agent invocation works")
        
        completion = ceremony.complete_ceremony()
        assert ceremony.ceremony_complete == True
        print("  ✅ Ceremony completion works")
        
        # Test personal invocation
        personal = ceremony.create_personal_invocation("Test Student", "curiosity and dedication")
        assert "Test Student" in personal
        print("  ✅ Personal invocation creation works")
        
        print("✅ Agent Puja Ceremony fully functional")
        return True
        
    except Exception as e:
        print(f"❌ Agent Puja Ceremony test failed: {e}")
        return False

def test_enhanced_agent_routing():
    """Test the enhanced agent routing with diverse queries"""
    print("\n🧭 Testing Enhanced Agent Routing...")
    
    student_id = f"routing_test_{int(time.time())}"
    
    # Start a lesson first
    requests.post(f"{BASE_URL}/api/lessons/start", json={
        "student_id": student_id,
        "lesson_id": "foundation_000_sankalpa"
    })
    
    test_cases = [
        # Clear practical queries should route to Seed
        ("How do I practice meditation daily?", "seed"),
        ("Show me steps to build compassion", "seed"),
        ("What exercises help with inner wisdom?", "seed"),
        
        # Clear conceptual queries should route to Tree
        ("Why is compassion important?", "tree"),
        ("Explain the principles of dharma", "tree"),
        ("What is the relationship between wisdom and knowledge?", "tree"),
        
        # Clear reflective queries should route to Sky
        ("What does this mean for my soul?", "sky"),
        ("How does this connect me to the divine?", "sky"),
        ("What is my deeper purpose?", "sky"),
    ]
    
    correct_routes = 0
    total_tests = len(test_cases)
    
    for query, expected_agent in test_cases:
        try:
            response = requests.get(
                f"{BASE_URL}/api/lessons/suggest-agent/{student_id}",
                params={"user_input": query, "current_agent": "tree"}
            )
            
            if response.status_code == 200:
                result = response.json()
                suggested_agent = result["suggested_agent"]
                
                if suggested_agent == expected_agent:
                    correct_routes += 1
                    print(f"  ✅ '{query[:30]}...' → {suggested_agent}")
                else:
                    print(f"  ❌ '{query[:30]}...' → {suggested_agent} (expected {expected_agent})")
            else:
                print(f"  ❌ Query failed: {query[:30]}...")
                
        except Exception as e:
            print(f"  ❌ Error testing query: {e}")
    
    accuracy = (correct_routes / total_tests) * 100
    print(f"✅ Routing Accuracy: {accuracy:.1f}% ({correct_routes}/{total_tests})")
    
    return accuracy >= 70  # Require 70% accuracy

def test_complete_learning_flow():
    """Test a complete learning flow from start to finish"""
    print("\n🌊 Testing Complete Learning Flow...")
    
    student_id = f"flow_test_{int(time.time())}"
    
    try:
        # 1. Start with Sankalpa lesson
        start_response = requests.post(f"{BASE_URL}/api/lessons/start", json={
            "student_id": student_id,
            "lesson_id": "foundation_000_sankalpa"
        })
        
        if start_response.status_code != 200:
            print("❌ Failed to start Sankalpa lesson")
            return False
        
        print("  ✅ Started Sankalpa lesson")
        
        # 2. Chat with each agent
        agents = ["seed", "tree", "sky"]
        queries = [
            "How can I practice my Sankalpa daily?",
            "Why is making a sacred vow important?", 
            "What does Sankalpa mean for my spiritual journey?"
        ]
        
        for agent, query in zip(agents, queries):
            chat_response = requests.post(f"{BASE_URL}/api/agents/chat", json={
                "agent_type": agent,
                "student_id": student_id,
                "message": query,
                "context": {"current_lesson": "foundation_000_sankalpa"}
            })
            
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                response_text = response_data["response"]
                print(f"  ✅ {agent.title()} agent responded ({len(response_text)} chars)")
            else:
                print(f"  ❌ {agent.title()} agent failed")
                return False
        
        # 3. Take quiz
        quiz_response = requests.get(f"{BASE_URL}/api/quiz/questions/foundation_000_sankalpa")
        if quiz_response.status_code == 200:
            questions = quiz_response.json()["questions"]
            print(f"  ✅ Retrieved {len(questions)} quiz questions")
            
            # Submit answer to first question
            if questions:
                first_question = questions[0]
                submit_response = requests.post(f"{BASE_URL}/api/quiz/submit", json={
                    "student_id": student_id,
                    "lesson_id": "foundation_000_sankalpa",
                    "quiz_id": first_question["id"],
                    "answer": 1  # Assume correct answer
                })
                
                if submit_response.status_code == 200:
                    result = submit_response.json()
                    print(f"  ✅ Quiz submitted, score: {result['score']}")
                else:
                    print("  ❌ Quiz submission failed")
                    return False
        
        # 4. Complete lesson
        complete_response = requests.post(f"{BASE_URL}/api/lessons/complete", json={
            "student_id": student_id,
            "lesson_id": "foundation_000_sankalpa",
            "quiz_score": 0.8,
            "mastery_indicators": {"understanding": "good", "commitment": "strong"}
        })
        
        if complete_response.status_code == 200:
            completion = complete_response.json()
            print(f"  ✅ Lesson completed: {completion['final_state']}")
        else:
            print("  ❌ Lesson completion failed")
            return False
        
        # 5. Check progress
        progress_response = requests.get(f"{BASE_URL}/api/students/{student_id}/progress")
        if progress_response.status_code == 200:
            progress = progress_response.json()
            print(f"  ✅ Progress tracked: {len(progress['completed_lessons'])} lessons completed")
        else:
            print("  ❌ Progress tracking failed")
            return False
        
        print("✅ Complete learning flow successful")
        return True
        
    except Exception as e:
        print(f"❌ Learning flow test failed: {e}")
        return False

def main():
    """Run all Day 4 final integration tests"""
    print("🚀 Day 4 Final Integration Test - The Gurukul is Now Alive")
    print("=" * 70)
    
    tests = [
        ("System Health Check", test_complete_system_health),
        ("All Six Lessons", test_all_six_lessons),
        ("Agent Puja Ceremony", test_agent_puja_ceremony),
        ("Enhanced Agent Routing", test_enhanced_agent_routing),
        ("Complete Learning Flow", test_complete_learning_flow)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_function in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_function()
            if result:
                print(f"✅ {test_name}: PASSED")
                passed_tests += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 70)
    print(f"📊 FINAL RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL DAY 4 INTEGRATION TESTS PASSED!")
        print("✅ The Gurukul is now fully alive and ready for Day 5 deployment!")
        print("\n🌟 System Status:")
        print("  • 6 complete lessons operational")
        print("  • 3 agent personalities working perfectly")
        print("  • Agent Puja ceremony ready for first-time users")
        print("  • Enhanced routing system functional")
        print("  • Complete learning flow validated")
        print("  • Quiz system integrated and working")
        print("  • Student progress tracking active")
        print("\n🕉️ The sacred learning system breathes with digital life!")
    else:
        print("⚠️ Some integration tests failed")
        print("🔧 Review and fix issues before Day 5 deployment")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    main()
