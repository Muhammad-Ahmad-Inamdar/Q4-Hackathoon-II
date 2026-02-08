#!/usr/bin/env python3
"""
Script to verify database tables exist in Neon PostgreSQL
"""
import os
from dotenv import load_dotenv
from sqlalchemy import inspect
from app.database import engine

load_dotenv()

def check_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("Database connection successful!")
    print(f"Tables found: {tables}")

    if 'user' in tables:
        print("[OK] Users table exists")
    else:
        print("[MISSING] Users table missing")

    if 'task' in tables:
        print("[OK] Tasks table exists")
    else:
        print("[MISSING] Tasks table missing")

if __name__ == "__main__":
    check_tables()