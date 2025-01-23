from typing import Protocol
from bson import ObjectId
from bson.errors import InvalidId

from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.main import db
from app.model.project import Project

PROJECT_COLLECTION_NAME = "project"


class ProjectRepositoryProtocol(Protocol):
    async def new(self, project: Project) -> Project | None: ...

    async def get(self, id: str) -> Project | None: ...

    async def get_all(self) -> list[Project]: ...

    async def update(self, id: str, data: Project) -> Project | None: ...


class MongoProjectRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def new(self, project: Project) -> Project | None:
        db_project = await self.collection.find_one({"title": project.title})

        if not db_project:
            new_project = project.model_dump()
            del new_project["id"]
            result = await self.collection.insert_one(new_project)
            project.id = str(result.inserted_id)
            return project

        return None

    async def get(self, id: str) -> Project | None:
        try:
            if project := await self.collection.find_one({"_id": ObjectId(id)}):
                return Project.from_dict(project)
        except InvalidId:
            raise ValueError(f"invalid project id: {id}")

        return None

    async def get_all(self) -> list[Project]:
        result = await self.collection.find({}).sort({"_id": -1}).to_list()
        return [Project.from_dict(a) for a in result]

    async def update(self, id: str, data: Project) -> Project | None:
        document = data.model_dump(exclude_unset=True, by_alias=True)
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": document}
        )
        if result.modified_count:
            return await self.get(id)
        return


project_repository = MongoProjectRepository(collection=db[PROJECT_COLLECTION_NAME])
