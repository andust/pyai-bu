import os

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

from app.constants.chat import ChatMode
from app.helpers.qdrant.vector_store import QdrantVectorStoreService
from app.model.question import Question
from app.repository.chat import chat_repository
from app.usecase.chat import ChatUseCase

router = APIRouter(default_response_class=JSONResponse)


class Ask(BaseModel):
    content: str
    chat_mode: ChatMode
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
    questions = db_chat.questions or []
    # prepare llm services
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
    )
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=os.environ["OPENAI_API_KEY"]
    )
    qdrant_vector_store = QdrantVectorStoreService(embeddings=embeddings)

    try:
        # ask question
        chat_use_case = ChatUseCase(
            vector_store=qdrant_vector_store, llm=llm, history=questions
        )
        ask_cb = {
            ChatMode.CHAT: chat_use_case.ask_chat(query=ask.content),
            ChatMode.RAG: chat_use_case.ask_rag(
                query=ask.content, must={"metadata.file_id": ask.document_id}
            ),
        }
        answer = await ask_cb[ask.chat_mode]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="chat mode not supported"
        )

    # update db and return questions
    qst = Question(content=ask.content, answer=answer)
    questions.append(qst)
    db_chat.questions = questions
    await chat_repository.update(chat_id, db_chat)

    return questions
