import sqlite3 
from functools import wraps

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):


@with_db_connection
def get_user_by_id(user_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()