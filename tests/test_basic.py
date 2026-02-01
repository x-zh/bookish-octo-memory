import unittest
import json
from src.scraper.tsm_scraper import TSMScraper
from src.analysis.predictor import PricePredictor

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

if __name__ == "__main__":
    unittest.main()
