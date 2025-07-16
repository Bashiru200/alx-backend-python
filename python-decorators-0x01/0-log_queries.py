import sqlite3
from functools import wraps

def log_queries(func):
    """Decorator: detect a SQL statement in *args/**kwargs and log it."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        query = None

        # ── 1. Look in positional arguments
        for arg in args:
            if isinstance(arg, str) and arg.strip().lower().startswith(
                ("select", "insert", "delete", "create", "drop")
            ):
                query = arg
                break

        # ── 2. Look in keyword arguments (if not found yet)
        if query is None:
            for val in kwargs.values():
                if isinstance(val, str) and val.strip().lower().startswith(
                    ("select", "insert", "delete", "create", "drop", "update", "alter")
                ):
                    query = val
                    break

        # ── 3. Log and call the wrapped function
        if query:
            print(f"Executing query: {query}")
        return func(*args, **kwargs)   # ← call the real function
    return wrapper                     # ← return wrapper (not None!)

# ---------------------------------------------------
@log_queries
def fetch_all_users(query: str):
    """Run the provided SQL query and return all rows."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor(create_table_sql)            # ← typo fixed (cursor, not cusor)
    cursor.execute(query,)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Example call
if __name__ == "__main__":
    users = fetch_all_users("SELECT * FROM users WHERE id = ?", (user_id,))
    print(users)