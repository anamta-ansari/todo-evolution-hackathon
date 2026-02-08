import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.db.session import engine
from backend.models.user import User
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message
from sqlmodel import SQLModel

# Create all tables
SQLModel.metadata.create_all(bind=engine)

print("Tables created successfully!")
print("Checking if user table exists...")
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables in database: {tables}")

if 'user' in tables:
    columns = inspector.get_columns('user')
    print(f"Columns in user table: {[col['name'] for col in columns]}")
    
if 'task' in tables:
    columns = inspector.get_columns('task')
    print(f"Columns in task table: {[col['name'] for col in columns]}")
    
    # Get foreign key info
    fks = inspector.get_foreign_keys('task')
    print(f"Foreign keys in task table: {fks}")