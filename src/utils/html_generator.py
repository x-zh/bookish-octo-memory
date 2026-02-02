import pandas as pd
import json
import os
from datetime import datetime

class HTMLGenerator:
    def __init__(self, history_filepath="data/price_history.csv", roadmap_filepath="config/roadmap.json", output_dir="docs"):
        self.history_filepath = history_filepath
        self.roadmap_filepath = roadmap_filepath
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def format_price(self, copper):
        if copper is None or pd.isna(copper): return "N/A"
        gold = int(copper // 10000)
        silver = int((copper % 10000) // 100)
        cp = int(copper % 100)
        return f"{gold}g {silver}s {cp}c"

    def generate(self, results, predictor):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Load roadmap
        with open(self.roadmap_filepath, 'r') as f:
            roadmap = json.load(f)

        items_html = ""
        for item in results:
            signals = predictor.analyze_item(item['item_id'], item['market_value'])
            signals_html = "".join([f'<span class="badge bg-info text-dark me-1">{s}</span>' for s in signals])
            if not signals_html:
                signals_html = '<span class="text-muted">No signals</span>'

            items_html += f"""
            <tr>
                <td>{item['name']}</td>
                <td>{self.format_price(item['market_value'])}</td>
                <td>{item['quantity'] or 'N/A'}</td>
                <td>{item['sale_rate'] or 'N/A'}</td>
                <td>{signals_html}</td>
            </tr>
            """

        roadmap_html = ""
        for phase in roadmap['phases']:
            status_class = "table-primary" if phase['status'] == 'Current' else "table-secondary" if phase['status'] == 'Upcoming' else ""
            roadmap_html += f"""
            <tr class="{status_class}">
                <td>{phase['name']}</td>
                <td>{phase['date']}</td>
                <td>{phase['status']}</td>
            </tr>
            """

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WoW Classic Gold Maker Insights</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; }}
        .container {{ margin-top: 30px; }}
        .card {{ margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ background-color: #212529; color: white; padding: 20px 0; margin-bottom: 30px; }}
    </style>
</head>
<body>
    <div class="header text-center">
        <h1>WoW Classic Gold Maker Insights</h1>
        <p>Realm: Dreamscythe-US | Last Updated: {now}</p>
    </div>

    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header bg-dark text-white">
                        <h2 class="h5 mb-0">Market Recommendations</h2>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Item Name</th>
                                        <th>Market Value</th>
                                        <th>Quantity</th>
                                        <th>Sale Rate</th>
                                        <th>Signals</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {items_html}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header bg-dark text-white">
                        <h2 class="h5 mb-0">Phase Roadmap</h2>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Phase</th>
                                        <th>Estimated Date</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {roadmap_html}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-center text-muted py-4">
        <p>Data provided by TradeSkillMaster Scraper</p>
    </footer>
</body>
</html>
        """

        with open(os.path.join(self.output_dir, "index.html"), "w") as f:
            f.write(html_content)
        print(f"Report generated at {os.path.join(self.output_dir, 'index.html')}")
