from contextlib import asynccontextmanager
import os

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from pydantic import SecretStr

from app.config.envirenment import get_settings
from app.constants.file import POSSIBLE_VECTOR_DB_CONTENT_TYPE
from app.helpers.document.main import recursive_character_text_splitter

_S = get_settings()


@asynccontextmanager
async def upload_documents(docs: list[Document], collection_name: str):
    clean_docs = [
        a for a in docs if a.metadata["content_type"] in POSSIBLE_VECTOR_DB_CONTENT_TYPE
    ]

    if not clean_docs:
        yield None
        return

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=SecretStr(os.environ["OPENAI_API_KEY"])
    )

    qdrant = await Qdrant.afrom_documents(
        recursive_character_text_splitter(clean_docs),
        embeddings,
        url=_S.QDRANT_URL,
        collection_name=collection_name,
    )

    try:
        yield qdrant
    finally:
        qdrant.client.close()
        embeddings.client
