import os
from typing import TypedDict

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from langgraph.graph import MessagesState, START, END, StateGraph
from pydantic import SecretStr

from app.helpers.qdrant.vector_store import QdrantVectorStoreService
from app.config.envirenment import get_settings


_S = get_settings()

class State(TypedDict):
    question: str
    document_id: str
    context: list[Document]
    answer: str

model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small", api_key=os.environ["OPENAI_API_KEY"]
)
qdrant_vector_store = QdrantVectorStoreService(embeddings=embeddings)


class DocumentMessagesState(MessagesState):
    document_id: str
    document_content: str


def _node_route(state: DocumentMessagesState):
    if state.get("document_id"):
        return "_query_document"
    else:
        return "_generate"


async def _query_document(state: DocumentMessagesState):
    """Find document in vector db."""

    query = state["messages"][-1].content or ""
    retrieved_docs = await qdrant_vector_store.similarity_search(
        query=query,  # type: ignore
        k=4,
        must={"metadata.file_id": state["document_id"]},
    )

    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}" f"Query: {query}")
        for doc in retrieved_docs
    )
    return {"document_content": serialized}


def _rag(state: DocumentMessagesState):
    """Generate RAG answer."""

    document_content = state["document_content"]
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use ten sentences maximum and keep the "
        "answer concise."
        "\n\n"
        f"{document_content}"
    )

    prompt = [SystemMessage(system_message_content)] + _state_conversation_messages(
        state["messages"]
    )
    response = model.invoke(prompt)
    return {"messages": [response]}


def _generate(state: DocumentMessagesState):
    """Generate chat answer."""

    system_message_content = """
        You are an assistant for question-answering tasks.
        If you don't know the answer, just say that you don't know and need more information.
        Use a maximum of fifty sentences and provide a concise answer.
    """

    prompt = [SystemMessage(system_message_content)] + _state_conversation_messages(
        state["messages"]
    )

    response = model.invoke(prompt)
    return {"messages": [response]}


def _state_conversation_messages(messages: list[AnyMessage]):
    result = []

    for i, message in enumerate(messages, 1):
        if message.type == "human":
            result.append(HumanMessage(content=message.content))
        else:
            result.append(AIMessage(content=message.content))

    return result


async def ask_use_case(
    chat_id: str, question: str, document_id: str | None = None
) -> str | None:
    async with AsyncMongoDBSaver.from_conn_string(_S.MONGO_CONNECTION) as checkpointer:
        graph_builder = StateGraph(DocumentMessagesState)

        graph_builder.add_node(_query_document)
        graph_builder.add_node(_generate)
        graph_builder.add_node(_rag)

        graph_builder.add_edge("_query_document", "_rag")
        graph_builder.add_edge("_rag", END)
        graph_builder.add_edge("_generate", END)

        graph_builder.add_conditional_edges(
            START,
            _node_route,
            {
                END: END,
                "_query_document": "_query_document",
                "_generate": "_generate",
            },
        )

        graph_builder = graph_builder.compile(checkpointer=checkpointer)
        response = await graph_builder.ainvoke(
            {
                
                "messages": [HumanMessage(content=question)],
                "document_id": document_id,
            },
            config={"configurable": {"thread_id": chat_id}},
        )
        return response["messages"][-1].content
