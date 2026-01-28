# Quickstart Guide: AI-Powered Todo Chatbot

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL-compatible database (Neon recommended)
- OpenAI API key
- Better Auth account

## Setup Instructions

### 1. Clone and Install Dependencies
```bash
git clone <repository-url>
cd todo-full-stack-web

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Environment Configuration
Create `.env` file in backend directory:
```env
DATABASE_URL=postgresql://username:password@host:port/database
BETTER_AUTH_SECRET=your_better_auth_secret
OPENAI_API_KEY=your_openai_api_key
```

Create `.env.local` file in frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_openai_domain_key
```

### 3. Database Setup
```bash
# Run database migrations to create Conversation and Message tables
python migrate_db.py
```

### 4. Run the Applications
Backend:
```bash
cd backend
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

### 5. Access the Application
- Frontend: http://localhost:3000
- Chat interface: http://localhost:3000/chat
- Backend API: http://localhost:8000/api

## Testing the Chatbot
1. Navigate to http://localhost:3000 and log in
2. Go to the chat interface at /chat
3. Try natural language commands like:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark task 1 as complete"
   - "Delete the meeting task"

## API Testing
Test the chat endpoint directly:
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}'
```

## Troubleshooting
- If you get JWT errors, ensure your token is valid and includes the user_id
- If the AI doesn't respond, check your OpenAI API key and connectivity
- If conversations aren't saving, verify database connection and permissions