import asyncio
import os
from backend.services.gemini_rest_client import GeminiRestClient

async def test_auto_user_detection():
    """
    Test that the auto-user detection is working correctly
    """
    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in environment variables")
        return
    
    # Initialize the client
    client = GeminiRestClient(api_key=api_key)
    
    print(f"Initialized Gemini client with model: {client.model}")
    
    # Test with a sample message and user ID
    test_messages = [
        {"role": "user", "content": "Add a task to buy groceries"}
    ]
    user_id = "test_user_123"
    
    try:
        print(f"Testing chat with tools for user: {user_id}")
        
        # Make a request to test the system
        result = await client.chat_with_tools(test_messages, user_id)
        
        print("Response received successfully!")
        print(f"Response: {result['response'][:200]}...")
        print(f"Tool calls made: {len(result['tool_calls'])}")
        
        if result['tool_calls']:
            for tool_call in result['tool_calls']:
                print(f"Tool: {tool_call['tool']}")
                print(f"Parameters: {tool_call['parameters']}")
                
        # Close the client
        await client.close()
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_auto_user_detection())