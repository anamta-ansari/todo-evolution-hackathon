#!/usr/bin/env python3
"""Test server to debug authentication endpoints"""

import sys
import os
import traceback

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print("Importing modules...")

try:
    from backend.main import app
    print("Successfully imported app")
except Exception as e:
    print(f"Error importing app: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    import uvicorn
    print("Successfully imported uvicorn")
except ImportError as e:
    print(f"Error importing uvicorn: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("Starting server on port 8001...")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info", reload=False)
    except Exception as e:
        print(f"Server failed to start: {e}")
        traceback.print_exc()
        sys.exit(1)