#!/usr/bin/env python3
"""
Script to create database tables in SQLite
"""
import sys
import os

# Add the app directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Set the environment to use the SQLite database
os.environ.setdefault('DATABASE_URL', os.getenv('DATABASE_URL', 'sqlite:///./todo_app.db'))

from app.database import create_tables

if __name__ == "__main__":
    print("Creating database tables...")
    try:
        create_tables()
        print("SUCCESS: Database tables created successfully!")
        print("Tables created: users, tasks")
    except Exception as e:
        print(f"ERROR creating tables: {e}")
        sys.exit(1)