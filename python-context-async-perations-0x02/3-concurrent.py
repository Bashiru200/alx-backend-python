import asyncio
import aiosqlite
import os


db_path = os.path.join(os.path.dirname(__file__), '..', 'python-decorators-0x01', 'users.db')
db_path = os.path.abspath(db_path)

async def async_fetch_users():
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All user")
            for user in users:
                print(user)

# Function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in older_users:
                print(user)

# Function to run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())