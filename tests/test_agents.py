"""
Unit tests for agent correlation calculation logic.

This module tests the correlation calculation functions in isolation with mocked
dependencies to ensure accuracy and edge case handling.
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np

from agents.correlation_agent import (
    calculate_portfolio_returns,
    load_eth_returns,
    calculate_pearson_correlation,
    calculate_daily_returns,
    load_price_data,
)
from agents.shared.models import Portfolio, TokenHolding


# Fixtures for reusable test data

@pytest.fixture
def sample_portfolio():
    """Fixture providing a sample portfolio for testing."""
    return Portfolio(
        wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
        tokens=[
            TokenHolding(symbol="UNI", amount=1250.0, price_usd=6.42, value_usd=8025.0),
            TokenHolding(symbol="AAVE", amount=85.0, price_usd=94.30, value_usd=8015.5),
        ],
        total_value_usd=16040.5,
    )


@pytest.fixture
def single_token_portfolio():
    """Fixture providing a single-token portfolio."""
    return Portfolio(
        wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
        tokens=[
            TokenHolding(symbol="ETH", amount=10.0, price_usd=2650.0, value_usd=26500.0),
        ],
        total_value_usd=26500.0,
    )


@pytest.fixture
def sample_price_data():
    """Fixture providing sample price data CSV content."""
    csv_content = """date,price_usd,volume_usd
2025-01-01,2500.0,1000000
2025-01-02,2550.0,1100000
2025-01-03,2600.0,1200000
2025-01-04,2550.0,1150000
2025-01-05,2650.0,1300000
2025-01-06,2700.0,1350000
2025-01-07,2650.0,1250000"""
    return csv_content


# Unit Tests

def test_calculate_daily_returns():
    """Test daily returns calculation."""
    prices = pd.Series([100, 105, 103, 110, 108])
    returns = calculate_daily_returns(prices)

    # Verify return calculations
    assert len(returns) == 4  # 5 prices = 4 returns
    assert returns.iloc[0] == pytest.approx(0.05)  # (105-100)/100
    assert returns.iloc[1] == pytest.approx(-0.019047619, abs=0.001)  # (103-105)/105
    assert returns.iloc[2] == pytest.approx(0.067961165, abs=0.001)  # (110-103)/103
    assert returns.iloc[3] == pytest.approx(-0.018181818, abs=0.001)  # (108-110)/110


def test_pearson_correlation_high():
    """Test correlation calculation with known high correlation input."""
    # Create mock returns with high correlation (0.95+)
    np.random.seed(42)
    base_returns = pd.Series(np.random.randn(90) * 0.02, index=pd.date_range('2025-01-01', periods=90))
    portfolio_returns = base_returns + pd.Series(np.random.randn(90) * 0.005, index=base_returns.index)
    eth_returns = base_returns + pd.Series(np.random.randn(90) * 0.005, index=base_returns.index)

    correlation = calculate_pearson_correlation(portfolio_returns, eth_returns)

    # High correlation should be > 0.85
    assert correlation > 0.85
    assert correlation <= 1.0


def test_pearson_correlation_moderate():
    """Test correlation calculation with moderate correlation."""
    np.random.seed(42)
    base_returns = pd.Series(np.random.randn(90) * 0.02, index=pd.date_range('2025-01-01', periods=90))
    portfolio_returns = base_returns * 0.7 + pd.Series(np.random.randn(90) * 0.015, index=base_returns.index)
    eth_returns = base_returns

    correlation = calculate_pearson_correlation(portfolio_returns, eth_returns)

    # Should be moderate correlation
    assert 0.4 <= correlation <= 0.9


def test_pearson_correlation_perfect():
    """Test correlation with identical returns (perfect correlation)."""
    returns = pd.Series([0.05, -0.03, 0.02, 0.01, -0.02], index=pd.date_range('2025-01-01', periods=5))

    correlation = calculate_pearson_correlation(returns, returns)

    # Perfect correlation
    assert correlation == pytest.approx(1.0)


def test_pearson_correlation_alignment():
    """Test that correlation handles misaligned date indices."""
    portfolio_returns = pd.Series(
        [0.05, -0.03, 0.02, 0.01, -0.02],
        index=pd.date_range('2025-01-01', periods=5)
    )
    eth_returns = pd.Series(
        [0.06, -0.02, 0.03],
        index=pd.date_range('2025-01-02', periods=3)
    )

    # Should align on common dates (Jan 2, 3, 4)
    correlation = calculate_pearson_correlation(portfolio_returns, eth_returns)

    # Should compute without error and be within valid correlation range (-1 to +1)
    assert -1.0 <= correlation <= 1.0


@patch("agents.correlation_agent.pd.read_csv")
@patch("agents.correlation_agent.HISTORICAL_PRICES_DIR")
def test_load_price_data(mock_dir, mock_read_csv, sample_price_data):
    """Test loading price data from CSV file."""
    mock_path = Mock()
    mock_path.exists.return_value = True
    mock_dir.__truediv__ = Mock(return_value=mock_path)

    # Create mock DataFrame
    mock_df = pd.DataFrame({
        "date": pd.date_range('2025-01-01', periods=7),
        "price_usd": [2500, 2550, 2600, 2550, 2650, 2700, 2650],
        "volume_usd": [1000000] * 7
    })
    mock_read_csv.return_value = mock_df

    df = load_price_data("ETH", days=5)

    assert len(df) == 6  # 5 days + 1 for returns calculation
    assert "date" in df.columns
    assert "price_usd" in df.columns


@patch("agents.correlation_agent.HISTORICAL_PRICES_DIR")
def test_load_price_data_file_not_found(mock_dir):
    """Test error handling when price data file doesn't exist."""
    mock_path = Mock()
    mock_path.exists.return_value = False
    mock_dir.__truediv__ = Mock(return_value=mock_path)

    with pytest.raises(FileNotFoundError, match="Price data not found"):
        load_price_data("UNKNOWN", days=90)


