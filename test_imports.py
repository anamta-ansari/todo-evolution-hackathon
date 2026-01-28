import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test importing each component individually to isolate the issue
print("Testing imports...")

try:
    from backend.db.session import engine
    print("OK Database engine imported")
except Exception as e:
    print(f"ERROR Database engine import failed: {e}")

try:
    from backend.models.user import User
    print("OK User model imported")
except Exception as e:
    print(f"ERROR User model import failed: {e}")

try:
    from backend.models.task import Task
    print("OK Task model imported")
except Exception as e:
    print(f"ERROR Task model import failed: {e}")

try:
    from backend.models.conversation import Conversation
    print("OK Conversation model imported")
except Exception as e:
    print(f"ERROR Conversation model import failed: {e}")

try:
    from backend.models.message import Message
    print("OK Message model imported")
except Exception as e:
    print(f"ERROR Message model import failed: {e}")

try:
    from backend.api.health import router as health_router
    print("OK Health router imported")
except Exception as e:
    print(f"ERROR Health router import failed: {e}")

try:
    from backend.api.auth import router as auth_router
    print("OK Auth router imported")
except Exception as e:
    print(f"ERROR Auth router import failed: {e}")

try:
    from backend.api.tasks import router as tasks_router
    print("OK Tasks router imported")
except Exception as e:
    print(f"ERROR Tasks router import failed: {e}")

try:
    from backend.routes.chat import router as chat_router
    print("OK Chat router imported")
except Exception as e:
    print(f"ERROR Chat router import failed: {e}")

print("\nAll imports completed!")