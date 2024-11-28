from typing import Sequence
from langchain_core.documents import Document

from app.libs.lch.document import serialize_document
from app.libs.pdf_reader.main import pdf_to_text
from app.model.file import FileProtocol, calculate_file_hash
from app.repository.file import FileRepositoryProtocol
from app.tasks.qdrant.upload_tasks import upload_to_qdrant


async def files_to_documents(files: list[FileProtocol]) -> list[Document]:
    docs = []
    for file in files:
        if not file.filename:
            continue
        file_hash = await calculate_file_hash(file)

        content = await file.read()

        if file.content_type == "application/pdf":
            page_content = "\n".join(pdf_to_text(content))
        else:
            page_content = str(content)

        docs.append(
            Document(
                page_content=page_content,
                metadata={
                    "file_hash": file_hash,
                    "filename": file.filename,
                    "content_type": file.content_type,
                },
            )
        )

    return docs


class FileUseCase:
    def __init__(self, file_repository: FileRepositoryProtocol) -> None:
        self.file_repository = file_repository

    async def upload(
        self, files: Sequence[FileProtocol], user_email: str
    ) -> list[Document]:
        documents = await self.file_repository.upload_files(
            files=files, user_email=user_email
        )

        upload_to_qdrant.delay([serialize_document(a) for a in documents])
        return documents
