import qdrant_client
from qdrant_client import models
from qdrant_client.http.exceptions import UnexpectedResponse


from app.config.envirenment import get_settings

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
