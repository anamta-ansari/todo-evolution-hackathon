import requests
import json

# Simple test of signin endpoint
BASE_URL = "http://localhost:8001"  # Server runs on port 8001

print("Testing signin endpoint:")

signin_data = {
    "email": "testuser@example.com",
    "password": "SecurePassword123!"  # Using the password from the previous test
}

try:
    response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
    print(f"Signin response status: {response.status_code}")
    print(f"Response text: {response.text}")
    
    if response.status_code == 200:
        print("Signin successful!")
        signin_response = response.json()
        access_token = signin_response['access_token']
        refresh_token = signin_response['refresh_token']
        print(f"  - Access token length: {len(access_token)}")
        print(f"  - Refresh token length: {len(refresh_token)}")
    else:
        print("Signin failed!")
        
except Exception as e:
    print(f"Signin error: {str(e)}")