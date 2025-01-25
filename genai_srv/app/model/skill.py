from typing import Literal
from pydantic import BaseModel


class Skill(BaseModel):
    name: str
    level: Literal[1, 2, 3, 4, 5]

    @staticmethod
    def from_dict(data: dict):
        return Skill(
            name=data.get("name", ""),
            level=data.get("level", 1),
        )
