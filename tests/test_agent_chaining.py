"""
Test Agent Chaining System
Comprehensive tests for intelligent agent transitions and context passing
"""

import requests
import json
import time
from typing import Dict, List

BASE_URL = "http://192.168.0.95:8000"

class AgentChainingTester:
    """Test the agent chaining system comprehensively"""
    
    def __init__(self):
        self.student_id = f"chain_test_{int(time.time())}"
        self.lesson_id = "foundation_000_sankalpa"
        
    def test_basic_agent_chaining(self) -> bool:
        """Test basic agent chaining functionality"""
        print("🔗 Testing Basic Agent Chaining...")
        
        # Start a lesson first
        start_response = requests.post(f"{BASE_URL}/api/lessons/start", json={
            "student_id": self.student_id,
            "lesson_id": self.lesson_id
        })
        
        if start_response.status_code != 200:
            print("❌ Failed to start lesson")
            return False
        
        # Test sequence: Seed -> Tree -> Sky -> Seed
        conversation_flow = [
            {
                "agent": "seed",
                "message": "How can I practice my Sankalpa daily?",
                "expected_next": "seed"  # Should stay with seed for practice
            },
            {
                "agent": "seed", 
                "message": "Why is making a Sankalpa important?",
                "expected_next": "tree"  # Should suggest tree for explanation
            },
            {
                "agent": "tree",
                "message": "What does this mean for my spiritual journey?", 
                "expected_next": "sky"  # Should suggest sky for spiritual meaning
            },
            {
                "agent": "sky",
                "message": "How do I apply this insight in my daily life?",
                "expected_next": "seed"  # Should suggest seed for application
            }
        ]
        
        correct_suggestions = 0
        total_tests = len(conversation_flow)
        
        for i, step in enumerate(conversation_flow):
            try:
                # Chat with current agent
                chat_response = requests.post(f"{BASE_URL}/api/agents/chat", json={
                    "agent_type": step["agent"],
                    "student_id": self.student_id,
                    "message": step["message"],
                    "context": {"current_lesson": self.lesson_id}
                })
                
                if chat_response.status_code == 200:
                    result = chat_response.json()
                    context = result.get("context", {})
                    transition_suggestion = context.get("transition_suggestion", {})
                    
                    suggested_agent = transition_suggestion.get("recommended_agent")
                    should_transition = transition_suggestion.get("should_transition", False)
                    
                    print(f"  Step {i+1}: {step['agent']} -> {suggested_agent}")
                    print(f"    Message: '{step['message'][:50]}...'")
                    print(f"    Should transition: {should_transition}")
                    print(f"    Expected: {step['expected_next']}, Got: {suggested_agent}")
                    
                    if suggested_agent == step["expected_next"]:
                        correct_suggestions += 1
                        print(f"    ✅ Correct suggestion")
                    else:
                        print(f"    ❌ Incorrect suggestion")
                else:
                    print(f"  ❌ Step {i+1} failed: HTTP {chat_response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"  ❌ Step {i+1} error: {e}")
                return False
        
        accuracy = (correct_suggestions / total_tests) * 100
        print(f"\n📊 Chaining Accuracy: {accuracy:.1f}% ({correct_suggestions}/{total_tests})")
        
        return accuracy >= 75  # Require 75% accuracy
    
    def test_context_preservation(self) -> bool:
        """Test that context is preserved across agent transitions"""
        print("\n🧠 Testing Context Preservation...")
        
        # Have a conversation that should build context
        conversation = [
            ("seed", "I want to practice gratitude daily"),
            ("tree", "Why is gratitude important for well-being?"),
            ("sky", "How does gratitude connect me to the divine?")
        ]
        
        for i, (agent, message) in enumerate(conversation):
            try:
                response = requests.post(f"{BASE_URL}/api/agents/chat", json={
                    "agent_type": agent,
                    "student_id": self.student_id,
                    "message": message,
                    "context": {"current_lesson": self.lesson_id}
                })
                
                if response.status_code == 200:
                    result = response.json()
                    context = result.get("context", {})
                    chain_summary = context.get("chain_summary", {})
                    
                    print(f"  Step {i+1}: {agent} agent")
                    print(f"    Total interactions: {chain_summary.get('total_interactions', 0)}")
                    print(f"    Agents used: {chain_summary.get('agents_used', [])}")
                    
                    # Check that context is building
                    if i == 0:
                        expected_interactions = 1
                    elif i == 1:
                        expected_interactions = 2
                    else:
                        expected_interactions = 3
                    
                    actual_interactions = chain_summary.get('total_interactions', 0)
                    if actual_interactions >= expected_interactions:
                        print(f"    ✅ Context preserved ({actual_interactions} interactions)")
                    else:
                        print(f"    ❌ Context lost ({actual_interactions} < {expected_interactions})")
                        return False
                else:
                    print(f"  ❌ Step {i+1} failed: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"  ❌ Step {i+1} error: {e}")
                return False
        
        print("✅ Context preservation working")
        return True
    
    def test_chain_suggestion_api(self) -> bool:
        """Test the dedicated chain suggestion API"""
        print("\n🎯 Testing Chain Suggestion API...")
        
        test_cases = [
            {
                "current_agent": "seed",
                "user_input": "Why is this practice important?",
                "expected_suggestion": "tree"
            },
            {
                "current_agent": "tree", 
                "user_input": "What does this mean for my soul?",
                "expected_suggestion": "sky"
            },
            {
                "current_agent": "sky",
                "user_input": "How do I practice this daily?",
                "expected_suggestion": "seed"
            }
        ]
        
        correct_suggestions = 0
        
        for i, test_case in enumerate(test_cases):
            try:
                response = requests.get(f"{BASE_URL}/api/agents/chain-suggestion/{self.student_id}", params={
                    "current_agent": test_case["current_agent"],
                    "user_input": test_case["user_input"],
                    "lesson_id": self.lesson_id
                })
                
                if response.status_code == 200:
                    result = response.json()
                    suggestion = result.get("suggestion", {})
                    recommended_agent = suggestion.get("recommended_agent")
                    
                    print(f"  Test {i+1}: {test_case['current_agent']} -> {recommended_agent}")
                    print(f"    Input: '{test_case['user_input'][:40]}...'")
                    print(f"    Expected: {test_case['expected_suggestion']}")
                    
                    if recommended_agent == test_case["expected_suggestion"]:
                        correct_suggestions += 1
                        print(f"    ✅ Correct")
                    else:
                        print(f"    ❌ Incorrect")
                else:
                    print(f"  ❌ Test {i+1} failed: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"  ❌ Test {i+1} error: {e}")
                return False
        
        accuracy = (correct_suggestions / len(test_cases)) * 100
        print(f"\n📊 API Suggestion Accuracy: {accuracy:.1f}%")
        
        return accuracy >= 66  # Require 2/3 accuracy
    
    def test_chain_summary_api(self) -> bool:
        """Test the chain summary API"""
        print("\n📋 Testing Chain Summary API...")
        
        try:
            response = requests.get(f"{BASE_URL}/api/agents/chain-summary/{self.student_id}", params={
                "lesson_id": self.lesson_id
            })
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get("summary", {})
                
                print(f"  Chain ID: {summary.get('chain_id', 'N/A')}")
                print(f"  Total interactions: {summary.get('total_interactions', 0)}")
                print(f"  Agents used: {summary.get('agents_used', [])}")
                print(f"  Current state: {summary.get('current_state', {})}")
                
                # Verify we have some interactions from previous tests
                if summary.get('total_interactions', 0) > 0:
                    print("  ✅ Chain summary working")
                    return True
                else:
                    print("  ❌ No interactions recorded")
                    return False
            else:
                print(f"  ❌ API failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def test_intelligent_routing_patterns(self) -> bool:
        """Test intelligent routing patterns"""
        print("\n🧭 Testing Intelligent Routing Patterns...")
        
        # Test different types of queries and their expected routing
        routing_tests = [
            # Practice-oriented queries -> Seed
            ("How do I meditate?", "seed"),
            ("Show me the steps", "seed"),
            ("What exercises can I do?", "seed"),
            
            # Understanding-oriented queries -> Tree  
            ("Why is this important?", "tree"),
            ("Explain the concept", "tree"),
            ("What's the principle behind this?", "tree"),
            
            # Meaning-oriented queries -> Sky
            ("What's the deeper meaning?", "sky"),
            ("How does this serve my soul?", "sky"),
            ("What's the spiritual significance?", "sky")
        ]
        
        correct_routes = 0
        total_tests = len(routing_tests)
        
        for query, expected_agent in routing_tests:
            try:
                response = requests.get(f"{BASE_URL}/api/agents/chain-suggestion/{self.student_id}", params={
                    "current_agent": "tree",  # Start from neutral position
                    "user_input": query,
                    "lesson_id": self.lesson_id
                })
                
                if response.status_code == 200:
                    result = response.json()
                    suggestion = result.get("suggestion", {})
                    recommended_agent = suggestion.get("recommended_agent")
                    
                    if recommended_agent == expected_agent:
                        correct_routes += 1
                        print(f"  ✅ '{query[:30]}...' -> {recommended_agent}")
                    else:
                        print(f"  ❌ '{query[:30]}...' -> {recommended_agent} (expected {expected_agent})")
                else:
                    print(f"  ❌ Query failed: {query[:30]}...")
                    
            except Exception as e:
                print(f"  ❌ Error testing query: {e}")
        
        accuracy = (correct_routes / total_tests) * 100
        print(f"\n📊 Routing Pattern Accuracy: {accuracy:.1f}% ({correct_routes}/{total_tests})")
        
        return accuracy >= 70  # Require 70% accuracy
    
    def run_comprehensive_test(self) -> bool:
        """Run all agent chaining tests"""
        print("🚀 Starting Comprehensive Agent Chaining Test")
        print("=" * 60)
        
        tests = [
            ("Basic Agent Chaining", self.test_basic_agent_chaining),
            ("Context Preservation", self.test_context_preservation),
            ("Chain Suggestion API", self.test_chain_suggestion_api),
            ("Chain Summary API", self.test_chain_summary_api),
            ("Intelligent Routing Patterns", self.test_intelligent_routing_patterns)
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
        
        print("\n" + "=" * 60)
        print(f"📊 FINAL RESULTS: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL AGENT CHAINING TESTS PASSED!")
            print("✅ Intelligent agent transitions working perfectly")
            print("✅ Context preservation across agents functional")
            print("✅ Chain suggestion APIs operational")
            print("✅ Routing patterns accurate and intelligent")
        else:
            print("⚠️ Some agent chaining tests failed")
            print("🔧 Review chaining logic before deployment")
        
        return passed_tests == total_tests

def main():
    """Run the agent chaining tests"""
    tester = AgentChainingTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🌟 Agent chaining system is ready for deployment!")
        print("🔗 Seamless agent transitions enabled")
        print("🧠 Context preservation working")
        print("🎯 Intelligent routing operational")
    else:
        print("\n🔧 Agent chaining system needs attention")
    
    return success

if __name__ == "__main__":
    main()
