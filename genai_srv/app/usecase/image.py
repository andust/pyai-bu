from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

from app.helpers.file.main import download_file
from app.repository.file import file_repository


class ImageGenerateQuery(BaseModel):
    content: str
    image_size: Literal["1024x1024", "1792x1024", "1024x1792"]


class ImageUseCase:
    def __init__(self, client: OpenAI) -> None:
        self.client = client

    async def generate(self, query: ImageGenerateQuery, user_email: str) -> list[str]:
        if not query.content.strip():
            return []

        image = self.client.images.generate(
            model="dall-e-3", prompt=query.content, n=1, size=query.image_size
        )

        uploaded_file_ids = []
        for file in image.data:
            if file.url:
                if upload_file := await download_file(file.url):
                    uploaded_file_ids += await file_repository.upload_files(
                        files=[upload_file],
                        user_email=user_email,
                    )

        return uploaded_file_ids
