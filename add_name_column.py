import sqlite3

def add_name_column_to_user_table():
    """Add the missing name column to the user table"""
    conn = sqlite3.connect('todo_app.db')
    cursor = conn.cursor()
    
    try:
        # Check if the name column already exists
        cursor.execute("PRAGMA table_info(user);")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'name' not in columns:
            # Add the name column to the user table
            cursor.execute("ALTER TABLE user ADD COLUMN name TEXT;")
            print("Added 'name' column to user table")
        else:
            print("'name' column already exists in user table")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(user);")
        all_columns = cursor.fetchall()
        print("\nCurrent columns in user table:")
        for col in all_columns:
            print(f"  - {col[1]} ({col[2]})")
            
        conn.commit()
        print("\nDatabase schema updated successfully!")
        
    except Exception as e:
        print(f"Error updating database schema: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_name_column_to_user_table()