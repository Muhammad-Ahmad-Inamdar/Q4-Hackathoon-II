#!/usr/bin/env python3
"""
Simple script to test database connection with the new SQLite configuration
"""

import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'backend'))

from src.backend.app.database import engine
from sqlmodel import text

def test_database_connection():
    """Test if the database connection works"""
    print("Testing database connection...")

    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print(f"[SUCCESS] Database connection successful!")
            print(f"Result: {result.fetchone()}")

            # Also try to create tables
            from src.backend.app.database import create_tables
            create_tables()
            print("[SUCCESS] Tables created successfully!")

    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n[INFO] All database tests passed! The configuration looks good.")
    else:
        print("\n[ERROR] Database tests failed. Please check your configuration.")
        sys.exit(1)