"""
Updated test to run from root directory with proper path handling
"""

import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Now import the backend modules
from backend.db.session import engine
from backend.models.user import User
from backend.models.task import Task
from backend.mcp.tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool

from sqlmodel import Session

def test_mcp_tools_with_user():
    print("Testing MCP tools with proper user creation...")
    
    # First, create a test user
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.get(User, "test_user_123")
        if not existing_user:
            test_user = User(
                id="test_user_123",
                email="test@example.com",
                password_hash="hashed_password_here"
            )
            session.add(test_user)
            session.commit()
            print("Created test user")
        else:
            print("Test user already exists")

    # Now test the MCP tools
    # Test add_task
    try:
        result = add_task_tool(user_id="test_user_123", title="Test Task", description="Testing MCP")
        print("OK add_task:", result)
        assert result["status"] == "created"
        assert "task_id" in result
        print("OK add_task test passed")
    except Exception as e:
        print(f"X add_task test failed: {e}")
        return False

    # Test list_tasks
    try:
        tasks = list_tasks_tool(user_id="test_user_123", status="all")
        print("OK list_tasks:", tasks)
        assert isinstance(tasks, list)
        print("OK list_tasks test passed")
    except Exception as e:
        print(f"X list_tasks test failed: {e}")
        return False

    # Store task_id for next tests
    task_id = result["task_id"]

    # Test complete_task
    try:
        complete_result = complete_task_tool(user_id="test_user_123", task_id=task_id)
        print("OK complete_task:", complete_result)
        assert complete_result["status"] == "completed"
        print("OK complete_task test passed")
    except Exception as e:
        print(f"X complete_task test failed: {e}")
        return False

    # Test update_task
    try:
        update_result = update_task_tool(user_id="test_user_123", task_id=task_id, title="Updated Test Task")
        print("OK update_task:", update_result)
        assert update_result["status"] == "updated"
        print("OK update_task test passed")
    except Exception as e:
        print(f"X update_task test failed: {e}")
        return False

    # Test delete_task
    try:
        delete_result = delete_task_tool(user_id="test_user_123", task_id=task_id)
        print("OK delete_task:", delete_result)
        assert delete_result["status"] == "deleted"
        print("OK delete_task test passed")
    except Exception as e:
        print(f"X delete_task test failed: {e}")
        return False

    print("\nAll MCP tools working correctly!")
    return True

if __name__ == "__main__":
    success = test_mcp_tools_with_user()
    if success:
        print("\nAll MCP tool tests passed!")
    else:
        print("\nSome MCP tool tests failed!")
        sys.exit(1)