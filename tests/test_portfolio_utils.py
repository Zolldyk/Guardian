"""
Unit tests for portfolio parsing and loading utilities.

Tests cover:
- Valid portfolio parsing
- Invalid data rejection (bad addresses, negative values, empty tokens)
- Demo wallet loading
- Portfolio value calculations
"""

import json
from unittest.mock import mock_open, patch

import pytest

from agents.shared.models import Portfolio
from agents.shared.portfolio_utils import (
    InvalidPortfolioError,
    list_demo_wallets,
    load_demo_wallet,
    parse_portfolio,
)


# Fixtures for test data
@pytest.fixture
def valid_portfolio_data():
    """Valid portfolio data for testing."""
    return {
        "wallet_address": "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        "tokens": [
            {"symbol": "UNI", "amount": 1250.0, "price_usd": 6.42, "value_usd": 8025.0},
            {"symbol": "AAVE", "amount": 85.0, "price_usd": 94.30, "value_usd": 8015.5},
        ],
        "total_value_usd": 16040.5,
    }


@pytest.fixture
def demo_wallets_json():
    """Mock demo wallets JSON data."""
    return {
        "wallets": [
            {
                "wallet_address": "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
                "name": "Test Wallet 1",
                "risk_profile": "high",
                "tokens": [
                    {
                        "symbol": "UNI",
                        "amount": 5000.0,
                        "price_usd": 6.42,
                        "value_usd": 32100.0,
                    }
                ],
                "total_value_usd": 32100.0,
            },
            {
                "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
                "name": "Test Wallet 2",
                "risk_profile": "moderate",
                "tokens": [
                    {
                        "symbol": "ETH",
                        "amount": 10.0,
                        "price_usd": 2650.0,
                        "value_usd": 26500.0,
                    }
                ],
                "total_value_usd": 26500.0,
            },
        ]
    }


# Test: Valid portfolio parsing
def test_parse_valid_portfolio(valid_portfolio_data):
    """Test parsing valid JSON into Portfolio model."""
    portfolio = parse_portfolio(valid_portfolio_data)

    assert isinstance(portfolio, Portfolio)
    assert portfolio.wallet_address == "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58"
    assert len(portfolio.tokens) == 2
    assert portfolio.tokens[0].symbol == "UNI"
    assert portfolio.tokens[0].amount == 1250.0
    assert portfolio.tokens[1].symbol == "AAVE"
    assert portfolio.total_value_usd == 16040.5
    assert portfolio.analysis_timestamp is not None


# Test: Invalid wallet address
def test_parse_invalid_wallet_address():
    """Test rejection of malformed wallet addresses."""
    # Missing 0x prefix
    invalid_data = {
        "wallet_address": "9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        "tokens": [
            {"symbol": "UNI", "amount": 100, "price_usd": 6.0, "value_usd": 600}
        ],
        "total_value_usd": 600,
    }

    with pytest.raises(InvalidPortfolioError) as excinfo:
        parse_portfolio(invalid_data)

    assert "validation failed" in str(excinfo.value).lower()

    # Wrong length (too short)
    invalid_data["wallet_address"] = "0x123"

    with pytest.raises(InvalidPortfolioError):
        parse_portfolio(invalid_data)

    # Invalid characters
    invalid_data["wallet_address"] = "0xZZZZD891ab1FaA750FAE5aba9b55623c7F69fD58"

    with pytest.raises(InvalidPortfolioError):
        parse_portfolio(invalid_data)


# Test: Negative amounts
def test_parse_negative_amounts():
    """Test rejection of negative token amounts."""
    invalid_data = {
        "wallet_address": "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        "tokens": [
            {"symbol": "UNI", "amount": -10, "price_usd": 6.42, "value_usd": -64.2}
        ],
        "total_value_usd": -64.2,
    }

    with pytest.raises(InvalidPortfolioError) as excinfo:
        parse_portfolio(invalid_data)

    assert "validation failed" in str(excinfo.value).lower()


# Test: Negative prices
def test_parse_negative_prices():
    """Test rejection of negative token prices."""
    invalid_data = {
        "wallet_address": "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        "tokens": [
            {"symbol": "UNI", "amount": 100, "price_usd": -6.42, "value_usd": -642.0}
        ],
        "total_value_usd": -642.0,
    }

    with pytest.raises(InvalidPortfolioError):
        parse_portfolio(invalid_data)


