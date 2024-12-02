import io

from bs4 import BeautifulSoup
from fastapi import UploadFile
from playwright.async_api import async_playwright
from starlette.datastructures import Headers

from app.helpers.date.main import now_datetime


class ScraperUseCase:
    async def scrape_pages(self, urls: list[str]) -> list[UploadFile]:
        files = []
        async with async_playwright() as playwright:
            firefox = playwright.firefox
            browser = await firefox.launch()
            page = await browser.new_page()
            for url in urls:
                await page.goto(url)

                body = await page.query_selector("body")
                if body:
                    body_content = await body.inner_html()
                    soup = BeautifulSoup(body_content, "html.parser")
                    for data in soup(["style", "script"]):
                        data.decompose()

                    text_file = io.BytesIO(
                        " ".join(soup.stripped_strings).encode("utf-8")
                    )
                    upload_file = UploadFile(
                        file=text_file,
                        filename=f"{url} ({now_datetime()})",
                        headers=Headers({"Content-Type": "text/plain"})
                    )

                    files.append(upload_file)

            await browser.close()

        return files
