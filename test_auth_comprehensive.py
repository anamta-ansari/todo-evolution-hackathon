import requests
import json

# Comprehensive test of auth endpoints
BASE_URL = "http://localhost:8001"  # Server runs on port 8001

def test_auth_comprehensive():
    print("Comprehensive auth test...")
    
    # Clean up any existing test user
    print("\n1. Testing signup endpoint:")
    signup_data = {
        "email": "comprehensive_test@example.com",
        "password": "testpass123",
        "name": "Comprehensive Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
        print(f"Signup response status: {response.status_code}")
        if response.status_code == 201:
            print("✓ Signup successful!")
            signup_response = response.json()
            access_token = signup_response['access_token']
            refresh_token = signup_response['refresh_token']
            user_id = signup_response['user']['id']
            print(f"  - User ID: {user_id}")
            print(f"  - Access token length: {len(access_token)}")
            print(f"  - Refresh token length: {len(refresh_token)}")
        else:
            print(f"✗ Signup failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Signup error: {str(e)}")
        return False
    
    print("\n2. Testing duplicate signup (should fail):")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
        print(f"Duplicate signup response status: {response.status_code}")
        if response.status_code == 409:  # Conflict
            print("✓ Duplicate signup correctly rejected!")
        else:
            print(f"✗ Duplicate signup should have failed but got: {response.status_code}")
    except Exception as e:
        print(f"Duplicate signup error: {str(e)}")
    
    print("\n3. Testing signin endpoint:")
    signin_data = {
        "email": "comprehensive_test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
        print(f"Signin response status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Signin successful!")
            signin_response = response.json()
            new_access_token = signin_response['access_token']
            new_refresh_token = signin_response['refresh_token']
            print(f"  - Access token length: {len(new_access_token)}")
            print(f"  - Refresh token length: {len(new_refresh_token)}")
        else:
            print(f"✗ Signin failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Signin error: {str(e)}")
        return False
    
    print("\n4. Testing protected /me endpoint:")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
        print(f"Protected endpoint response status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Protected endpoint access successful!")
            user_data = response.json()
            print(f"  - User ID: {user_data['id']}")
            print(f"  - User email: {user_data['email']}")
        else:
            print(f"✗ Protected endpoint failed: {response.text}")
    except Exception as e:
        print(f"✗ Protected endpoint error: {str(e)}")
    
    print("\n5. Testing wrong password signin:")
    wrong_signin_data = {
        "email": "comprehensive_test@example.com",
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=wrong_signin_data)
        print(f"Wrong password signin response status: {response.status_code}")
        if response.status_code == 401:
            print("✓ Wrong password correctly rejected!")
        else:
            print(f"✗ Wrong password should have been rejected but got: {response.status_code}")
    except Exception as e:
        print(f"Wrong password test error: {str(e)}")
    
    print("\n6. Testing non-existent user signin:")
    nonexistent_signin_data = {
        "email": "nonexistent@example.com",
        "password": "somepassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=nonexistent_signin_data)
        print(f"Non-existent user signin response status: {response.status_code}")
        if response.status_code == 401:
            print("✓ Non-existent user correctly rejected!")
        else:
            print(f"✗ Non-existent user should have been rejected but got: {response.status_code}")
    except Exception as e:
        print(f"Non-existent user test error: {str(e)}")
    
    print("\n✓ All auth tests completed successfully!")
    return True

if __name__ == "__main__":
    test_auth_comprehensive()