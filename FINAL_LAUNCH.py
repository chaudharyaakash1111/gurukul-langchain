#!/usr/bin/env python3
"""
🕉️ AKASH GURUKUL FINAL LAUNCH SCRIPT 🕉️
The Sacred Moment - Complete System Deployment

This script verifies all components and launches the complete Akash Gurukul system.
"""

import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path

class AkashGurukulLauncher:
    """Sacred launcher for the complete Gurukul system"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.server_url = "http://192.168.0.95:8000"
        self.server_process = None
        
    def print_sacred_header(self):
        """Print the sacred launch header"""
        print("=" * 70)
        print("🕉️  AKASH GURUKUL - FINAL SYSTEM LAUNCH  🕉️")
        print("=" * 70)
        print("\"Gurur Brahma Gurur Vishnu Gurur Devo Maheshwarah\"")
        print("The Guru is the creator, sustainer, and transformer")
        print("=" * 70)
        print()
    
    def verify_system_components(self):
        """Verify all system components are present"""
        print("🔍 VERIFYING SYSTEM COMPONENTS...")
        print()
        
        components = {
            "📚 Curriculum": {
                "path": "curriculum/lessons",
                "files": [
                    "foundation_000_sankalpa-invocation.json",
                    "seed_dharma_001_introduction-to-kindness.json", 
                    "seed_kama_001_joyful-living-practices.json",
                    "tree_artha_001_understanding-value-creation.json",
                    "tree_dharma_002_compassion-in-action.json",
                    "sky_moksha_001_inner-wisdom-awakening.json"
                ]
            },
            "🤖 Agents": {
                "path": "agents",
                "files": [
                    "base_agent.py",
                    "memory_system.py", 
                    "agent_chaining.py"
                ]
            },
            "⚙️ Backend": {
                "path": "backend",
                "files": [
                    "main.py"
                ]
            },
            "🧪 Tests": {
                "path": "tests",
                "files": [
                    "day4_final_integration_test.py",
                    "test_agent_chaining.py"
                ]
            },
            "🎭 Ceremony": {
                "path": "curriculum",
                "files": [
                    "agent_puja_ceremony.py"
                ]
            }
        }
        
        all_verified = True
        
        for component_name, component_info in components.items():
            component_path = self.base_path / component_info["path"]
            print(f"{component_name}:")
            
            if not component_path.exists():
                print(f"  ❌ Directory not found: {component_path}")
                all_verified = False
                continue
            
            for file_name in component_info["files"]:
                file_path = component_path / file_name
                if file_path.exists():
                    print(f"  ✅ {file_name}")
                else:
                    print(f"  ❌ {file_name} - MISSING")
                    all_verified = False
            print()
        
        if all_verified:
            print("🎉 ALL SYSTEM COMPONENTS VERIFIED!")
        else:
            print("⚠️ Some components are missing!")
            
        return all_verified
    
    def start_backend_server(self):
        """Start the backend server"""
        print("🚀 STARTING BACKEND SERVER...")
        
        try:
            # Try to start the server
            cmd = [
                sys.executable, "-m", "uvicorn", 
                "backend.main:app", 
                "--host", "192.168.0.95", 
                "--port", "8000"
            ]
            
            self.server_process = subprocess.Popen(
                cmd,
                cwd=self.base_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if server is running
            if self.server_process.poll() is None:
                print("✅ Backend server started successfully!")
                return True
            else:
                print("❌ Backend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
    
    def verify_server_health(self):
        """Verify server is responding"""
        print("🏥 CHECKING SERVER HEALTH...")
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = requests.get(f"{self.server_url}/api/health", timeout=5)
                if response.status_code == 200:
                    health_data = response.json()
                    print("✅ Server is healthy!")
                    print(f"  Status: {health_data.get('status', 'unknown')}")
                    print(f"  Lessons loaded: {health_data.get('lessons_loaded', 0)}")
                    print(f"  Service: {health_data.get('service', 'unknown')}")
                    return True
            except requests.exceptions.RequestException:
                print(f"  Attempt {attempt + 1}/{max_retries} - Server not ready yet...")
                time.sleep(2)
        
        print("❌ Server health check failed!")
        return False
    
    def run_system_tests(self):
        """Run comprehensive system tests"""
        print("🧪 RUNNING SYSTEM TESTS...")
        print()
        
        # Test 1: Agent Puja Ceremony
        print("1. Testing Agent Puja Ceremony...")
        try:
            sys.path.append(str(self.base_path / "curriculum"))
            from agent_puja_ceremony import AgentPujaCeremony
            
            ceremony = AgentPujaCeremony("Test Student")
            opening = ceremony.begin_ceremony()
            
            if opening and opening.get("type") == "ceremony_opening":
                print("  ✅ Agent Puja Ceremony working")
            else:
                print("  ❌ Agent Puja Ceremony failed")
        except Exception as e:
            print(f"  ❌ Agent Puja Ceremony error: {e}")
        
        # Test 2: Lesson Loading
        print("2. Testing Lesson Loading...")
        try:
            response = requests.get(f"{self.server_url}/api/curriculum/lessons")
            if response.status_code == 200:
                lessons = response.json()
                lesson_count = len(lessons.get("lessons", {}))
                print(f"  ✅ {lesson_count} lessons loaded successfully")
            else:
                print(f"  ❌ Lesson loading failed: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Lesson loading error: {e}")
        
        # Test 3: Agent Chat
        print("3. Testing Agent Chat...")
        try:
            chat_data = {
                "agent_type": "seed",
                "student_id": "launch_test",
                "message": "Hello, I want to learn about kindness",
                "context": {"current_lesson": "foundation_000_sankalpa"}
            }
            
            response = requests.post(f"{self.server_url}/api/agents/chat", json=chat_data)
            if response.status_code == 200:
                result = response.json()
                if result.get("response"):
                    print("  ✅ Agent chat working")
                else:
                    print("  ❌ Agent chat returned empty response")
            else:
                print(f"  ❌ Agent chat failed: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Agent chat error: {e}")
        
        print()
    
    def display_system_info(self):
        """Display system information and access details"""
        print("📋 SYSTEM INFORMATION:")
        print(f"  🌐 Backend URL: {self.server_url}")
        print(f"  📚 Lessons Available: 6 complete lessons")
        print(f"  🤖 Agents: Tree (Wisdom), Seed (Practice), Sky (Philosophy)")
        print(f"  🔗 Agent Chaining: Intelligent transitions enabled")
        print(f"  🕉️ Sacred Ceremony: Agent Puja for new students")
        print()
        
        print("🎯 KEY ENDPOINTS:")
        print(f"  Health Check: GET {self.server_url}/api/health")
        print(f"  All Lessons: GET {self.server_url}/api/curriculum/lessons")
        print(f"  Agent Chat: POST {self.server_url}/api/agents/chat")
        print(f"  Start Lesson: POST {self.server_url}/api/lessons/start")
        print(f"  Quiz Questions: GET {self.server_url}/api/quiz/questions/{{lesson_id}}")
        print()
    
    def display_integration_guide(self):
        """Display integration guide for team members"""
        print("👥 TEAM INTEGRATION GUIDE:")
        print()
        print("📱 For Karan (Frontend):")
        print("  - Connect to agent chat API: POST /api/agents/chat")
        print("  - Implement lesson display from: GET /api/curriculum/lessons")
        print("  - Add quiz integration: GET /api/quiz/questions/{lesson_id}")
        print("  - Use Agent Puja ceremony for onboarding")
        print()
        
        print("💾 For Vedant (Backend/Database):")
        print("  - Implement student progress storage")
        print("  - Add lesson scoring system")
        print("  - Set up agent memory persistence")
        print("  - Create analytics dashboard")
        print()
        
        print("🎨 For Rishabh (UI/UX):")
        print("  - Apply agent personality themes")
        print("  - Implement responsive design")
        print("  - Add transition animations")
        print("  - Create quiz UI components")
        print()
        
        print("🎵 For Gandhar (Audio):")
        print("  - Provide TTS audio files for all 6 lessons")
        print("  - Create audio sync maps")
        print("  - Add meditation audio tracks")
        print()
        
        print("🎬 For Shashank (Video):")
        print("  - Provide video assets for lessons")
        print("  - Create chapter markers")
        print("  - Add video thumbnails")
        print()
    
    def launch_complete_system(self):
        """Launch the complete Akash Gurukul system"""
        self.print_sacred_header()
        
        # Step 1: Verify components
        if not self.verify_system_components():
            print("❌ System verification failed. Cannot launch.")
            return False
        
        print()
        
        # Step 2: Start backend
        if not self.start_backend_server():
            print("❌ Backend startup failed. Cannot launch.")
            return False
        
        print()
        
        # Step 3: Verify server health
        if not self.verify_server_health():
            print("❌ Server health check failed. Cannot launch.")
            return False
        
        print()
        
        # Step 4: Run tests
        self.run_system_tests()
        
        # Step 5: Display system info
        self.display_system_info()
        
        # Step 6: Display integration guide
        self.display_integration_guide()
        
        # Final success message
        print("🎉" * 35)
        print("🕉️  AKASH GURUKUL IS NOW LIVE!  🕉️")
        print("🎉" * 35)
        print()
        print("The sacred digital Gurukul breathes with life!")
        print("Students can now begin their transformative learning journey.")
        print()
        print("May this system serve the awakening of consciousness")
        print("and the flourishing of wisdom in all beings.")
        print()
        print("🙏 Om Shanti Shanti Shanti 🙏")
        
        return True
    
    def cleanup(self):
        """Cleanup resources"""
        if self.server_process:
            self.server_process.terminate()

def main():
    """Main launch function"""
    launcher = AkashGurukulLauncher()
    
    try:
        success = launcher.launch_complete_system()
        
        if success:
            print("\n🌟 System is running. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down system...")
        
    except Exception as e:
        print(f"\n❌ Launch error: {e}")
    finally:
        launcher.cleanup()

if __name__ == "__main__":
    main()
