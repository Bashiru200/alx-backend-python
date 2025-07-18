import sqlite3 
from functools import wraps

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        finally:
            conn.close()
    return wrapper

@with_db_connection
def create_table(conn):
    """Create a users table."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    ''')

@with_db_connection
def insert_user(conn, name, age, email):
    """Insert a new user."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", (name, age, email))


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

__name__ = "__main__"
user = get_user_by_id(user_id=1 and 2)
print(user)