#!/usr/bin/env python3
"""Setup script to initialize the Smart Library System"""
import subprocess
import sys
import os

def run_command(cmd, description):
    print(f"📋 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    print("🏗️  Setting up Smart Library System...")
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ Error: Please run this from the smart_library_system directory")
        return 1
    
    steps = [
        ("pip install -r requirements.txt", "Installing dependencies"),
        ("python scripts/init_db.py", "Initializing database"),
        ("python scripts/seed_data.py", "Seeding sample data"),
    ]
    
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"❌ Setup failed at step: {desc}")
            return 1
    
    print("
🎉 Setup completed successfully!")
    print("
📖 Next steps:")
    print("   python run.py                    # Start the server")
    print("   # OR")
    print("   uvicorn app.main:app --reload    # Alternative way")
    print("
🌐 The API will be available at:")
    print("   • API: http://localhost:8000")
    print("   • Docs: http://localhost:8000/docs")
    print("   • Health: http://localhost:8000/health")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
