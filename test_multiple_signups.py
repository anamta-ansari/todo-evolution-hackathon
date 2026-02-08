"""
Test script to reproduce and fix the signup issue - multiple attempts
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.api.auth import signup
from backend.models.user import UserCreate
from backend.db.session import get_session
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

def test_multiple_signups():
    # Test first signup
    user_data1 = UserCreate(email='test1@example.com', password='password123')
    
    # Get session
    session_gen = get_session()
    session = next(session_gen)

    try:
        print("Attempting first signup...")
        result1 = signup(user_data1, session)
        print('First signup successful:', result1)
        
        # Close session and get a new one for second signup
        session.close()
        session_gen = get_session()
        session = next(session_gen)
        
        # Test second signup with different email
        user_data2 = UserCreate(email='test2@example.com', password='password123')
        print("Attempting second signup...")
        result2 = signup(user_data2, session)
        print('Second signup successful:', result2)
        
        # Try to signup the same user again (should fail)
        print("Attempting duplicate signup (should fail)...")
        try:
            result3 = signup(user_data1, session)  # Using same email as first
            print('Duplicate signup unexpectedly succeeded:', result3)
        except Exception as e:
            print('Duplicate signup correctly failed:', str(e))
            
        return True
    except Exception as e:
        print('Error occurred:', str(e))
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    test_multiple_signups()