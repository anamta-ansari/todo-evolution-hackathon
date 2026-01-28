# Chat API Contract

## Endpoint: POST /api/{user_id}/chat

### Description
Handles conversational interactions with the AI assistant for todo management operations.

### Request
**Method**: POST
**Path**: `/api/{user_id}/chat`

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)
- `Content-Type: application/json` (required)

**Path Parameters**:
- `user_id` (string, required): The ID of the authenticated user

**Body Parameters**:
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

- `conversation_id` (integer, optional): ID of existing conversation, creates new if not provided
- `message` (string, required): The user's message to the AI assistant

### Response
**Success Response (200 OK)**:
```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your task list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "user123",
        "title": "Buy groceries"
      }
    }
  ]
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or expired JWT token
- `403 Forbidden`: user_id in JWT doesn't match URL parameter
- `500 Internal Server Error`: AI service unavailable

### Security
- JWT token must be valid and not expired
- user_id in JWT must match the user_id in the URL path
- All operations are filtered by authenticated user_id

## MCP Tool Contracts

### Tool: add_task
**Purpose**: Create a new task

**Parameters**:
```json
{
  "user_id": "string (required)",
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

**Returns**:
```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

**Error Handling**:
- Missing user_id → {"error": "user_id required"}
- Empty title → {"error": "title cannot be empty"}
- Database error → {"error": "failed to create task"}

### Tool: list_tasks
**Purpose**: Retrieve user's tasks

**Parameters**:
```json
{
  "user_id": "string (required)",
  "status": "string (optional: 'all' | 'pending' | 'completed', default: 'all')"
}
```

**Returns**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-01-20T10:00:00Z"
  }
]
```

**Error Handling**:
- Invalid status value → return all tasks
- No tasks found → return empty array []

### Tool: complete_task
**Purpose**: Mark task as complete

**Parameters**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)"
}
```

**Returns**:
```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

**Error Handling**:
- Task not found → {"error": "task not found"}
- Task belongs to different user → {"error": "unauthorized"}

### Tool: delete_task
**Purpose**: Remove a task

**Parameters**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)"
}
```

**Returns**:
```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

**Error Handling**:
- Task not found → {"error": "task not found"}
- Task belongs to different user → {"error": "unauthorized"}

### Tool: update_task
**Purpose**: Modify task details

**Parameters**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)",
  "title": "string (optional)",
  "description": "string (optional)"
}
```

**Returns**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

**Error Handling**:
- No fields to update → {"error": "no fields provided"}
- Task not found → {"error": "task not found"}