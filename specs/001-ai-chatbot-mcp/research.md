# Research: AI-Powered Todo Chatbot with MCP Architecture

## Decision: MCP SDK Selection
**Rationale**: After researching available MCP (Model Context Protocol) SDKs, we determined that the Official MCP SDK is the most appropriate for this implementation. It provides standardized schemas for tool definition and reliable integration with AI agents.

**Alternatives considered**: 
- Building custom tool protocol
- Using LangChain's tool system
- Using OpenAI Functions API directly

## Decision: OpenAI Agents SDK vs OpenAI Functions
**Rationale**: We chose the OpenAI Agents SDK over the simpler Functions API because the Agents SDK provides better support for complex multi-step interactions that are needed for a conversational todo bot. The Agents SDK also offers better context management for maintaining conversation history.

**Alternatives considered**:
- OpenAI Functions API (simpler but less flexible)
- Anthropic Claude Tools
- Self-hosted LLM with custom tool calling

## Decision: Database Schema for Conversations
**Rationale**: The decision to implement separate Conversation and Message tables is based on best practices for chat applications. This structure allows for efficient querying of conversation histories while maintaining proper relationships with user data.

**Alternatives considered**:
- Storing entire conversation history as JSON in a single field
- Embedding messages directly in the user record
- Using a document database instead of PostgreSQL

## Decision: Stateless Architecture Implementation
**Rationale**: Following the constitution's requirement for stateless architecture, we'll implement conversation state reconstruction from the database on each interaction. This enables horizontal scaling and ensures session continuity across server restarts.

**Alternatives considered**:
- Server-side session storage (violates constitution)
- Client-side state management (security concerns)
- Redis caching (adds complexity and violates stateless principle)

## Decision: Frontend Chat Interface
**Rationale**: Using OpenAI ChatKit provides a robust, tested chat interface that handles many UI complexities out of the box. It integrates well with OpenAI's ecosystem and provides a good user experience.

**Alternatives considered**:
- Building a custom chat interface from scratch
- Using other chat UI libraries like Gifted Chat
- Using React Markdown with custom message handling

## Decision: Authentication and User Isolation
**Rationale**: Leveraging Better Auth with JWT tokens provides secure, scalable authentication that integrates well with both frontend and backend. The JWT verification middleware ensures user isolation at the API level.

**Alternatives considered**:
- Session-based authentication
- OAuth providers only
- Custom authentication system