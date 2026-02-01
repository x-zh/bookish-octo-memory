import asyncio
import json
import re
import os
from playwright.async_api import async_playwright
from datetime import datetime

class TSMScraper:
    def __init__(self, realm_id=1086):
        self.realm_id = realm_id
        self.base_url = "https://tradeskillmaster.com/classic/us/items/{item_id}?realm={realm_id}"
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

    async def fetch_item_data(self, page, item_id):
        # Note: /items/ (plural) is required for Classic US items
        url = f"https://tradeskillmaster.com/classic/us/items/{item_id}?realm={self.realm_id}"

        print(f"Fetching data for item {item_id} from {url}...")
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            content = await page.content()

            market_value = self._extract_value(content, "marketValue")
            avg_sale_price = self._extract_value(content, "avgSalePrice")
            sale_rate = self._extract_value(content, "saleRate")

            # Extract Quantity from HTML
            quantity_match = re.search(r'Available Quantity</div><div class=\"[^\"]+\">(\d+)</div>', content)
            quantity = int(quantity_match.group(1)) if quantity_match else None

            # Extract Name from HTML
            name_match = re.search(r'<b class=\"q[0-9]\">([^<]+)</b>', content)
            name = name_match.group(1) if name_match else "Unknown"

            return {
                "item_id": item_id,
                "name": name,
                "market_value": market_value,
                "quantity": quantity,
                "avg_sale_price": avg_sale_price,
                "sale_rate": sale_rate,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching item {item_id}: {e}")
            return None

    async def fetch_all_items(self, item_list):
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = await context.new_page()

            for item in item_list:
                item_id = item['id']
                data = await self.fetch_item_data(page, item_id)
                if data:
                    results.append(data)
                await asyncio.sleep(2) # Be polite

            await browser.close()
        return results

    def _extract_value(self, content, key):
        # Match pattern: key\",value
        match = re.search(rf'{key}\\",([\d\.]+)', content)
        if match:
            val = match.group(1)
            try:
                return float(val) if '.' in val else int(val)
            except ValueError:
                return val
        return None

    def format_price(self, copper):
        if copper is None: return "N/A"
        gold = int(copper // 10000)
        silver = int((copper % 10000) // 100)
        cp = int(copper % 100)
        return f"{gold}g {silver}s {cp}c"

if __name__ == "__main__":
    scraper = TSMScraper()
    item_id = 13468 # Black Lotus

    async def run_test():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            data = await scraper.fetch_item_data(page, item_id)
            await browser.close()
            return data

    data = asyncio.run(run_test())
    if data:
        print(f"Item: {data['name']}")
        print(f"Market Value: {scraper.format_price(data['market_value'])}")
        print(f"Quantity: {data['quantity']}")
        print(f"Sale Rate: {data['sale_rate']}")
    else:
        print("Failed to fetch data.")
