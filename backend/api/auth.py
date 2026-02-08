# backend/api/auth.py
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from backend.db.session import get_session
from backend.models.user import User, UserCreate, UserRead
from backend.dependencies.auth import (
    create_access_token,
    create_refresh_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)
import bcrypt
from typing import Dict
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class Credentials(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # Convert strings to bytes for bcrypt
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    # Bcrypt has a 72 character limit, so we truncate if necessary
    # Ensure we handle the password properly before passing to bcrypt
    if len(password) > 72:
        # Take the first 72 characters to stay within bcrypt limits
        password = password[:72]
    # Convert string to bytes for bcrypt
    password_bytes = password.encode('utf-8')
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Convert back to string for storage
    return hashed.decode('utf-8')

from fastapi.responses import JSONResponse

# Define response model for signup
class SignUpResponse(BaseModel):
    user: UserRead
    access_token: str
    refresh_token: str
    token_type: str

@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    """Create a new user account"""
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create new user
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        name=user.name
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Create JWT tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": db_user.id, "email": db_user.email},
        expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(
        data={"user_id": db_user.id, "email": db_user.email}
    )

    # Return user data with tokens
    user_response = UserRead.model_validate(db_user)
    return {
        "user": user_response,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# Define response model for signin
class SignInResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id: int
    email: str

@router.post("/signin", response_model=SignInResponse)
def signin(credentials: Credentials, session: Session = Depends(get_session)):
    """Authenticate a user and return JWT tokens"""
    # Find user by email
    user = session.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(
        data={"user_id": user.id, "email": user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/refresh")
def refresh_access_token(request: RefreshTokenRequest):
    """Refresh the access token using a refresh token"""
    # Decode and verify the refresh token
    try:
        # Verify that this is a refresh token specifically
        payload = verify_token(request.refresh_token, expected_token_type="refresh")
        user_id = payload.get("user_id")
        email = payload.get("email")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate refresh token"
            )

        # Create a new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"user_id": user_id, "email": email},
            expires_delta=access_token_expires
        )

        # Also generate a new refresh token to rotate it
        new_refresh_token = create_refresh_token(
            data={"user_id": user_id, "email": email}
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
def logout():
    """Logout endpoint (client-side token removal is sufficient)"""
    # In a real application, you might want to add the token to a blacklist
    # For now, we just confirm the logout
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserRead)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get the profile of the currently authenticated user"""
    return current_user