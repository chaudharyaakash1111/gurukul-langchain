"""
Day 4 Agent Routing Verification Test
Comprehensive testing of Tree, Seed, Sky routing to ensure proper agent selection
"""

import requests
import json
import time
from typing import Dict, List, Tuple

BASE_URL = "http://192.168.0.95:8000"

class AgentRoutingTester:
    """Comprehensive tester for agent routing system"""
    
    def __init__(self):
        self.test_results = []
        self.student_id = f"routing_test_{int(time.time())}"
        
    def test_agent_suggestion_accuracy(self) -> bool:
        """Test agent suggestion accuracy with various query types"""
        print("🧪 Testing Agent Suggestion Accuracy...")
        
        test_cases = [
            # Seed Agent (Practical) queries
            {
                "query": "How can I practice kindness in my daily life?",
                "expected_agent": "seed",
                "category": "practical",
                "description": "Direct practice question"
            },
            {
                "query": "What steps should I take to develop compassion?",
                "expected_agent": "seed", 
                "category": "practical",
                "description": "Step-by-step guidance request"
            },
            {
                "query": "Can you show me exercises for inner wisdom?",
                "expected_agent": "seed",
                "category": "practical", 
                "description": "Exercise/technique request"
            },
            {
                "query": "How do I apply this teaching in real situations?",
                "expected_agent": "seed",
                "category": "practical",
                "description": "Application guidance"
            },
            
            # Tree Agent (Conceptual) queries
            {
                "query": "Why is compassion important for spiritual growth?",
                "expected_agent": "tree",
                "category": "conceptual",
                "description": "Why/explanation question"
            },
            {
                "query": "What is the relationship between wisdom and knowledge?",
                "expected_agent": "tree",
                "category": "conceptual", 
                "description": "Conceptual relationship"
            },
            {
                "query": "Explain the principles behind mindful living",
                "expected_agent": "tree",
                "category": "conceptual",
                "description": "Principle explanation"
            },
            {
                "query": "How does this connect to other wisdom traditions?",
                "expected_agent": "tree",
                "category": "conceptual",
                "description": "Connection/framework question"
            },
            
            # Sky Agent (Reflective) queries  
            {
                "query": "What does this mean for my soul's journey?",
                "expected_agent": "sky",
                "category": "reflective",
                "description": "Soul/spiritual meaning"
            },
            {
                "query": "How does this teaching connect me to the divine?",
                "expected_agent": "sky",
                "category": "reflective",
                "description": "Divine connection"
            },
            {
                "query": "What is my deeper purpose in learning this?",
                "expected_agent": "sky",
                "category": "reflective",
                "description": "Purpose/meaning inquiry"
            },
            {
                "query": "How does this reflect the nature of consciousness?",
                "expected_agent": "sky",
                "category": "reflective",
                "description": "Philosophical reflection"
            }
        ]
        
        correct_suggestions = 0
        total_tests = len(test_cases)
        
        for i, test_case in enumerate(test_cases):
            try:
                # Get agent suggestion
                response = requests.get(
                    f"{BASE_URL}/api/lessons/suggest-agent/{self.student_id}",
                    params={
                        "user_input": test_case["query"],
                        "current_agent": "seed"  # Start from seed
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    suggested_agent = result["suggested_agent"]
                    expected_agent = test_case["expected_agent"]
                    
                    is_correct = suggested_agent == expected_agent
                    if is_correct:
                        correct_suggestions += 1
                    
                    print(f"  Test {i+1}/{total_tests}: {test_case['description']}")
                    print(f"    Query: '{test_case['query'][:50]}...'")
                    print(f"    Expected: {expected_agent}, Got: {suggested_agent} {'✅' if is_correct else '❌'}")
                    
                    self.test_results.append({
                        "test": "agent_suggestion",
                        "query": test_case["query"],
                        "expected": expected_agent,
                        "actual": suggested_agent,
                        "correct": is_correct,
                        "category": test_case["category"]
                    })
                else:
                    print(f"  ❌ Test {i+1} failed: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"  ❌ Test {i+1} error: {e}")
                return False
        
        accuracy = (correct_suggestions / total_tests) * 100
        print(f"\n📊 Agent Suggestion Accuracy: {accuracy:.1f}% ({correct_suggestions}/{total_tests})")
        
        # Analyze by category
        categories = {}
        for result in self.test_results:
            if result["test"] == "agent_suggestion":
                cat = result["category"]
                if cat not in categories:
                    categories[cat] = {"correct": 0, "total": 0}
                categories[cat]["total"] += 1
                if result["correct"]:
                    categories[cat]["correct"] += 1
        
        print("\n📈 Accuracy by Category:")
        for category, stats in categories.items():
            cat_accuracy = (stats["correct"] / stats["total"]) * 100
            print(f"  {category.title()}: {cat_accuracy:.1f}% ({stats['correct']}/{stats['total']})")
        
        return accuracy >= 75  # Require 75% accuracy
    
    def test_agent_response_quality(self) -> bool:
        """Test that each agent responds appropriately to their type of query"""
        print("\n🎭 Testing Agent Response Quality...")
        
        # Start a lesson first
        lesson_start = requests.post(f"{BASE_URL}/api/lessons/start", json={
            "student_id": self.student_id,
            "lesson_id": "foundation_000_sankalpa"
        })
        
        if lesson_start.status_code != 200:
            print("❌ Failed to start lesson for response testing")
            return False
        
        agent_tests = [
            {
                "agent": "seed",
                "query": "How can I practice gratitude daily?",
                "expected_keywords": ["practice", "daily", "steps", "routine", "habit"],
                "description": "Practical guidance request"
            },
            {
                "agent": "tree", 
                "query": "Why is gratitude important for well-being?",
                "expected_keywords": ["because", "research", "principle", "understand", "connection"],
                "description": "Conceptual explanation request"
            },
            {
                "agent": "sky",
                "query": "What does gratitude reveal about the nature of existence?",
                "expected_keywords": ["reflect", "contemplate", "meaning", "soul", "deeper"],
                "description": "Philosophical inquiry"
            }
        ]
        
        all_passed = True
        
        for test in agent_tests:
            try:
                response = requests.post(f"{BASE_URL}/api/agents/chat", json={
                    "agent_type": test["agent"],
                    "student_id": self.student_id,
                    "message": test["query"],
                    "context": {"current_lesson": "foundation_000_sankalpa"}
                }, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    agent_response = result["response"].lower()
                    
                    # Check for expected keywords
                    keywords_found = sum(1 for keyword in test["expected_keywords"] 
                                       if keyword in agent_response)
                    keyword_score = keywords_found / len(test["expected_keywords"])
                    
                    # Check response length (should be substantial)
                    length_ok = len(agent_response) > 100
                    
                    # Check agent-specific characteristics
                    agent_appropriate = self._check_agent_appropriateness(
                        test["agent"], agent_response
                    )
                    
                    test_passed = keyword_score >= 0.4 and length_ok and agent_appropriate
                    
                    print(f"  {test['agent'].title()} Agent - {test['description']}")
                    print(f"    Keywords: {keywords_found}/{len(test['expected_keywords'])} ({'✅' if keyword_score >= 0.4 else '❌'})")
                    print(f"    Length: {len(agent_response)} chars ({'✅' if length_ok else '❌'})")
                    print(f"    Appropriate: {'✅' if agent_appropriate else '❌'}")
                    print(f"    Overall: {'✅ PASS' if test_passed else '❌ FAIL'}")
                    
                    if not test_passed:
                        all_passed = False
                        
                else:
                    print(f"  ❌ {test['agent'].title()} Agent failed: HTTP {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                print(f"  ❌ {test['agent'].title()} Agent error: {e}")
                all_passed = False
        
        return all_passed
    
    def _check_agent_appropriateness(self, agent_type: str, response: str) -> bool:
        """Check if response matches agent personality"""
        response_lower = response.lower()
        
        if agent_type == "seed":
            # Should be practical and action-oriented
            practical_indicators = ["practice", "try", "do", "start", "begin", "step", "daily", "routine"]
            return any(indicator in response_lower for indicator in practical_indicators)
            
        elif agent_type == "tree":
            # Should be explanatory and conceptual
            conceptual_indicators = ["because", "understand", "principle", "concept", "reason", "connection", "framework"]
            return any(indicator in response_lower for indicator in conceptual_indicators)
            
        elif agent_type == "sky":
            # Should be reflective and philosophical
            reflective_indicators = ["reflect", "contemplate", "meaning", "purpose", "soul", "deeper", "spiritual", "divine"]
            return any(indicator in response_lower for indicator in reflective_indicators)
        
        return False
    
    def test_agent_diversity_encouragement(self) -> bool:
        """Test that the system encourages trying different agents"""
        print("\n🔄 Testing Agent Diversity Encouragement...")
        
        # Make multiple requests with the same agent to see if system suggests others
        current_agent = "seed"
        query = "Tell me about wisdom"
        
        suggestions = []
        for i in range(5):
            try:
                response = requests.get(
                    f"{BASE_URL}/api/lessons/suggest-agent/{self.student_id}",
                    params={
                        "user_input": query,
                        "current_agent": current_agent
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    suggested_agent = result["suggested_agent"]
                    suggestions.append(suggested_agent)
                    current_agent = suggested_agent  # Use suggested agent for next iteration
                else:
                    print(f"  ❌ Request {i+1} failed: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"  ❌ Request {i+1} error: {e}")
                return False
        
        # Check if we got variety in suggestions
        unique_agents = set(suggestions)
        diversity_score = len(unique_agents) / 3.0  # 3 possible agents
        
        print(f"  Suggestions: {suggestions}")
        print(f"  Unique agents: {list(unique_agents)}")
        print(f"  Diversity score: {diversity_score:.1%}")
        
        # Should suggest at least 2 different agents in 5 requests
        return len(unique_agents) >= 2
    
    def test_fallback_behavior(self) -> bool:
        """Test fallback behavior for edge cases"""
        print("\n🛡️ Testing Fallback Behavior...")
        
        edge_cases = [
            {
                "query": "",  # Empty query
                "description": "Empty query"
            },
            {
                "query": "asdfghjkl qwertyuiop",  # Nonsense query
                "description": "Nonsense query"
            },
            {
                "query": "a",  # Very short query
                "description": "Very short query"
            },
            {
                "query": "What is the meaning of life, the universe, and everything according to the ancient wisdom traditions and how does this relate to modern quantum physics and consciousness studies?",  # Very long query
                "description": "Very long query"
            }
        ]
        
        all_handled = True
        
        for test_case in edge_cases:
            try:
                response = requests.get(
                    f"{BASE_URL}/api/lessons/suggest-agent/{self.student_id}",
                    params={
                        "user_input": test_case["query"],
                        "current_agent": "seed"
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    suggested_agent = result["suggested_agent"]
                    
                    # Should suggest a valid agent
                    valid_agent = suggested_agent in ["seed", "tree", "sky"]
                    
                    print(f"  {test_case['description']}: {suggested_agent} {'✅' if valid_agent else '❌'}")
                    
                    if not valid_agent:
                        all_handled = False
                else:
                    print(f"  ❌ {test_case['description']} failed: HTTP {response.status_code}")
                    all_handled = False
                    
            except Exception as e:
                print(f"  ❌ {test_case['description']} error: {e}")
                all_handled = False
        
        return all_handled
    
    def run_comprehensive_test(self) -> bool:
        """Run all agent routing tests"""
        print("🚀 Starting Comprehensive Agent Routing Test")
        print("=" * 60)
        
        tests = [
            ("Agent Suggestion Accuracy", self.test_agent_suggestion_accuracy),
            ("Agent Response Quality", self.test_agent_response_quality),
            ("Agent Diversity Encouragement", self.test_agent_diversity_encouragement),
            ("Fallback Behavior", self.test_fallback_behavior)
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
            print("🎉 ALL AGENT ROUTING TESTS PASSED!")
            print("✅ Tree, Seed, Sky routing is working as intended")
        else:
            print("⚠️ Some agent routing tests failed")
            print("🔧 Review and fix routing logic before deployment")
        
        return passed_tests == total_tests

def main():
    """Run the agent routing verification"""
    tester = AgentRoutingTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🌟 Agent routing system is ready for Day 5 deployment!")
    else:
        print("\n🔧 Agent routing system needs attention before deployment")
    
    return success

if __name__ == "__main__":
    main()
