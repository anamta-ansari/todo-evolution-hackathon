#!/usr/bin/env python3
"""
Test script to verify signup and login functionality
"""
import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8001"

import time

def test_signup_and_login():
    # Test data - use timestamp to ensure uniqueness
    timestamp = str(int(time.time()))
    test_email = f"testuser_{timestamp}@example.com"
    test_password = "securepassword123"
    
    print("Testing signup...")
    
    # Signup request
    signup_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
        print(f"Signup response status: {response.status_code}")
        
        if response.status_code == 201:
            print("Signup successful!")
            signup_response = response.json()
            print(f"User ID: {signup_response['user']['id']}")
            print(f"Access Token: {signup_response['access_token'][:20]}...")
            print(f"Refresh Token: {signup_response['refresh_token'][:20]}...")
            
            # Extract tokens for login test
            access_token = signup_response['access_token']
            
            print("\nTesting login...")
            
            # Login request
            login_data = {
                "email": test_email,
                "password": test_password
            }
            
            response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=login_data)
            print(f"Login response status: {response.status_code}")
            
            if response.status_code == 200:
                print("Login successful!")
                login_response = response.json()
                print(f"User ID: {login_response['user_id']}")
                print(f"Email: {login_response['email']}")
                print(f"Access Token: {login_response['access_token'][:20]}...")
                
                # Test protected route
                print("\nTesting protected route (/me)...")
                headers = {
                    "Authorization": f"Bearer {access_token}"
                }
                
                response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
                print(f"Protected route response status: {response.status_code}")
                
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"Protected route success! User data: {user_data}")
                    print("All tests passed!")
                else:
                    print(f"Protected route failed: {response.text}")
                    
            else:
                print(f"Login failed: {response.text}")
                
        elif response.status_code == 409:
            print("User already exists, proceeding to login test...")
            
            # Try login with existing user
            login_data = {
                "email": test_email,
                "password": test_password
            }
            
            response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=login_data)
            print(f"Login response status: {response.status_code}")
            
            if response.status_code == 200:
                print("Login successful!")
                login_response = response.json()
                print(f"User ID: {login_response['user_id']}")
                print(f"Email: {login_response['email']}")
                
                # Extract token for protected route test
                access_token = login_response['access_token']
                
                # Test protected route
                print("\nTesting protected route (/me)...")
                headers = {
                    "Authorization": f"Bearer {access_token}"
                }
                
                response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
                print(f"Protected route response status: {response.status_code}")
                
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"Protected route success! User data: {user_data}")
                    print("All tests passed!")
                else:
                    print(f"Protected route failed: {response.text}")
            else:
                print(f"Login failed: {response.text}")
        else:
            print(f"Signup failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"Cannot connect to server at {BASE_URL}. Please make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_signup_and_login()