import sqlite3
import os

# Connect to the database
db_path = os.path.join('G:', 'phase-II', 'Todo-AI-Chatbot', 'todo_app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Checking database schema...")

# Get all table schemas
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\nAll table schemas:")
for table_name, table_sql in tables:
    print(f"\nTable '{table_name}':")
    print(table_sql)

# Specifically check the user table
print("\n" + "="*50)
print("USER TABLE DETAILS:")
cursor.execute("PRAGMA table_info(user);")
columns = cursor.fetchall()
print("Columns in user table:")
for col in columns:
    cid, name, type_, notnull, default_value, pk = col
    print(f"  {name}: {type_} | NOT NULL: {bool(notnull)} | DEFAULT: {default_value} | PK: {bool(pk)}")

# Check user data
print("\nUser data:")
cursor.execute("SELECT * FROM user;")
users = cursor.fetchall()
for user in users:
    print(user)

conn.close()