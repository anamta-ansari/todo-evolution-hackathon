import os
import httpx
import json
import asyncio
from typing import Dict, Any, List, Optional
from backend.mcp.tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
)

class GeminiRestClient:
    def __init__(self, api_key: str = None, model: str = "gemini-2.5-flash"):
        """
        Initialize the Gemini REST client
        
        Args:
            api_key: Gemini API key (defaults to environment variable)
            model: Name of the Gemini model to use
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.client = httpx.AsyncClient(timeout=30.0)
        
    def _get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Define the tools available to the Gemini model in Gemini format
        """
        return [
            {
                "name": "add_task",
                "description": "Create a new task for the authenticated user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user (automatically provided)"},
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "The description of the task"}
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "list_tasks",
                "description": "List the authenticated user's tasks with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user (automatically provided)"},
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter tasks by status"
                        }
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as complete for the authenticated user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user (automatically provided)"},
                        "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task for the authenticated user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user (automatically provided)"},
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "update_task",
                "description": "Update task title or description for the authenticated user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user (automatically provided)"},
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "The new title for the task"},
                        "description": {"type": "string", "description": "The new description for the task"}
                    },
                    "required": ["task_id"]
                }
            }
        ]
    
    async def _execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
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
    
    async def _make_request(self, payload: Dict[str, Any], max_retries: int = 5) -> Dict[str, Any]:
        """
        Make a request to the Gemini API with retry logic for rate limiting

        Args:
            payload: The request payload
            max_retries: Maximum number of retries for rate limit errors

        Returns:
            The API response as a dictionary
        """
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        for attempt in range(max_retries + 1):
            try:
                response = await self.client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise ValueError("Invalid API key. Please check your GEMINI_API_KEY.")
                elif e.response.status_code == 429:
                    if attempt < max_retries:
                        # Exponential backoff with jitter: wait 1s, 2-3s, 4-7s, 8-15s, 16-31s
                        base_wait = 2 ** attempt
                        import random
                        wait_time = base_wait + random.uniform(0, base_wait - 1)  # Add jitter
                        print(f"Rate limit exceeded. Waiting {wait_time:.2f}s before retry {attempt + 1}/{max_retries}")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        raise ValueError("Rate limit exceeded. Please try again later.")
                else:
                    raise ValueError(f"HTTP error {e.response.status_code}: {e.response.text}")
            except httpx.RequestError as e:
                raise ValueError(f"Request error: {str(e)}")

        # This should not be reached, but included for completeness
        raise ValueError("Max retries exceeded for rate limit error")
    
    async def _extract_function_call_with_delay(self, response_data: Dict[str, Any], delay: float = 0.5) -> Optional[Dict[str, Any]]:
        """
        Extract function call from Gemini response with a delay to respect rate limits

        Args:
            response_data: The response from Gemini API
            delay: Delay in seconds before extracting function call

        Returns:
            Function call information or None if no function call
        """
        # Add a small delay to help with rate limiting
        await asyncio.sleep(delay)
        
        if "candidates" in response_data:
            for candidate in response_data["candidates"]:
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "functionCall" in part:
                            function_call = part["functionCall"]
                            return {
                                "name": function_call.get("name"),
                                "args": function_call.get("args", {})
                            }
        return None
    
    def _format_contents(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Format messages for Gemini API
        
        Args:
            messages: List of messages in format {"role": "...", "content": "..."}
            
        Returns:
            Formatted contents for Gemini API
        """
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Map roles appropriately
            if role == "user":
                gemini_role = "user"
            elif role == "assistant":
                gemini_role = "model"
            else:
                gemini_role = role  # Use as-is if already in correct format
            
            contents.append({
                "role": gemini_role,
                "parts": [{"text": content}]
            })
        
        return contents
    
    async def chat_with_tools(self, messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
        """
        Process a chat conversation with tool calling
        
        Args:
            messages: List of messages in format {"role": "...", "content": "..."}
            user_id: The ID of the user for this conversation
            
        Returns:
            Dictionary with response content and any tool calls made
        """
        # Format the conversation history for Gemini
        contents = self._format_contents(messages)
        
        # Prepare the system instruction
        system_instruction = {
            "parts": [{
                "text": f"You are a helpful task management assistant for user ID: {user_id}. The user is already authenticated, and their user ID is {user_id}. NEVER ask for the user's ID. Use the provided tools to add, list, complete, delete, and update tasks for this authenticated user. Always confirm actions clearly and be concise."
            }]
        }
        
        # Prepare the payload
        payload = {
            "contents": contents,
            "tools": [
                {
                    "functionDeclarations": self._get_tool_definitions()
                }
            ],
            "systemInstruction": system_instruction,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048
            }
        }
        
        try:
            # Make the first request to get potential function call
            response_data = await self._make_request(payload)

            # Check if the response contains function calls with a small delay to respect rate limits
            function_call = await self._extract_function_call_with_delay(response_data, delay=0.5)

            if function_call:
                # Add user_id to function args if not present
                if "user_id" not in function_call["args"]:
                    function_call["args"]["user_id"] = user_id

                # Execute the tool
                tool_result = await self._execute_tool(function_call["name"], function_call["args"])

                # Add the function call and result to the conversation history
                updated_contents = contents[:]
                # Add the function call from the model
                updated_contents.append({
                    "role": "model",
                    "parts": [{"functionCall": {
                        "name": function_call["name"],
                        "args": function_call["args"]
                    }}]
                })
                # Add the function result
                updated_contents.append({
                    "role": "function",
                    "parts": [{"functionResponse": {
                        "name": function_call["name"],
                        "response": tool_result
                    }}]
                })

                # Make a second request to get the final response
                final_payload = {
                    "contents": updated_contents,
                    "systemInstruction": system_instruction,
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 2048
                    }
                }

                # Add a small delay before the second API call to respect rate limits
                await asyncio.sleep(1.0)
                
                final_response_data = await self._make_request(final_payload)

                # Extract the final text response
                final_text = ""
                if "candidates" in final_response_data:
                    for candidate in final_response_data["candidates"]:
                        if "content" in candidate and "parts" in candidate["content"]:
                            for part in candidate["content"]["parts"]:
                                if "text" in part:
                                    final_text += part["text"]

                return {
                    "response": final_text,
                    "tool_calls": [{
                        "tool": function_call["name"],
                        "parameters": function_call["args"],
                        "result": tool_result
                    }]
                }
            else:
                # No function calls, just return the response
                response_text = ""
                if "candidates" in response_data:
                    for candidate in response_data["candidates"]:
                        if "content" in candidate and "parts" in candidate["content"]:
                            for part in candidate["content"]["parts"]:
                                if "text" in part:
                                    response_text += part["text"]

                return {
                    "response": response_text,
                    "tool_calls": []
                }

        except Exception as e:
            # Handle any errors gracefully
            return {
                "response": f"An error occurred while processing your request: {str(e)}",
                "tool_calls": [],
                "error": str(e)
            }
    
    async def close(self):
        """
        Close the HTTP client
        """
        await self.client.aclose()