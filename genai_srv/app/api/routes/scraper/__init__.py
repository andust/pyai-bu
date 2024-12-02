from fastapi import APIRouter


from . import scraper


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(scraper.router, prefix="/scraper", tags=["scraper"])
    return rt


router = _build_router()
