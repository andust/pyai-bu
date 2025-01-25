from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.api.guard.main import get_current_user
from app.model.chat import Chat
from app.model.user import User
from app.repository.chat import chat_repository


router = APIRouter(default_response_class=JSONResponse)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[Chat],
)
async def all_chats(user: User = Depends(get_current_user)):
    # TODO all user chats
    return await chat_repository.get_all()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Chat,
)
async def new_chat(user: User = Depends(get_current_user)):
    return await chat_repository.new(user_id=user.id)


@router.get(
    "/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=Chat,
)
async def get_chat(chat_id: str, user: User = Depends(get_current_user)):
    chat = await chat_repository.get(chat_id)
    if chat and user.id != chat.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="not found for user"
        )
    return chat


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_chat(chat_id: str):
    db_chat = await chat_repository.get(chat_id)
    if db_chat:
        return await chat_repository.delete(chat_id)

    return
