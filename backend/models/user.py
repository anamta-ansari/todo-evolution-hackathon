from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
import re

# Handle circular import
if TYPE_CHECKING:
    from .task import Task

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')

    def validate_email(self):
        """Validate that the email follows a standard format"""
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")

class UserCreate(UserBase):
    password: str = Field(min_length=8)  # Require minimum 8 characters for password

class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class UserUpdate(UserBase):
    email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None, min_length=8)

class User(UserBase, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    password_hash: str = Field(nullable=False)  # Store hashed password
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Temporarily removing relationship to fix circular import issue
    # tasks: List["Task"] = Relationship(back_populates="user")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_email()