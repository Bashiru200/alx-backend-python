import sqlite3
import os

# # Build the correct path to the database file
db_path = os.path.join(os.path.dirname(__file__), '..', 'python-decorators-0x01', 'users.db')
db_path = os.path.abspath(db_path)


class ExecuteQuery:
    def __init__(self, db_npath):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    with ExecuteQuery(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WhERE age > ?", [25])
        results = cursor.fetchall()
        print("Users older than 25:")
        for row in results:
            print(row)