from typing import Protocol
from bson import ObjectId
from bson.errors import InvalidId

from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.main import db
from app.model.estimation_feed import EstimationFeed

ESTIMATION_FEED_COLLECTION_NAME = "estimation_feed"


class EstimationFeedRepositoryProtocol(Protocol):
    async def new(self, estimation_feed: EstimationFeed) -> EstimationFeed | None: ...

    async def get(self, id: str) -> EstimationFeed | None: ...

    async def get_all(self) -> list[EstimationFeed]: ...


class MongoEstimationFeedRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def new(self, estimation_feed: EstimationFeed) -> EstimationFeed | None:
        db_estimation_feed = await self.collection.find_one({"title": estimation_feed.title, "developer_id": estimation_feed.developer_id})
        if not db_estimation_feed:
            new_estimation_feed = estimation_feed.model_dump()
            del new_estimation_feed["id"]
            result = await self.collection.insert_one(new_estimation_feed)
            estimation_feed.id = str(result.inserted_id)
            return estimation_feed
        
        return

    async def get(self, id: str) -> EstimationFeed | None:
        try:
            if estimation_feed := await self.collection.find_one({"_id": ObjectId(id)}):
                return EstimationFeed.from_dict(estimation_feed)
        except InvalidId:
            raise ValueError(f"invalid estimation_feed id: {id}")

        return None

    async def get_all(self) -> list[EstimationFeed]:
        result = await self.collection.find({}).sort({"_id": -1}).to_list()
        return [EstimationFeed.from_dict(a) for a in result]


estimation_feed_repository = MongoEstimationFeedRepository(
    collection=db[ESTIMATION_FEED_COLLECTION_NAME]
)
