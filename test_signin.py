import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.api.auth import signin, Credentials
from backend.db.session import get_session
from sqlmodel import Session

def test_signin():
    # Test signing in with the user created in the previous test
    credentials = Credentials(email='test1@example.com', password='password123')

    # Get session
    session_gen = get_session()
    session = next(session_gen)

    try:
        print("Attempting to signin user...")
        result = signin(credentials, session)
        print('Signin successful:', result)
        return True
    except Exception as e:
        print('Signin failed:', str(e))
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    test_signin()