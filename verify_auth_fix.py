#!/usr/bin/env python3
"""
Comprehensive verification script to test authentication endpoints
"""
import requests
import json
import time
import sys
import os

# Add the current directory to the Python path to resolve import issues
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Base URL for the API
BASE_URL = "http://localhost:8001"

def test_signup_and_signin():
    """Test the complete authentication flow"""
    
    # Generate unique test credentials
    timestamp = str(int(time.time()))
    test_email = f"testuser_{timestamp}@example.com"
    test_password = "SecurePassword123!"
    
    print("="*60)
    print("COMPREHENSIVE AUTHENTICATION VERIFICATION")
    print("="*60)
    
    print(f"\nUsing test credentials:")
    print(f"Email: {test_email}")
    print(f"Password: {test_password}")
    
    # Test 1: Signup
    print(f"\n1. Testing SIGNUP endpoint...")
    print(f"   POST {BASE_URL}/api/v1/auth/signup")
    
    signup_payload = {
        "email": test_email,
        "password": test_password,
        "name": f"Test User {timestamp}"  # Adding name as it's optional but might be expected
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/signup",
            json=signup_payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("   ✅ SIGNUP SUCCESSFUL!")
            signup_data = response.json()
            
            # Extract tokens and user info
            access_token = signup_data.get("access_token")
            refresh_token = signup_data.get("refresh_token")
            user_info = signup_data.get("user")
            
            print(f"   User ID: {user_info.get('id')}")
            print(f"   Access Token: {access_token[:20]}..." if access_token else "   No access token")
            print(f"   Refresh Token: {refresh_token[:20]}..." if refresh_token else "   No refresh token")
            
        elif response.status_code == 409:
            print("   ⚠️  User already exists (this is OK for testing)")
            # Continue with sign-in using the existing user
            pass
        else:
            print(f"   ❌ SIGNUP FAILED: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to server at {BASE_URL}. Please make sure the server is running.")
        return False
    except Exception as e:
        print(f"   ❌ Error during signup: {str(e)}")
        return False
    
    # Determine the email to use for sign-in (either new or existing)
    signin_email = test_email
    if response.status_code == 409:
        # If user already existed, use the same email but with a slight delay to ensure DB is ready
        time.sleep(1)
    
    # Test 2: Signin
    print(f"\n2. Testing SIGNIN endpoint...")
    print(f"   POST {BASE_URL}/api/v1/auth/signin")
    
    signin_payload = {
        "email": signin_email,
        "password": test_password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/signin",
            json=signin_payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ SIGNIN SUCCESSFUL!")
            signin_data = response.json()
            
            access_token = signin_data.get("access_token")
            refresh_token = signin_data.get("refresh_token")
            
            print(f"   User ID: {signin_data.get('user_id')}")
            print(f"   Email: {signin_data.get('email')}")
            print(f"   Access Token: {access_token[:20]}..." if access_token else "   No access token")
            print(f"   Refresh Token: {refresh_token[:20]}..." if refresh_token else "   No refresh token")
            
        else:
            print(f"   ❌ SIGNIN FAILED: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to server at {BASE_URL}. Please make sure the server is running.")
        return False
    except Exception as e:
        print(f"   ❌ Error during signin: {str(e)}")
        return False
    
    # Test 3: Access protected endpoint
    print(f"\n3. Testing PROTECTED endpoint (/me)...")
    print(f"   GET {BASE_URL}/api/v1/auth/me")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/auth/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ PROTECTED ENDPOINT ACCESS SUCCESSFUL!")
            user_data = response.json()
            print(f"   Retrieved User: {user_data}")
        else:
            print(f"   ❌ PROTECTED ENDPOINT FAILED: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to server at {BASE_URL}. Please make sure the server is running.")
        return False
    except Exception as e:
        print(f"   ❌ Error accessing protected endpoint: {str(e)}")
        return False
    
    print(f"\n{'='*60}")
    print("ALL AUTHENTICATION TESTS PASSED! ✅")
    print("Authentication system is working correctly.")
    print(f"{'='*60}")
    
    return True

def check_server_status():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Server is not running at {BASE_URL}")
        print("   Please start the server with: python -m uvicorn backend.main:app --host 0.0.0.0 --port 8001")
        return False

def main():
    print("Verifying authentication system...")
    
    if not check_server_status():
        print("\nServer is not running. Please start the server before running this verification.")
        return False
    
    return test_signup_and_signin()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Authentication verification failed.")
        sys.exit(1)
    else:
        print("\n✅ Authentication verification completed successfully.")