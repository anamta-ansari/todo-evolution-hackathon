from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlalchemy import Column, Integer


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    user_id: int = Field(foreign_key="user.id", index=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: MessageRole
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")