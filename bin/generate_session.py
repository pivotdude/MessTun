from pyrogram import Client
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")


async def generate_session_string():
    async with Client("temp_session", API_ID, API_HASH) as app:
        session_string = await app.export_session_string()
        print(f"Pyrogram session string:")
        print(session_string)
        return session_string


if __name__ == "__main__":
    import asyncio

    asyncio.run(generate_session_string())
