from typing import Literal
from pydantic import BaseModel

from app.constants.chat import ChatMode



class Question(BaseModel):
    content: str
    context: Literal[ChatMode.RAG, ChatMode.CHAT] = ChatMode.CHAT
    answer: str = ""

