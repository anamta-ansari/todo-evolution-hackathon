import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.mcp.tools import add_task_tool

print("Testing add_task MCP tool directly...")

try:
    # Test with a sample user_id and task
    result = add_task_tool(
        user_id="1",  # Using integer as string since the function expects a string
        title="Buy groceries",
        description="Milk, bread, eggs"
    )
    print(f"✅ MCP tool works: {result}")
except Exception as e:
    print(f"❌ MCP tool error: {e}")
    import traceback
    traceback.print_exc()