import requests
import subprocess
import time
import signal
import sys
import threading

def run_server():
    """Function to run the server in a subprocess"""
    server_process = subprocess.Popen([sys.executable, "run_server.py"])
    return server_process

def test_api():
    """Function to test the API after a delay"""
    time.sleep(5)  # Wait for server to start
    
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8001/health")
        print(f"Health endpoint: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Health endpoint error: {e}")
    
    print("Testing signup endpoint...")
    try:
        signup_data = {
            "email": "test@example.com",
            "password": "securepassword123"
        }
        response = requests.post("http://localhost:8001/api/v1/auth/signup", json=signup_data)
        print(f"Signup endpoint: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Signup endpoint error: {e}")

if __name__ == "__main__":
    print("Starting server in subprocess...")
    server_proc = run_server()
    
    try:
        # Run the API tests in the main thread
        test_api()
    finally:
        # Terminate the server process
        server_proc.terminate()
        server_proc.wait()