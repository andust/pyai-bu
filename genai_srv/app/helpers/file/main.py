from io import BytesIO
from urllib.parse import urlparse
from fastapi import UploadFile
import httpx

from app.constants.file import MAX_FILE_SIZE
from app.helpers.string.main import byte_hash
from app.model.file import FileProtocol


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


async def content_to_file(content: str, filename: str) -> UploadFile:
    content_encode = content.encode("urf-8")
    if len(content_encode) > MAX_FILE_SIZE:
        raise ValueError("file to big - must be < 10 MB")

    byte_stram = BytesIO(content.encode("urf-8"))
    return UploadFile(filename=filename, file=byte_stram)


async def file_hash(file: FileProtocol) -> str:
    content = await file.read()
    await file.seek(0)
    return byte_hash(content)
