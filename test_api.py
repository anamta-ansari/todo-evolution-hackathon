import asyncio
import httpx
import json

async def test_api():
    """
    Test the API endpoint to see if it's accessible and how it responds
    """
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        # First, we need to authenticate to get a user ID and token
        # For now, let's just test if the server is responding
        try:
            # Test the root endpoint
            response = await client.get("/")
            print(f"Root endpoint status: {response.status_code}")
            print(f"Root endpoint response: {response.json()}")
            
            # Test a health check endpoint if available
            try:
                health_response = await client.get("/health")
                print(f"Health endpoint status: {health_response.status_code}")
                print(f"Health endpoint response: {health_response.json()}")
            except Exception as e:
                print(f"Health endpoint error (this is OK if not implemented): {e}")
                
        except Exception as e:
            print(f"Error connecting to server: {e}")
            print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(test_api())