"""
Script to check and fix database table issues
"""

import sqlite3
from backend.db.session import DATABASE_URL
import os

def check_and_fix_tables():
    print(f"Checking database: {DATABASE_URL}")
    
    # Extract database file path from URL
    db_path = DATABASE_URL.replace("sqlite:///", "")
    print(f"Database file: {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"All tables: {[table[0] for table in tables]}")
    
    # Check foreign key constraints
    cursor.execute("PRAGMA foreign_key_list(task);")
    fks = cursor.fetchall()
    print(f"Foreign keys in task table: {fks}")
    
    # If both 'user' and 'users' tables exist, we need to decide which one to keep
    if 'user' in [table[0] for table in tables] and 'users' in [table[0] for table in tables]:
        print("Both 'user' and 'users' tables exist. Need to fix this.")
        
        # Check which table the foreign key references
        for fk in fks:
            print(f"FK: {fk}")
            if fk[2] == 'user':
                print("Foreign key references 'user' table")
            elif fk[2] == 'users':
                print("Foreign key references 'users' table")
    
    conn.close()

if __name__ == "__main__":
    check_and_fix_tables()