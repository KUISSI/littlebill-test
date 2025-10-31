from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["hiboutik_data"]