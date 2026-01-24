# Stock Scanner

A command line tool for scanning stocks based on technical indicators and identifying trading opportunities.

## Project Structure

```
stock-scanner
├── src
│   ├── main.py         # Command line interface for the tool
│   ├── indicators.py   # Logic for technical indicators
│   └── __init__.py     # Marks the directory as a Python package
├── tests
│   ├── test_avg_close.py     # Unit tests for average price calculation
│   ├── test_cli_output.py    # Unit tests for CLI output
│   ├── test_cli_rsi.py       # Unit tests for RSI calculation
│   ├── test_latest_close.py  # Unit tests for latest close
│   └── test_rsi.py           # Unit tests for RSI
├── data
│   ├── prices.csv            # CSV data with closing prices
│   └── sample_prices.csv     # Sample CSV data with closing prices
├── pyproject.toml       # Configuration file for the project
├── requirements.txt      # Required Python packages
└── README.md             # Project documentation
```

## Installation

To install the required packages, run:

```
pip install -r requirements.txt
```

## Usage

To calculate the average closing price for a specific stock symbol, use the following command:

```
python -m src.main <stock_symbol>
```

Replace `<stock_symbol>` with the desired stock symbol.

Optional flags:
- `--bands`: Display Bollinger Bands
- `--rsi`: Display Relative Strength Index (14-day)

## Example

If you want to calculate the average closing price and Bollinger Bands for the stock symbol "AAPL", you would run:

```
python -m src.main AAPL --bands
```

Or to include the RSI (Relative Strength Index):

```
python -m src.main AAPL --rsi
```

## License

This project is licensed under the MIT License.