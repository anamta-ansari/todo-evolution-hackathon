import os
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel
from backend.models.user import User
from backend.models.task import Task

# Use absolute path directly
DATABASE_URL = "sqlite:///G:/TODO-FULL-STACK-WEB/todo_app.db"

# For SQLite, we need to use StaticPool and check_same_thread
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30
        },
        poolclass=StaticPool,
        echo=True,
        pool_pre_ping=True
    )
else:
    engine = create_engine(DATABASE_URL)

print("Testing database connection with absolute path...")

# Create a test user first
try:
    with Session(engine) as session:
        # Check if test user exists
        existing_user = session.get(User, "test_user_123")
        if not existing_user:
            test_user = User(
                id="test_user_123",
                email="test@example.com",
                password_hash="hashed_password_here"
            )
            session.add(test_user)
            session.commit()
            print("Created test user")
        else:
            print("Test user already exists")
            
        # Now test creating a task
        from backend.models.task import Task
        test_task = Task(
            user_id="test_user_123",
            title="Test task from direct connection",
            description="Testing direct database connection"
        )
        session.add(test_task)
        session.commit()
        print(f"Created task with ID: {test_task.id}")
        
        # Query tasks for the user
        tasks = session.query(Task).filter(Task.user_id == "test_user_123").all()
        print(f"Found {len(tasks)} tasks for user")
        
except Exception as e:
    print(f"ERROR: Database operation failed: {e}")
    import traceback
    traceback.print_exc()

print("Direct database test completed!")