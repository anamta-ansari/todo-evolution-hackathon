#!/usr/bin/env python3
"""
Script to start the backend server with proper configuration
"""
import subprocess
import sys
import os
import time

def start_server():
    # Add the current directory to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # Start the server using uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8001",
        "--reload"  # Enable auto-reload for development
    ]
    
    print("Starting server with command:", " ".join(cmd))
    
    # Start the server process
    process = subprocess.Popen(cmd)
    
    # Wait a bit for the server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Check if the process is still running
    if process.poll() is not None:
        print("❌ Server failed to start. Check for errors above.")
        return None
    
    print("✅ Server started successfully on http://localhost:8001")
    return process

if __name__ == "__main__":
    server_process = start_server()
    
    if server_process:
        print("Server is running. Press Ctrl+C to stop.")
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping server...")
            server_process.terminate()
            server_process.wait()
            print("Server stopped.")