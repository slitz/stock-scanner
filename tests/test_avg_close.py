# ...existing code...
import pytest
from src.indicators import calculate_average_price, calculate_bollinger_bands, get_latest_close

@pytest.fixture
def data():
    return [
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

def test_average_price(data):
    average = calculate_average_price("AAPL", data)
    assert average == pytest.approx(159.5)

def test_no_data():
    average = calculate_average_price("AAPL", [])
    assert average == 0.0

def test_different_symbol(data):
    average = calculate_average_price("GOOGL", data)
    assert average == 0.0


def test_bollinger_bands(data):
    bands = calculate_bollinger_bands("AAPL", data)
    assert bands["average"] == pytest.approx(159.5)
    # precomputed population std dev for 150..169 is sqrt(33.25)
    assert bands["std_dev"] == pytest.approx(5.766281297335398)
    assert bands["upper"] == pytest.approx(171.0325625946708)
    assert bands["lower"] == pytest.approx(147.9674374053292)


def test_bollinger_no_data():
    bands = calculate_bollinger_bands("AAPL", [])
    assert bands == {"average": 0.0, "std_dev": 0.0, "upper": 0.0, "lower": 0.0}

if __name__ == '__main__':
    import pytest
    pytest.main([__file__])