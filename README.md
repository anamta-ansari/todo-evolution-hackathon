# Todo-AI-Chatbot

An AI-powered todo chatbot application with MCP architecture.

## Prerequisites

- Python 3.8+
- Node.js 18+
- A Google Gemini API key (optional, for AI features)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with your configuration:
```env
DATABASE_URL=sqlite:///./todo_app.db
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Start the backend server:
```bash
python -m uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install JavaScript dependencies:
```bash
npm install
```

3. Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the frontend development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Usage

1. Make sure both backend and frontend servers are running
2. Visit `http://localhost:3000` in your browser
3. Register an account or log in if you already have one
4. Use the floating chat button to interact with the AI assistant
5. Ask the AI to add, list, complete, or delete tasks

## Troubleshooting

### Common Issues

#### "Failed to fetch" error
- Make sure the backend server is running on `http://localhost:8000`
- Verify that `NEXT_PUBLIC_API_URL` in `.env.local` is set to `http://localhost:8000`
- Check that CORS is properly configured in the backend

#### "No authentication token found" error
- Make sure you're logged in before using the chat feature
- Verify that the authentication token is stored in localStorage after login
- Check that the token hasn't expired

#### Rate limiting issues
- The system has rate limiting to prevent abuse (120 requests per minute per IP for development)
- If you're testing extensively, you might hit the rate limit
- The system implements exponential backoff with jitter for Gemini API rate limits
- For production use, consider adjusting these values based on your needs
- Wait a minute before continuing if you receive a 429 error

### Testing the Backend

You can test the backend functionality using the test page:
1. Make sure the backend server is running
2. Visit `http://localhost:3000/test-chat` in your browser
3. Click "Run Tests" to verify all components are working

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/signin` - User login
- `POST /api/{user_id}/chat` - Chat endpoint with AI integration
- `GET /api/v1/users/{user_id}/tasks` - Get user tasks
- `POST /api/v1/users/{user_id}/tasks` - Create a new task
- `PUT /api/v1/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/v1/users/{user_id}/tasks/{task_id}` - Delete a task

## Architecture

This application follows the MCP (Model-Controller-Protocol) architecture pattern with:
- FastAPI backend with SQLModel for database operations
- Next.js frontend with React
- Google Gemini API for AI capabilities
- Rate limiting for security
- JWT-based authentication