# Test: Zero amounts
def test_parse_zero_amounts():
    """Test rejection of zero token amounts."""
    invalid_data = {
        "wallet_address": "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        "tokens": [{"symbol": "UNI", "amount": 0, "price_usd": 6.42, "value_usd": 0}],
        "total_value_usd": 0,
    }

    with pytest.raises(InvalidPortfolioError):
        parse_portfolio(invalid_data)


# Test: Empty tokens list
def test_parse_empty_tokens_list():
    """Test rejection of portfolios with no holdings."""
    invalid_data = {
        "wallet_address": "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        "tokens": [],
        "total_value_usd": 0,
    }

    with pytest.raises(InvalidPortfolioError) as excinfo:
        parse_portfolio(invalid_data)

    assert "validation failed" in str(excinfo.value).lower()


# Test: Missing required fields
def test_parse_missing_fields():
    """Test rejection of portfolios with missing required fields."""
    # Missing wallet_address
    invalid_data = {
        "tokens": [
            {"symbol": "UNI", "amount": 100, "price_usd": 6.0, "value_usd": 600}
        ],
        "total_value_usd": 600,
    }

    with pytest.raises(InvalidPortfolioError):
        parse_portfolio(invalid_data)

    # Missing tokens
    invalid_data = {
        "wallet_address": "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        "total_value_usd": 600,
    }

    with pytest.raises(InvalidPortfolioError):
        parse_portfolio(invalid_data)


# Test: Portfolio total value calculation
def test_portfolio_total_value_calculation(valid_portfolio_data):
    """Verify total_value_usd matches sum of token values."""
    portfolio = parse_portfolio(valid_portfolio_data)

    # Calculate sum of token values
    calculated_total = sum(token.value_usd for token in portfolio.tokens)

    # Should match the total_value_usd
    assert portfolio.total_value_usd == calculated_total
    assert portfolio.total_value_usd == 16040.5


# Test: Load demo wallet with mock
def test_load_demo_wallet_with_mock(demo_wallets_json):
    """Test loading demo wallet from mocked JSON file."""
    mock_json_data = json.dumps(demo_wallets_json)

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch("pathlib.Path.exists", return_value=True):
            portfolio = load_demo_wallet("0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58")

            assert isinstance(portfolio, Portfolio)
            assert (
                portfolio.wallet_address
                == "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58"
            )
            assert len(portfolio.tokens) == 1
            assert portfolio.tokens[0].symbol == "UNI"
            assert portfolio.total_value_usd == 32100.0


# Test: Load demo wallet - wallet not found
def test_load_demo_wallet_not_found(demo_wallets_json):
    """Test error handling when wallet address not found."""
    mock_json_data = json.dumps(demo_wallets_json)

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch("pathlib.Path.exists", return_value=True):
            with pytest.raises(InvalidPortfolioError) as excinfo:
                load_demo_wallet("0xNOTFOUND000000000000000000000000000000")

            assert "not found" in str(excinfo.value).lower()


# Test: Load demo wallet - file not found
def test_load_demo_wallet_file_not_found():
    """Test error handling when demo-wallets.json doesn't exist."""
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError) as excinfo:
            load_demo_wallet("0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58")

        assert "not found" in str(excinfo.value).lower()


# Test: List demo wallets with mock
def test_list_demo_wallets_with_mock(demo_wallets_json):
    """Test listing all demo wallet addresses."""
    mock_json_data = json.dumps(demo_wallets_json)

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch("pathlib.Path.exists", return_value=True):
            addresses = list_demo_wallets()

            assert len(addresses) == 2
            assert "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58" in addresses
            assert "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0" in addresses


# Integration test: Load each real demo wallet
def test_load_all_real_demo_wallets():
    """Integration test: Load and validate all real demo wallets from file."""
    try:
        addresses = list_demo_wallets()
        assert len(addresses) >= 3, "Expected at least 3 demo wallets"

        for addr in addresses:
            portfolio = load_demo_wallet(addr)
            assert isinstance(portfolio, Portfolio)
            assert portfolio.wallet_address == addr
            assert len(portfolio.tokens) >= 1
            assert portfolio.total_value_usd > 0
    except FileNotFoundError:
        pytest.skip("Demo wallets file not found - skipping integration test")
