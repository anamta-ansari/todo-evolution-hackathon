---
id: 2
title: "Create Implementation Plan"
stage: plan
date_iso: 2026-01-25
surface: agent
model: Qwen
feature: "AI-Powered Todo Chatbot"
branch: "001-ai-chatbot-mcp"
user: "Admin"
command: "/sp.plan"
labels:
  - "planning"
  - "architecture"
  - "mcp-tools"
  - "ai-integration"
files_yaml:
  - "specs/001-ai-chatbot-mcp/plan.md"
  - "specs/001-ai-chatbot-mcp/research.md"
  - "specs/001-ai-chatbot-mcp/data-model.md"
  - "specs/001-ai-chatbot-mcp/contracts/chat-api-contract.md"
  - "specs/001-ai-chatbot-mcp/quickstart.md"
tests_yaml: []
prompt_text: |
  /sp.plan

  # Phase III Implementation Plan

  ## Step 1: Database Schema Setup
  **Objective:** Add Conversation and Message tables

  **Tasks:**
  1. Create SQLModel models for Conversation and Message in `/backend/models/`
  2. Write database migration script (Alembic or manual SQL)
  3. Test schema creation on Neon database
  4. Verify foreign key relationships (user_id, conversation_id)

  **Files to Create:**
  - `/backend/models/conversation.py`
  - `/backend/models/message.py`
  - `/backend/migrations/add_conversation_tables.py` (if using Alembic)

  **Acceptance Criteria:**
  - Tables created successfully in Neon DB
  - Can insert and query conversations and messages
  - Indexes created on user_id and conversation_id

  ---

  ## Step 2: Implement MCP Server
  **Objective:** Build MCP server with 5 tools

  **Tasks:**
  1. Install Official MCP SDK: `pip install mcp`
  2. Create `/backend/mcp/server.py` with MCP server setup
  3. Implement tool schemas (add_task, list_tasks, complete_task, delete_task, update_task)
  4. Implement tool handlers in `/backend/mcp/tools.py`
  5. Connect tools to database using SQLModel
  6. Test each tool independently with mock data

  **Files to Create:**
  - `/backend/mcp/server.py`
  - `/backend/mcp/tools.py`

  **Testing:**
  - Mock user_id and verify each tool returns correct JSON
  - Test error cases (task not found, invalid user_id)

  **Acceptance Criteria:**
  - All 5 MCP tools respond correctly
  - Tools enforce user_id filtering
  - Error responses follow specification

  ---

  ## Step 3: Build Chat API Endpoint
  **Objective:** Create POST /api/{user_id}/chat endpoint

  **Tasks:**
  1. Create `/backend/routes/chat.py`
  2. Implement JWT verification middleware (reuse from Phase II)
  3. Implement conversation history retrieval
  4. Integrate OpenAI Agents SDK with MCP tools
  5. Store user and assistant messages in database
  6. Return formatted response

  **Files to Create:**
  - `/backend/routes/chat.py`

  **Testing:**
  - Send test message with valid JWT token
  - Verify conversation_id creation for new chats
  - Verify message history retrieval
  - Test AI tool invocation

  **Acceptance Criteria:**
  - Endpoint returns 401 for invalid tokens
  - Creates new conversation if not provided
  - Persists all messages to database
  - AI correctly invokes MCP tools

  ---

  ## Step 4: OpenAI Agent Configuration
  **Objective:** Set up OpenAI Agents SDK with system prompt and MCP integration

  **Tasks:**
  1. Install OpenAI Agents SDK: `pip install openai`
  2. Configure agent with system prompt
  3. Register MCP tools with agent
  4. Implement message history formatting for agent
  5. Test agent responses with various user intents

  **Files to Modify:**
  - `/backend/routes/chat.py` (agent initialization)

  **Testing:**
  - Test: "Add task X" → calls add_task
  - Test: "Show my tasks" → calls list_tasks
  - Test: "Mark task 3 done" → calls complete_task
  - Test ambiguous inputs for clarification

  **Acceptance Criteria:**
  - Agent correctly interprets natural language commands
  - Agent provides helpful confirmations
  - Agent handles errors gracefully

  ---

  ## Step 5: Frontend ChatKit Integration
  **Objective:** Build chat interface using OpenAI ChatKit

  **Tasks:**
  1. Install ChatKit: `npm install @openai/chatkit`
  2. Create `/frontend/app/chat/page.tsx`
  3. Implement chat API client in `/frontend/lib/chat-api.ts`
  4. Attach JWT token to all API requests
  5. Configure OpenAI domain allowlist
  6. Style chat UI with Tailwind CSS

  **Files to Create:**
  - `/frontend/app/chat/page.tsx`
  - `/frontend/lib/chat-api.ts`

  **Testing:**
  - Verify JWT token sent in Authorization header
  - Test message sending and receiving
  - Verify conversation persistence across page refreshes

  **Acceptance Criteria:**
  - Chat UI renders correctly
  - Messages sent to backend successfully
  - Responses displayed in real-time
  - Authentication works end-to-end

  ---

  ## Step 6: OpenAI Dashboard Configuration
  **Objective:** Configure domain allowlist for ChatKit

  **Tasks:**
  1. Deploy frontend to Vercel (or other hosting)
  2. Get production URL
  3. Add domain to OpenAI allowlist: https://platform.openai.com/settings/organization/security/domain-allowlist
  4. Copy domain key
  5. Set `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` in Vercel environment variables
  6. Redeploy frontend

  **Acceptance Criteria:**
  - ChatKit works on production URL
  - No CORS errors in browser console

  ---

  ## Step 7: End-to-End Testing
  **Objective:** Verify complete chatbot workflow

  **Test Cases:**
  1. **New user first chat:**
     - User logs in
     - Sends message: "Add task to buy milk"
     - Verify task appears in database
     - Verify AI confirmation message

  2. **Multi-turn conversation:**
     - User: "Show my tasks"
     - AI: Lists tasks
     - User: "Mark the first one done"
     - Verify task updated to completed

  3. **Conversation persistence:**
     - User sends messages
     - Close browser
     - Reopen chat
     - Verify conversation history loaded

  4. **Error handling:**
     - User: "Delete task 999"
     - Verify AI responds appropriately

  5. **Multi-user isolation:**
     - User A adds tasks
     - User B logs in
     - Verify User B cannot see User A's tasks

  **Acceptance Criteria:**
  - All test cases pass
  - No security vulnerabilities (user data leakage)
  - Graceful error handling

  ---

  ## Step 8: Documentation & Deployment
  **Objective:** Prepare for submission

  **Tasks:**
  1. Update README.md with Phase III setup instructions
  2. Document environment variables needed
  3. Create demo video (under 90 seconds)
  4. Deploy backend (if not already deployed)
  5. Deploy frontend to Vercel
  6. Submit GitHub repo link + deployed URLs

  **Acceptance Criteria:**
  - README includes clear setup steps
  - Demo video shows natural language chat working
  - Both frontend and backend deployed successfully

  ---

  ## Timeline Estimate

  | Step | Duration | Dependencies |
  |------|----------|--------------|
  | Step 1: Database Schema | 2 hours | None |
  | Step 2: MCP Server | 4 hours | Step 1 |
  | Step 3: Chat API Endpoint | 3 hours | Step 1, 2 |
  | Step 4: Agent Configuration | 2 hours | Step 3 |
  | Step 5: Frontend ChatKit | 3 hours | Step 3 |
  | Step 6: OpenAI Config | 1 hour | Step 5 deployed |
  | Step 7: Testing | 2 hours | All previous |
  | Step 8: Docs & Deploy | 2 hours | Step 7 |

  **Total:** ~19 hours

  ---

  ## Risk Mitigation

  **Risk 1:** OpenAI API rate limits
  - **Mitigation:** Use API key with sufficient quota, implement retry logic

  **Risk 2:** MCP SDK compatibility issues
  - **Mitigation:** Follow official MCP SDK docs, test tools independently first

  **Risk 3:** ChatKit domain allowlist delays
  - **Mitigation:** Configure early, test with localhost first

  **Risk 4:** Conversation history grows large
  - **Mitigation:** Limit history to last 20 messages per conversation in agent context
