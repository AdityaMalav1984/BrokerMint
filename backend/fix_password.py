import sqlite3
import bcrypt
import os

# Connect to database
db_path = os.path.join(os.path.dirname(__file__), '..', 'shared_data', 'brokermint.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Generate correct hash for password "admin"
password = "admin"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print(f"Password: {password}")
print(f"Hash: {hashed_password}")

# Update the admin user
cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (hashed_password,))
conn.commit()

# Verify the update
cursor.execute("SELECT username, password_hash FROM users WHERE username = 'admin'")
user = cursor.fetchone()
print(f"Updated user: {user}")

conn.close()
print("Admin password has been reset to 'admin'")