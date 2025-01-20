from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from playwright.async_api import Error as PlaywrightError

from app.usecase.scraper import ScrapeData


async def document_to_newsletter_use_case(
    llm: BaseLanguageModel, documents: list[ScrapeData], question_context: str
) -> str:
    try:
        text_files = [str(document.content) for document in documents]

        prompt = PromptTemplate.from_template("""                      
            I need a newsletter in Polish of the Document content.
            We will skip all greetings in the newsletter, we only need the title, content and a short summary at the end (about 100 characters in a relaxed atmosphere).
            Approximately 1500 characters are needed for all.
            Take into account the context of the question, if any.
            If you can't' find the information you need just say you need more information.

            Document content: {document_content}
            Question context: {question_context}
        """)

        rag_chain = (
            {
                "document_content": lambda x: "\n".join(x["document_content"]),
                "question_context": lambda x: "\n".join(x["question_context"]),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        response: str = rag_chain.invoke(
            {"document_content": text_files, "question_context": question_context}
        )

        return response

    except PlaywrightError:
        # TODO handle this error
        return ""
