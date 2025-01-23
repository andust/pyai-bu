from pydantic import BaseModel, HttpUrl


class UrlsDTO(BaseModel):
    urls: list[HttpUrl]


class IdDTO(BaseModel):
    id: str
