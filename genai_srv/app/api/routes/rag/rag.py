import os

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from pydantic import BaseModel, SecretStr

from app.constants.chat import ChatMode
from app.libs.qdrant.vector_store import QdrantVectorStoreService
from qdrant_client import QdrantClient
from app.model.question import Question
from app.repository.chat import chat_repository
from app.usecase.chat import ChatUseCase

from qdrant_client.http import models
router = APIRouter(default_response_class=JSONResponse)
from app.config.envirenment import get_settings

_S = get_settings()

class Ask(BaseModel):
    content: str
    chat_mode: ChatMode
    document_id: str


@router.get(
    "/test-vector-store",
    status_code=status.HTTP_200_OK,
)
async def aaa():
    # llm = ChatOpenAI(
    #     model="gpt-4o-mini",
    #     temperature=0.7,
    #     api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
    # )
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=os.environ["OPENAI_API_KEY"]
    )
    client = QdrantClient(url=_S.QDRANT_URL)
    # qdrant = QdrantVectorStore.from_existing_collection(
    qdrant = QdrantVectorStore(
        client=client,
        embedding=embeddings,
        collection_name=_S.QDRANT_MAIN_DOCUMANTS,
    )


    vector_result = await qdrant.asimilarity_search(
        query="popierania do korony polskiej kandydatury",
        k=3,
        filter=models.Filter(must=[models.FieldCondition(key="metadata.file_id", match=models.MatchValue(value="673d8ea893142d3f4dc6f9d9"))]),
    )

    print(vector_result)
    return vector_result



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
            ChatMode.RAG: chat_use_case.ask_rag(
                query=ask.content, must={"metadata.file_id": ask.document_id}
            )
        }
        answer = await ask_cb[ask.chat_mode]
        print(ask.content, ask.chat_mode, ask.document_id, answer)
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
