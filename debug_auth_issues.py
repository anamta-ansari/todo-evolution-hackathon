#!/usr/bin/env python3
"""
Debug authentication issues
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"  # Adjust port as needed

def test_signup():
    print("=== Testing Signup ===")
    signup_url = f"{BASE_URL}/api/v1/auth/signup"
    
    # Test user data
    signup_data = {
        "email": f"test_{int(datetime.now().timestamp())}@example.com",
        "password": "SecurePassword123!"
    }
    
    print(f"Attempting to signup with: {signup_data}")
    
    try:
        response = requests.post(
            signup_url,
            json=signup_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Signup Response Status: {response.status_code}")
        print(f"Signup Response Body: {response.text}")
        
        if response.status_code == 201:
            print("[SUCCESS] Signup successful!")
            return response.json()
        elif response.status_code == 422:
            print("[ERROR] Signup failed with validation error (422)")
            return None
        else:
            print(f"[ERROR] Signup failed with status {response.status_code}")
            return None

    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection error - is the server running?")
        return None
    except Exception as e:
        print(f"[ERROR] Error during signup: {e}")
        return None


def test_signin(email="test@example.com", password="testpassword"):
    print("\n=== Testing Signin ===")
    signin_url = f"{BASE_URL}/api/v1/auth/signin"
    
    signin_data = {
        "email": email,
        "password": password
    }
    
    print(f"Attempting to signin with: {signin_data}")
    
    try:
        response = requests.post(
            signin_url,
            json=signin_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Signin Response Status: {response.status_code}")
        print(f"Signin Response Body: {response.text}")
        
        if response.status_code == 200:
            print("[SUCCESS] Signin successful!")
            return response.json()
        else:
            print(f"[ERROR] Signin failed with status {response.status_code}")
            return None

    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection error - is the server running?")
        return None
    except Exception as e:
        print(f"[ERROR] Error during signin: {e}")
        return None


def test_protected_endpoint(token):
    if not token:
        print("\n=== Skipping protected endpoint test (no token) ===")
        return
        
    print("\n=== Testing Protected Endpoint ===")
    protected_url = f"{BASE_URL}/api/v1/auth/me"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("Attempting to access protected endpoint (/auth/me)")
    
    try:
        response = requests.get(protected_url, headers=headers)
        
        print(f"Protected endpoint Response Status: {response.status_code}")
        print(f"Protected endpoint Response Body: {response.text}")
        
        if response.status_code == 200:
            print("[SUCCESS] Protected endpoint access successful!")
            return True
        else:
            print(f"[ERROR] Protected endpoint access failed with status {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection error - is the server running?")
        return False
    except Exception as e:
        print(f"[ERROR] Error accessing protected endpoint: {e}")
        return False


if __name__ == "__main__":
    print("Starting authentication debugging...")
    
    # First, try to sign in with an existing user
    existing_user_result = test_signin("test@example.com", "testpassword")
    
    if not existing_user_result:
        # If signin fails, try with the first test user we know exists
        existing_user_result = test_signin("testuser@example.com", "SecurePassword123!")
    
    # Extract token if available
    access_token = None
    if existing_user_result and "access_token" in existing_user_result:
        access_token = existing_user_result["access_token"]
    
    # Test protected endpoint
    test_protected_endpoint(access_token)
    
    # Try a new signup
    new_user_result = test_signup()
    
    print("\n=== Debugging Complete ===")