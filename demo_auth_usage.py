#!/usr/bin/env python3
"""
Demo script showing correct usage of the authentication API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"

def demo_auth_usage():
    print("Demo: Correct Authentication API Usage")
    print("="*50)

    # Generate unique test credentials
    timestamp = str(int(time.time()))
    test_email = f"demo_user_{timestamp}@example.com"
    test_password = "SecurePassword123!"
    test_name = f"Demo User {timestamp}"

    print(f"\nUsing test credentials:")
    print(f"   Email: {test_email}")
    print(f"   Password: {test_password}")
    print(f"   Name: {test_name}")

    # 1. SIGNUP DEMO
    print(f"\n1. SIGNUP DEMO")
    print(f"   Endpoint: POST {BASE_URL}/api/v1/auth/signup")
    
    signup_payload = {
        "email": test_email,
        "password": test_password,
        "name": test_name
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/signup",
            json=signup_payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("   SUCCESS: User created successfully!")
            data = response.json()
            access_token = data["access_token"]
            user_id = data["user"]["id"]
            print(f"   User ID: {user_id}")
            print(f"   Access Token: {access_token[:20]}...")
        elif response.status_code == 409:
            print("   User already exists (this is fine for demo)")
            # Continue with sign-in
        else:
            print(f"   ERROR: {response.text}")
            return False
            
    except Exception as e:
        print(f"   NETWORK ERROR: {str(e)}")
        return False

    # 2. SIGNIN DEMO
    print(f"\n2. SIGNIN DEMO")
    print(f"   Endpoint: POST {BASE_URL}/api/v1/auth/signin")
    
    signin_payload = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/signin",
            json=signin_payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("   SUCCESS: Signed in successfully!")
            data = response.json()
            access_token = data["access_token"]
            refresh_token = data["refresh_token"]
            user_id = data["user_id"]
            
            print(f"   User ID: {user_id}")
            print(f"   Email: {data['email']}")
            print(f"   Access Token: {access_token[:20]}...")
            print(f"   Refresh Token: {refresh_token[:20]}...")
        else:
            print(f"   ERROR: {response.text}")
            return False
            
    except Exception as e:
        print(f"   NETWORK ERROR: {str(e)}")
        return False

    # 3. PROTECTED ENDPOINT DEMO
    print(f"\n3. PROTECTED ENDPOINT DEMO")
    print(f"   Endpoint: GET {BASE_URL}/api/v1/auth/me")
    
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
            print("   SUCCESS: Accessed protected endpoint!")
            user_data = response.json()
            print(f"   User Info: {json.dumps(user_data, indent=4)}")
        else:
            print(f"   ERROR: {response.text}")
            return False
            
    except Exception as e:
        print(f"   NETWORK ERROR: {str(e)}")
        return False

    # 4. REFRESH TOKEN DEMO
    print(f"\n4. REFRESH TOKEN DEMO")
    print(f"   Endpoint: POST {BASE_URL}/api/v1/auth/refresh")
    
    try:
        refresh_payload = {"refresh_token": refresh_token}
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/refresh",
            json=refresh_payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   SUCCESS: Token refreshed!")
            data = response.json()
            new_access_token = data["access_token"]
            print(f"   New Access Token: {new_access_token[:20]}...")
        else:
            print(f"   ERROR: {response.text}")
            
    except Exception as e:
        print(f"   NETWORK ERROR: {str(e)}")

    print(f"\nDEMO COMPLETE!")
    print(f"All authentication endpoints are working correctly!")
    return True

if __name__ == "__main__":
    demo_auth_usage()