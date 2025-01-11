from enum import Enum


class QuestionType(str, Enum):
    CHAT = "chat"
    RAG = "rag"
    NEWSLETTER = "newsletter"
