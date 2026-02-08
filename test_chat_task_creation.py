import requests
import json

# Get the access token from login
login_url = "http://localhost:8000/api/v1/auth/signin"
login_data = {
    "email": "testuser@example.com",
    "password": "SecurePassword123!"
}

response = requests.post(login_url, json=login_data)
access_token = response.json()["access_token"]
user_id = response.json()["user_id"]

print(f"Using token: {access_token}")
print(f"User ID: {user_id}")

# Test AI chat functionality for task creation
chat_url = f"http://localhost:8000/api/{user_id}/chat"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

chat_data = {
    "message": "Add a task to buy groceries"
}

print("\nTesting AI chat for task creation...")
response = requests.post(chat_url, json=chat_data, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    print("Task creation via AI chat successful!")
    response_data = response.json()
    conversation_id = response_data.get("conversation_id")
    ai_response = response_data.get("response")
    print(f"Conversation ID: {conversation_id}")
    print(f"AI Response: {ai_response}")
else:
    print("Task creation via AI chat failed!")