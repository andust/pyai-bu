from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def recursive_character_text_splitter(
    docs: list[Document], chunk_size=700, chunk_overlap=100
) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)


def format_docs(docs: list[Document]) -> str:
    for doc in docs:
        print(doc.metadata)
    return "\n\n".join(doc.page_content for doc in docs)
