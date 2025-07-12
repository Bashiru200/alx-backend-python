import mysql.connector
from typing import Generator, Dict, List, Any


def stream_users_in_batches(
    batch_size: int = 50,
    host: str = "localhost",
    user: str = "root",
    password: str = "Bashir!@20",
    database: str = "ALX_prodev"
) -> Generator[List[Dict[str, Any]], None, None]:
    """Yield users in batches of size `batch_size` from the user_data table."""
    conn = mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    
    batch: List[Dict[str, Any]] = []

    try:
        for row in cursor:  # ✅ 1st loop
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch
    finally:
        if cursor.with_rows:
            cursor.fetchall()  # drain unread results
        cursor.close()
        conn.close()


def batch_processing(batch_size: int = 50) -> List[Dict[str, Any]]:
    """Process each batch and return users over age 25."""
    result = []

    for batch in stream_users_in_batches(batch_size):  # ✅ 2nd loop
        for user in batch:                              # ✅ 3rd loop
            if user["age"] > 25:
                result.append(user)

    return result


# Example usage
if __name__ == "__main__":
    filtered_users = batch_processing(50)
    print(f"Found {len(filtered_users)} users over age 25. Sample:")
    for user in filtered_users[:5]:
        print(user)
