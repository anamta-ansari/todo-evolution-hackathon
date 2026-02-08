import sys
import os
import logging
sys.path.insert(0, '.')

# Set up logging to see errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Importing app...")
try:
    from backend.main import app
    print("App imported successfully")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Importing uvicorn...")
try:
    import uvicorn
    print("Uvicorn imported successfully")
except Exception as e:
    print(f"Error importing uvicorn: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    print("Starting server...")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, reload=False, log_level="info")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()