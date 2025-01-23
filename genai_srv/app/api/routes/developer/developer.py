import os

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from app.constants.common import ComplexityLevel
from app.constants.dto import IdDTO
from app.model.skill import Skill
from app.repository.developer import developer_repository
from app.model.developer import Developer
# from app.usecase.estimation import estimate_developer_use_case

router = APIRouter(default_response_class=JSONResponse)


@router.post("/", status_code=status.HTTP_200_OK, response_model=Developer | None)
async def new_developer(developer: Developer):
    await developer_repository.new(developer=Developer(
        user_id="677b1162d538985a7190b6a1",
        full_name="ab",
        skills=[
            Skill(name="Python", level=5),
            Skill(name="Django", level=5),
            Skill(name="FastAPI", level=4),
            Skill(name="Celery", level=3),
            Skill(name="JavaScript", level=5),
            Skill(name="React", level=5),
            Skill(name="Node.js", level=4),
            Skill(name="Express.js", level=4),
            Skill(name="PHP", level=3),
            Skill(name="HTML", level=5),
            Skill(name="CSS", level=5),
            Skill(name="WordPress", level=3),
            Skill(name="MongoDB", level=3),
            Skill(name="Postgresql", level=4),
        ],
        month_experience=120
    ))


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Developer])
async def all_developer():
    return await developer_repository.get_all()


@router.get("/{developer_id}", status_code=status.HTTP_200_OK, response_model=Developer | None)
async def get_developer(developer_id: str):
    return await developer_repository.get(id=developer_id)
