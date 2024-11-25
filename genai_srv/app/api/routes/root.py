from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return "ok!"
