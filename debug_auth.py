import requests
import json
from jose import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Decode the token to see its contents
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6InRlc3R1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzY5NjIyNjQ4LCJ0b2tlbl90eXBlIjoiYWNjZXNzIn0.H-ijz7KoF3uJn4HBD6IU034Iv0g-VzPSrpzDbJL3prI"

# Get the secret from environment
secret = os.getenv("BETTER_AUTH_SECRET")

try:
    # Decode the token without verifying (just to see contents)
    decoded = jwt.decode(token, options={"verify_signature": False})
    print(f"Decoded token: {decoded}")
    print(f"user_id in token: {decoded.get('user_id')} (type: {type(decoded.get('user_id'))})")
except Exception as e:
    print(f"Error decoding token: {e}")

# Also test a simple authenticated request to a different endpoint
tasks_url = "http://localhost:8001/api/v1/tasks"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print(f"\nTesting access to tasks endpoint with the same token...")
response = requests.get(tasks_url, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")