import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db.session import get_session
from backend.models.user import User
from sqlmodel import text
from sqlalchemy.exc import OperationalError

def check_db_schema():
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Query the database schema using raw SQL
        result = session.exec(text("SELECT name, sql FROM sqlite_master WHERE type='table';"))
        tables = result.all()
        print("All table schemas:")
        for table in tables:
            print(f"\nTable '{table.name}':")
            print(table.sql)
        
        print("\n" + "="*50)
        print("USER TABLE DETAILS:")
        # Get column info for user table
        result = session.exec(text("PRAGMA table_info(user);"))
        columns = result.all()
        print("Columns in user table:")
        for col in columns:
            print(f"  {col.name}: {col.type} | NOT NULL: {col.notnull} | DEFAULT: {col.dflt_value} | PK: {col.pk}")
        
        # Check if there are any users
        result = session.exec(text("SELECT * FROM user;"))
        users = result.all()
        print(f"\nNumber of users in table: {len(users)}")
        for user in users:
            print(user)
            
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_db_schema()