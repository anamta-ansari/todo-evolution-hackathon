import requests
import json

# Test the current auth endpoints
BASE_URL = "http://localhost:8001"  # Server runs on port 8001

def test_auth_endpoints_detailed():
    print("Testing current auth endpoints in detail...")
    
    # Test signup
    print("\n1. Testing signup endpoint:")
    signup_data = {
        "email": "test@example.com",
        "password": "shortpass123",  # Using a shorter password to avoid bcrypt issues
        "name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
        print(f"Signup response status: {response.status_code}")
        print(f"Signup response headers: {response.headers}")
        print(f"Signup response: {response.text}")
        
        if response.status_code == 201:
            print("Signup successful!")
            response_data = response.json()
            access_token = response_data.get('access_token')
            refresh_token = response_data.get('refresh_token')
            print(f"Access token: {access_token[:20] if access_token else 'None'}...")
            print(f"Refresh token: {refresh_token[:20] if refresh_token else 'None'}...")
        elif response.status_code == 422:
            print("Validation error - checking request body...")
        elif response.status_code == 500:
            print("Internal server error - this indicates a bug in the server code")
    except Exception as e:
        print(f"Signup error: {str(e)}")
    
    # Test signin
    print("\n2. Testing signin endpoint:")
    signin_data = {
        "email": "test@example.com",
        "password": "shortpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
        print(f"Signin response status: {response.status_code}")
        print(f"Signin response headers: {response.headers}")
        print(f"Signin response: {response.text}")
        
        if response.status_code == 200:
            print("Signin successful!")
        elif response.status_code == 401:
            print("Unauthorized - user doesn't exist or wrong password")
        elif response.status_code == 422:
            print("Validation error - checking request body...")
        elif response.status_code == 500:
            print("Internal server error - this indicates a bug in the server code")
    except Exception as e:
        print(f"Signin error: {str(e)}")

if __name__ == "__main__":
    test_auth_endpoints_detailed()