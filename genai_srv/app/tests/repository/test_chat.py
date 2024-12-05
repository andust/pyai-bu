import pytest

from app.repository.chat import CHAT_COLLECTION_NAME, MongoChatRepository


@pytest.mark.asyncio
async def test_create_one_new_chat(test_db):
    user_id = "123"
    collection = test_db[CHAT_COLLECTION_NAME]
    chat_repo = MongoChatRepository(collection=collection)
    chat_instance_1 = await chat_repo.new(user_id=user_id)
    assert chat_instance_1 is not None
    assert chat_instance_1.user_id == user_id

    chat_instance_2 = await chat_repo.new(user_id=user_id)
    assert chat_instance_1.id == chat_instance_2.id
