import mysql.connector
from typing import Generator, Dict, Any


def stream_users(
    host: str = "localhost",
    user: str = "root",
    password: str = "Bashir!@20",
    database: str = "ALX_prodev",
) -> Generator[Dict[str, Any], None, None]:
    """Yield rows from the `user_data` table one by one without leaving unread results.

    Uses exactly one loop and makes sure the cursor is fully consumed before
    closing it, preventing the `InternalError: Unread result found` that occurs
    when the generator is closed early (e.g., via `islice`).
    """
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    try:
        while True:  # single loop
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    finally:
        # fetch remaining rows to avoid the 'Unread result' error
        if cursor.with_rows:
            cursor.fetchall()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    from itertools import islice

    for user in islice(stream_users(), 6):
        print(user)
