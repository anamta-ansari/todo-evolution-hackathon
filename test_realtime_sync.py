"""
Test script to verify real-time task synchronization between chat and dashboard
"""
import requests
import json
import time
from datetime import datetime

def test_realtime_sync():
    print("Testing real-time task synchronization...")
    
    # Login credentials (adjust as needed)
    login_data = {
        "email": "test@example.com",  # Replace with actual test email
        "password": "password123"    # Replace with actual test password
    }
    
    # Login to get token
    try:
        response = requests.post("http://localhost:8000/api/v1/auth/signin", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            user_id = response.json()["user_id"]
            print(f"[SUCCESS] Successfully logged in. User ID: {user_id}")
        else:
            print(f"[ERROR] Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Login error: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 1: Get initial task count
    try:
        response = requests.get(f"http://localhost:8000/api/v1/users/{user_id}/tasks", headers=headers)
        initial_tasks = len(response.json()) if response.status_code == 200 else 0
        print(f"[SUCCESS] Initial task count: {initial_tasks}")
    except Exception as e:
        print(f"[ERROR] Error getting initial tasks: {e}")
        return False
    
    # Step 2: Simulate chat creating a task
    task_title = f"Test task {datetime.now().strftime('%H:%M:%S')}"
    chat_message = f"Add a task to {task_title}"
    
    try:
        chat_response = requests.post(
            f"http://localhost:8000/{user_id}/chat",
            json={"message": chat_message},
            headers=headers
        )
        
        if chat_response.status_code == 200:
            print(f"[SUCCESS] Chat message sent successfully: '{chat_message}'")
        else:
            print(f"[ERROR] Chat message failed: {chat_response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Error sending chat message: {e}")
        return False
    
    # Step 3: Wait for auto-refresh (should happen within 3 seconds)
    print("Waiting for dashboard to refresh...")
    time.sleep(4)  # Wait slightly longer than the 3-second refresh interval
    
    # Step 4: Get updated task count
    try:
        response = requests.get(f"http://localhost:8000/api/v1/users/{user_id}/tasks", headers=headers)
        updated_tasks = len(response.json()) if response.status_code == 200 else 0
        print(f"[SUCCESS] Updated task count: {updated_tasks}")
    except Exception as e:
        print(f"[ERROR] Error getting updated tasks: {e}")
        return False
    
    # Step 5: Verify task was added
    if updated_tasks > initial_tasks:
        print("[SUCCESS] Task was successfully added and detected by dashboard!")
        
        # Get the new task details
        response = requests.get(f"http://localhost:8000/api/v1/users/{user_id}/tasks", headers=headers)
        tasks = response.json()
        new_task = tasks[-1]  # Last task should be the newly added one
        
        print(f"[SUCCESS] New task details: ID={new_task['id']}, Title='{new_task['title']}'")
        return True
    else:
        print("[ERROR] Task was not detected by dashboard after refresh")
        return False

if __name__ == "__main__":
    success = test_realtime_sync()
    if success:
        print("\n[SUCCESS] Real-time synchronization test PASSED!")
    else:
        print("\n[ERROR] Real-time synchronization test FAILED!")