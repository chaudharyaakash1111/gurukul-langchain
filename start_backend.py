#!/usr/bin/env python3
"""
Akash Gurukul Backend Startup Script
Simple script to start the backend server with proper configuration
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn', 
        'langchain',
        'pydantic',
        'jsonschema'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies found")
    return True

def check_lesson_files():
    """Check if lesson files are present"""
    lesson_dir = Path("curriculum/lessons")
    if not lesson_dir.exists():
        print("❌ Lesson directory not found: curriculum/lessons")
        return False
    
    lesson_files = list(lesson_dir.glob("*.json"))
    if not lesson_files:
        print("❌ No lesson files found in curriculum/lessons")
        return False
    
    print(f"✅ Found {len(lesson_files)} lesson files")
    return True

def start_server(host="0.0.0.0", port=8000, reload=False):
    """Start the FastAPI server"""
    print(f"🚀 Starting Akash Gurukul Backend Server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Reload: {reload}")
    print()
    
    cmd = [
        "uvicorn",
        "backend.main:app",
        "--host", host,
        "--port", str(port)
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return False
    except FileNotFoundError:
        print("❌ uvicorn not found. Please install with: pip install uvicorn")
        return False
    
    return True

def test_server(host="localhost", port=8000, timeout=30):
    """Test if server is running and responsive"""
    url = f"http://{host}:{port}/api/health"
    
    print(f"🔍 Testing server at {url}")
    
    for i in range(timeout):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Server is healthy!")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Lessons: {data.get('lessons_loaded', 0)}")
                print(f"   Agents: {data.get('agents_active', 0)}")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < timeout - 1:
            print(f"⏳ Waiting for server... ({i+1}/{timeout})")
            time.sleep(1)
    
    print("❌ Server health check failed")
    return False

def main():
    """Main startup function"""
    print("🕉️  Akash Gurukul Backend Startup")
    print("=" * 50)
    
    # Check current directory
    if not Path("backend/main.py").exists():
        print("❌ Please run this script from the project root directory")
        print("   Expected file: backend/main.py")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check lesson files
    if not check_lesson_files():
        sys.exit(1)
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Start Akash Gurukul Backend")
    parser.add_argument("--host", default="192.168.0.95", help="Host to bind to (default: your network IP)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--test-only", action="store_true", help="Only test the server, don't start it")
    
    args = parser.parse_args()
    
    if args.test_only:
        # Just test if server is already running
        test_host = "localhost" if args.host == "0.0.0.0" else args.host
        if test_server(test_host, args.port):
            print("🎉 Server is running and healthy!")
        else:
            print("❌ Server is not responding")
            sys.exit(1)
    else:
        # Start the server
        print("🔧 Starting server...")
        start_server(args.host, args.port, args.reload)

if __name__ == "__main__":
    main()
