from contextlib import asynccontextmanager
import os

import qdrant_client
from qdrant_client import models
from qdrant_client.http.exceptions import UnexpectedResponse

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from pydantic import SecretStr

from app.config.envirenment import get_settings
from app.constants.file import POSSIBLE_VECTOR_DB_CONTENT_TYPE
from app.libs.lch.document import recursive_character_text_splitter

_S = get_settings()


async def create_collection(name: str):
    try:
        client = qdrant_client.AsyncQdrantClient(url=_S.QDRANT_URL)
        await client.create_collection(
            collection_name=name,
            vectors_config=models.VectorParams(
                size=1536, distance=models.Distance.COSINE
            ),
        )
    except UnexpectedResponse as e:
        print(e)


@asynccontextmanager
async def upload_documents(docs: list[Document]):
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
        collection_name=_S.QDRANT_MAIN_DOCUMANTS,
    )

    try:
        yield qdrant
    finally:
        qdrant.client.close()
        embeddings.client
