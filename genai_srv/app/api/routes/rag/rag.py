import os
from typing import Literal
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel, SecretStr

from app.constants.chat import QuestionType
from app.helpers.qdrant.vector_store import QdrantVectorStoreService
from app.model.question import Question
from app.repository.chat import chat_repository
from app.usecase.chat_graph import ChatUseCase


router = APIRouter(default_response_class=JSONResponse)


class Ask(BaseModel):
    question: str
    question_type: Literal[QuestionType.CHAT, QuestionType.RAG, QuestionType.AWS]
    document_id: str


@router.post(
    "/ask/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[Question],
)
async def ask(chat_id: str, ask: Ask):
    # get db data
    db_chat = await chat_repository.get(chat_id)
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="chat not found"
        )


    model = ChatOpenAI(
        # model="gpt-4o-mini",
        model="gpt-4o",
        api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
    )

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=SecretStr(os.environ["OPENAI_API_KEY"])
    )
    qdrant_vector_store = QdrantVectorStoreService(embeddings=embeddings)


    questions = db_chat.questions or []

    chat_use_case = ChatUseCase(
        model=model,
        embeddings=embeddings,
        vector_store=qdrant_vector_store
    )
    answer = await chat_use_case.ask(
        chat_id=chat_id, question=ask.question, document_id=ask.document_id, question_type=ask.question_type
    )
    if answer:
        # update db and return questions
        qst = Question(content=ask.question, answer=answer, mode=ask.question_type)
        questions.append(qst)
        db_chat.questions = questions
        await chat_repository.update(chat_id, db_chat)

        return questions
