import sqlite3

def check_database():
    conn = sqlite3.connect('todo_app.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print('Tables in database:')
    for table in tables:
        print(f'  - {table[0]}')
        
        # Get columns for user table if it exists
        if 'user' in table[0].lower():
            cursor.execute(f'PRAGMA table_info([{table[0]}]);')
            columns = cursor.fetchall()
            print('  Columns in user table:')
            for col in columns:
                print(f'    - {col[1]} ({col[2]}) type={col[2]}, not_null={col[3]}, default={col[4]}, pk={col[5]}')
    
    conn.close()

if __name__ == "__main__":
    check_database()