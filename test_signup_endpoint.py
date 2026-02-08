import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from backend.main import app
from fastapi.testclient import TestClient

# Create test client
client = TestClient(app)

# Test signup
print("Testing signup endpoint...")
response = client.post("/api/v1/auth/signup", json={
    "email": "testuser@example.com",
    "password": "password123"
})

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code != 201:
    print("Headers:", response.headers)
    try:
        print("JSON Response:", response.json())
    except:
        print("Non-JSON Response")