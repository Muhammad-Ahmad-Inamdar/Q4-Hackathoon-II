#!/usr/bin/env python3
"""
Migration script to add priority and deadline fields to tasks table
Run this after updating the models to add new fields
"""
import sys
import os
from sqlalchemy import create_engine, text, inspect

# Add the app directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.database import engine

def check_column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def add_column_if_not_exists(table_name: str, column_name: str, column_type: str, default: str = None):
    """Add a column to a table if it doesn't exist"""
    if check_column_exists(table_name, column_name):
        print(f"  [OK] Column '{column_name}' already exists in '{table_name}'")
        return
    
    with engine.connect() as conn:
        alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        if default:
            alter_sql += f" DEFAULT {default}"
        
        conn.execute(text(alter_sql))
        conn.commit()
        print(f"  [OK] Added column '{column_name}' to '{table_name}'")

def migrate():
    """Run the migration"""
    print("=" * 60)
    print("Running Migration: Add priority and deadline fields to tasks")
    print("=" * 60)
    
    try:
        # Check if tasks table exists
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'task' not in tables:
            print("[ERROR] 'task' table does not exist!")
            print("   Please run create_db_tables.py first to create the database schema.")
            return False
        
        print("\n[INFO] Checking tasks table columns...")
        
        # Add priority column (VARCHAR with default 'normal')
        add_column_if_not_exists('task', 'priority', 'VARCHAR(20)', "'normal'")
        
        # Add deadline column (TIMESTAMP, nullable)
        # PostgreSQL uses TIMESTAMP instead of DATETIME
        add_column_if_not_exists('task', 'deadline', 'TIMESTAMP')
        
        print("\n[SUCCESS] Migration completed successfully!")
        print("\nSummary:")
        print("   - Added 'priority' column (VARCHAR(20), DEFAULT 'normal')")
        print("   - Added 'deadline' column (DATETIME, nullable)")
        print("\nNote: Existing tasks will have priority='normal' and deadline=NULL")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] During migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
