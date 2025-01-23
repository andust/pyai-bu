import logging
from typing import Sequence

from langchain_core.documents import Document

from app.config.envirenment import get_settings
from app.helpers.file.main import file_hash
from app.helpers.pdf.main import pdf_to_text
from app.helpers.qdrant.upload import upload_documents
from app.model.file import FileProtocol
from app.repository.file import FileRepositoryProtocol

_S = get_settings()

async def files_to_documents(files: list[FileProtocol]) -> list[Document]:
    docs = []
    for file in files:
        if not file.filename:
            continue
        fhash = await file_hash(file)

        content = await file.read()

        if file.content_type == "application/pdf":
            page_content = "\n".join(pdf_to_text(content))
        else:
            page_content = str(content)

        docs.append(
            Document(
                page_content=page_content,
                metadata={
                    "file_hash": fhash,
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
        async with upload_documents(docs=documents, collection_name=_S.QDRANT_MAIN_DOCUMANTS):
            logging.info("document uploaded to qdrant")
        return documents
