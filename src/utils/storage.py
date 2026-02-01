import pandas as pd
import os

class PriceStorage:
    def __init__(self, filepath="data/price_history.csv"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def save_data(self, data_list):
        if not data_list:
            return

        df_new = pd.DataFrame(data_list)

        if os.path.exists(self.filepath):
            df_old = pd.read_csv(self.filepath)
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            # Remove duplicates if same item and same timestamp (or close enough)
            # Actually, let's just keep everything and handle it in analysis
            df_combined.to_csv(self.filepath, index=False)
        else:
            df_new.to_csv(self.filepath, index=False)

        print(f"Saved {len(data_list)} records to {self.filepath}")

    def load_data(self):
        if os.path.exists(self.filepath):
            return pd.read_csv(self.filepath)
        return pd.DataFrame()
