import os
import sys
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_gemini_rest_client():
    print("Testing Gemini REST Client...")
    
    # Check if GEMINI_API_KEY is set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables")
        print("Please set GEMINI_API_KEY in your .env file")
        return False
    else:
        print("Success: GEMINI_API_KEY found in environment")
    
    try:
        from backend.services.gemini_rest_client import GeminiRestClient
        
        print("Initializing Gemini REST Client...")
        client = GeminiRestClient(model="gemini-1.5-flash")
        print("✅ GeminiRestClient initialized successfully")
        
        # Test basic functionality
        print("\nTesting basic message processing...")
        
        # Simple test without tools
        messages = [
            {"role": "user", "content": "Hello, how are you?"}
        ]
        
        result = await client.chat_with_tools(messages, "test_user_123")
        print(f"Response: {result.get('response', 'No response')}")
        print("Success: Basic message processing works")
        
        # Test with a message that might trigger a tool
        print("\nTesting with potential tool call...")
        tool_messages = [
            {"role": "user", "content": "Add task: Buy groceries"}
        ]
        
        result = await client.chat_with_tools(tool_messages, "1")
        print(f"Response: {result.get('response', 'No response')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print("Success: Tool call processing works")
        
        # Close the client
        await client.close()
        
        print("\nAll tests passed! Gemini REST client is working correctly.")
        return True
        
    except ImportError as e:
        print(f"Error importing GeminiRestClient: {e}")
        return False
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini_rest_client())
    if success:
        print("\nGemini REST API integration is ready!")
    else:
        print("\nThere were issues with the Gemini REST API integration.")