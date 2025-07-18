import sqlite3
from functools import wraps

def insert_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        result = func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper

@insert_data
def insert_user(cursor, name, age, email):
    """Insert a new user."""
    cursor.execute("INSERT INTO users (name, age, email) Values (?, ?, ?)",(name, age, email))
    return "user inserted successfully."

if __name__ == "__main__":
    result = insert_user("Bashiru Barry", 30, "bash23@gmail.com")
    print(result)