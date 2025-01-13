from dataclasses import dataclass

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.helpers.date.main import now_datetime


@dataclass
class ScrapeData:
    content: bytes
    filename: str
    headers: dict

class ScraperUseCase:
    async def scrape_pages(self, urls: list[str]) -> list[ScrapeData]:
        result = []
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

                    result.append(ScrapeData(
                        content=" ".join(soup.stripped_strings).encode("utf-8"),
                        filename=f"{url} ({now_datetime()})",
                        headers={"Content-Type": "text/plain"},
                    ))

            await browser.close()

        return result
