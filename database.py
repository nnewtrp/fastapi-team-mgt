import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URI = os.environ["MONGODB_URI"]
MONGODB_DB = os.environ["MONGODB_DB"]

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB]
teams_collection = db["teams"]
members_collection = db["members"]
