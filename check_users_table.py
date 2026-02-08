#!/usr/bin/env python3
"""
Check user table in the database using the proper SQLModel connection
"""

from backend.db.session import get_session
from backend.models.user import User
from sqlmodel import select
from sqlalchemy.exc import OperationalError


def check_users_table():
    print("Checking users table...")
    
    try:
        # Get a database session
        session_generator = get_session()
        session = next(session_generator)
        
        # Try to query the users table
        statement = select(User)
        results = session.exec(statement)
        users = results.all()
        
        print(f"Found {len(users)} users in the database:")
        for user in users:
            print(f"- ID: {user.id}, Email: {user.email}, Created: {user.created_at}")
            
    except OperationalError as e:
        print(f"Database error: {e}")
        print("The table may not exist yet.")
    except Exception as e:
        print(f"Error checking users table: {e}")
    finally:
        try:
            session.close()
        except:
            pass


if __name__ == "__main__":
    check_users_table()