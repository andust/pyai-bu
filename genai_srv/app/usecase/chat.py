from typing import Any, Protocol

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.libs.lch.document import format_docs
from app.libs.lch.promp import log_promp
from app.model.question import Question


class VectorStoreProtocol(Protocol):
    async def similarity_search(
        self, query: str, k: int, must: dict[str, Any] | None = None
    ) -> list[Document]: ...


class ChatUseCase:
    def __init__(
        self,
        vector_store: VectorStoreProtocol,
        llm: ChatOpenAI,
        history: list[Question] | None = None,
    ) -> None:
        tmp_history = history or []
        self.llm = llm
        self.vector_store = vector_store
        self.history = tmp_history[:10]

    @property
    def history_content(self) -> str:
        return "\n".join(
            [f"question: {a.content}, answer: {a.answer}" for a in self.history[:5]]
        )



    async def ask_chat(self, query: str) -> str:
        prompt = PromptTemplate.from_template("""
            You are an assistant for question-answering tasks.
            If you don't know the answer, just say that you don't know and need more information.
            Use a maximum of fifty sentences and provide a concise answer.
            Here is the conversation history:
            {history}
            Question: {question} 
            Answer:
        """)

        rag_chain = (
            {"history": RunnablePassthrough(), "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | log_promp
            | StrOutputParser()
        )

        response: str = rag_chain.invoke(
            {"question": query, "history": self.history_content},
        )
        return response

    async def ask_rag(self, query: str, must: dict | None = None) -> str:
        retriever = await self.vector_store.similarity_search(
            query=query,
            k=4,
            must=must,
        )

        # prompt = hub.pull("rlm/rag-prompt")

        prompt = PromptTemplate.from_template("""                      
            You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
            Keep in mind conversation history.
            If you don't know the answer, just say that you don't know. Use a maximum of fifty sentences and keep the answer concise.
                                              
            Question: {question} 

            Context: {context} 

            History: {history}
            Answer:
        """)


        rag_chain = (
            {
                "context": lambda x: format_docs(retriever),
                "question": RunnablePassthrough(),
                "history": RunnablePassthrough(),
            }
            | prompt
            | log_promp
            | self.llm
            | log_promp
            | StrOutputParser()
        )

        response: str = rag_chain.invoke(query)

        return response
