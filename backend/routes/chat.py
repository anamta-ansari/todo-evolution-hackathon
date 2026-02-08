import asyncio
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlmodel import Session, select
from backend.db.session import get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.dependencies.auth import verify_token as base_verify_token
from backend.models.conversation import Conversation
from backend.models.message import Message, MessageRole
import os

# Import rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

# Import the new Gemini REST client
try:
    from backend.services.gemini_rest_client import GeminiRestClient

    # Try to initialize with model from environment variable or default to gemini-pro
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    gemini_rest_client = None
    gemini_rest_available = False

    # Try different model names in sequence
    model_names = [
        os.getenv("GEMINI_MODEL", ""),  # Custom model from env
        "gemini-2.5-flash",             # Latest flash model (lower rate limits)
        "gemini-2.5-pro",               # Latest pro model
        "gemini-pro",                   # Standard model
        "gemini-1.0-pro-vision-latest", # Alternative
        "gemini-1.0-pro-001",           # Another variant
        "gemini-pro-vision"             # Vision model as fallback
    ]

    # Remove empty string if it's the first option (when env var is not set)
    model_names = [model for model in model_names if model.strip()]

    for model_name in model_names:
        try:
            gemini_rest_client = GeminiRestClient(model=model_name)
            gemini_rest_available = True
            print(f"Successfully initialized Gemini client with model: {model_name}")
            break
        except Exception as e:
            print(f"Failed to initialize Gemini client with model '{model_name}': {str(e)}")
            continue

    if not gemini_rest_available:
        raise ValueError("No valid Gemini model could be initialized")

except (ImportError, ValueError) as e:
    # Fallback if GEMINI_API_KEY is not set or other issues
    gemini_rest_available = False
    GeminiRestClient = None
    gemini_rest_client = None
    print(f"Gemini client initialization failed: {str(e)}")

# Create a limiter for this router
router_limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


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
@router_limiter.limit("120/minute")  # Allow 120 requests per minute per IP for development/testing
async def chat(
    request: Request,
    user_id: str,
    chat_request: ChatRequest,
    session: Session = Depends(get_session),
    token_payload: dict = Depends(verify_token)
):
    # Add a small initial delay to help with rate limiting
    await asyncio.sleep(0.2)
    # Extract user_id from token payload
    token_user_id = token_payload.get("user_id")

    # Convert both to integers for comparison since user IDs should be integers
    try:
        path_user_id = int(user_id)
        token_user_id_int = int(token_user_id)

        # Verify user_id matches token
        if path_user_id != token_user_id_int:
            raise HTTPException(status_code=403, detail="Forbidden")
    except (ValueError, TypeError):
        # If conversion fails, fall back to string comparison
        if str(user_id) != str(token_user_id):
            raise HTTPException(status_code=403, detail="Forbidden")

    # Get or create conversation
    conversation = None
    if chat_request.conversation_id:
        conversation = session.get(Conversation, chat_request.conversation_id)
        if not conversation or conversation.user_id != path_user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=path_user_id)
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
        user_id=path_user_id,
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=chat_request.message
    )
    session.add(user_message)
    session.commit()

    # Build messages for Gemini
    # Convert SQLModel messages to Gemini format
    gemini_history = []
    for msg in history:
        role = "user" if msg.role == MessageRole.USER else "model"
        gemini_history.append({
            "role": role,
            "parts": [msg.content]
        })

    # Process the message using the Gemini REST client if available, otherwise use mock
    if gemini_rest_available:
        try:
            # Prepare the conversation history for the Gemini API
            conversation_messages = []

            # Add historical messages
            for msg in history:
                role = "user" if msg.role == MessageRole.USER else "assistant"
                conversation_messages.append({
                    "role": role,
                    "content": msg.content
                })

            # Add the current user message
            conversation_messages.append({
                "role": "user",
                "content": chat_request.message
            })

            # Process with the Gemini REST client
            result = await gemini_rest_client.chat_with_tools(
                messages=conversation_messages,
                user_id=str(path_user_id)
            )

            assistant_message_content = result.get("response", "")
            tool_calls_info = result.get("tool_calls", [])

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini REST service error: {str(e)}")
    else:
        # Fallback to mock implementation if Gemini REST is not available
        user_msg = chat_request.message.lower()
        if "add" in user_msg and ("task" in user_msg or "buy groceries" in user_msg):
            # Simulate calling add_task tool
            tool_result = call_mcp_tool("add_task", {"user_id": str(path_user_id), "title": "buy groceries", "description": ""})
            assistant_message_content = f"I've created a task for you: buy groceries (ID: {tool_result.get('task_id', 1)})"
            tool_calls_info = [{
                "tool": "add_task",
                "parameters": {"user_id": str(path_user_id), "title": "buy groceries", "description": ""}
            }]
        elif "list" in user_msg or ("what" in user_msg and ("task" in user_msg or "tasks" in user_msg)) or ("do" in user_msg and "have" in user_msg and ("task" in user_msg or "tasks" in user_msg)) or ("show" in user_msg and ("task" in user_msg or "tasks" in user_msg)):
            # Simulate calling list_tasks tool
            tool_result = call_mcp_tool("list_tasks", {"user_id": str(path_user_id)})
            if tool_result:
                task_list = ", ".join([f"{task['title']} (ID: {task['id']})" for task in tool_result])
                assistant_message_content = f"You have {len(tool_result)} task(s): {task_list}"
            else:
                assistant_message_content = "You don't have any tasks."
            tool_calls_info = [{
                "tool": "list_tasks",
                "parameters": {"user_id": str(path_user_id), "status": "all"}
            }]
        elif "complete" in user_msg or "done" in user_msg:
            # Simulate calling complete_task tool - first we need to get a task to complete
            tasks = call_mcp_tool("list_tasks", {"user_id": str(path_user_id)})
            task_to_complete = tasks[0] if tasks else None
            if task_to_complete:
                tool_result = call_mcp_tool("complete_task", {"user_id": str(path_user_id), "task_id": task_to_complete["id"]})
                assistant_message_content = f"I've marked the task '{tool_result.get('title', task_to_complete['title'])}' as completed."
                tool_calls_info = [{
                    "tool": "complete_task",
                    "parameters": {"user_id": str(path_user_id), "task_id": task_to_complete["id"]}
                }]
            else:
                assistant_message_content = "You don't have any tasks to complete."
                tool_calls_info = []
        elif "delete" in user_msg:
            # Simulate calling delete_task tool
            tasks = call_mcp_tool("list_tasks", {"user_id": str(path_user_id)})
            task_to_delete = tasks[0] if tasks else None
            if task_to_delete:
                tool_result = call_mcp_tool("delete_task", {"user_id": str(path_user_id), "task_id": task_to_delete["id"]})
                assistant_message_content = f"I've deleted the task '{tool_result.get('title', task_to_delete['title'])}'."
                tool_calls_info = [{
                    "tool": "delete_task",
                    "parameters": {"user_id": str(path_user_id), "task_id": task_to_delete["id"]}
                }]
            else:
                assistant_message_content = "You don't have any tasks to delete."
                tool_calls_info = []
        else:
            assistant_message_content = "I understood your request. How else can I help you with your tasks?"
            tool_calls_info = []

    # Store assistant message
    assistant_message = Message(
        user_id=path_user_id,
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