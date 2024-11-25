from fastapi import Depends, File, UploadFile, status, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter


from app.api.guard.main import get_current_user
from app.model.user import User
from app.repository.file import file_repository
from app.usecase.file import FileUseCase

router = APIRouter(default_response_class=JSONResponse)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def all_files(user: User = Depends(get_current_user)):
    results = await file_repository.get_many()
    return results

@router.post("/upload/")
async def upload_file(files: list[UploadFile] = File(...)):
    file_usecase = FileUseCase(file_repository=file_repository)
    result = await file_usecase.upload(files=files, user_email="andrzej@example.com")
    return result


@router.get(
    "/download/{file_id}",
    status_code=status.HTTP_200_OK,
)
async def download(file_id: str):
    file_data = await file_repository.get(file_id)
    return Response(content=file_data.content, media_type=file_data.content_type)
