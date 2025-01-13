import io
from fastapi import Depends, status, UploadFile
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.constants.common import UrlsQuery
from app.repository.file import file_repository
from app.api.guard.main import get_current_user
from app.model.user import User
from app.usecase.file import FileUseCase
from app.usecase.scraper import ScraperUseCase
from playwright.async_api import Error as PlaywrightError
from starlette.datastructures import Headers


router = APIRouter(default_response_class=JSONResponse)


@router.post(
    "/scrape-pages",
    status_code=status.HTTP_200_OK,
)
async def scrape_pages(scrape_pages: UrlsQuery, user: User = Depends(get_current_user)):
    scraper_use_case = ScraperUseCase()
    try:
        page_contents = await scraper_use_case.scrape_pages(
            urls=[str(a) for a in scrape_pages.urls]
        )

        file_usecase = FileUseCase(file_repository=file_repository)
        return await file_usecase.upload(
            files=[
                UploadFile(
                    file=io.BytesIO(page_content.content),
                    filename=page_content.filename,
                    headers=Headers(page_content.headers),
                )
                for page_content in page_contents
            ],
            user_email=user.email,
        )
    except PlaywrightError:
        # TODO handle this error
        return []
