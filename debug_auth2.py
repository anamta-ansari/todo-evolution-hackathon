import requests
import json

# Get a fresh token
login_url = "http://localhost:8001/api/v1/auth/signin"
login_data = {
    "email": "testuser@example.com",
    "password": "SecurePassword123!"
}

response = requests.post(login_url, json=login_data)
access_token = response.json()["access_token"]
user_id = response.json()["user_id"]

print(f"Fetched token: {access_token}")
print(f"User ID: {user_id} (type: {type(user_id)})")

# Test accessing a protected endpoint (tasks)
tasks_url = "http://localhost:8001/api/v1/tasks"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

print(f"\nTesting access to tasks endpoint...")
response = requests.get(tasks_url, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# Now test the chat endpoint with the correct user ID from the token
chat_url = f"http://localhost:8001/api/{user_id}/chat"  # Use the user_id from the response
print(f"\nTesting chat endpoint: {chat_url}")
chat_data = {
    "message": "Add a task to buy groceries"
}

response = requests.post(chat_url, json=chat_data, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")