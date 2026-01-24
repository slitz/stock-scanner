from typing import List, Dict, Any
import math
import csv
from pathlib import Path


def calculate_average_price(symbol: str, data: List[Dict[str, Any]]) -> float:
    """Return the average closing price for `symbol` using entries in `data`.
    Returns 0.0 when no matching prices are found."""
    prices: List[float] = []
    for entry in data:
        if entry.get("symbol") == symbol and "close" in entry:
            try:
                prices.append(float(entry["close"]))
            except (TypeError, ValueError):
                # Skip rows with invalid close values
                continue

    if not prices:
        return 0.0

    return sum(prices) / len(prices)


def calculate_bollinger_bands(symbol: str, data: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate Bollinger Bands (population std dev) for `symbol` over provided `data`.

    Returns a dict with keys: `average`, `std_dev`, `upper`, `lower`.
    Uses population standard deviation (divides by n) and band width = 2 * std_dev.
    If no data is found for `symbol`, all values are 0.0.
    """
    prices: List[float] = []
    for entry in data:
        if entry.get("symbol") == symbol and "close" in entry:
            try:
                prices.append(float(entry["close"]))
            except (TypeError, ValueError):
                continue

    if not prices:
        return {"average": 0.0, "std_dev": 0.0, "upper": 0.0, "lower": 0.0}

    avg = sum(prices) / len(prices)
    variance = sum((p - avg) ** 2 for p in prices) / len(prices)  # population variance
    std_dev = math.sqrt(variance)
    band_width = 2 * std_dev
    upper = avg + band_width
    lower = avg - band_width

    return {"average": avg, "std_dev": std_dev, "upper": upper, "lower": lower}


def get_latest_close(symbol: str, data: List[Dict[str, Any]]) -> float:
    """Return the latest closing price for `symbol`. Uses the 'date' field when available; otherwise uses the last occurrence."""
    from datetime import datetime

    dated_entries = []
    last_price = None
    for entry in data:
        if entry.get("symbol") == symbol and "close" in entry:
            try:
                close = float(entry["close"])
            except (TypeError, ValueError):
                continue
            date_str = entry.get("date")
            if date_str:
                try:
                    dt = datetime.fromisoformat(date_str)
                    dated_entries.append((dt, close))
                except ValueError:
                    # Ignore non-ISO dates for parsing; fallback to last_price
                    pass
            last_price = close

    if dated_entries:
        # pick entry with the max date
        return max(dated_entries, key=lambda x: x[0])[1]

    if last_price is not None:
        return last_price

    return 0.0


def calculate_rsi(symbol: str, data: List[Dict[str, Any]], period: int = 14) -> float:
    """Calculate the Relative Strength Index (RSI) for `symbol` over the preceding `period` trading days.
    
    RSI = 100 * (avg_gains / (avg_gains + avg_losses))
    
    Returns 0.0 if insufficient data or no data for symbol.
    """
    prices: List[float] = []
    for entry in data:
        if entry.get("symbol") == symbol and "close" in entry:
            try:
                prices.append(float(entry["close"]))
            except (TypeError, ValueError):
                continue

    if len(prices) < period + 1:
        # Need at least period + 1 prices to calculate period changes
        return 0.0

    # Get the last period + 1 prices to calculate period changes
    recent_prices = prices[-(period + 1):]

    # Calculate gains and losses
    gains = []
    losses = []
    for i in range(1, len(recent_prices)):
        change = recent_prices[i] - recent_prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(change))

    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)

    if avg_loss == 0:
        # If there are no losses, RSI is 100
        return 100.0 if avg_gain > 0 else 0.0

    rsi = 100.0 * (avg_gain / (avg_gain + avg_loss))
    return rsi


def load_data_from_csv(file_path: str) -> List[Dict[str, Any]]:
    p = Path(file_path)
    data: List[Dict[str, Any]] = []
    with p.open(mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def scan_for_opportunities(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Scan all stocks in data and find those where:
    - Latest closing price is below the lower Bollinger Band
    - RSI (14-day) is below 30
    
    Returns a list of dicts with keys: symbol, latest_close, lower_band, rsi
    """
    # Get all unique symbols
    symbols = set()
    for entry in data:
        if "symbol" in entry:
            symbols.add(entry["symbol"])
    
    opportunities = []
    
    for symbol in sorted(symbols):
        latest_close = get_latest_close(symbol, data)
        bands = calculate_bollinger_bands(symbol, data)
        rsi = calculate_rsi(symbol, data)
        
        # Check both conditions
        if latest_close > 0 and latest_close < bands["lower"] and rsi < 30:
            opportunities.append({
                "symbol": symbol,
                "latest_close": latest_close,
                "lower_band": bands["lower"],
                "rsi": rsi,
            })
    
    return opportunities
