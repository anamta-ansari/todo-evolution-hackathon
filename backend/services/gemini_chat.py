import os
import google.generativeai as genai
from typing import Dict, Any, List
from backend.mcp.tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
)

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiChatService:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini chat service
        
        Args:
            model_name: Name of the Gemini model to use (default: gemini-1.5-flash)
        """
        self.model_name = model_name
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 2048,
            },
            # Define the tools that the model can use
            tools=self._get_gemini_tools()
        )
    
    def _get_gemini_tools(self) -> List[Dict[str, Any]]:
        """
        Define the tools available to the Gemini model in Gemini format
        """
        return [
            {
                "name": "add_task",
                "description": "Create a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "The description of the task"}
                    },
                    "required": ["user_id", "title"]
                }
            },
            {
                "name": "list_tasks",
                "description": "List user's tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "status": {
                            "type": "string", 
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter tasks by status"
                        }
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "complete_task",
                "description": "Mark task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            {
                "name": "update_task",
                "description": "Update task details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "The new title for the task"},
                        "description": {"type": "string", "description": "The new description for the task"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        ]
    
    def _execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the appropriate MCP tool based on the tool name and arguments
        """
        # Ensure user_id is a string as expected by the tools
        if "user_id" in tool_args:
            tool_args["user_id"] = str(tool_args["user_id"])
        
        if tool_name == "add_task":
            return add_task_tool(**tool_args)
        elif tool_name == "list_tasks":
            return list_tasks_tool(**tool_args)
        elif tool_name == "complete_task":
            return complete_task_tool(**tool_args)
        elif tool_name == "delete_task":
            return delete_task_tool(**tool_args)
        elif tool_name == "update_task":
            return update_task_tool(**tool_args)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def chat_with_tools(self, messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
        """
        Process a chat conversation with tool calling
        
        Args:
            messages: List of messages in the format {"role": "user|model", "parts": ["message content"]}
            user_id: The ID of the user for this conversation
            
        Returns:
            Dictionary with response content and any tool calls made
        """
        try:
            # Create a chat session with the history
            chat = self.model.start_chat(history=messages[:-1])  # Exclude the latest message
            
            # Send the latest message and get response
            latest_message = messages[-1]["parts"][0] if messages else "Hello"
            
            # Generate content with potential tool calls
            response = chat.send_message(latest_message, stream=False)
            
            # Process any function calls in the response
            tool_calls_info = []
            response_text = ""
            
            # Check if the response contains function calls
            if hasattr(response.candidates[0], 'function_calls'):
                for function_call in response.candidates[0].function_calls:
                    tool_name = function_call.name
                    # Convert the args to a dictionary
                    tool_args = {}
                    for arg_name, arg_value in function_call.args.items():
                        tool_args[arg_name] = arg_value
                    
                    # Ensure user_id is included in tool args
                    if "user_id" not in tool_args:
                        tool_args["user_id"] = user_id
                    
                    # Execute the tool
                    tool_result = self._execute_tool(tool_name, tool_args)
                    
                    # Add to tool calls info
                    tool_calls_info.append({
                        "tool": tool_name,
                        "parameters": tool_args,
                        "result": tool_result
                    })
                    
                    # Add the tool result to the chat for context
                    chat.send_message(str(tool_result))
                
                # Get the final response after tool execution
                final_response = chat.send_message("Based on the tool results, provide a natural language response to the user.", stream=False)
                response_text = final_response.text
            else:
                # No function calls, just return the response
                response_text = response.text
            
            return {
                "response": response_text,
                "tool_calls": tool_calls_info
            }
            
        except Exception as e:
            # Handle any errors gracefully
            return {
                "response": f"An error occurred while processing your request: {str(e)}",
                "tool_calls": [],
                "error": str(e)
            }
    
    def process_message(self, message: str, user_id: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Process a single message with conversation history
        
        Args:
            message: The user's message
            user_id: The ID of the user
            history: Previous conversation history
            
        Returns:
            Dictionary with response content and any tool calls made
        """
        # Prepare the system instruction
        system_instruction = """You are a helpful task management assistant.
        You help users manage their todo list through natural language.

        Available tools:
        - add_task: Create new tasks
        - list_tasks: Show tasks (all/pending/completed)
        - complete_task: Mark tasks as done
        - delete_task: Remove tasks
        - update_task: Modify task details

        Always confirm actions clearly and be helpful."""
        
        # Format the conversation history for Gemini
        formatted_history = []
        if history:
            for msg in history:
                role = "user" if msg.get("role") == "user" else "model"
                formatted_history.append({
                    "role": role,
                    "parts": [msg.get("content", "")]
                })
        
        # Add the current message
        formatted_history.append({
            "role": "user",
            "parts": [message]
        })
        
        # Process with tools
        return self.chat_with_tools(formatted_history, user_id)