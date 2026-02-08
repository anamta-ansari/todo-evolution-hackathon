import requests
import json

# Test the current auth endpoints
BASE_URL = "http://localhost:8001"  # Server runs on port 8001

def test_auth_endpoints():
    print("Testing current auth endpoints...")
    
    # Test signup
    print("\n1. Testing signup endpoint:")
    signup_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
        print(f"Signup response status: {response.status_code}")
        print(f"Signup response: {response.text}")
    except Exception as e:
        print(f"Signup error: {str(e)}")
    
    # Test signin
    print("\n2. Testing signin endpoint:")
    signin_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
        print(f"Signin response status: {response.status_code}")
        print(f"Signin response: {response.text}")
    except Exception as e:
        print(f"Signin error: {str(e)}")

if __name__ == "__main__":
    test_auth_endpoints()