from contextlib import asynccontextmanager
from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config.envirenment import get_settings

_S = get_settings()

client = AsyncIOMotorClient(_S.MONGO_CONNECTION)
db = client[_S.MONGO_DB]



@asynccontextmanager
async def new_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:

    try:
        new_client = AsyncIOMotorClient(_S.MONGO_CONNECTION)
        new_db = new_client[_S.MONGO_DB]
        yield new_db
    finally:
        new_db.client.close()