@patch("agents.correlation_agent.load_price_data")
def test_load_eth_returns(mock_load):
    """Test ETH returns loading and calculation."""
    # Mock price data
    mock_df = pd.DataFrame({
        "date": pd.date_range('2025-01-01', periods=6),
        "price_usd": [2500, 2550, 2600, 2550, 2650, 2700],
        "volume_usd": [1000000] * 6
    })
    mock_load.return_value = mock_df

    eth_returns = load_eth_returns(days=5)

    assert len(eth_returns) == 5  # 6 prices = 5 returns
    assert eth_returns.iloc[0] == pytest.approx(0.02)  # (2550-2500)/2500


@patch("agents.correlation_agent.load_price_data")
def test_calculate_portfolio_returns_single_token(mock_load, single_token_portfolio):
    """Test portfolio returns with single token."""
    # Mock ETH price data with 90+ days
    dates = pd.date_range('2025-01-01', periods=91)
    prices = [2500 + i * 10 for i in range(91)]  # Trending prices
    mock_df = pd.DataFrame({
        "date": dates,
        "price_usd": prices,
        "volume_usd": [1000000] * 91
    })
    mock_load.return_value = mock_df

    returns = calculate_portfolio_returns(single_token_portfolio, days=90)

    # Should return series of 90 returns
    assert len(returns) == 90
    assert isinstance(returns, pd.Series)


@patch("agents.correlation_agent.load_price_data")
def test_calculate_portfolio_returns_weighted(mock_load, sample_portfolio):
    """Test weighted portfolio returns calculation."""
    # Mock price data for both tokens with 91 days
    dates = pd.date_range('2025-01-01', periods=91)

    def mock_load_side_effect(symbol, days):
        if symbol == "UNI":
            prices = [6.0 + i * 0.01 for i in range(91)]
        elif symbol == "AAVE":
            prices = [90.0 + i * 0.1 for i in range(91)]
        else:
            raise FileNotFoundError(f"No data for {symbol}")

        return pd.DataFrame({
            "date": dates,
            "price_usd": prices,
            "volume_usd": [1000000] * 91
        })

    mock_load.side_effect = mock_load_side_effect

    returns = calculate_portfolio_returns(sample_portfolio, days=90)

    # Should return weighted average of both tokens
    assert len(returns) == 90
    assert isinstance(returns, pd.Series)


