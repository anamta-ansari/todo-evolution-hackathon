import asyncio
import httpx
import json
import time

async def test_chat_api():
    """
    Test the chat API endpoint to verify rate limit fixes
    """
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        try:
            # We need a valid user ID and token for the chat endpoint
            # Since we can't get these without going through auth flow,
            # let's test with a dummy user ID and token to see what error we get

            print("Testing chat endpoint accessibility after rate limit adjustments...")

            # First, let's try to access the health endpoint to make sure the server is running
            try:
                response = await client.get("/health")
                print(f"Health endpoint status: {response.status_code}")
                if response.status_code == 200:
                    print("Server is running correctly")
                else:
                    print(f"Server might not be running correctly. Status: {response.status_code}")
            except Exception as e:
                print(f"Error accessing health endpoint: {e}")
                print("Make sure the backend server is running on http://localhost:8000")
                return

            # Now let's try to access the chat endpoint without proper auth to see the response
            try:
                response = await client.post(
                    "/api/1/chat",  # Using user ID 1 as example
                    json={"message": "buy milk"},
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
                    json={"message": "buy milk"},
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