import asyncio
import json
import os
from src.scraper.tsm_scraper import TSMScraper
from src.utils.storage import PriceStorage
from src.analysis.predictor import PricePredictor

async def main():
    print("=== WoW Classic Gold Making Insights ===")

    # 1. Load Items
    try:
        with open("config/items.json", "r") as f:
            items_config = json.load(f)
            items = items_config["items"]
    except Exception as e:
        print(f"Error loading items: {e}")
        return

    # 2. Scrape Data
    scraper = TSMScraper(realm_id=1086)
    print(f"Scraping data for {len(items)} items...")
    results = await scraper.fetch_all_items(items)

    # 3. Store Data
    storage = PriceStorage()
    storage.save_data(results)

    # 4. Analyze and Predict
    predictor = PricePredictor()
    print("\n--- Top Recommendations ---")
    found_recommendation = False

    for item_data in results:
        signals = predictor.analyze_item(item_data['item_id'], item_data['market_value'])
        if signals:
            found_recommendation = True
            print(f"\nItem: {item_data['name']} ({item_data['item_id']})")
            print(f"Current Price: {scraper.format_price(item_data['market_value'])}")
            for signal in signals:
                print(f"  [!] {signal}")

    if not found_recommendation:
        print("No specific buy/sell signals at this time.")

if __name__ == "__main__":
    asyncio.run(main())
