import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Add the backend directory to the path
backend_dir = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, backend_dir)

from backend.mcp.tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool

def test_mcp_tools():
    print("Testing MCP tools...")
    
    # Test add_task
    try:
        result = add_task_tool(user_id="test_user_123", title="Test Task", description="Testing MCP")
        print("✅ add_task:", result)
        assert result["status"] == "created"
        assert "task_id" in result
        print("✅ add_task test passed")
    except Exception as e:
        print(f"X add_task test failed: {e}")
        return False

    # Test list_tasks
    try:
        tasks = list_tasks_tool(user_id="test_user_123", status="all")
        print("✅ list_tasks:", tasks)
        assert isinstance(tasks, list)
        print("✅ list_tasks test passed")
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
    success = test_mcp_tools()
    if success:
        print("\nAll MCP tool tests passed!")
    else:
        print("\nSome MCP tool tests failed!")
        sys.exit(1)