response_text: |
  Successfully created the implementation plan for the AI-Powered Todo Chatbot with MCP Architecture. The plan includes:
  
  1. Updated technical context with language, dependencies, and constraints
  2. Detailed project structure showing all required files and directories
  3. Comprehensive research document covering key decisions
  4. Data model defining all entities and their relationships
  5. API contracts for the chat endpoint and MCP tools
  6. Quickstart guide with setup instructions
  7. Constitution compliance check with all items verified
  
  The plan is ready for the task breakdown phase (/sp.tasks).
outcome: |
  The implementation plan is complete and comprehensive, covering all aspects of the AI-Powered Todo Chatbot with MCP Architecture. All required artifacts have been created and the constitution compliance has been verified.
evaluation: |
  The plan successfully addresses all requirements from the feature specification and complies with the project constitution. All necessary research has been conducted, data models defined, API contracts established, and setup instructions provided.
---

# Implementation Plan Summary

## Overview

Created a comprehensive implementation plan for the AI-Powered Todo Chatbot with MCP Architecture. The plan covers all aspects of development from database schema to deployment.

## Key Artifacts Created

- **Implementation Plan** (plan.md): Overall project structure and compliance check
- **Research Document** (research.md): Key technology decisions and rationale
- **Data Model** (data-model.md): Entity definitions and relationships
- **API Contracts** (contracts/chat-api-contract.md): Endpoint specifications
- **Quickstart Guide** (quickstart.md): Setup and testing instructions

## Compliance Status

All constitution requirements for Phase III have been verified and marked as completed in the plan document.