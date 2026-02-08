import sys
import os
sys.path.insert(0, '.')

# Add debugging to see what's happening
print("Importing app...")
try:
    from backend.main import app
    print("App imported successfully")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()

print("Importing uvicorn...")
try:
    import uvicorn
    print("Uvicorn imported successfully")
except Exception as e:
    print(f"Error importing uvicorn: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    print("Starting server...")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()