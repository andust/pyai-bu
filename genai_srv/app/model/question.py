from typing import Literal
from pydantic import BaseModel

from app.constants.chat import QuestionType


class Question(BaseModel):
    content: str
    mode: Literal[QuestionType.RAG, QuestionType.CHAT, QuestionType.NEWSLETTER, QuestionType.AWS] = (
        QuestionType.CHAT
    )
    answer: str = ""
