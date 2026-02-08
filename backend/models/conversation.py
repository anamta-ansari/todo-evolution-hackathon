from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy import Column, Integer


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")