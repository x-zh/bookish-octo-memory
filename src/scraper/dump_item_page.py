import asyncio
from playwright.async_api import async_playwright

async def dump_item_page(item_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = f"https://tradeskillmaster.com/classic/us/items/{item_id}?realm=1086"
        print(f"Navigating to {url}...")
        await page.goto(url)
        await page.wait_for_timeout(5000) # Wait for JS
        content = await page.content()
        with open(f"item_{item_id}.html", "w") as f:
            f.write(content)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(dump_item_page(13468)) # Black Lotus
