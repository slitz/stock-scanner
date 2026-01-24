import pytest
from src.indicators import calculate_rsi


def test_rsi_uptrend():
    """Test RSI with a steady uptrend - should be high RSI (close to 100)."""
    data = [
        {"symbol": "TEST", "close": 100.0},
        {"symbol": "TEST", "close": 101.0},
        {"symbol": "TEST", "close": 102.0},
        {"symbol": "TEST", "close": 103.0},
        {"symbol": "TEST", "close": 104.0},
        {"symbol": "TEST", "close": 105.0},
        {"symbol": "TEST", "close": 106.0},
        {"symbol": "TEST", "close": 107.0},
        {"symbol": "TEST", "close": 108.0},
        {"symbol": "TEST", "close": 109.0},
        {"symbol": "TEST", "close": 110.0},
        {"symbol": "TEST", "close": 111.0},
        {"symbol": "TEST", "close": 112.0},
        {"symbol": "TEST", "close": 113.0},
        {"symbol": "TEST", "close": 114.0},
    ]
    rsi = calculate_rsi("TEST", data, period=14)
    # In a pure uptrend with +1.0 changes each period, avg_gain=1.0, avg_loss=0.0, so RSI=100
    assert rsi == pytest.approx(100.0)


def test_rsi_downtrend():
    """Test RSI with a steady downtrend - should be low RSI (close to 0)."""
    data = [
        {"symbol": "TEST", "close": 114.0},
        {"symbol": "TEST", "close": 113.0},
        {"symbol": "TEST", "close": 112.0},
        {"symbol": "TEST", "close": 111.0},
        {"symbol": "TEST", "close": 110.0},
        {"symbol": "TEST", "close": 109.0},
        {"symbol": "TEST", "close": 108.0},
        {"symbol": "TEST", "close": 107.0},
        {"symbol": "TEST", "close": 106.0},
        {"symbol": "TEST", "close": 105.0},
        {"symbol": "TEST", "close": 104.0},
        {"symbol": "TEST", "close": 103.0},
        {"symbol": "TEST", "close": 102.0},
        {"symbol": "TEST", "close": 101.0},
        {"symbol": "TEST", "close": 100.0},
    ]
    rsi = calculate_rsi("TEST", data, period=14)
    # In a pure downtrend with -1.0 changes each period, avg_gain=0.0, avg_loss=1.0, so RSI=0
    assert rsi == pytest.approx(0.0)


def test_rsi_mixed():
    """Test RSI with mixed up and down movements."""
    data = [
        {"symbol": "TEST", "close": 100.0},
        {"symbol": "TEST", "close": 101.0},  # +1
        {"symbol": "TEST", "close": 100.0},  # -1
        {"symbol": "TEST", "close": 102.0},  # +2
        {"symbol": "TEST", "close": 101.0},  # -1
        {"symbol": "TEST", "close": 103.0},  # +2
        {"symbol": "TEST", "close": 102.0},  # -1
        {"symbol": "TEST", "close": 104.0},  # +2
        {"symbol": "TEST", "close": 103.0},  # -1
        {"symbol": "TEST", "close": 105.0},  # +2
        {"symbol": "TEST", "close": 104.0},  # -1
        {"symbol": "TEST", "close": 106.0},  # +2
        {"symbol": "TEST", "close": 105.0},  # -1
        {"symbol": "TEST", "close": 107.0},  # +2
        {"symbol": "TEST", "close": 106.0},  # -1
    ]
    rsi = calculate_rsi("TEST", data, period=14)
    # Over 14 periods: gains = [1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0]
    # losses = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    # avg_gain = (1+2+2+2+2+2+2) / 14 = 13/14 ≈ 0.9286
    # avg_loss = (1+1+1+1+1+1+1) / 14 = 7/14 = 0.5
    # RSI = 100 * (0.9286 / (0.9286 + 0.5)) ≈ 100 * 0.65 ≈ 65
    assert rsi == pytest.approx(64.99, abs=0.1)


def test_rsi_insufficient_data():
    """Test RSI with insufficient data returns 0.0."""
    data = [
        {"symbol": "TEST", "close": 100.0},
        {"symbol": "TEST", "close": 101.0},
    ]
    rsi = calculate_rsi("TEST", data, period=14)
    assert rsi == 0.0


def test_rsi_no_data():
    """Test RSI with no data for symbol returns 0.0."""
    data = [
        {"symbol": "OTHER", "close": 100.0},
    ]
    rsi = calculate_rsi("TEST", data, period=14)
    assert rsi == 0.0


def test_rsi_custom_period():
    """Test RSI with custom period."""
    data = [
        {"symbol": "TEST", "close": 100.0},
        {"symbol": "TEST", "close": 101.0},
        {"symbol": "TEST", "close": 102.0},
        {"symbol": "TEST", "close": 103.0},
        {"symbol": "TEST", "close": 104.0},
    ]
    rsi = calculate_rsi("TEST", data, period=4)
    # 4 changes: +1, +1, +1, +1
    # avg_gain = 1.0, avg_loss = 0.0
    assert rsi == pytest.approx(100.0)
