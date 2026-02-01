import pandas as pd
import json
from datetime import datetime, timedelta

class PricePredictor:
    def __init__(self, history_filepath="data/price_history.csv", roadmap_filepath="config/roadmap.json"):
        self.history_filepath = history_filepath
        self.roadmap_filepath = roadmap_filepath
        self.history = self._load_history()
        self.roadmap = self._load_roadmap()

    def _load_history(self):
        try:
            df = pd.read_csv(self.history_filepath)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except:
            return pd.DataFrame(columns=['item_id', 'name', 'market_value', 'quantity', 'timestamp'])

    def _load_roadmap(self):
        try:
            with open(self.roadmap_filepath, 'r') as f:
                return json.load(f)
        except:
            return {"phases": [], "demand_shifts": []}

    def analyze_item(self, item_id, current_price):
        signals = []
        now = datetime.now()

        # 1. Weekly Pattern Analysis
        item_history = self.history[self.history['item_id'] == item_id].copy()
        if not item_history.empty:
            # Overall average
            avg_price = item_history['market_value'].mean()

            # Same day of week average
            day_of_week = now.weekday()
            same_day_history = item_history[item_history['timestamp'].dt.weekday == day_of_week]

            if not same_day_history.empty:
                day_avg = same_day_history['market_value'].mean()
                if current_price < day_avg * 0.95:
                    signals.append(f"BUY: Price is {((day_avg - current_price)/day_avg)*100:.1f}% below typical {now.strftime('%A')} price.")

            if current_price < avg_price * 0.9:
                signals.append(f"BUY: Price is {((avg_price - current_price)/avg_price)*100:.1f}% below overall historical average.")
            elif current_price > avg_price * 1.1:
                signals.append(f"SELL: Price is {((current_price - avg_price)/avg_price)*100:.1f}% above overall historical average.")

        # 2. Phase Demand Analysis
        upcoming_phase_names = [p['name'] for p in self.roadmap['phases'] if p['status'] in ['Upcoming', 'Future']]
        for shift in self.roadmap['demand_shifts']:
            if shift['phase'] in upcoming_phase_names and item_id in shift['item_ids']:
                signals.append(f"ACCUMULATE: High demand expected in {shift['phase']} due to {shift['reason']}.")

        return signals

if __name__ == "__main__":
    predictor = PricePredictor()
    # Sample test
    item_id = 13468 # Black Lotus
    current_price = 1500000 # 150g (Assume avg is 177g)
    signals = predictor.analyze_item(item_id, current_price)
    print(f"Signals for {item_id}: {signals}")
