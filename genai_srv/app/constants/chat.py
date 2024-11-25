from enum import Enum


class ChatMode(str, Enum):
    CHAT = "chat"
    RAG = "rag"