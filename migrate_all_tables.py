"""
Migration script to create all necessary database tables
"""

from backend.db.session import engine
from backend.models.user import User
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message
from sqlmodel import SQLModel

def create_all_tables():
    print("Starting database migration to create all tables...")

    try:
        # Create all tables
        SQLModel.metadata.create_all(bind=engine)
        print("All database tables created successfully!")

        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")

        # Check for required tables
        required_tables = ["user", "task", "conversations", "messages"]
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"Warning: Missing tables: {missing_tables}")
        else:
            print("All required tables are present!")

    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    create_all_tables()