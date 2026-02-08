from sqlmodel import create_engine, Session
from .models import User, Task  # Import all models to register them
import os
from fastapi import Depends
from typing import Generator
from dotenv import load_dotenv

# Load environment variables if not already loaded
if not os.getenv("DATABASE_URL"):
    load_dotenv()

# Determine if we're using SQLite or PostgreSQL based on the URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        echo=False  # Set to True for debugging
    )
else:
    # PostgreSQL configuration
    from sqlalchemy.pool import QueuePool
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False  # Disable for production
    )

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def create_tables():
    """Create all tables in the database"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)