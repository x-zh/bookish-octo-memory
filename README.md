# WoW Classic Gold Maker Insights

An automated tool to mine gold-making insights from World of Warcraft (WoW) Classic Anniversary Edition (Fresh) Auction House data using TradeSkillMaster (TSM).

## Features

- **Automated Scraping**: Fetches "Market Value", "Quantity", and "Sale Rate" from TSM for high-value items on the **Dreamscythe-US** realm.
- **Price Analysis Engine**:
    - **Weekly Patterns**: Detects price dips compared to overall averages and specific day-of-week historical averages.
    - **Phase Prediction**: Identifies items that will spike in demand during future game phases (e.g., Elemental Earth for AQ, Arcanite Bars for Naxx).
- **Daily Automation**: Integrated GitHub Actions workflow runs the analysis daily and updates the price history.
- **CLI Dashboard**: Quick summary of "Buy", "Sell", and "Accumulate" recommendations.

## Setup

### Prerequisites

- Python 3.12+
- `pip`

### Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

## Usage

Run the main analysis script:

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 src/main.py
```

## Configuration

- **Items**: Add or remove items to track in `config/items.json`.
- **Roadmap**: Update phase dates and demand shifts in `config/roadmap.json`.

## Project Structure

- `src/main.py`: Entry point for the analysis.
- `src/scraper/`: Contains the TSM data collection logic.
- `src/analysis/`: Contains the prediction and signal generation engine.
- `src/utils/`: Storage and helper utilities.
- `.github/workflows/`: Daily automation configuration.
- `data/`: Local storage for price history (CSV).

## Disclaimer

This tool is intended for educational purposes. Use web scrapers responsibly and in accordance with the website's terms of service.
