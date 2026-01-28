<!-- SYNC IMPACT REPORT
Version change: 3.0.0 -> 4.0.0
Modified principles: Principles I-VIII updated to reflect Phase III requirements (AI-Powered Todo Chatbot with MCP Architecture)
Added sections: Principle IX (MCP-First Design), Principle X (Stateless Architecture), Principle XI (Natural Language Processing Standards)
Removed sections: Dashboard & CRUD Standards (replaced with new focus)
Templates requiring updates:
- ✅ .specify/templates/plan-template.md - Updated to reflect new principles
- ✅ .specify/templates/spec-template.md - Updated to reflect new principles
- ✅ .specify/templates/tasks-template.md - Updated to reflect new principles
- ✅ .specify/templates/commands/*.md - Verified no outdated references
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Scope of Phase III
AI-Powered Todo Chatbot with MCP Architecture: Implement conversational interface for todo management; Frontend integrates with OpenAI ChatKit for natural language interactions; Backend exposes all todo operations as MCP tools for AI consumption; AI agent interprets user intent and manages tasks through MCP tools; System maintains conversation history in database for session continuity.

### II. Technology Stack for Phase III
Frontend: Next.js 16+ (App Router) with TypeScript, OpenAI ChatKit for conversational UI; Backend: Python FastAPI with OpenAI Agents SDK and Official MCP SDK; ORM: SQLModel with Neon Serverless PostgreSQL; Authentication: Better Auth with JWT tokens; AI Model: OpenAI GPT-4 or compatible model; MCP Tools: Official MCP SDK for standardized tool exposure.

### III. Project Structure (Post Phase III)
Monorepo organization with dedicated backend/ and frontend/ directories; Frontend uses App Router with protected routes including chat interface; MCP tools defined in dedicated tools/ directory with standardized schemas; Clear separation of concerns between frontend, backend, and AI orchestration layers; Standardized specs/ directory for documentation and planning artifacts; Conversational interface accessible at /chat route after authentication.

### IV. Deliverables for Phase III (NON-NEGOTIABLE)
Working conversational interface for todo management; MCP tools for all 5 todo operations (Add, List, Update, Delete, Mark Complete); Conversation history persistence across server restarts; AI correctly interprets user intent and invokes appropriate MCP tools; Multiple concurrent users can chat independently with proper user isolation; Natural language processing with helpful, confirmatory responses.

### V. Test-First Approach
TDD mandatory: Tests written → Requirements validated → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced for all MCP tools and AI integration; Integration tests validate end-to-end conversational flow.

### VI. Documentation and Clarity
All MCP tools must include appropriate docstrings and schema definitions; README updated with chatbot setup and run instructions; Architecture decisions documented in specs/ directory; MCP tool schemas clearly defined with input/output specifications.

### VII. Security & User Isolation Standards
- Chat interface protected: redirect to /login if not authenticated
- Backend enforces ownership: all operations filtered by authenticated user_id
- Frontend never displays tasks from other users
- All API calls must include Authorization: Bearer <token>
- MCP tools enforce user isolation: unauthorized requests return 401, ownership mismatches return 403
- Conversation history isolated by user_id
- Frontend properly handles authentication state and redirects to login when unauthenticated

### VIII. API Design Standards
- Single /api/{user_id}/chat endpoint handles all AI interactions
- Predictable API response schemas with consistent error handling
- Proper HTTP status codes for success and error conditions
- Rate limiting implemented to prevent abuse
- Request/response logging for debugging and monitoring

### IX. MCP-First Design
- All todo operations must be exposed as MCP tools following standardized schemas
- MCP tools must be stateless and store all state in database
- Tool schemas must be consistent and predictable for AI consumption
- Error handling in MCP tools must be explicit and informative
- MCP tools must validate inputs and return appropriate error messages
- Tool discovery and documentation must be available for AI agents

### X. Stateless Architecture
- Server maintains no session state between requests
- All conversation history persists in database
- AI agent state is reconstructed from database on each interaction
- Horizontal scaling enabled through stateless design
- Session continuity maintained through database persistence
- No server-side caching of user data or conversation state

### XI. Natural Language Processing Standards
- AI must correctly interpret user intent (add, list, complete, delete, update tasks)
- Responses must be helpful, confirmatory, and error-tolerant
- Ambiguous requests should be clarified rather than guessed
- Error messages must be user-friendly and actionable
- AI responses should confirm successful operations
- Natural language understanding must handle variations in user phrasing

## Frontend Architecture Standards
- Use Next.js App Router with proper route protection
- Implement consistent authentication state management
- Follow accessibility best practices for all UI components
- Ensure responsive design for all pages and components
- Handle authentication errors gracefully with user-friendly messages
- Implement proper loading states and error boundaries
- Integrate OpenAI ChatKit for conversational interface
- Organize components logically (ChatInterface, MessageHistory, etc.)

## Backend Architecture Standards
- Follow FastAPI best practices for API design
- Use SQLModel for consistent database modeling
- Implement proper error handling and validation
- Follow security best practices for API endpoints including JWT verification
- Ensure database connection pooling and optimization
- Enforce user isolation in all data access operations
- Maintain consistent API endpoint patterns for chat operations
- Expose standardized MCP tools with predictable schemas
- Implement conversation history management in database

## Development Workflow
- All changes must follow the spec-plan-tasks implementation cycle
- Code reviews required for all pull requests
- Automated testing required before merge
- Clear commit messages following conventional format
- Branch naming convention: feature/[issue-number]-[short-description]
- MCP tool schemas must be validated before implementation

## Governance
This constitution governs Phase III development: implementing the AI-Powered Todo Chatbot with MCP Architecture. All development activities must comply with these principles. Amendments require explicit documentation and team approval.

**Version**: 4.0.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-01-25