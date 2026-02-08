import traceback
from backend.main import app
from backend.api.auth import signup
from backend.models.user import UserCreate
from backend.db.session import get_session
from sqlmodel import Session

def test_user_creation():
    try:
        # Create a mock user
        user_data = UserCreate(email="testuser@example.com", password="SecurePassword123!")
        
        # Get a session
        session_gen = get_session()
        session = next(session_gen)
        
        # Try to call signup function directly
        result = signup(user_data, session)
        print("Signup successful:", result)
        
    except Exception as e:
        print("Error during signup:")
        print(traceback.format_exc())
        print("\nError:", str(e))

if __name__ == "__main__":
    test_user_creation()