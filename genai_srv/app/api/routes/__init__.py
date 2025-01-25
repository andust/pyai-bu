from fastapi.applications import FastAPI
from app.api.routes import (
    root,
    file,
    chat,
    rag,
    scraper,
    newsletter,
    estimation_feed,
    project,
)
from app.config.envirenment import get_settings


_S = get_settings()
PREFIX = f"/api/{_S.API_VERSION}"


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(root.router, prefix=PREFIX)
    app.include_router(file.router, prefix=PREFIX)
    app.include_router(chat.router, prefix=PREFIX)
    app.include_router(rag.router, prefix=PREFIX)
    app.include_router(newsletter.router, prefix=PREFIX)
    app.include_router(project.router, prefix=PREFIX)
    app.include_router(estimation_feed.router, prefix=PREFIX)
    app.include_router(scraper.router, prefix=PREFIX)
    return app
