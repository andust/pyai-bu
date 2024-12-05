from io import BytesIO

from fastapi import UploadFile
from starlette.datastructures import Headers

from app.config.celery import celery_app
from app.db.main import new_db
from app.helpers.async_await.main import run_async
from app.repository.file import new_file_repository
from app.usecase.file import FileUseCase


async def aupload_to_qdrant(files: list[dict], user_email: str):
    async with new_db() as db_instance:
        file_repo = new_file_repository(db_instance)

        file_usecase = FileUseCase(file_repository=file_repo)
        documents = await file_usecase.upload(
            files=[
                UploadFile(
                    file=BytesIO(f["file_content"]),
                    filename=f["filename"],
                    headers=Headers({"Content-Type": f["content_type"]}),
                )
                for f in files
            ],
            user_email=user_email,
        )

        return [str(a.metadata["file_id"]) for a in documents]


@celery_app.task
def upload_to_qdrant(files: list[dict], user_email: str):
    return run_async(aupload_to_qdrant(files, user_email=user_email))
