"""
Test script to reproduce and fix the signup issue
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.api.auth import signup
from backend.models.user import UserCreate
from backend.db.session import get_session
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

def test_signup():
    # Create a test user
    user_data = UserCreate(email='test@example.com', password='password123')

    # Get session
    session_gen = get_session()
    session = next(session_gen)

    try:
        print("Attempting to signup user...")
        result = signup(user_data, session)
        print('Signup successful:', result)
        return True
    except IntegrityError as e:
        print('IntegrityError occurred:', str(e))
        return False
    except Exception as e:
        print('Other error occurred:', str(e))
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    test_signup()