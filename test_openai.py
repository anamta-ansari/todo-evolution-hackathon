import os
from openai import OpenAI

print("Testing OpenAI API...")
print(f"API Key (first 10 chars): {os.getenv('OPENAI_API_KEY', '')[:10]}")

try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print("✅ OpenAI API is working!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ OpenAI API error: {e}")