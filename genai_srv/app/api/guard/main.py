from fastapi import HTTPException, Request, status
import httpx

from app.config.envirenment import get_settings
from app.model.user import User

_S = get_settings()


async def get_current_user(request: Request):
    access = request.cookies.get("access")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{_S.USER_SERVICE}/api/v1/user", cookies={"access": f"{access}"}
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return User(**response.json())
