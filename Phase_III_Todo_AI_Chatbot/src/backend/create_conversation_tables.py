"""
Database migration script for adding conversation tables.
Run this script to create conversations and messages tables.
"""
import sys
import os

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel, create_engine
from backend.models.conversation_model import Conversation
from models.message import Message
from models import User, Task  # Import existing models for reference
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

def create_conversation_tables():
    """Create conversations and messages tables"""
    print(f"Connecting to database: {DATABASE_URL}")
    
    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=True
        )
    else:
        from sqlalchemy.pool import QueuePool
        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_pre_ping=True,
            echo=True
        )
    
    print("Creating conversations and messages tables...")
    # Create only Conversation and Message tables
    Conversation.metadata.create_all(engine)
    Message.metadata.create_all(engine)

    print("[OK] Tables created successfully!")
    print("  - conversations")
    print("  - messages")

if __name__ == "__main__":
    create_conversation_tables()
