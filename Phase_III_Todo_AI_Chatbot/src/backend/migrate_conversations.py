"""
Database migration script for adding conversation tables to Neon DB.

This script creates the conversations and messages tables in the PostgreSQL database
configured via DATABASE_URL in .env file.

Usage:
    python -m src.backend.migrate_conversations
    
Or from src/backend directory:
    python migrate_conversations.py
"""
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in .env file")
    sys.exit(1)

print(f"Database URL: {DATABASE_URL[:50]}...")  # Show partial URL for verification

# Import models AFTER setting up path - this registers them with SQLModel metadata
from app.models import Conversation, Message, User, Task


def create_conversation_tables():
    """Create conversations and messages tables in the database"""
    print(f"\nConnecting to database...")
    
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
            echo=True  # Enable SQL logging for debugging
        )

    print("\nCreating conversations and messages tables...")
    
    # Create all tables (User, Task, Conversation, Message)
    # SQLModel will only create tables that don't exist
    SQLModel.metadata.create_all(engine)

    print("\n[OK] Tables created/verified successfully!")
    print("\nTables:")
    print("  - user (existing)")
    print("  - task (existing)")
    print("  - conversations (new)")
    print("  - messages (new)")
    
    # Verify tables exist
    print("\nVerifying table structure...")
    with engine.connect() as conn:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nExisting tables: {tables}")
        
        if 'conversations' in tables:
            print("[OK] conversations table exists")
            cols = [col['name'] for col in inspector.get_columns('conversations')]
            print(f"  Columns: {cols}")
        else:
            print("[FAIL] conversations table NOT found")
            
        if 'messages' in tables:
            print("[OK] messages table exists")
            cols = [col['name'] for col in inspector.get_columns('messages')]
            print(f"  Columns: {cols}")
        else:
            print("[FAIL] messages table NOT found")
    
    print("\n[OK] Migration complete!")


if __name__ == "__main__":
    create_conversation_tables()
