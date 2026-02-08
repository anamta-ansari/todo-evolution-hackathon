import os
import asyncio
from backend.services.gemini_rest_client import GeminiRestClient

async def test_model_change():
    """
    Test that the model has been changed to gemini-2.5-flash to resolve rate limiting
    """
    # Initialize the client with the new model
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in environment variables")
        return
    
    # Test with the new default model (should be gemini-2.5-flash)
    client = GeminiRestClient(api_key=api_key)
    
    print(f"Initialized Gemini client with model: {client.model}")
    
    # Test a simple request to make sure the client works
    test_messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    
    try:
        # Make a simple request to test the connection
        result = await client.chat_with_tools(test_messages, user_id="test")
        print("Successfully connected to Gemini API with new model!")
        print(f"Response preview: {result['response'][:100]}...")
        
        # Close the client
        await client.close()
        
    except Exception as e:
        print(f"Error connecting to Gemini API: {e}")
        print("This could be due to an invalid API key or network issues.")

if __name__ == "__main__":
    asyncio.run(test_model_change())