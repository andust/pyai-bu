import asyncio
import logging


from app.config.celery import celery_app
from app.helpers.document.main import deserialize_document
from app.helpers.qdrant.upload import upload_documents


async def aupload_to_qdrant(documents):
    documents = [deserialize_document(a) for a in documents]
    async with upload_documents(docs=documents):
        logging.info("document uploaded to qdrant")
        return [str(a.metadata["file_id"]) for a in documents]


@celery_app.task
def upload_to_qdrant(docs):
    return asyncio.run(aupload_to_qdrant(docs))
