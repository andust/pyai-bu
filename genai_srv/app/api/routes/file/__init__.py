from fastapi import APIRouter


from . import file


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(file.router, prefix="/file", tags=["file"])
    return rt


router = _build_router()
