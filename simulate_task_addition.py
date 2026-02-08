import asyncio
import httpx
import json
import time

async def simulate_user_interaction():
    """
    Simulate a user trying to add tasks to see if rate limit issues are resolved
    """
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        try:
            print("Simulating user interaction to test rate limit fixes...")
            
            # First, check if the server is running
            try:
                response = await client.get("/health")
                print(f"Server health check: {response.status_code}")
            except Exception as e:
                print(f"Server not accessible: {e}")
                print("Please start the backend server first using 'python run_server.py'")
                return

            # Simulate adding multiple tasks with slight delays to avoid triggering rate limits
            tasks_to_add = ["buy milk", "buy groceries", "walk the dog", "call mom"]
            
            for i, task in enumerate(tasks_to_add):
                try:
                    # Note: This will fail without proper authentication, but we're testing
                    # if the rate limiting is working properly
                    response = await client.post(
                        f"/api/1/chat",
                        json={"message": f"add task {task}"},
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": "Bearer fake-token"  # Will fail auth but not rate limit
                        }
                    )
                    
                    print(f"Request {i+1}: Status {response.status_code} - {task}")
                    
                    # Small delay between requests to avoid overwhelming the server
                    await asyncio.sleep(0.5)
                    
                except httpx.TimeoutException:
                    print(f"Request {i+1} timed out - {task}")
                except Exception as e:
                    print(f"Request {i+1} error for '{task}': {e}")
                    
            print("\nTest completed. If you're still experiencing rate limit errors:")
            print("1. Make sure your API key is valid in the .env file")
            print("2. Start the backend server with 'python run_server.py'")
            print("3. Sign in to get a valid token, then retry with the actual token")
            
        except Exception as e:
            print(f"General error in simulation: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_user_interaction())