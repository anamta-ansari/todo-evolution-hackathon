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

# List available models
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = httpx.get(url, timeout=30.0)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("[SUCCESS] Models listed successfully!")
        print("Available models:")
        for model in data.get('models', []):
            name = model.get('name')
            if 'generateContent' in str(model.get('supportedGenerationMethods', [])):
                print(f"  - {name}")
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