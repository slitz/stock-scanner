import pytest
from src.indicators import get_latest_close


def test_latest_close_with_fixture():
    data = [
        {"symbol": "AAPL", "close": 150.0},
        {"symbol": "AAPL", "close": 152.0},
        {"symbol": "AAPL", "close": 153.0},
        {"symbol": "AAPL", "close": 151.0},
        {"symbol": "AAPL", "close": 155.0},
        {"symbol": "AAPL", "close": 154.0},
        {"symbol": "AAPL", "close": 156.0},
        {"symbol": "AAPL", "close": 157.0},
        {"symbol": "AAPL", "close": 158.0},
        {"symbol": "AAPL", "close": 159.0},
        {"symbol": "AAPL", "close": 160.0},
        {"symbol": "AAPL", "close": 161.0},
        {"symbol": "AAPL", "close": 162.0},
        {"symbol": "AAPL", "close": 163.0},
        {"symbol": "AAPL", "close": 164.0},
        {"symbol": "AAPL", "close": 165.0},
        {"symbol": "AAPL", "close": 166.0},
        {"symbol": "AAPL", "close": 167.0},
        {"symbol": "AAPL", "close": 168.0},
        {"symbol": "AAPL", "close": 169.0},
    ]
    latest = get_latest_close("AAPL", data)
    assert latest == pytest.approx(169.0)


def test_latest_with_no_date():
    data_no_date = [
        {"symbol": "AAPL", "close": 150.0},
        {"symbol": "AAPL", "close": 155.0},
    ]
    assert get_latest_close("AAPL", data_no_date) == pytest.approx(155.0)


def test_latest_no_data():
    assert get_latest_close("AAPL", []) == 0.0
