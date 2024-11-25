from fastapi import APIRouter


from . import rag


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(rag.router, prefix="/rag", tags=["rag"])
    return rt


router = _build_router()
