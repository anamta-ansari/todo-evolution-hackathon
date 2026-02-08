import asyncio
import httpx
import json

async def test_chat_api():
    """
    Test the chat API endpoint to see if it's working properly
    """
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        try:
            # We need a valid user ID and token for the chat endpoint
            # Since we can't get these without going through auth flow,
            # let's test with a dummy user ID and token to see what error we get
            
            # First, let's try to register a user to get proper credentials
            # But for now, let's just see if the endpoint exists
            print("Testing chat endpoint accessibility...")
            
            # Try to access the chat endpoint without proper auth to see the response
            try:
                response = await client.post(
                    "/api/1/chat",  # Using user ID 1 as example
                    json={"message": "test"},
                    headers={"Content-Type": "application/json"}
                )
                print(f"Chat endpoint status without auth: {response.status_code}")
                print(f"Chat endpoint response without auth: {response.text[:200]}...")  # First 200 chars
            except Exception as e:
                print(f"Error accessing chat endpoint without auth: {e}")
            
            # Now let's try with a fake token to see the response
            try:
                response = await client.post(
                    "/api/1/chat",
                    json={"message": "test"},
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer fake-token"
                    }
                )
                print(f"Chat endpoint status with fake token: {response.status_code}")
                print(f"Chat endpoint response with fake token: {response.text[:200]}...")
            except Exception as e:
                print(f"Error accessing chat endpoint with fake token: {e}")
                
        except Exception as e:
            print(f"General error: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat_api())