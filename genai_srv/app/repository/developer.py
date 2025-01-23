from typing import Protocol
from bson import ObjectId
from bson.errors import InvalidId

from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.main import db
from app.model.developer import Developer

DEVELOPER_COLLECTION_NAME = "developer"


class DeveloperRepositoryProtocol(Protocol):
    async def new(self, developer: Developer) -> Developer | None: ...

    async def get(self, id: str) -> Developer | None: ...

    async def get_all(self) -> list[Developer]: ...


class MongoDeveloperRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def new(self, developer: Developer) -> Developer | None:
        db_developer = await self.collection.find_one({"user_id": developer.user_id})

        if not db_developer:
            new_developer = developer.model_dump()
            del new_developer["id"]
            result = await self.collection.insert_one(new_developer)
            developer.id = str(result.inserted_id)
            return developer

        return None

    async def get(self, id: str) -> Developer | None:
        try:
            if developer := await self.collection.find_one({"_id": ObjectId(id)}):
                return Developer.from_dict(developer)
        except InvalidId:
            raise ValueError(f"invalid developer id: {id}")

        return None

    async def get_all(self) -> list[Developer]:
        result = await self.collection.find({}).sort({"_id": -1}).to_list()
        print("--" * 20, result)
        return [Developer.from_dict(a) for a in result]


developer_repository = MongoDeveloperRepository(
    collection=db[DEVELOPER_COLLECTION_NAME]
)
