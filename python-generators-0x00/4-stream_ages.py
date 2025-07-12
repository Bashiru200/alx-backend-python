import mysql.connector
from typing import Generator, Dict, Any


def stream_ages(
    host: str = "localhost",
    user: str = "root",
    password: str = "Bashir!@20",
    database: str = "ALX_prodev",
) -> Generator[Dict[str, Any], None, None]:
    """Yield ages from `user_data` **over 25** one‑by‑one (exactly one loop)."""
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    try:
        for row in cursor:                     # 1️⃣ single loop
            if row["age"] > 25:                # filter correctly
                print({row['age']})  # optional side‑effect
                yield row                      # use yield so the caller gets the data
    finally:
        if cursor.with_rows:
            cursor.fetchall()
        cursor.close()                         # no unread rows left
        conn.close()


if __name__ == "__main__":
    from itertools import islice

    for age_row in islice(stream_ages(), 6):
        print(age_row)
