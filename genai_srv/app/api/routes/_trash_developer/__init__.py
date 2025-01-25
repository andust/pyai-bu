from fastapi import APIRouter


from . import developer


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(developer.router, prefix="/developer", tags=["developer"])
    return rt


router = _build_router()
