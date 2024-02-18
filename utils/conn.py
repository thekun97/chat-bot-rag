import os
from motor.motor_asyncio import AsyncIOMotorClient


async def init_mongo():
    mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    mongo_database = mongo_client[os.getenv("MONGO_DBNAME")]
    # mongo_collections = {
    #     collection: mongo_database.get_collection(collection),
    # }
    # return {0: mongo_client, 1: mongo_database, 2: mongo_collections}
    return mongo_client, mongo_database
