from fastapi import APIRouter


from . import newsletter


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(newsletter.router, prefix="/newsletter", tags=["newsletter"])
    return rt


router = _build_router()
