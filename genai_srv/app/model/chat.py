from pydantic import BaseModel

from app.model.question import Question


class Chat(BaseModel):
    id: str | None = None
    user_id: str
    title: str | None = None
    questions: list[Question] | None = None

    @staticmethod
    def from_dict(data: dict):
        return Chat(
            id=str(data.get("_id")) or None,
            user_id=data.get("user_id") or "",
            title=data.get("title") or "",
            questions=data.get("questions"),
        )
