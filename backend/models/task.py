from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer

# Handle circular import
if TYPE_CHECKING:
    from .user import User

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    complete: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[datetime] = Field(default=None)

    def validate_title(self):
        """Validate that the title does not exceed 255 characters"""
        if len(self.title) > 255:
            raise ValueError("Title must not exceed 255 characters")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)
    complete: Optional[bool] = Field(default=None)
    priority: Optional[PriorityEnum] = Field(default=None)
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[datetime] = Field(default=None)

class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Task(TaskBase, table=True):
    __tablename__ = "task"

    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Temporarily removing relationship to fix circular import issue
    # user: "User" = Relationship(back_populates="tasks")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_title()