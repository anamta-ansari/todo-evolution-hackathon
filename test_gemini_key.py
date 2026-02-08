import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[ERROR] GEMINI_API_KEY not set in environment")
    exit(1)

print(f"[SUCCESS] API key found: {api_key[:20]}...")

# Test API call with a valid model
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{"text": "Say hello"}]
    }],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 100
    }
}

try:
    response = httpx.post(url, json=payload, timeout=30.0)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("[SUCCESS] API call successful!")
        print(f"Sample response: {str(data)[:200]}...")
    elif response.status_code == 429:
        print("[ERROR] Rate limit exceeded")
        print(f"Response: {response.text}")
    elif response.status_code == 403:
        print("[ERROR] API key invalid or quota exceeded")
        print(f"Response: {response.text}")
    else:
        print(f"[ERROR] Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"[ERROR] Request failed: {e}")