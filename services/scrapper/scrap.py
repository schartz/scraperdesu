import os
import asyncio
from loguru import logger
import pathlib
from urllib.parse import urlparse

from playwright.async_api import async_playwright

from config import AppConfig
from models.schemas import ScrapeUpdateMessage, ScrapeUpdateMessagePayload
from services.mq_publisher import ActiveMQPublisher
from utils.helpers import loop_batched

config = AppConfig.get_config()


async def scrap_the_website(url: str = "", uid: str = "-1", cid: str = ""):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        href = await page.evaluate(
            "() => {return Array.from(document.links).map(item => item.href)}"
        )
        link_urls = []
        input_host = urlparse(url).hostname
        output_base = f"{config.EXCLUDED_PATH}/{input_host}"
        os.makedirs(output_base, exist_ok=True)

        for i in href:
            link = urlparse(i)
            if link.hostname == input_host and i not in link_urls:
                os.makedirs(
                    output_base + "/" + str(pathlib.Path(link.path).stem), exist_ok=True
                )
                link_urls.append(link.scheme + "://" + link.hostname + link.path)

        link_urls = list(set(link_urls))
        total_pages = len(link_urls)
        scraped_pages = 0

        for link_batch in loop_batched(link_urls):
            scraped_pages += len(link_batch)
            async with asyncio.TaskGroup() as tg:
                for link in link_batch:
                    _l = urlparse(link)
                    filepath = output_base + "/" + str(pathlib.Path(_l.path).stem)
                    txt_filename = (
                        filepath + "/" + str(pathlib.Path(_l.path).stem) + ".txt"
                    )

                    if str(pathlib.Path(_l.path).stem) == "":
                        txt_filename = filepath + _l.hostname + ".txt"

                    _ = tg.create_task(scrape_page(browser, link, txt_filename))
            update_message = ScrapeUpdateMessagePayload(
                company_id=cid,
                user_id=uid,
                total_pages=total_pages,
                scraped_pages=scraped_pages,
                is_done=scraped_pages == total_pages,
                website_url=url,
            )
            await send_scrape_update(update_message)

        await browser.close()
        logger.info("scraping complete")


async def scrape_page(
    browser, page_url: str, file_save_path: str, save_screenshot: bool = True
):
    try:
        page = await browser.new_page()
        await page.goto(page_url)
        a_handle = await page.evaluate_handle("document.body")
        result_handle = await page.evaluate_handle("body => body.innerText", a_handle)
        text = await result_handle.json_value()
        text = f"{page_url}\n\n{text}"
        with open(file_save_path, "w") as f:
            f.write(text)
        if save_screenshot:
            await page.screenshot(
                path=file_save_path.replace(".txt", ".png"), full_page=True
            )
        await page.close()

    except Exception as e:
        logger.info(e)


async def send_scrape_update(msg: ScrapeUpdateMessagePayload):
    _msg = ScrapeUpdateMessage(payload=msg)

    mq_publisher = ActiveMQPublisher.get_mq_connection()
    mq_publisher.publish(_msg.model_dump(), config.AQ_SCRAPE_QUEUE_PUB)
