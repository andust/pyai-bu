from fastapi import APIRouter


from . import project


def _build_router() -> APIRouter:
    rt = APIRouter()
    rt.include_router(project.router, prefix="/project", tags=["project"])
    return rt


router = _build_router()
