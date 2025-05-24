#!/usr/bin/env python3
"""Simple startup script for development"""
import subprocess
import sys
import os

def main():
    print("🚀 Starting Smart Library System...")
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Error: Please run this from the smart_library_system directory")
        print("   Expected structure: smart_library_system/app/main.py")
        return 1
    
    # Run uvicorn
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return 1
    except KeyboardInterrupt:
        print("
👋 Server stopped")
        return 0

if __name__ == "__main__":
    sys.exit(main())
