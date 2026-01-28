from openai import OpenAI
import os
from typing import Dict, Any, List
from backend.mcp.tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
)


class TodoAIAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """
        You are a helpful task management assistant. 
        You help users manage their todo list through natural language.
        
        Available tools:
        - add_task: Create new tasks
        - list_tasks: Show tasks (all/pending/completed)
        - complete_task: Mark tasks as done
        - delete_task: Remove tasks
        - update_task: Modify task details
        
        Guidelines:
        - Always confirm actions clearly (e.g., "I've added 'Buy groceries' to your list")
        - When listing tasks, format them in a readable way
        - If user request is ambiguous, ask for clarification
        - Handle errors gracefully with helpful suggestions
        - Be concise but friendly
        """

    def process_message(self, user_message: str, user_id: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Process a user message and return the AI response and any tool calls
        """
        if conversation_history is None:
            conversation_history = []

        # Prepare messages for the AI
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        # Define available tools
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

        try:
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using gpt-3.5-turbo for testing
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            # Extract the response
            ai_response = response.choices[0].message
            content = ai_response.content or ""

            # Process any tool calls
            tool_calls_results = []
            if ai_response.tool_calls:
                for tool_call in ai_response.tool_calls:
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)  # In production, use json.loads safely
                    
                    # Add user_id to the arguments
                    function_args["user_id"] = user_id
                    
                    # Call the appropriate tool
                    if function_name == "add_task":
                        result = add_task_tool(**function_args)
                    elif function_name == "list_tasks":
                        result = list_tasks_tool(**function_args)
                    elif function_name == "complete_task":
                        result = complete_task_tool(**function_args)
                    elif function_name == "delete_task":
                        result = delete_task_tool(**function_args)
                    elif function_name == "update_task":
                        result = update_task_tool(**function_args)
                    else:
                        result = {"error": f"Unknown tool: {function_name}"}
                    
                    tool_calls_results.append({
                        "tool": function_name,
                        "parameters": function_args,
                        "result": result
                    })

            return {
                "response": content,
                "tool_calls": tool_calls_results
            }

        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "tool_calls": []
            }