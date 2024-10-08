import os
from icecream import ic
import pathlib
from urllib.parse import urlparse

from playwright.async_api import async_playwright

from config import AppConfig

config = AppConfig.get_config()


async def scrap_the_website(url: str = ""):
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

        for link in link_urls:
            
        await browser.close()
async def scrape_page(browser, page_url: str, file_save_path: str, save_screenshot: bool = True):
    try:
        page = await browser.new_page()
        await page.goto(page_url) 
        a_handle = await page.evaluate_handle("document.body")
        result_handle = await page.evaluate_handle(
            "body => body.innerText", a_handle
        )
        text = await result_handle.json_value()
        _l = urlparse(page_url) 
        # filepath = output_base + "/" + str(pathlib.Path(_l.path).stem)
        # txt_filename = filepath + "/" + str(pathlib.Path(_l.path).stem) + ".txt"

        # if str(pathlib.Path(_l.path).stem) == "":
        #     txt_filename = filepath + _l.hostname + ".txt"

        print("%%%", file_save_path)
        with open(file_save_path, "w") as f:
            f.write(text)

        print("****************************************")
        print("****************************************")
    except Exception as e:
        ic(e)

