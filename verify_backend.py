import asyncio
import httpx
import json

async def test_backend():
    """
    Test the backend API endpoints to ensure they're working properly
    """
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
        try:
            # Test the root endpoint
            print("Testing root endpoint...")
            response = await client.get("/")
            print(f"Root endpoint status: {response.status_code}")
            print(f"Root endpoint response: {response.json()}")
            
            # Test the health endpoint
            print("\nTesting health endpoint...")
            health_response = await client.get("/health")
            print(f"Health endpoint status: {health_response.status_code}")
            print(f"Health endpoint response: {health_response.json()}")
            
            print("\nBackend server is running and accessible!")
            print("Make sure to start the backend server with:")
            print("cd backend && python -m uvicorn main:app --reload --port 8000")
            
        except Exception as e:
            print(f"\nError connecting to backend server: {e}")
            print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(test_backend())