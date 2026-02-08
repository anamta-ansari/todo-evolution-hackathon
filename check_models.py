from backend.models.user import User
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message
from sqlmodel import SQLModel
import inspect

print("User model info:")
print(f"  Table name: {User.__tablename__}")
print(f"  Fields: {[field for field in User.__fields__]}")
print(f"  Primary keys: {[key for key in User.__table__.primary_key.columns.keys()]}")

print("\nTask model info:")
print(f"  Table name: {Task.__tablename__}")
print(f"  Fields: {[field for field in Task.__fields__]}")
print(f"  Primary keys: {[key for key in Task.__table__.primary_key.columns.keys()]}")

print("\nConversation model info:")
print(f"  Table name: {Conversation.__tablename__}")
print(f"  Fields: {[field for field in Conversation.__fields__]}")
print(f"  Primary keys: {[key for key in Conversation.__table__.primary_key.columns.keys()]}")

print("\nMessage model info:")
print(f"  Table name: {Message.__tablename__}")
print(f"  Fields: {[field for field in Message.__fields__]}")
print(f"  Primary keys: {[key for key in Message.__table__.primary_key.columns.keys()]}")

print(f"\nAll tables in metadata: {list(SQLModel.metadata.tables.keys())}")