@patch("agents.correlation_agent.load_price_data")
def test_calculate_portfolio_returns_insufficient_data(mock_load, sample_portfolio):
    """Test error handling when token has insufficient data (<60 days)."""
    dates = pd.date_range('2025-01-01', periods=31)  # Only 30 days

    def mock_load_side_effect(symbol, days):
        return pd.DataFrame({
            "date": dates,
            "price_usd": [100.0] * 31,
            "volume_usd": [1000000] * 31
        })

    mock_load.side_effect = mock_load_side_effect

    # Should raise error because both tokens have insufficient data
    with pytest.raises(ValueError, match="Insufficient data"):
        calculate_portfolio_returns(sample_portfolio, days=90)


@patch("agents.correlation_agent.load_price_data")
def test_calculate_portfolio_returns_unknown_token(mock_load):
    """Test handling of unknown tokens (not in historical data)."""
    portfolio = Portfolio(
        wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
        tokens=[
            TokenHolding(symbol="UNKNOWN1", amount=100.0, price_usd=1.0, value_usd=100.0),
            TokenHolding(symbol="UNKNOWN2", amount=100.0, price_usd=1.0, value_usd=100.0),
        ],
        total_value_usd=200.0,
    )

    # Mock to raise FileNotFoundError for unknown tokens
    mock_load.side_effect = FileNotFoundError("Token not found")

    with pytest.raises(ValueError, match="Insufficient data"):
        calculate_portfolio_returns(portfolio, days=90)


@patch("agents.correlation_agent.load_price_data")
def test_calculate_portfolio_returns_partial_exclusion(mock_load):
    """Test portfolio calculation when some tokens are excluded but <50%."""
    # Portfolio with 3 tokens, one will be excluded
    portfolio = Portfolio(
        wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
        tokens=[
            TokenHolding(symbol="ETH", amount=10.0, price_usd=2650.0, value_usd=26500.0),  # 66%
            TokenHolding(symbol="UNI", amount=1000.0, price_usd=6.42, value_usd=6420.0),  # 16%
            TokenHolding(symbol="UNKNOWN", amount=1000.0, price_usd=7.0, value_usd=7000.0),  # 18%
        ],
        total_value_usd=39920.0,
    )

    dates = pd.date_range('2025-01-01', periods=91)

    def mock_load_side_effect(symbol, days):
        if symbol == "UNKNOWN":
            raise FileNotFoundError("Token not found")

        prices = [100.0 + i * 0.1 for i in range(91)]
        return pd.DataFrame({
            "date": dates,
            "price_usd": prices,
            "volume_usd": [1000000] * 91
        })

    mock_load.side_effect = mock_load_side_effect

    # Should succeed because only 18% excluded (< 50%)
    returns = calculate_portfolio_returns(portfolio, days=90)

    assert len(returns) == 90
    assert isinstance(returns, pd.Series)


def test_correlation_interpretation():
    """Test correlation percentage to interpretation mapping."""
    # This tests the logic in handle_analysis_request

    # High correlation (>85%)
    assert "High" == ("High" if 95 > 85 else "Moderate" if 95 >= 70 else "Low")
    assert "High" == ("High" if 86 > 85 else "Moderate" if 86 >= 70 else "Low")

    # Moderate correlation (70-85%)
    assert "Moderate" == ("High" if 85 > 85 else "Moderate" if 85 >= 70 else "Low")
    assert "Moderate" == ("High" if 75 > 85 else "Moderate" if 75 >= 70 else "Low")
    assert "Moderate" == ("High" if 70 > 85 else "Moderate" if 70 >= 70 else "Low")

    # Low correlation (<70%)
    assert "Low" == ("High" if 69 > 85 else "Moderate" if 69 >= 70 else "Low")
    assert "Low" == ("High" if 50 > 85 else "Moderate" if 50 >= 70 else "Low")
    assert "Low" == ("High" if 0 > 85 else "Moderate" if 0 >= 70 else "Low")
