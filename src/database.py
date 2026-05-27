import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import json_util

file_path = os.path.dirname(__file__)
OUTPUT_FILE = f"{file_path}/../data/data.json"
BATCH_SIZE = 20


async def connect():
    load_dotenv()
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    return client[os.getenv("DB_NAME", "")]



async def fetch():
    db = await connect()
    collection = db[os.getenv("COLLECTION_NAME", "")]
    total = await collection.count_documents({})
    query = {}
    processed = 0
    cursor = collection.find(query).sort("_id", 1).batch_size(BATCH_SIZE)
    print(f"Fetching in batches of {BATCH_SIZE} elements.")
    print(f"Fetched documents: {processed}/{total} ({round((processed/total)*100, 2)}%)", end="\r")
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        async for doc in cursor:
            f.write(json_util.dumps(doc) + ",\n")
            processed += 1
            print(f"Fetched documents: {processed}/{total} ({round((processed/total)*100, 2)}%)", end="              \r")

    print("\nDone")


if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("[")
    asyncio.run(fetch())
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write("]")