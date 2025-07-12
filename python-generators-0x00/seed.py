# seed.py
from db_utils import (
    connect_db,
    connect_to_prodev,
    create_database,
    create_table,
    insert_data,
)

def main():
    # ── 1. connect without DB and create it ────────────────────────────
    conn = connect_db()
    if not conn:
        return
    create_database(conn)
    conn.close()
    print("✅ Database created (or already existed)")

    # ── 2. connect to the new DB and set it up ─────────────────────────
    conn = connect_to_prodev()
    if not conn:
        return
    create_table(conn)
    insert_data(conn, "user_data.csv")
    print("✅ Table created and data inserted")

    # ── 3. quick sanity checks ─────────────────────────────────────────
    cur = conn.cursor()
    cur.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                "WHERE SCHEMA_NAME = 'ALX_prodev';")
    if cur.fetchone():
        print("🎉 Database ALX_prodev is present")

    cur.execute("SELECT * FROM user_data LIMIT 5;")
    print("Sample rows:", cur.fetchall())
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
