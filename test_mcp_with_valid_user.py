import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.mcp.tools import add_task_tool
from backend.db.session import engine
from backend.models.user import User
from sqlmodel import Session, select

# First, let's get a valid user from the database
with Session(engine) as session:
    # Get the first user in the database
    user = session.exec(select(User)).first()
    
    if user:
        print(f"Found user: ID={user.id}, Email={user.email}")
        
        print("Testing add_task MCP tool with valid user...")
        try:
            result = add_task_tool(
                user_id=str(user.id),  # Using the actual user ID from the database
                title="Buy groceries",
                description="Milk, bread, eggs"
            )
            print(f"✅ MCP tool works: {result}")
        except Exception as e:
            print(f"❌ MCP tool error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ No users found in the database. You need to create a user first.")