import logging

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from langchain_core.documents import Document

from app.config.envirenment import get_settings
from app.constants.file import ContentType
from app.helpers.qdrant.upload import upload_documents
from app.model.estimation_feed import EstimationFeed
from app.repository.estimation_feed import estimation_feed_repository

_S = get_settings()

router = APIRouter(default_response_class=JSONResponse)


@router.post("/", status_code=status.HTTP_200_OK, response_model=EstimationFeed | None)
async def new_estimation_feed(estimation_feed: EstimationFeed):
    new_estimation_feed = await estimation_feed_repository.new(
        estimation_feed=estimation_feed
    )

    if new_estimation_feed:
        file_content = f"""
            Title: {new_estimation_feed.title}\n
            Description: {new_estimation_feed.description}\n
            Complexity: {new_estimation_feed.complexity}\n
            Estimated time hours: {new_estimation_feed.estimated_time_hours}\n
            Actual time hours: {new_estimation_feed.actual_time_hours}\n
            Tech stack: {new_estimation_feed.tech_stack}
        """

        document = Document(
            page_content=file_content,
            metadata={
                "estimation_feed_id": str(new_estimation_feed.id),
                "content_type": ContentType.TEXT_PLAIN,
                "tech_stack": new_estimation_feed.tech_stack,
                "developer_id": new_estimation_feed.developer_id,
            },
        )
        async with upload_documents(
            docs=[document], collection_name=_S.QDRANT_ESTIMATION_FEED_DOCUMANTS
        ):
            logging.info("document uploaded to qdrant")

    return new_estimation_feed


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[EstimationFeed])
async def all_project():
    return await estimation_feed_repository.get_all()