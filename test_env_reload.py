import os
import sys
import importlib

# Force reload of environment variables
os.environ.clear()
# Reload the environment
from dotenv import load_dotenv
load_dotenv('G:/TODO-FULL-STACK-WEB/.env')

# Now import the modules
sys.path.insert(0, 'G:/TODO-FULL-STACK-WEB')
sys.path.insert(0, 'G:/TODO-FULL-STACK-WEB/backend')

# Import and test the tools
from backend.mcp.tools import add_task_tool, list_tasks_tool

print("Testing MCP tools after reloading environment...")

# Test creating a task
try:
    result = add_task_tool(user_id="test_user_123", title="Buy milk", description="Get dairy milk from store")
    print(f"OK: Task created - {result}")
except Exception as e:
    print(f"ERROR: Failed to create task: {e}")
    import traceback
    traceback.print_exc()

# Test listing tasks
try:
    tasks = list_tasks_tool(user_id="test_user_123", status="all")
    print(f"OK: Tasks retrieved - {len(tasks)} tasks found")
except Exception as e:
    print(f"ERROR: Failed to list tasks: {e}")
    import traceback
    traceback.print_exc()

print("\nEnvironment reload test completed!")