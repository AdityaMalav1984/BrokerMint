import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'shared_data', 'brokermint.db')
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check users table
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("Users in database:")
    for user in users:
        print(user)
    
    conn.close()
else:
    print("Database file does not exist!")