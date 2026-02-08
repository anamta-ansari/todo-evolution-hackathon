import requests
import json

# Test login
login_url = "http://localhost:8001/api/v1/auth/signin"
login_data = {
    "email": "testuser@example.com",
    "password": "SecurePassword123!"
}

print("Testing login...")
response = requests.post(login_url, json=login_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    print("Login successful!")
    response_data = response.json()
    token = response_data.get("access_token")
    user_id = response_data.get("user_id")
    print(f"Access Token: {token}")
    print(f"User ID: {user_id}")
else:
    print("Login failed!")