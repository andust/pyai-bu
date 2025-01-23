from datetime import datetime
from enum import Enum
from typing import Literal, Protocol

from pydantic import BaseModel

from app.constants.file import ContentType, ProcessState


class FileProtocol(Protocol):
    filename: str | None
    content_type: str | None

    async def read(self) -> bytes: ...

    async def write(self, data: bytes) -> None: ...

    async def close(self) -> None: ...

    async def seek(self, offset: int) -> None: ...


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

