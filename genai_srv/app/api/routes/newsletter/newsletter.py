import os

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.constants.chat import QuestionType
from app.constants.dto import UrlsDTO
from app.model.question import Question
from app.usecase.newsletter import document_to_newsletter_use_case
from app.usecase.scraper import ScraperUseCase

router = APIRouter(default_response_class=JSONResponse)

class NewsletterQuery(UrlsDTO):
    question_context: str

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Question,
)
async def generate_newsletter(query: NewsletterQuery):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        # model="gpt-4o",
        api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
    )

    raw_urls = [str(a) for a in query.urls]

    try:

        scraper_use_case = ScraperUseCase()
        scrape_data = await scraper_use_case.scrape_pages(
            urls=[str(a) for a in query.urls]
        )

        answer = await document_to_newsletter_use_case(llm=llm, documents=scrape_data, question_context=query.question_context)
        qst = Question(
            content="\n".join(raw_urls), answer=answer, mode=QuestionType.NEWSLETTER
        )

        return qst
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="problem with newsletter"
        )
