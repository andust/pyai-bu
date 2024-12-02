from datetime import datetime
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


class FileData(BaseModel):
    content: bytes
    content_type: Literal[
        "application/pdf",
        "text/plain",
        "text/csv",
        "image/png",
        "image/jpeg",
        "image/jpg",
    ]
    id: str | None = None
    filename: str | None = None
    upload_date: datetime | None = None
    vectorDBStatus: ProcessState = ProcessState.PENDING

