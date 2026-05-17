import os

from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "team_management")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB]
teams_collection = db["teams"]
