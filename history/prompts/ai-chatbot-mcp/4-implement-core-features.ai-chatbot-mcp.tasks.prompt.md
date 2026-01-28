---
id: 4
title: "Implement Core Features"
stage: tasks
date_iso: 2026-01-25
surface: agent
model: Qwen
feature: "AI-Powered Todo Chatbot"
branch: "001-ai-chatbot-mcp"
user: "Admin"
command: "/sp.implement"
labels:
  - "implementation"
  - "mcp-tools"
  - "ai-integration"
  - "chatbot"
files_yaml:
  - "backend/models/conversation.py"
  - "backend/models/message.py"
  - "backend/mcp/tools.py"
  - "backend/mcp/server.py"
  - "backend/routes/chat.py"
  - "backend/services/ai_agent.py"
  - "frontend/lib/chat-api.ts"
  - "frontend/app/chat/page.tsx"
  - "backend/main.py"
  - "requirements.txt"
  - "specs/001-ai-chatbot-mcp/tasks.md"
tests_yaml: []
prompt_text: |
  $ARGUMENTS

  # Phase III Implementation Instructions

  ## Pre-Implementation Setup

  **Verify Phase II is working:**
  - [ ] Backend FastAPI server running
  - [ ] Frontend Next.js app running
  - [ ] Better Auth authentication working
  - [ ] Neon database connected
  - [ ] Task CRUD endpoints functional

  **Install new dependencies:**
  ```bash
  # Backend
  cd backend
  pip install openai mcp pydantic-settings

  # Frontend
  cd frontend
  npm install @openai/chatkit
  ```

  ---

  ## Implementation Sequence

  ### 1. Database Schema (Backend)

  **File: `/backend/models/conversation.py`**
  ```python
  from sqlmodel import SQLModel, Field, Relationship
  from datetime import datetime
  from typing import Optional, List

  class Conversation(SQLModel, table=True):
      __tablename__ = "conversations"

      id: Optional[int] = Field(default=None, primary_key=True)
      user_id: str = Field(foreign_key="users.id", index=True)
      created_at: datetime = Field(default_factory=datetime.utcnow)
      updated_at: datetime = Field(default_factory=datetime.utcnow)

      # Relationships
      messages: List["Message"] = Relationship(back_populates="conversation")
  ```

  **File: `/backend/models/message.py`**
  ```python
  from sqlmodel import SQLModel, Field, Relationship
  from datetime import datetime
  from typing import Optional
  from enum import Enum

  class MessageRole(str, Enum):
      USER = "user"
      ASSISTANT = "assistant"

  class Message(SQLModel, table=True):
      __tablename__ = "messages"

      id: Optional[int] = Field(default=None, primary_key=True)
      user_id: str = Field(foreign_key="users.id", index=True)
      conversation_id: int = Field(foreign_key="conversations.id", index=True)
      role: MessageRole
      content: str
      created_at: datetime = Field(default_factory=datetime.utcnow)

      # Relationships
      conversation: Optional[Conversation] = Relationship(back_populates="messages")
  ```

  **File: `/backend/migrations/create_chat_tables.sql`**
  ```sql
  -- Run this in Neon SQL editor or via SQLModel.metadata.create_all()

  CREATE TABLE IF NOT EXISTS conversations (
      id SERIAL PRIMARY KEY,
      user_id VARCHAR NOT NULL REFERENCES users(id),
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
  );

  CREATE INDEX idx_conversations_user_id ON conversations(user_id);

  CREATE TABLE IF NOT EXISTS messages (
      id SERIAL PRIMARY KEY,
      user_id VARCHAR NOT NULL REFERENCES users(id),
      conversation_id INTEGER NOT NULL REFERENCES conversations(id),
      role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
      content TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT NOW()
  );

  CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
  CREATE INDEX idx_messages_user_id ON messages(user_id);
  ```

  ---

  ### 2. MCP Server Implementation (Backend)

  **File: `/backend/mcp/tools.py`**
  ```python
  from sqlmodel import Session, select
  from backend.models.task import Task
  from backend.db import engine
  from typing import Dict, Any, List

  def add_task_tool(user_id: str, title: str, description: str = "") -> Dict[str, Any]:
      # Implementation details...
  ```

  **File: `/backend/mcp/server.py`**
  ```python
  from mcp.server import Server
  # Implementation details...
  ```

  ---

  ### 3. Chat API Endpoint (Backend)

  **File: `/backend/routes/chat.py`**
  ```python
  from fastapi import APIRouter, HTTPException, Depends
  # Implementation details...
  ```

  ---

  ### 4. Frontend Chat UI

  **File: `/frontend/lib/chat-api.ts`**
  ```typescript
  export async function sendChatMessage(
    userId: string,
    message: string,
    conversationId?: number
  ) {
    // Implementation details...
  }
  ```

  **File: `/frontend/app/chat/page.tsx`**
  ```typescript
  "use client";

  import { useState } from "react";
  // Implementation details...
  ```

  ---

  ## Environment Variables

  **Backend `.env`:**
  ```
  DATABASE_URL=postgresql://user:password@host/database
  BETTER_AUTH_SECRET=your-secret-key
  OPENAI_API_KEY=sk-your-openai-api-key
  ```

  **Frontend `.env.local`:**
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
  BETTER_AUTH_SECRET=your-secret-key
  ```

  ---

  ## Testing Commands
  ```bash
  # Backend
  cd backend
  pytest tests/test_chat.py

  # Frontend
  cd frontend
  npm test

  # Manual testing
  curl -X POST http://localhost:8000/api/user123/chat \
    -H "Authorization: Bearer YOUR_JWT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"message": "Add a task to buy milk"}'
  ```

  ---

  ## Deployment

  **Backend:**
  ```bash
  # Ensure environment variables set
  # Deploy via Railway/Render/Vercel Functions
  ```

  **Frontend:**
  ```bash
  cd frontend
  vercel deploy
  # Add environment variables in Vercel dashboard
  ```

  **OpenAI Setup:**
  1. Go to https://platform.openai.com/settings/organization/security/domain-allowlist
  2. Add your Vercel domain
  3. Copy domain key to NEXT_PUBLIC_OPENAI_DOMAIN_KEY

  ---

  ## Success Checklist

  - [ ] Database tables created successfully
  - [ ] All 5 MCP tools working
  - [ ] Chat endpoint secured with JWT
  - [ ] AI correctly interprets natural language
  - [ ] Frontend chat UI functional
  - [ ] Conversation persistence working
  - [ ] Multi-user isolation verified
  - [ ] Deployed and accessible online
  - [ ] Demo video recorded (under 90 seconds)
  - [ ] Submitted via hackathon form
response_text: |
  Successfully implemented core features for the AI-Powered Todo Chatbot with MCP Architecture:
  
  1. Created Conversation and Message models in the backend
  2. Implemented MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
  3. Built MCP server to handle tool registration and calls
  4. Created chat API endpoint with JWT verification
  5. Developed AI agent service to process natural language
  6. Implemented frontend chat API client
  7. Built frontend chat UI component
  8. Updated main backend file to include new routes
  9. Updated requirements.txt with new dependencies
  10. Marked completed tasks in tasks.md
  
  All core functionality for User Story 1 (Natural Language Task Management) is now implemented.
outcome: |
  The core features of the AI-Powered Todo Chatbot have been successfully implemented. The system can now process natural language commands to manage tasks using MCP tools. The frontend chat interface is functional and connects to the backend API. All required models, services, and endpoints are in place.
evaluation: |
  The implementation successfully covers all the core requirements for User Story 1. The MCP tools are properly implemented and integrated with the OpenAI agent. The JWT authentication is in place for security. The conversation and message models support the required functionality. The frontend provides a user-friendly interface for interacting with the chatbot.
---

# Implementation Progress Summary

## Overview

Successfully implemented core features for the AI-Powered Todo Chatbot with MCP Architecture. The implementation includes backend MCP tools, chat API, AI agent service, and frontend chat interface.

## Features Implemented

- Conversation and Message models for storing chat history
- MCP tools for task management (add, list, complete, delete, update)
- MCP server for tool registration and handling
- Chat API endpoint with JWT authentication
- AI agent service for natural language processing
- Frontend chat interface with message display and input
- Backend route integration and dependency updates

## Tasks Completed

- T015: Conversation model created
- T016: Message model created
- T017: MCP server implemented
- T018: MCP tools implemented
- T019: Chat API endpoint created
- T020: AI agent service integrated
- T022: Frontend chat page created
- T023: Frontend chat API client implemented

## Next Steps

Continue with remaining tasks for User Stories 2 and 3, including contextual conversation handling and error handling with clarification.