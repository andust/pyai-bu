from typing import Protocol
from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.main import db
from app.model.chat import Chat

CHAT_COLLECTION_NAME = "chat"


class ChatRepositoryProtocol(Protocol):
    async def new(self, user_id: str) -> Chat | None: ...

    async def get(self, id: str) -> Chat | None: ...

    async def get_all(self) -> list[Chat]: ...

    async def update(self, id: str, data: Chat) -> Chat | None: ...

    async def delete(self, id: str) -> bool: ...


class MongoChatRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def new(self, user_id: str) -> Chat | None:
        db_chat = await self.collection.find_one(
            {"user_id": user_id, "questions": None}
        )
        if not db_chat:
            new_chat = Chat(user_id=user_id)
            dump_data = new_chat.model_dump()
            del dump_data["id"]
            result = await self.collection.insert_one(dump_data)
            new_chat.id = str(result.inserted_id)

            return new_chat

        return Chat.from_dict(db_chat)

    async def get(self, id: str) -> Chat | None:
        if document := await self.collection.find_one({"_id": ObjectId(id)}):
            return Chat.from_dict(document)
        return

    async def get_all(self) -> list[Chat]:
        result = await self.collection.find({}).sort({"_id": -1}).to_list()
        return [Chat.from_dict(a) for a in result]

    async def update(self, id: str, data: Chat) -> Chat | None:
        document = data.model_dump(exclude_unset=True, by_alias=True)
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": document}
        )
        if result.modified_count:
            return await self.get(id)
        return

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one(
            {"_id": ObjectId(id)},
        )
        if result.deleted_count:
            return True
        return False


chat_repository = MongoChatRepository(collection=db[CHAT_COLLECTION_NAME])
