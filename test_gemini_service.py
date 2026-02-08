import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Test if the Gemini service can be imported and initialized
try:
    from backend.services.gemini_chat import GeminiChatService
    
    print("Testing Gemini service initialization...")
    
    # Check if GEMINI_API_KEY is set in environment
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("⚠️  GEMINI_API_KEY not found in environment variables")
        print("Please set GEMINI_API_KEY in your .env file")
    else:
        print("✅ GEMINI_API_KEY found in environment")
    
    # Try to initialize the service
    try:
        service = GeminiChatService()
        print("✅ GeminiChatService initialized successfully")
        
        # Test the tools definition
        tools = service._get_gemini_tools()
        print(f"✅ Defined {len(tools)} tools for Gemini")
        
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        
    except Exception as e:
        print(f"❌ Error initializing GeminiChatService: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"❌ Error importing GeminiChatService: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting completed.")