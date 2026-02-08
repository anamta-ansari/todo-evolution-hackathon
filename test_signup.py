import requests
import json

# Test signup
signup_url = "http://localhost:8001/api/v1/auth/signup"
signup_data = {
    "email": "testuser@example.com",
    "password": "SecurePassword123!"
}

print("Testing signup...")
response = requests.post(signup_url, json=signup_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 201:
    print("Signup successful!")
    response_data = response.json()
    token = response_data.get("access_token")
    user_id = response_data.get("user").get("id") if "user" in response_data else None
    print(f"Access Token: {token}")
    print(f"User ID: {user_id}")
else:
    print("Signup failed!")