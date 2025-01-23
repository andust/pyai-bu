from typing import Literal
from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    role: Literal["super-admin", "admin", "client"]

    @staticmethod
    def from_dict(data: dict):
        return User(
            id=data.get("_id", None),
            email=data.get("email", ""),
            role=data.get("role", []),
        )
