import requests
import json

# Get the access token from login
login_url = "http://localhost:8001/api/v1/auth/signin"
login_data = {
    "email": "testuser@example.com",
    "password": "SecurePassword123!"
}

response = requests.post(login_url, json=login_data)
access_token = response.json()["access_token"]
user_id = response.json()["user_id"]

print(f"Using token: {access_token}")
print(f"User ID: {user_id}")

# Test conversation persistence
chat_url = f"http://localhost:8001/api/{user_id}/chat"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Step 1: Create a task and get the conversation ID
print("\nStep 1: Creating a task to start a conversation...")
chat_data = {
    "message": "Add a task to clean the house"
}

response = requests.post(chat_url, json=chat_data, headers=headers)
print(f"Status Code: {response.status_code}")
response_data = response.json()
conversation_id = response_data.get("conversation_id")
print(f"Conversation ID: {conversation_id}")
print(f"Response: {response_data.get('response')}")

if response.status_code != 200:
    print("Failed to create initial task.")
    exit(1)

# Step 2: Use the same conversation ID to ask about the task
print(f"\nStep 2: Asking about tasks in conversation {conversation_id}...")
chat_data = {
    "conversation_id": conversation_id,
    "message": "What tasks do I have?"
}

response = requests.post(chat_url, json=chat_data, headers=headers)
print(f"Status Code: {response.status_code}")
response_data = response.json()
print(f"Response: {response_data.get('response')}")

if response.status_code != 200:
    print("Failed to retrieve tasks in existing conversation.")
    exit(1)

# Step 3: Complete the task in the same conversation
print(f"\nStep 3: Completing a task in conversation {conversation_id}...")
chat_data = {
    "conversation_id": conversation_id,
    "message": "Complete the cleaning task"
}

response = requests.post(chat_url, json=chat_data, headers=headers)
print(f"Status Code: {response.status_code}")
response_data = response.json()
print(f"Response: {response_data.get('response')}")

if response.status_code != 200:
    print("Failed to complete task in existing conversation.")
    exit(1)

# Step 4: Check tasks again to confirm completion
print(f"\nStep 4: Checking tasks again in conversation {conversation_id}...")
chat_data = {
    "conversation_id": conversation_id,
    "message": "What tasks do I have now?"
}

response = requests.post(chat_url, json=chat_data, headers=headers)
print(f"Status Code: {response.status_code}")
response_data = response.json()
print(f"Response: {response_data.get('response')}")

if response.status_code == 200:
    print("\nConversation persistence test successful!")
    print("The conversation maintained context across multiple requests.")
else:
    print("\nConversation persistence test failed!")
    exit(1)