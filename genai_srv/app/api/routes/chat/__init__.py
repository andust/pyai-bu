from fastapi import APIRouter


from . import chat


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(chat.router, prefix="/chat", tags=["chat"])
    return rt


router = _build_router()
