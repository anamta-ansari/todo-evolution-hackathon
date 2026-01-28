from mcp.server import Server
from mcp.server.stdio import stdio_server
from backend.mcp.tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
)
import json

# Initialize MCP server
app = Server("todo-mcp-server")


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls from AI agent"""
    
    if name == "add_task":
        return add_task_tool(
            user_id=arguments["user_id"],
            title=arguments["title"],
            description=arguments.get("description", "")
        )
    
    elif name == "list_tasks":
        return list_tasks_tool(
            user_id=arguments["user_id"],
            status=arguments.get("status", "all")
        )
    
    elif name == "complete_task":
        return complete_task_tool(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"]
        )
    
    elif name == "delete_task":
        return delete_task_tool(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"]
        )
    
    elif name == "update_task":
        return update_task_tool(
            user_id=arguments["user_id"],
            task_id=arguments["task_id"],
            title=arguments.get("title"),
            description=arguments.get("description")
        )
    
    else:
        raise ValueError(f"Unknown tool: {name}")


# List available tools
@app.list_tools()
async def list_tools():
    return [
        {
            "name": "add_task",
            "description": "Create a new task",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        },
        {
            "name": "list_tasks",
            "description": "List user's tasks",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        },
        {
            "name": "complete_task",
            "description": "Mark task as complete",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "delete_task",
            "description": "Delete a task",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "update_task",
            "description": "Update task details",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    ]