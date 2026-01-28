"""
Simple test to verify database connectivity and table creation
"""

from sqlmodel import SQLModel, Field, Session
from backend.db.session import engine
from backend.models.user import User
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message

def test_db_connection():
    print("Testing database connection and table creation...")
    
    # Create all tables as done in main.py
    SQLModel.metadata.create_all(bind=engine)
    print("Tables created/verified successfully")
    
    # Test inserting a user
    with Session(engine) as session:
        # Check if test user exists
        existing_user = session.get(User, "test_user_123")
        if not existing_user:
            # Create a test user
            test_user = User(
                id="test_user_123",
                email="test@example.com",
                password_hash="dummy_hash"
            )
            session.add(test_user)
            session.commit()
            print("Test user created successfully")
        else:
            print("Test user already exists")
    
    print("Database connection test completed successfully!")

if __name__ == "__main__":
    test_db_connection()