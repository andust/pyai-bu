import motor.motor_asyncio
import motor

from app.config.envirenment import get_settings

_S = get_settings()


client = motor.motor_asyncio.AsyncIOMotorClient(_S.MONGO_CONNECTION)
db = client[_S.MONGO_DB]
# items_collection = db["items"]
# chats_collection = db["chats"]
