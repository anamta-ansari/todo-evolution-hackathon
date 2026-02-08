"""
Simple script to create a test user for testing purposes
"""
import requests
import json

def create_test_user():
    # Test user data
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/v1/auth/signup", json=user_data)
        if response.status_code == 201:
            print(f"[SUCCESS] Test user created: {response.json()['user']['email']}")
            return True
        elif response.status_code == 409:
            print("[INFO] Test user already exists, continuing with test...")
            return True
        else:
            print(f"[ERROR] Failed to create test user: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception during user creation: {e}")
        return False

if __name__ == "__main__":
    success = create_test_user()
    if success:
        print("\n[SUCCESS] Test user setup completed!")
    else:
        print("\n[ERROR] Test user setup failed!")