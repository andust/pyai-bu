from typing import Literal
from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    role: Literal["super-admin", "admin", "client"]
