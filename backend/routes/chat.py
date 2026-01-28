from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from backend.db.session import get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.dependencies.auth import verify_token as base_verify_token
from backend.models.conversation import Conversation
from backend.models.message import Message, MessageRole
from openai import OpenAI
import os
import json

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Verify the JWT token and return the payload"""
    return base_verify_token(credentials.credentials, expected_token_type="access")


class ChatRequest(BaseModel):
    conversation_id: int = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list = []


def call_mcp_tool(tool_name: str, tool_args: dict):
    """Helper function to call MCP tools"""
    # This is a simplified version - in a real implementation, 
    # you would connect to the MCP server properly
    import asyncio
    
    async def call_async():
        from backend.mcp.server import call_tool
        return await call_tool(tool_name, tool_args)
    
    # For now, we'll call the functions directly
    if tool_name == "add_task":
        from backend.mcp.tools import add_task_tool
        return add_task_tool(**tool_args)
    elif tool_name == "list_tasks":
        from backend.mcp.tools import list_tasks_tool
        return list_tasks_tool(**tool_args)
    elif tool_name == "complete_task":
        from backend.mcp.tools import complete_task_tool
        return complete_task_tool(**tool_args)
    elif tool_name == "delete_task":
        from backend.mcp.tools import delete_task_tool
        return delete_task_tool(**tool_args)
    elif tool_name == "update_task":
        from backend.mcp.tools import update_task_tool
        return update_task_tool(**tool_args)
    else:
        return {"error": f"Unknown tool: {tool_name}"}


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session),
    token_payload: dict = Depends(verify_token)
):
    # Extract user_id from token payload
    token_user_id = token_payload.get("user_id")
    # Verify user_id matches token
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Get or create conversation
    conversation = None
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
    
    # Fetch message history
    history_query = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at)
    history = session.exec(history_query).all()
    
    # Store user message
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=request.message
    )
    session.add(user_message)
    session.commit()
    
    # Build messages for OpenAI
    messages = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history
    ]
    messages.append({"role": "user", "content": request.message})
    
    # Prepare tools for OpenAI
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "title": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List user's tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "task_id": {"type": "integer"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "task_id": {"type": "integer"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task details",
                "parameters": {
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
        }
    ]
    
    # Call OpenAI with tools
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using gpt-3.5-turbo for testing
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful task management assistant. 
                    You help users manage their todo list through natural language.
                    
                    Available tools:
                    - add_task: Create new tasks
                    - list_tasks: Show tasks (all/pending/completed)
                    - complete_task: Mark tasks as done
                    - delete_task: Remove tasks
                    - update_task: Modify task details
                    
                    Always confirm actions clearly and be helpful."""
                }
            ] + messages,
            tools=tools,
            tool_choice="auto"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
    
    # Extract response
    assistant_message_content = response.choices[0].message.content or ""
    tool_calls_info = []
    
    if response.choices[0].message.tool_calls:
        # Handle tool calls
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_args["user_id"] = user_id  # Inject user_id
            
            # Call appropriate MCP tool
            tool_result = call_mcp_tool(tool_name, tool_args)
            tool_calls_info.append({
                "tool": tool_name,
                "parameters": tool_args
            })
            
            # Update assistant message with tool result
            assistant_message_content += f"\n{json.dumps(tool_result)}"
    
    # Store assistant message
    assistant_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=assistant_message_content
    )
    session.add(assistant_message)
    session.commit()
    
    return ChatResponse(
        conversation_id=conversation.id,
        response=assistant_message_content,
        tool_calls=tool_calls_info
    )