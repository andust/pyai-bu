from pydantic import BaseModel


class MemorySummary(BaseModel):
    content: str
    chat_id = str
