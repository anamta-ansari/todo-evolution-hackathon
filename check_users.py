import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db.session import get_session
from backend.models.user import User
from sqlmodel import select

def check_users():
    session_gen = get_session()
    session = next(session_gen)

    try:
        # Query all users
        statement = select(User)
        users = session.exec(statement).all()
        
        print('Users in database:')
        for user in users:
            print(f'ID: {user.id}, Email: {user.email}, Created: {user.created_at}')
            
    finally:
        session.close()

if __name__ == '__main__':
    check_users()