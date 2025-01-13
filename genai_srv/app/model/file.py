from datetime import datetime
from enum import Enum
from typing import Literal, Protocol

from pydantic import BaseModel

from app.constants.file import ProcessState


class FileProtocol(Protocol):
    filename: str | None
    content_type: str | None

    async def read(self) -> bytes: ...

    async def write(self, data: bytes) -> None: ...

    async def close(self) -> None: ...

    async def seek(self, offset: int) -> None: ...


class ContentType(str, Enum):
    PDF = "application/pdf"
    TEXT_PLAIN = "text/plain"
    TEXT_CSV = "text/csv"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_JPG = "image/jpg"

    @classmethod
    def text_types(cls):
        return [cls.TEXT_PLAIN, cls.TEXT_CSV]

    @classmethod
    def image_types(cls):
        return [cls.IMAGE_PNG, cls.IMAGE_JPEG, cls.IMAGE_JPG]


class FileData(BaseModel):
    content: bytes
    content_type: Literal[
        ContentType.PDF,
        ContentType.TEXT_PLAIN,
        ContentType.TEXT_CSV,
        ContentType.IMAGE_PNG,
        ContentType.IMAGE_JPEG,
        ContentType.IMAGE_JPG,
    ]
    id: str | None = None
    filename: str | None = None
    upload_date: datetime | None = None
    vectorDBStatus: ProcessState = ProcessState.PENDING

