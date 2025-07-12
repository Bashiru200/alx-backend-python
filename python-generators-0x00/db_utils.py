# db_utils.py
import mysql.connector
from mysql.connector import Error


def connect_db(host="localhost", user="root", password="Bashir!@20"):
    """Connect to the default MySQL server (no specific DB)."""
    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
    except Error as err:
        print(f"Connection error: {err}")
        return None


def connect_to_prodev(host="localhost", user="root", password="Bashir!@20", db="ALX_prodev"):
    """Connect to the ALX_prodev database once it exists."""
    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
    except Error as err:
        print(f"Connection error: {err}")
        return None


def create_database(conn, db_name="ALX_prodev"):
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} "
                   "DEFAULT CHARACTER SET utf8mb4 "
                   "DEFAULT COLLATE utf8mb4_unicode_ci;")
    cursor.close()


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36)      NOT NULL,
            name    VARCHAR(50)   NOT NULL,
            email   VARCHAR(100)  NOT NULL,
            age     TINYINT UNSIGNED NOT NULL,
            PRIMARY KEY (user_id),
            UNIQUE KEY uq_user_data_email (email)
        ) ENGINE=InnoDB
          DEFAULT CHARSET=utf8mb4
          COLLATE=utf8mb4_unicode_ci;
    """)
    cursor.close()


def insert_data(conn, csv_path):
    import csv, uuid
    cursor = conn.cursor()
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (str(uuid.uuid4()), row["name"], row["email"], int(row["age"]))
            for row in reader
        ]
    cursor.executemany(
        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
        rows
    )
    conn.commit()
    cursor.close()
