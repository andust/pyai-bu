from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import SystemMessage
from langchain_core.messages.human import HumanMessage
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from langgraph.graph import MessagesState, START, END, StateGraph

from app.helpers.chat.message import state_conversation_messages
from app.helpers.qdrant.vector_store import QdrantVectorStoreService
from app.config.envirenment import get_settings


_S = get_settings()


class DocumentMessagesState(MessagesState):
    document_id: str
    document_content: str


class ChatUseCase:
    def __init__(
        self,
        model: BaseLanguageModel,
        embeddings: Embeddings,
        vector_store: QdrantVectorStoreService,
    ) -> None:
        self.model = model
        self.embeddings = embeddings
        self.vector_store = vector_store

    def node_route(self, state: DocumentMessagesState):
        if state.get("document_id"):
            return "query_document"
        else:
            return "generate"

    async def query_document(self, state: DocumentMessagesState):
        """Find document in vector db."""

        query = state["messages"][-1].content or ""
        retrieved_docs = await self.vector_store.similarity_search(
            query=query,  # type: ignore
            k=6,
            must={"metadata.file_id": state["document_id"]},
        )

        serialized = "\n\n".join(
            (
                f"Source: {doc.metadata}\n"
                f"Content: {doc.page_content}"
                f"Query: {query}"
            )
            for doc in retrieved_docs
        )
        return {"document_content": serialized}

    def rag(self, state: DocumentMessagesState):
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

        prompt = [SystemMessage(system_message_content)] + state_conversation_messages(
            state["messages"]
        )
        response = self.model.invoke(prompt)
        return {"messages": [response]}

    def generate(self, state: DocumentMessagesState):
        """Generate chat answer."""

        system_message_content = """
            You are an assistant for question-answering tasks.
            If you don't know the answer, just say that you don't know and need more information.
            Use a maximum of fifty sentences and provide a concise answer.
        """

        prompt = [SystemMessage(system_message_content)] + state_conversation_messages(
            state["messages"]
        )

        response = self.model.invoke(prompt)
        return {"messages": [response]}

    async def ask(
        self, chat_id: str, question: str, document_id: str | None = None
    ) -> str | None:
        async with AsyncMongoDBSaver.from_conn_string(
            _S.MONGO_CONNECTION
        ) as checkpointer:
            graph_builder = StateGraph(DocumentMessagesState)

            graph_builder.add_node(self.query_document)
            graph_builder.add_node(self.generate)
            graph_builder.add_node(self.rag)

            graph_builder.add_edge("query_document", "rag")
            graph_builder.add_edge("rag", END)
            graph_builder.add_edge("generate", END)

            graph_builder.add_conditional_edges(
                START,
                self.node_route,
                {
                    END: END,
                    "query_document": "query_document",
                    "generate": "generate",
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
