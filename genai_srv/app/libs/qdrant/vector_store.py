from contextlib import asynccontextmanager
from typing import Any

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore

from qdrant_client.http import models
# from qdrant_client import models

from app.config.envirenment import get_settings

_S = get_settings()


@asynccontextmanager
async def qdrant_vector_store(embeddings):
    try:
        qdrant = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            url=_S.QDRANT_URL,
            collection_name=_S.QDRANT_MAIN_DOCUMANTS,
        )
        yield qdrant
    finally:
        qdrant.client.close()


class QdrantVectorStoreService:
    def __init__(self, embeddings: OpenAIEmbeddings) -> None:
        self.qdrant = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            url=_S.QDRANT_URL,
            collection_name=_S.QDRANT_MAIN_DOCUMANTS,
        )

    async def similarity_search(
        self, query: str, k: int, must: dict[str, Any] | None = None
    ) -> list[Document]:
        filter = None
        if must:
            must_filters = []
            for key, value in must.items():
                must_filters.append(
                    models.FieldCondition(key=key, match=models.MatchValue(value=value))
                )

            filter = models.Filter(must=must_filters)

        print("-----> FILTER", filter)

        vector_result = await self.qdrant.asimilarity_search(
            query=query,
            k=k,
            filter=filter,
        )
        print("-----> VECTOR_RESULT", vector_result)
        return vector_result
