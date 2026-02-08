#!/usr/bin/env python3
"""
Test the actual signup endpoint with detailed debugging
"""
import requests
import json

# Test signup with detailed debugging
signup_url = "http://localhost:8001/api/v1/auth/signup"
signup_data = {
    "email": "testuser@example.com",
    "password": "SecurePassword123!",
    "name": "Test User"
}

print("Testing signup with detailed data...")
print(f"Sending data: {json.dumps(signup_data, indent=2)}")

try:
    response = requests.post(signup_url, json=signup_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 201:
        print("[OK] Signup successful!")
        try:
            response_data = response.json()
            token = response_data.get("access_token")
            user_id = response_data.get("user", {}).get("id")
            print(f"Access Token: {token}")
            print(f"User ID: {user_id}")
        except:
            print("Could not parse JSON response")
    else:
        print("[ERROR] Signup failed!")
        
except requests.exceptions.ConnectionError:
    print("[ERROR] Could not connect to server. Is it running?")
except Exception as e:
    print(f"[ERROR] Exception occurred: {str(e)}")