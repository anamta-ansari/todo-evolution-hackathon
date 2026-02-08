#!/usr/bin/env python3
"""
Test the specific endpoints that were failing based on the logs
"""

import requests
import json
from datetime import datetime

# Base URL for the API - using port 8000 as we confirmed it's running
BASE_URL = "http://127.0.0.1:8000"

def test_signin_with_correct_creds():
    print("=== Testing Signin with Correct Credentials ===")
    signin_url = f"{BASE_URL}/api/v1/auth/signin"
    
    # Using credentials that we know exist from our previous check
    signin_data = {
        "email": "testuser@example.com",
        "password": "SecurePassword123!"
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
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request error during signin: {e}")
        return None


def test_signup_with_new_user():
    print("\n=== Testing Signup with New User ===")
    signup_url = f"{BASE_URL}/api/v1/auth/signup"
    
    # Create unique email for new user
    timestamp = int(datetime.now().timestamp())
    signup_data = {
        "email": f"newuser_{timestamp}@example.com",
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
            print("This could mean the email format is invalid or password doesn't meet requirements")
            return None
        elif response.status_code == 409:
            print("[ERROR] Signup failed - user already exists (409 Conflict)")
            return None
        else:
            print(f"[ERROR] Signup failed with status {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request error during signup: {e}")
        return None


def test_preflight_request():
    print("\n=== Testing Preflight Request (OPTIONS) ===")
    options_url = f"{BASE_URL}/api/v1/auth/signup"
    
    print("Sending OPTIONS request to:", options_url)
    
    try:
        response = requests.options(
            options_url,
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        print(f"OPTIONS Response Status: {response.status_code}")
        print(f"OPTIONS Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("[SUCCESS] Preflight request successful!")
            return True
        else:
            print(f"[ERROR] Preflight request failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request error during OPTIONS: {e}")
        return False


def test_with_incorrect_password():
    print("\n=== Testing Signin with Incorrect Password ===")
    signin_url = f"{BASE_URL}/api/v1/auth/signin"
    
    # Using correct email but wrong password
    signin_data = {
        "email": "testuser@example.com",
        "password": "wrongpassword"
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
        
        if response.status_code == 401:
            print("[EXPECTED] Signin failed with 401 as expected for wrong password")
            return True
        else:
            print(f"[UNEXPECTED] Signin returned unexpected status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request error during signin: {e}")
        return False


if __name__ == "__main__":
    print("Testing specific endpoints that were reported as failing...")
    
    # Test preflight request (which succeeded in logs)
    test_preflight_request()
    
    # Test signup (which failed with 422 in logs)
    test_signup_with_new_user()
    
    # Test signin with incorrect credentials (which failed with 401 in logs)
    test_with_incorrect_password()
    
    # Test signin with correct credentials
    test_signin_with_correct_creds()
    
    print("\n=== Testing Complete ===")