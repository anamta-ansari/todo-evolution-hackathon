import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test the functionality directly without starting the full server
from backend.mcp.tools import add_task_tool, list_tasks_tool
from backend.services.ai_agent import TodoAIAssistant
from sqlmodel import Session
from backend.db.session import engine

print("Testing backend functionality directly...")

# Test creating a task
try:
    result = add_task_tool(user_id="test_user_123", title="Buy milk", description="Get dairy milk from store")
    print(f"OK: Task created - {result}")
except Exception as e:
    print(f"ERROR: Failed to create task: {e}")

# Test listing tasks
try:
    tasks = list_tasks_tool(user_id="test_user_123", status="all")
    print(f"OK: Tasks retrieved - {len(tasks)} tasks found")
except Exception as e:
    print(f"ERROR: Failed to list tasks: {e}")

# Test the AI agent
try:
    ai_agent = TodoAIAssistant()
    response = ai_agent.process_message("Add a task to buy groceries", "test_user_123")
    print(f"OK: AI agent processed message - {response['response'][:50]}...")
except Exception as e:
    print(f"ERROR: AI agent failed: {e}")

print("\nDirect functionality test completed!")