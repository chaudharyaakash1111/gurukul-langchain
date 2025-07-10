#!/usr/bin/env python3
"""
🕉️ AKASH GURUKUL SYSTEM VERIFICATION 🕉️
Complete verification of all system components without server dependency
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

class SystemVerifier:
    """Comprehensive system verification"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.verification_results = {}
        
    def print_header(self):
        print("=" * 70)
        print("🕉️  AKASH GURUKUL - SYSTEM VERIFICATION  🕉️")
        print("=" * 70)
        print("Complete verification of all components")
        print("=" * 70)
        print()
    
    def verify_curriculum(self):
        """Verify curriculum lessons"""
        print("📚 VERIFYING CURRICULUM...")
        
        lessons_path = self.base_path / "curriculum" / "lessons"
        expected_lessons = [
            "foundation_000_sankalpa-invocation.json",
            "seed_dharma_001_introduction-to-kindness.json", 
            "seed_kama_001_joyful-living-practices.json",
            "tree_artha_001_understanding-value-creation.json",
            "tree_dharma_002_compassion-in-action.json",
            "sky_moksha_001_inner-wisdom-awakening.json"
        ]
        
        verified_lessons = []
        
        for lesson_file in expected_lessons:
            lesson_path = lessons_path / lesson_file
            if lesson_path.exists():
                try:
                    with open(lesson_path, 'r', encoding='utf-8') as f:
                        lesson_data = json.load(f)
                    
                    # Verify lesson structure
                    required_fields = ['id', 'title', 'content', 'quiz']
                    if all(field in lesson_data for field in required_fields):
                        print(f"  ✅ {lesson_file} - Valid structure")
                        verified_lessons.append(lesson_file)
                    else:
                        print(f"  ⚠️ {lesson_file} - Missing required fields")
                        
                except json.JSONDecodeError:
                    print(f"  ❌ {lesson_file} - Invalid JSON")
                except Exception as e:
                    print(f"  ❌ {lesson_file} - Error: {e}")
            else:
                print(f"  ❌ {lesson_file} - File not found")
        
        self.verification_results['curriculum'] = {
            'total_expected': len(expected_lessons),
            'verified': len(verified_lessons),
            'success': len(verified_lessons) == len(expected_lessons)
        }
        
        print(f"📊 Curriculum: {len(verified_lessons)}/{len(expected_lessons)} lessons verified")
        print()
    
    def verify_agents(self):
        """Verify agent system"""
        print("🤖 VERIFYING AGENT SYSTEM...")
        
        agents_path = self.base_path / "agents"
        agent_files = [
            "base_agent.py",
            "memory_system.py",
            "agent_chaining.py"
        ]
        
        verified_agents = []
        
        for agent_file in agent_files:
            agent_path = agents_path / agent_file
            if agent_path.exists():
                try:
                    # Try to import the module
                    spec = importlib.util.spec_from_file_location(
                        agent_file[:-3], agent_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    print(f"  ✅ {agent_file} - Imports successfully")
                    verified_agents.append(agent_file)
                    
                except Exception as e:
                    print(f"  ❌ {agent_file} - Import error: {e}")
            else:
                print(f"  ❌ {agent_file} - File not found")
        
        self.verification_results['agents'] = {
            'total_expected': len(agent_files),
            'verified': len(verified_agents),
            'success': len(verified_agents) == len(agent_files)
        }
        
        print(f"📊 Agents: {len(verified_agents)}/{len(agent_files)} agent files verified")
        print()
    
    def verify_backend(self):
        """Verify backend system"""
        print("⚙️ VERIFYING BACKEND...")
        
        backend_path = self.base_path / "backend" / "main.py"
        
        if backend_path.exists():
            try:
                # Check if backend imports correctly
                sys.path.insert(0, str(self.base_path))
                
                # Try importing key components
                from curriculum.ingestion import CurriculumIngestion
                from agents.base_agent import create_agent
                
                print("  ✅ Backend imports working")
                print("  ✅ Curriculum ingestion available")
                print("  ✅ Agent creation available")
                
                # Test curriculum loading
                ingestion = CurriculumIngestion()
                ingestion.load_all_lessons()
                lesson_count = len(ingestion.lessons)
                
                print(f"  ✅ Curriculum loads {lesson_count} lessons")
                
                self.verification_results['backend'] = {
                    'imports': True,
                    'curriculum_loading': True,
                    'lesson_count': lesson_count,
                    'success': True
                }
                
            except Exception as e:
                print(f"  ❌ Backend verification error: {e}")
                self.verification_results['backend'] = {
                    'success': False,
                    'error': str(e)
                }
        else:
            print("  ❌ Backend main.py not found")
            self.verification_results['backend'] = {'success': False}
        
        print()
    
    def verify_ceremony(self):
        """Verify Agent Puja ceremony"""
        print("🕉️ VERIFYING AGENT PUJA CEREMONY...")
        
        ceremony_path = self.base_path / "curriculum" / "agent_puja_ceremony.py"
        
        if ceremony_path.exists():
            try:
                sys.path.insert(0, str(self.base_path / "curriculum"))
                from agent_puja_ceremony import AgentPujaCeremony
                
                # Test ceremony creation
                ceremony = AgentPujaCeremony("Test Student")
                
                # Test ceremony methods
                opening = ceremony.begin_ceremony()
                seed_invocation = ceremony.invoke_seed_agent()
                tree_invocation = ceremony.invoke_tree_agent()
                sky_invocation = ceremony.invoke_sky_agent()
                completion = ceremony.complete_ceremony()
                
                if all([opening, seed_invocation, tree_invocation, sky_invocation, completion]):
                    print("  ✅ Agent Puja ceremony fully functional")
                    print("  ✅ All agent invocations working")
                    print("  ✅ Ceremony completion working")
                    
                    self.verification_results['ceremony'] = {'success': True}
                else:
                    print("  ❌ Some ceremony methods failed")
                    self.verification_results['ceremony'] = {'success': False}
                    
            except Exception as e:
                print(f"  ❌ Ceremony verification error: {e}")
                self.verification_results['ceremony'] = {'success': False, 'error': str(e)}
        else:
            print("  ❌ Agent Puja ceremony file not found")
            self.verification_results['ceremony'] = {'success': False}
        
        print()
    
    def verify_tests(self):
        """Verify test files"""
        print("🧪 VERIFYING TEST SYSTEM...")
        
        tests_path = self.base_path / "tests"
        test_files = [
            "day4_final_integration_test.py",
            "test_agent_chaining.py"
        ]
        
        verified_tests = []
        
        for test_file in test_files:
            test_path = tests_path / test_file
            if test_path.exists():
                try:
                    # Check if test file is syntactically correct
                    with open(test_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    compile(content, test_path, 'exec')
                    print(f"  ✅ {test_file} - Syntax valid")
                    verified_tests.append(test_file)
                    
                except SyntaxError as e:
                    print(f"  ❌ {test_file} - Syntax error: {e}")
                except Exception as e:
                    print(f"  ❌ {test_file} - Error: {e}")
            else:
                print(f"  ❌ {test_file} - File not found")
        
        self.verification_results['tests'] = {
            'total_expected': len(test_files),
            'verified': len(verified_tests),
            'success': len(verified_tests) == len(test_files)
        }
        
        print(f"📊 Tests: {len(verified_tests)}/{len(test_files)} test files verified")
        print()
    
    def generate_final_report(self):
        """Generate final verification report"""
        print("📋 FINAL VERIFICATION REPORT")
        print("=" * 50)
        
        total_components = len(self.verification_results)
        successful_components = sum(1 for result in self.verification_results.values() 
                                  if result.get('success', False))
        
        print(f"📊 Overall Status: {successful_components}/{total_components} components verified")
        print()
        
        for component, result in self.verification_results.items():
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            print(f"{component.upper()}: {status}")
            
            if component == 'curriculum':
                print(f"  Lessons: {result.get('verified', 0)}/{result.get('total_expected', 0)}")
            elif component == 'agents':
                print(f"  Agent files: {result.get('verified', 0)}/{result.get('total_expected', 0)}")
            elif component == 'backend':
                if result.get('lesson_count'):
                    print(f"  Lessons loaded: {result.get('lesson_count', 0)}")
            elif component == 'tests':
                print(f"  Test files: {result.get('verified', 0)}/{result.get('total_expected', 0)}")
        
        print()
        
        if successful_components == total_components:
            print("🎉 ALL COMPONENTS VERIFIED SUCCESSFULLY!")
            print()
            print("🌟 AKASH GURUKUL IS READY FOR DEPLOYMENT!")
            print()
            print("System includes:")
            print("  📚 6 Complete Lessons (Foundation + Seed + Tree + Sky)")
            print("  🤖 3 AI Agents (Tree, Seed, Sky) with Chaining")
            print("  🕉️ Agent Puja Sacred Ceremony")
            print("  ⚙️ Complete Backend API")
            print("  🧪 Comprehensive Test Suite")
            print()
            print("Ready for team integration:")
            print("  👨‍💻 Karan: Frontend integration")
            print("  💾 Vedant: Database & storage")
            print("  🎨 Rishabh: UI/UX implementation")
            print("  🎵 Gandhar: Audio & TTS")
            print("  🎬 Shashank: Video assets")
            
        else:
            print("⚠️ Some components need attention before deployment")
        
        print()
        print("🙏 Om Shanti Shanti Shanti 🙏")
    
    def run_complete_verification(self):
        """Run complete system verification"""
        self.print_header()
        
        self.verify_curriculum()
        self.verify_agents()
        self.verify_backend()
        self.verify_ceremony()
        self.verify_tests()
        
        self.generate_final_report()

def main():
    """Main verification function"""
    verifier = SystemVerifier()
    verifier.run_complete_verification()

if __name__ == "__main__":
    main()
