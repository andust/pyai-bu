from pydantic import BaseModel

from app.model.skill import Skill


class Developer(BaseModel):
    id: str | None = None
    user_id: str
    full_name: str
    skills: list[Skill]
    month_experience: int

    @staticmethod
    def from_dict(data: dict):
        return Developer(
            id=str(data.get("_id", "")),
            user_id=data.get("user_id", ""),
            full_name=data.get("full_name", ""),
            skills=data.get("skills", []),
            month_experience=data.get("month_experience", 1),
        )
