import requests
import json

# Test with the same credentials that were failing before
BASE_URL = "http://localhost:8001"

print("Testing with sample credentials...")

# Test signup first
signup_data = {
    "email": "user@example.com",
    "password": "password123",
    "name": "Test User"
}

print("\nTesting signup:")
try:
    response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
    print(f"Signup status: {response.status_code}")
    print(f"Signup response: {response.text}")
except Exception as e:
    print(f"Signup error: {str(e)}")

# Test signin with the same credentials
signin_data = {
    "email": "user@example.com",
    "password": "password123"
}

print("\nTesting signin:")
try:
    response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
    print(f"Signin status: {response.status_code}")
    print(f"Signin response: {response.text}")
except Exception as e:
    print(f"Signin error: {str(e)}")