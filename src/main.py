import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

from .indicators import (
    calculate_average_price,
    calculate_bollinger_bands,
    load_data_from_csv,
    get_latest_close,
    calculate_rsi,
    scan_for_opportunities,
)


def _resolve_data_file() -> Path:
    """Return the path to the prices.csv data file."""
    base_dir = Path(__file__).resolve().parents[1]
    return base_dir / "data" / "prices.csv"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate average close and Bollinger Bands for a stock")
    parser.add_argument("symbol", nargs="?", help="Stock symbol to query (e.g., AAPL)")
    parser.add_argument("--bands", action="store_true", help="Also print Bollinger Bands")
    parser.add_argument("--rsi", action="store_true", help="Also print Relative Strength Index (14-day)")
    parser.add_argument("--scan", action="store_true", help="Scan all stocks for oversold opportunities (latest close < lower band AND RSI < 30)")
    args = parser.parse_args(argv)

    data_file = _resolve_data_file()
    if not data_file.exists():
        print(f"Error: The data file was not found at: {data_file}")
        return 2

    try:
        data = load_data_from_csv(str(data_file))
    except Exception as e:
        print(f"Failed to load data: {e}")
        return 3

    if args.scan:
        opportunities = scan_for_opportunities(data)
        if not opportunities:
            print("No oversold opportunities found (price below lower band AND RSI < 30)")
            return 0
        
        print(f"Found {len(opportunities)} oversold opportunities:\n")
        print(f"{'Symbol':<10} {'Price':<12} {'Lower Band':<12} {'RSI':<8}")
        print("-" * 42)
        for opp in opportunities:
            print(f"{opp['symbol']:<10} ${opp['latest_close']:<11.2f} ${opp['lower_band']:<11.2f} {opp['rsi']:<7.2f}")
        return 0

    if not args.symbol:
        parser.print_help()
        return 1

    avg = calculate_average_price(args.symbol, data)
    if avg == 0.0:
        print(f"No data for symbol: {args.symbol}")
        return 0

    latest = get_latest_close(args.symbol, data)
    print(f"Close: ${latest:.2f}")
    print(f"Average: ${avg:.2f}")

    if args.bands:
        bands = calculate_bollinger_bands(args.symbol, data)
        print(f"Lower Band: ${bands['lower']:.2f}")
        print(f"Upper Band: ${bands['upper']:.2f}")

    if args.rsi:
        rsi = calculate_rsi(args.symbol, data)
        print(f"RSI (14): {rsi:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
