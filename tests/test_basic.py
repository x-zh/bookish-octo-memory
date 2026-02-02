import unittest
import json
from src.scraper.tsm_scraper import TSMScraper
from src.analysis.predictor import PricePredictor
from src.utils.html_generator import HTMLGenerator
import os

class TestGoldMaker(unittest.TestCase):
    def test_price_formatting(self):
        scraper = TSMScraper()
        self.assertEqual(scraper.format_price(1773209), "177g 32s 9c")
        self.assertEqual(scraper.format_price(50), "0g 0s 50c")
        self.assertEqual(scraper.format_price(10200), "1g 2s 0c")

    def test_predictor_no_history(self):
        # Should not crash if history is missing
        predictor = PricePredictor(history_filepath="nonexistent.csv")
        signals = predictor.analyze_item(13468, 10000)
        self.assertIsInstance(signals, list)

    def test_html_generation(self):
        predictor = PricePredictor()
        generator = HTMLGenerator(output_dir="test_docs")
        results = [
            {"item_id": 13468, "name": "Black Lotus", "market_value": 10000, "quantity": 5, "sale_rate": 0.5}
        ]
        generator.generate(results, predictor)
        self.assertTrue(os.path.exists("test_docs/index.html"))
        # Clean up
        if os.path.exists("test_docs/index.html"):
            os.remove("test_docs/index.html")
        if os.path.exists("test_docs"):
            os.rmdir("test_docs")

if __name__ == "__main__":
    unittest.main()
