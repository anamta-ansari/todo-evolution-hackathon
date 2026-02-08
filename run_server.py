import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("Starting server...")

# Import and run the app
from backend.main import app
import uvicorn

try:
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="debug")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()