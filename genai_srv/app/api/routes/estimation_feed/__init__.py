from fastapi import APIRouter


from . import estimation_feed


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(estimation_feed.router, prefix="/estimation-feed", tags=["estimation_feed"])
    return rt


router = _build_router()
