from typing import List, Dict, Any
import math
import csv
from pathlib import Path


def calculate_average_price(symbol: str, data: List[Dict[str, Any]], period: int) -> float:
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
    
    recent_prices = prices[-period:]

    return sum(recent_prices) / period

def calculate_bollinger_bands(symbol: str, data: List[Dict[str, Any]], period: int) -> Dict[str, float]:
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

    recent_prices = prices[-period:]

    avg = sum(recent_prices) / period
    variance = sum((p - avg) ** 2 for p in recent_prices) / period  # population variance
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

def calculate_rsi(symbol: str, data: List[Dict[str, Any]], period: int) -> float:
    """Calculate the Relative Strength Index (RSI) for `symbol` using Wilder's smoothing.

    RSI = 100 - 100 / (1 + RS), where
    RS = smoothed_avg_gain / smoothed_avg_loss

    Wilder's smoothing is a recursive average:
      avg_gain_t = (avg_gain_{t-1} * (period - 1) + gain_t) / period
      avg_loss_t = (avg_loss_{t-1} * (period - 1) + loss_t) / period

    Returns 0.0 if insufficient data or no data for symbol.
    Preserves prior behavior for edge cases:
      - If avg_loss == 0 and avg_gain > 0 => 100.0
      - If avg_loss == 0 and avg_gain == 0 => 0.0
    """

    # Collect rows for the symbol and (optionally) sort if a 'date' field is present.
    rows = [entry for entry in data if entry.get("symbol") == symbol and "close" in entry]
    if not rows:
        return 0.0

    # If a sortable 'date' key exists, sort by it to be safe; otherwise assume input is chronological.
    try:
        rows.sort(key=lambda x: x.get("date"))
    except Exception:
        pass

    # Extract/clean closes
    prices: List[float] = []
    for entry in rows:
        try:
            prices.append(float(entry["close"]))
        except (TypeError, ValueError):
            continue

    # Need at least period + 1 prices to compute initial period changes
    if len(prices) < period + 1:
        return 0.0

    # --- 1) Initial averages from the first `period` changes
    recent_prices = prices[-(period + 1):]
    gains: List[float] = []
    losses: List[float] = []
    for i in range(1, period + 1):        
        change = recent_prices[i] - recent_prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(-change)  # positive loss magnitude
            
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    # --- 2) Wilder smoothing over the rest of the series
    for i in range(period + 1, len(prices)):
        change = prices[i] - prices[i - 1]
        gain = change if change > 0 else 0.0
        loss = -change if change < 0 else 0.0

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        
    # --- 3) Final RSI for the latest point
    if avg_loss == 0.0:
        # Preserve your previous convention:
        #  - 100 if there are gains and no losses
        #  - 0 if there are neither (flat) or gains==0
        return 100.0 if avg_gain > 0 else 0.0

    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi

def load_data_from_csv(file_path: str) -> List[Dict[str, Any]]:
    p = Path(file_path)
    data: List[Dict[str, Any]] = []
    with p.open(mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def scan_for_opportunities(data: List[Dict[str, Any]], bollinger_bands_period: int, rsi_period: int) -> List[Dict[str, Any]]:
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
        bands = calculate_bollinger_bands(symbol, data, bollinger_bands_period)  # Use 20-day period for bands
        rsi = calculate_rsi(symbol, data, rsi_period)
        
        # Check both conditions
        if latest_close > 0 and latest_close < bands["lower"] and rsi < 30:
            opportunities.append({
                "symbol": symbol,
                "latest_close": latest_close,
                "lower_band": bands["lower"],
                "rsi": rsi,
            })
    
    return opportunities
