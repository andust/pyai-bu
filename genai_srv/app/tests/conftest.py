import pytest
from copy import deepcopy
from motor.motor_asyncio import AsyncIOMotorClient
import pytest_asyncio
from app.config.envirenment import get_settings

from langchain_core.documents import Document

from app.constants.chat import QuestionType
from app.constants.common import ComplexityLevel
from app.repository.chat import CHAT_COLLECTION_NAME
from app.repository.project import PROJECT_COLLECTION_NAME
from app.tests.mock_data.chat import CHATS
from app.tests.mock_data.project import PROJECTS


@pytest.fixture
def docs() -> list[Document]:
    doc1 = Document(
        page_content="This is the first document.",
        metadata={"id": 1, "user_id": "1abc"},
    )
    doc2 = Document(
        page_content="This is the second document with more content.",
        metadata={"id": 2, "user_id": "2abc"},
    )
    return [doc1, doc2]


@pytest_asyncio.fixture
async def default_chats(test_db):
    collection = test_db[CHAT_COLLECTION_NAME]

    chats = deepcopy(CHATS)

    await collection.insert_many(chats)

    yield chats

    await collection.delete_many({"_id": {"$in": [chat["_id"] for chat in chats]}})


@pytest_asyncio.fixture
async def default_projects(test_db):
    collection = test_db[PROJECT_COLLECTION_NAME]

    projects = deepcopy(PROJECTS)

    await collection.insert_many(projects)

    yield projects

    await collection.delete_many(
        {"_id": {"$in": [project["_id"] for project in projects]}}
    )


@pytest_asyncio.fixture
async def test_db():
    _S = get_settings()
    test_client = AsyncIOMotorClient(_S.TEST_MONGO_CONNECTION)
    test_db = test_client[_S.TEST_MONGO_DB]
    try:
        yield test_db
    finally:
        # await test_client.drop_database(_S.TEST_MONGO_DB)
        test_client.close()
