import sys
import asyncio
import os

# Add the current directory to the Python path to resolve import issues
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Windows asyncio compatibility fix
# This must be at the very top before any other imports
if sys.platform == 'win32':
    # Use WindowsSelectorEventLoopPolicy for better compatibility
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.db.session import engine
from backend.models.user import User
from backend.models.task import Task
from sqlmodel import SQLModel
from backend.api.health import router as health_router
from backend.api.auth import router as auth_router
from backend.api.tasks import router as tasks_router
from backend.routes.chat import router as chat_router

# Import both models to ensure they're registered with SQLAlchemy
from backend.models import user, task, conversation, message

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    SQLModel.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed
    pass

# Create FastAPI app with lifespan
app = FastAPI(
    title="Todo Backend - Phase III",
    description="AI-Powered Todo Chatbot with MCP Architecture",
    version="3.0.0",
    lifespan=lifespan
)

# Configure CORS for localhost with common ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
        "http://localhost:3002",
        "http://127.0.0.1:3002"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health_router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(chat_router, prefix="")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Backend API - Phase III"}