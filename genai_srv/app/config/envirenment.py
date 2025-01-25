from typing import Callable

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IS_PRODUCTION: bool
    API_VERSION: str
    OPENAI_API_KEY: str

    USER_SERVICE: str

    MONGO_CONNECTION: str
    MONGO_DB: str

    TEST_MONGO_CONNECTION: str
    TEST_MONGO_DB: str

    QDRANT_URL: str
    QDRANT_MAIN_DOCUMANTS: str
    QDRANT_ESTIMATION_FEED_DOCUMANTS: str


def _configure_initial_settings() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()  # type: ignore

    def fn() -> Settings:
        return settings

    return fn


get_settings = _configure_initial_settings()
