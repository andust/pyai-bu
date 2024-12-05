import pytest
from motor.motor_asyncio import AsyncIOMotorClient
import pytest_asyncio
from app.config.envirenment import get_settings

from langchain_core.documents import Document



@pytest.fixture
def docs() -> list[Document]:
    doc1 = Document(page_content="This is the first document.", metadata={"id": 1, "user_id": "1abc"})
    doc2 = Document(
        page_content="This is the second document with more content.",
        metadata={"id": 2, "user_id": "2abc"},
    )
    return [doc1, doc2]


@pytest_asyncio.fixture
async def test_db():
    _S = get_settings()
    test_client = AsyncIOMotorClient(_S.TEST_MONGO_CONNECTION)
    test_db = test_client[_S.TEST_MONGO_DB]
    try:
        yield test_db
    finally:
        await test_client.drop_database(_S.TEST_MONGO_DB)
        test_client.close()
