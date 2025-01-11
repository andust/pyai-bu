from pydantic import BaseModel, HttpUrl


class UrlsQuery(BaseModel):
    urls: list[HttpUrl]
