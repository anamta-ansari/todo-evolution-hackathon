import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.main import app
from backend.db.session import engine
from sqlmodel import SQLModel

print("Testing startup event manually...")

try:
    # Create all tables (this is what happens in the startup event)
    SQLModel.metadata.create_all(bind=engine)
    print("OK: Tables created successfully")
except Exception as e:
    print(f"ERROR: Failed to create tables: {e}")

print("Manual startup test completed")