from io import BytesIO
from urllib.parse import urlparse
from fastapi import UploadFile
import httpx


def extract_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.path.split("/")[-1] or "downloaded_image"


async def download_file(url: str) -> UploadFile:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
    except (httpx.HTTPStatusError, httpx.RequestError):
        raise ValueError("Could not retrieve image from URL.")

    image_bytes = BytesIO(response.content)

    return UploadFile(
        filename=extract_filename_from_url(url),
        file=image_bytes,
        headers={"content-type": response.headers.get("content-type")},  # type: ignore
    )
