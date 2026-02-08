"""
Script to properly reset the database schema for PostgreSQL
"""
import os
from sqlmodel import SQLModel, create_engine
from backend.models.user import User
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Dropping and recreating tables in: {DATABASE_URL}")

# Create engine
engine = create_engine(DATABASE_URL)

# Drop all tables
print("Dropping all tables...")
SQLModel.metadata.drop_all(engine)

# Create all tables
print("Creating all tables...")
SQLModel.metadata.create_all(engine)

print("Tables created successfully!")