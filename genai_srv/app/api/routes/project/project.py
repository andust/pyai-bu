import os

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from pydantic import SecretStr

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

from app.config.envirenment import get_settings
from app.model.estimation import Estimation
from app.model.project import Project
from app.repository.project import project_repository
from app.usecase.project import ProjectUseCase

_S = get_settings()

router = APIRouter(default_response_class=JSONResponse)


@router.post("/", status_code=status.HTTP_200_OK, response_model=Project | None)
async def new_project(project: Project):
    new_project = await project_repository.new(project=project)

    return new_project


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Project])
async def all_project():
    return await project_repository.get_all()


@router.get(
    "/{project_id}", status_code=status.HTTP_200_OK, response_model=Project | None
)
async def get_project(project_id: str):
    return await project_repository.get(id=project_id)


@router.get(
    "/{project_id}/estimate", status_code=status.HTTP_200_OK, response_model=Project
)
async def estimate_project(
    project_id: str,
) -> Project | None:
    model = ChatOpenAI(
        model="gpt-4o-mini",
        # model="gpt-4o",
        api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
    )

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=os.environ["OPENAI_API_KEY"]
    )

    project = await project_repository.get(project_id)
    if project:
        project_use_case = ProjectUseCase(
            model=model, embeddings=embeddings, project=project
        )
        result = await project_use_case.estimate()
        project.estimation = Estimation(
            result=result,
            complexity=project.complexity,  # TODO get this data from AI
            estimated_time_hours=1,  # TODO get this data from AI
            tech_stack=[],  # TODO get this data from AI
        )
        if updated_project := await project_repository.update(
            id=project_id, data=project
        ):
            return updated_project
    return None
