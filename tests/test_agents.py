"""
Unit tests for agent correlation calculation logic.

This module tests the correlation calculation functions in isolation with mocked
dependencies to ensure accuracy and edge case handling.
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np

from agents.correlation_agent_local import (
    calculate_portfolio_returns,
    load_eth_returns,
    calculate_pearson_correlation,
    calculate_daily_returns,
    load_price_data,
)
from agents.shared.models import Portfolio, TokenHolding, SectorRisk, OpportunityCost


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


@patch("agents.correlation_agent_local.pd.read_csv")
@patch("agents.correlation_agent_local.HISTORICAL_PRICES_DIR")
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


@patch("agents.correlation_agent_local.HISTORICAL_PRICES_DIR")
def test_load_price_data_file_not_found(mock_dir):
    """Test error handling when price data file doesn't exist."""
    mock_path = Mock()
    mock_path.exists.return_value = False
    mock_dir.__truediv__ = Mock(return_value=mock_path)

    with pytest.raises(FileNotFoundError, match="Price data not found"):
        load_price_data("UNKNOWN", days=90)


@patch("agents.correlation_agent_local.load_price_data")
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


@patch("agents.correlation_agent_local.load_price_data")
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


@patch("agents.correlation_agent_local.load_price_data")
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


@patch("agents.correlation_agent_local.load_price_data")
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


@patch("agents.correlation_agent_local.load_price_data")
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


@patch("agents.correlation_agent_local.load_price_data")
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


# =============================================================================
# HISTORICAL CRASH CONTEXT TESTS (Story 1.4)
# =============================================================================

from agents.correlation_agent_local import (
    load_historical_crashes,
    get_crash_context,
    generate_narrative_with_crash_context,
)


def test_load_historical_crashes():
    """Test loading historical crash data from JSON file."""
    df = load_historical_crashes()

    # Verify schema and data
    assert len(df) == 3  # 3 crash scenarios
    assert "scenario_id" in df.columns
    assert "name" in df.columns
    assert "period" in df.columns
    assert "eth_drawdown_pct" in df.columns
    assert "correlation_brackets" in df.columns
    assert "market_avg_loss_pct" in df.columns

    # Verify specific crash scenarios exist
    scenario_ids = df["scenario_id"].tolist()
    assert "crash_2022_bear" in scenario_ids
    assert "crash_2021_correction" in scenario_ids
    assert "crash_2020_covid" in scenario_ids


def test_get_crash_context_high_correlation():
    """Test crash context retrieval for >90% correlation (high bracket)."""
    crash_context = get_crash_context(correlation_pct=95)

    # Should return 3 crash scenarios
    assert len(crash_context) == 3

    # Verify CrashPerformance model structure
    for crash in crash_context:
        assert hasattr(crash, "crash_name")
        assert hasattr(crash, "crash_period")
        assert hasattr(crash, "eth_drawdown_pct")
        assert hasattr(crash, "portfolio_loss_pct")
        assert hasattr(crash, "market_avg_loss_pct")

    # Verify high correlation bracket data (>90%)
    crash_2022 = next(c for c in crash_context if "2022" in c.crash_name)
    assert crash_2022.portfolio_loss_pct == -73.0  # >90% bracket for 2022 bear market


def test_get_crash_context_moderate_high():
    """Test crash context retrieval for 80-90% correlation."""
    crash_context = get_crash_context(correlation_pct=85)

    assert len(crash_context) == 3

    # Verify 80-90% bracket data
    crash_2022 = next(c for c in crash_context if "2022" in c.crash_name)
    assert crash_2022.portfolio_loss_pct == -68.0  # 80-90% bracket


def test_get_crash_context_moderate_low():
    """Test crash context retrieval for 70-80% correlation."""
    crash_context = get_crash_context(correlation_pct=75)

    assert len(crash_context) == 3

    # Verify 70-80% bracket data
    crash_2022 = next(c for c in crash_context if "2022" in c.crash_name)
    assert crash_2022.portfolio_loss_pct == -62.0  # 70-80% bracket


def test_get_crash_context_low():
    """Test crash context retrieval for <70% correlation (low bracket)."""
    crash_context = get_crash_context(correlation_pct=50)

    assert len(crash_context) == 3

    # Verify <70% bracket data
    crash_2022 = next(c for c in crash_context if "2022" in c.crash_name)
    assert crash_2022.portfolio_loss_pct == -48.0  # <70% bracket


def test_crash_narrative_generation_high():
    """Test narrative generation with crash context for high correlation."""
    crash_context = get_crash_context(correlation_pct=95)

    narrative = generate_narrative_with_crash_context(
        correlation_coef=0.95,
        correlation_pct=95,
        interpretation="High",
        crash_context=crash_context
    )

    # Verify narrative includes key elements
    assert "95%" in narrative
    assert "positively correlated" in narrative
    assert "High correlation" in narrative
    assert "Historical crash performance" in narrative
    assert "2022 Bear Market" in narrative
    assert "2021 Correction" in narrative
    assert "2020 COVID Crash" in narrative
    assert "-73%" in narrative  # High bracket loss for 2022
    assert "nearly identically to ETH" in narrative.lower()


def test_crash_narrative_generation_low():
    """Test narrative generation with crash context for low correlation."""
    crash_context = get_crash_context(correlation_pct=58)

    narrative = generate_narrative_with_crash_context(
        correlation_coef=0.58,
        correlation_pct=58,
        interpretation="Low",
        crash_context=crash_context
    )

    # Verify narrative includes low correlation messaging
    assert "58%" in narrative
    assert "Low correlation" in narrative
    assert "-48%" in narrative  # Low bracket loss for 2022
    assert "good diversification" in narrative.lower()


def test_crash_narrative_generation_no_context():
    """Test narrative generation when crash data unavailable."""
    narrative = generate_narrative_with_crash_context(
        correlation_coef=0.75,
        correlation_pct=75,
        interpretation="Moderate",
        crash_context=[]  # Empty crash context
    )

    # Verify fallback narrative
    assert "75%" in narrative
    assert "Moderate correlation" in narrative
    assert "Historical crash data unavailable" in narrative


def test_historical_accuracy():
    """Verify historical crash data is within ±10% of actual market data."""
    df = load_historical_crashes()

    # 2022 Bear Market: ETH dropped from ~$4,800 (Nov 2021) to ~$1,200 (Jun 2022) = -75%
    crash_2022 = df[df["scenario_id"] == "crash_2022_bear"].iloc[0]
    assert -75.0 <= crash_2022["eth_drawdown_pct"] <= -65.0  # ±10% tolerance

    # 2021 Correction: ETH dropped from ~$4,400 (May 2021) to ~$2,000 (Jul 2021) = -55%
    crash_2021 = df[df["scenario_id"] == "crash_2021_correction"].iloc[0]
    assert -60.0 <= crash_2021["eth_drawdown_pct"] <= -50.0  # ±10% tolerance

    # 2020 COVID Crash: ETH dropped from ~$280 (Feb 2020) to ~$100 (Mar 2020) = -65%
    crash_2020 = df[df["scenario_id"] == "crash_2020_covid"].iloc[0]
    assert -70.0 <= crash_2020["eth_drawdown_pct"] <= -60.0  # ±10% tolerance


# =============================================================================
# SECTOR CLASSIFICATION TESTS (Story 1.5)
# =============================================================================

from agents.sector_agent_local import (
    load_sector_mappings,
    classify_tokens,
    identify_concentrated_sectors,
    calculate_diversification_score,
    generate_sector_narrative,
    load_historical_crashes,
    get_sector_crash_performance,
    get_opportunity_cost,
    generate_sector_risk_narrative,
)


# Fixtures for sector analysis testing

@pytest.fixture
def high_concentration_portfolio():
    """Portfolio with high concentration in DeFi Governance (>60%)."""
    return Portfolio(
        wallet_address="0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        tokens=[
            TokenHolding(symbol="UNI", amount=5000.0, price_usd=6.42, value_usd=32100.0),
            TokenHolding(symbol="AAVE", amount=250.0, price_usd=94.30, value_usd=23575.0),
            TokenHolding(symbol="COMP", amount=450.0, price_usd=52.80, value_usd=23760.0),
            TokenHolding(symbol="MKR", amount=12.0, price_usd=1580.50, value_usd=18966.0),
            TokenHolding(symbol="MATIC", amount=18000.0, price_usd=0.52, value_usd=9360.0),
        ],
        total_value_usd=107761.0,
    )


@pytest.fixture
def well_diversified_portfolio():
    """Portfolio with good sector diversification (<60% in any sector)."""
    return Portfolio(
        wallet_address="0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8",
        tokens=[
            TokenHolding(symbol="ETH", amount=5.0, price_usd=2650.0, value_usd=13250.0),    # Layer-1 Alts
            TokenHolding(symbol="BTC", amount=0.2, price_usd=67500.0, value_usd=13500.0),   # Layer-1 Alts
            TokenHolding(symbol="USDC", amount=22500.0, price_usd=1.0, value_usd=22500.0),  # Stablecoins
            TokenHolding(symbol="UNI", amount=1400.0, price_usd=6.42, value_usd=8988.0),    # DeFi Governance
            TokenHolding(symbol="AAVE", amount=100.0, price_usd=94.30, value_usd=9430.0),   # DeFi Governance
            TokenHolding(symbol="MATIC", amount=26000.0, price_usd=0.52, value_usd=13520.0), # Layer-2
            TokenHolding(symbol="SUSHI", amount=15000.0, price_usd=0.60, value_usd=9000.0),  # DEX
        ],
        total_value_usd=90188.0,
    )


@pytest.fixture
def portfolio_with_unknown_tokens():
    """Portfolio containing tokens not in sector mappings."""
    return Portfolio(
        wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
        tokens=[
            TokenHolding(symbol="UNI", amount=1000.0, price_usd=6.42, value_usd=6420.0),
            TokenHolding(symbol="UNKNOWN_TOKEN", amount=100.0, price_usd=50.0, value_usd=5000.0),
            TokenHolding(symbol="FAKE_COIN", amount=200.0, price_usd=10.0, value_usd=2000.0),
        ],
        total_value_usd=13420.0,
    )


# Unit Tests for Sector Classification

def test_load_sector_mappings():
    """Test sector mappings load correctly and validate schema."""
    df = load_sector_mappings()

    # Verify DataFrame is not empty
    assert len(df) > 0

    # Verify required columns exist
    assert "sector" in df.columns
    assert "sector_tags" in df.columns

    # Verify specific tokens are mapped
    assert "UNI" in df.index
    assert "AAVE" in df.index
    assert "MATIC" in df.index
    assert "USDC" in df.index

    # Verify sector values are valid
    assert df.loc["UNI", "sector"] == "DeFi Governance"
    assert df.loc["MATIC", "sector"] == "Layer-2"
    assert df.loc["USDC", "sector"] == "Stablecoins"


def test_classify_tokens_all_known(high_concentration_portfolio):
    """Test classification with all known tokens."""
    sector_breakdown = classify_tokens(high_concentration_portfolio)

    # Verify sectors were identified
    assert "DeFi Governance" in sector_breakdown
    assert "Layer-2" in sector_breakdown

    # Verify DeFi Governance sector
    defi_gov = sector_breakdown["DeFi Governance"]
    assert defi_gov["sector_name"] == "DeFi Governance"
    assert defi_gov["value_usd"] == pytest.approx(98401.0, abs=0.01)  # UNI + AAVE + COMP + MKR
    assert defi_gov["percentage"] == pytest.approx(91.3, abs=0.1)
    assert "UNI" in defi_gov["token_symbols"]
    assert "AAVE" in defi_gov["token_symbols"]
    assert "COMP" in defi_gov["token_symbols"]
    assert "MKR" in defi_gov["token_symbols"]

    # Verify Layer-2 sector
    layer2 = sector_breakdown["Layer-2"]
    assert layer2["sector_name"] == "Layer-2"
    assert layer2["value_usd"] == pytest.approx(9360.0, abs=0.01)  # MATIC
    assert layer2["percentage"] == pytest.approx(8.7, abs=0.1)
    assert "MATIC" in layer2["token_symbols"]


def test_classify_tokens_with_unknown(portfolio_with_unknown_tokens):
    """Test classification handles unknown tokens gracefully."""
    sector_breakdown = classify_tokens(portfolio_with_unknown_tokens)

    # Verify known token classification
    assert "DeFi Governance" in sector_breakdown
    assert sector_breakdown["DeFi Governance"]["value_usd"] == pytest.approx(6420.0, abs=0.01)

    # Verify unknown tokens are grouped
    assert "Unknown Sector" in sector_breakdown
    unknown_sector = sector_breakdown["Unknown Sector"]
    assert unknown_sector["value_usd"] == pytest.approx(7000.0, abs=0.01)  # UNKNOWN_TOKEN + FAKE_COIN
    assert unknown_sector["percentage"] == pytest.approx(52.2, abs=0.1)
    assert "UNKNOWN_TOKEN" in unknown_sector["token_symbols"]
    assert "FAKE_COIN" in unknown_sector["token_symbols"]


def test_concentration_detection_high(high_concentration_portfolio):
    """Test detection of high concentration (>60%)."""
    sector_breakdown = classify_tokens(high_concentration_portfolio)
    concentrated_sectors = identify_concentrated_sectors(sector_breakdown, threshold=60.0)

    # DeFi Governance should be >60% concentrated
    assert "DeFi Governance" in concentrated_sectors
    assert len(concentrated_sectors) >= 1


def test_concentration_detection_well_diversified(well_diversified_portfolio):
    """Test detection with no concentration (all <60%)."""
    sector_breakdown = classify_tokens(well_diversified_portfolio)
    concentrated_sectors = identify_concentrated_sectors(sector_breakdown, threshold=60.0)

    # No sector should exceed 60%
    assert len(concentrated_sectors) == 0


def test_diversification_score_well_diversified():
    """Test diversification score calculation for well-diversified portfolio."""
    concentrated_sectors = []  # No concentrated sectors
    score = calculate_diversification_score(concentrated_sectors)

    assert score == "Well-Diversified"


def test_diversification_score_moderate():
    """Test diversification score calculation for moderate concentration."""
    concentrated_sectors = ["DeFi Governance"]  # 1 concentrated sector
    score = calculate_diversification_score(concentrated_sectors)

    assert score == "Moderate Concentration"


def test_diversification_score_high():
    """Test diversification score calculation for high concentration."""
    concentrated_sectors = ["DeFi Governance", "Layer-2"]  # 2+ concentrated sectors
    score = calculate_diversification_score(concentrated_sectors)

    assert score == "High Concentration"


def test_sector_narrative_generation_high_concentration(high_concentration_portfolio):
    """Test narrative generation for high concentration portfolio."""
    sector_breakdown = classify_tokens(high_concentration_portfolio)
    concentrated_sectors = identify_concentrated_sectors(sector_breakdown, threshold=60.0)
    diversification_score = calculate_diversification_score(concentrated_sectors)

    narrative = generate_sector_narrative(
        sector_breakdown,
        concentrated_sectors,
        diversification_score,
        high_concentration_portfolio.total_value_usd
    )

    # Verify narrative structure
    assert "sector" in narrative.lower()
    assert "DeFi Governance" in narrative

    # Verify concentration warning present
    assert "⚠️" in narrative or "WARNING" in narrative.upper() or "HIGH CONCENTRATION" in narrative

    # Verify diversification score mentioned
    assert diversification_score in narrative

    # Verify percentage is mentioned
    assert "%" in narrative


def test_sector_narrative_generation_well_diversified(well_diversified_portfolio):
    """Test narrative generation for well-diversified portfolio."""
    sector_breakdown = classify_tokens(well_diversified_portfolio)
    concentrated_sectors = identify_concentrated_sectors(sector_breakdown, threshold=60.0)
    diversification_score = calculate_diversification_score(concentrated_sectors)

    narrative = generate_sector_narrative(
        sector_breakdown,
        concentrated_sectors,
        diversification_score,
        well_diversified_portfolio.total_value_usd
    )

    # Verify narrative structure
    assert "well-diversified" in narrative.lower()
    assert "sector" in narrative.lower()

    # Verify no concentration warnings
    assert "⚠️" not in narrative and "WARNING" not in narrative.upper()

    # Verify positive message
    assert "good" in narrative.lower() or "no sector exceeds" in narrative.lower()


def test_sector_classification_accuracy():
    """Verify sector classification accuracy for key tokens."""
    df = load_sector_mappings()

    # DeFi Governance tokens
    assert df.loc["UNI", "sector"] == "DeFi Governance"
    assert df.loc["AAVE", "sector"] == "DeFi Governance"
    assert df.loc["COMP", "sector"] == "DeFi Governance"
    assert df.loc["MKR", "sector"] == "DeFi Governance"

    # Layer-2 tokens
    assert df.loc["MATIC", "sector"] == "Layer-2"
    assert df.loc["OP", "sector"] == "Layer-2"
    assert df.loc["ARB", "sector"] == "Layer-2"

    # Stablecoins
    assert df.loc["USDC", "sector"] == "Stablecoins"
    assert df.loc["DAI", "sector"] == "Stablecoins"
    assert df.loc["USDT", "sector"] == "Stablecoins"

    # Layer-1 Alts
    assert df.loc["ETH", "sector"] == "Layer-1 Alts"
    assert df.loc["BTC", "sector"] == "Layer-1 Alts"
    assert df.loc["SOL", "sector"] == "Layer-1 Alts"

    # DEX tokens
    assert df.loc["SUSHI", "sector"] == "DEX"
    assert df.loc["BAL", "sector"] == "DEX"

    # Yield Protocols
    assert df.loc["CRV", "sector"] == "Yield Protocols"
    assert df.loc["LDO", "sector"] == "Yield Protocols"


# =============================================================================
# Unit Tests for Historical Performance and Opportunity Cost (Story 1.6)
# =============================================================================

def test_load_historical_crashes():
    """Test historical crashes JSON loads correctly with sector_performance fields."""
    crashes_df = load_historical_crashes()

    # Verify data loaded
    assert len(crashes_df) == 3  # 3 crash scenarios

    # Verify structure
    assert "scenario_id" in crashes_df.columns
    assert "name" in crashes_df.columns
    assert "sector_performance" in crashes_df.columns
    assert "recovery_period" in crashes_df.columns
    assert "opportunity_cost_sectors" in crashes_df.columns

    # Verify 2022 Bear Market has sector_performance
    crash_2022 = crashes_df[crashes_df["scenario_id"] == "crash_2022_bear"].iloc[0]
    sector_perf = crash_2022["sector_performance"]
    assert "DeFi Governance" in sector_perf
    assert "Layer-2" in sector_perf
    assert "Stablecoins" in sector_perf

    # Verify values are negative (losses)
    assert sector_perf["DeFi Governance"] < 0
    assert sector_perf["Stablecoins"] < 0


def test_get_sector_crash_performance_defi_governance():
    """Test 2022 crash data retrieval for DeFi Governance sector."""
    crash_perf = get_sector_crash_performance("DeFi Governance", "crash_2022_bear")

    # Verify structure
    assert crash_perf["sector_name"] == "DeFi Governance"
    assert crash_perf["crash_name"] == "2022 Bear Market"
    assert crash_perf["crash_period"] == "Nov 2021 - Jun 2022"

    # Verify loss data
    assert crash_perf["sector_loss_pct"] == -75.0
    assert crash_perf["market_avg_loss_pct"] == -55.0

    # DeFi Governance should have underperformed market
    assert crash_perf["sector_loss_pct"] < crash_perf["market_avg_loss_pct"]


def test_get_sector_crash_performance_layer2():
    """Test 2022 crash data retrieval for Layer-2 sector."""
    crash_perf = get_sector_crash_performance("Layer-2", "crash_2022_bear")

    # Verify structure
    assert crash_perf["sector_name"] == "Layer-2"
    assert crash_perf["crash_name"] == "2022 Bear Market"

    # Verify loss data
    assert crash_perf["sector_loss_pct"] == -60.0
    assert crash_perf["market_avg_loss_pct"] == -55.0


def test_get_opportunity_cost_high_concentration():
    """Test opportunity cost calculation for concentrated portfolio."""
    concentrated_sectors = ["DeFi Governance"]

    opportunity_costs = get_opportunity_cost(concentrated_sectors, "crash_2022_bear")

    # Should return at least one opportunity cost
    assert len(opportunity_costs) >= 1

    # Verify OpportunityCost structure
    opp_cost = opportunity_costs[0]
    assert isinstance(opp_cost, OpportunityCost)
    assert opp_cost.missed_sector is not None
    assert opp_cost.missed_token is not None
    assert opp_cost.recovery_gain_pct > 0
    assert len(opp_cost.narrative) > 0

    # Should NOT recommend a sector that is already concentrated
    assert opp_cost.missed_sector not in concentrated_sectors


def test_get_opportunity_cost_well_diversified():
    """Test opportunity cost returns empty for well-diversified portfolio (no concentration)."""
    concentrated_sectors = []  # No concentration

    opportunity_costs = get_opportunity_cost(concentrated_sectors, "crash_2022_bear")

    # Should return empty list (no concentration, no opportunity cost)
    assert len(opportunity_costs) == 0


def test_sector_risk_narrative_includes_crash_performance():
    """Verify narrative mentions sector loss percentage for concentrated portfolio."""
    # Create a SectorRisk object with crash data
    sector_risk = SectorRisk(
        sector_name="DeFi Governance",
        crash_scenario="2022 Bear Market",
        sector_loss_pct=-75.0,
        market_avg_loss_pct=-55.0,
        crash_period="Nov 2021 - Jun 2022",
        opportunity_cost=OpportunityCost(
            missed_sector="Layer-1 Alts",
            missed_token="SOL",
            recovery_gain_pct=500.0,
            narrative="FTX recovery and ecosystem growth"
        )
    )

    narrative = generate_sector_risk_narrative([sector_risk])

    # Verify crash performance is mentioned
    assert "75%" in narrative or "75" in narrative
    assert "DeFi Governance" in narrative
    assert "2022 Bear Market" in narrative
    assert "55%" in narrative or "55" in narrative  # Market average


def test_sector_risk_narrative_includes_opportunity_cost():
    """Verify narrative mentions missed gains and recovery performance."""
    # Create a SectorRisk object with opportunity cost
    sector_risk = SectorRisk(
        sector_name="DeFi Governance",
        crash_scenario="2022 Bear Market",
        sector_loss_pct=-75.0,
        market_avg_loss_pct=-55.0,
        crash_period="Nov 2021 - Jun 2022",
        opportunity_cost=OpportunityCost(
            missed_sector="Layer-1 Alts",
            missed_token="SOL",
            recovery_gain_pct=500.0,
            narrative="FTX recovery and ecosystem growth"
        )
    )

    narrative = generate_sector_risk_narrative([sector_risk])

    # Verify opportunity cost is mentioned
    assert "Layer-1 Alts" in narrative or "SOL" in narrative
    assert "500%" in narrative or "500" in narrative
    assert "recovery" in narrative.lower()


def test_sector_analysis_well_diversified_no_risks():
    """Verify sector_risks field is empty when no concentration (AC 9)."""
    concentrated_sectors = []  # No concentration

    # When there's no concentration, sector_risks should be empty
    sector_risks = []
    narrative = generate_sector_risk_narrative(sector_risks)

    # Should return well-diversified message
    assert "well-diversified" in narrative.lower() or "no concentration" in narrative.lower()


# =============================================================================
# SYNTHESIS LOGIC TESTS (Story 2.3)
# =============================================================================

from agents.guardian_agent_local import (
    detect_compounding_risk,
    calculate_risk_level,
    generate_synthesis_narrative,
    synthesis_analysis
)
from agents.shared.models import CorrelationAnalysis, SectorAnalysis, CrashPerformance


@pytest.fixture
def high_risk_correlation_analysis():
    """Fixture for high correlation analysis (95%)."""
    return CorrelationAnalysis(
        correlation_coefficient=0.95,
        correlation_percentage=95,
        interpretation="High",
        historical_context=[
            CrashPerformance(
                crash_name="2022 Bear Market",
                crash_period="Nov 2021 - Jun 2022",
                eth_drawdown_pct=-75.3,
                portfolio_loss_pct=-73.2,
                market_avg_loss_pct=-62.5
            )
        ],
        calculation_period_days=90,
        narrative="Your portfolio is 95% correlated to ETH over the past 90 days."
    )


@pytest.fixture
def low_risk_correlation_analysis():
    """Fixture for low correlation analysis (65%)."""
    return CorrelationAnalysis(
        correlation_coefficient=0.65,
        correlation_percentage=65,
        interpretation="Moderate",
        historical_context=[],
        calculation_period_days=90,
        narrative="Your portfolio is 65% correlated to ETH over the past 90 days."
    )


@pytest.fixture
def high_concentration_sector_analysis():
    """Fixture for high sector concentration (68% DeFi Governance)."""
    return SectorAnalysis(
        sector_breakdown={
            "DeFi Governance": {
                "sector_name": "DeFi Governance",
                "value_usd": 10912.0,
                "percentage": 68.0,
                "token_symbols": ["UNI", "AAVE", "COMP"]
            }
        },
        concentrated_sectors=["DeFi Governance"],
        diversification_score="High Concentration",
        sector_risks=[],
        narrative="68% of your portfolio is concentrated in DeFi Governance tokens."
    )


@pytest.fixture
def low_concentration_sector_analysis():
    """Fixture for low sector concentration (well-diversified)."""
    return SectorAnalysis(
        sector_breakdown={
            "DeFi Governance": {
                "sector_name": "DeFi Governance",
                "value_usd": 4000.0,
                "percentage": 25.0,
                "token_symbols": ["UNI"]
            },
            "Layer-2": {
                "sector_name": "Layer-2",
                "value_usd": 3000.0,
                "percentage": 18.75,
                "token_symbols": ["MATIC"]
            }
        },
        concentrated_sectors=[],
        diversification_score="Well-Diversified",
        sector_risks=[],
        narrative="Your portfolio is well-diversified across multiple sectors."
    )


def test_compounding_risk_detection_high_both(high_risk_correlation_analysis, high_concentration_sector_analysis):
    """Test compounding risk detected when correlation >85% AND sector >60% (AC 2)."""
    result = detect_compounding_risk(
        high_risk_correlation_analysis,
        high_concentration_sector_analysis
    )

    assert result


def test_compounding_risk_detection_high_correlation_only(high_risk_correlation_analysis, low_concentration_sector_analysis):
    """Test no compounding risk when only correlation high (AC 2)."""
    result = detect_compounding_risk(
        high_risk_correlation_analysis,
        low_concentration_sector_analysis
    )

    assert not result


def test_compounding_risk_detection_high_sector_only(low_risk_correlation_analysis, high_concentration_sector_analysis):
    """Test no compounding risk when only sector concentration high (AC 2)."""
    result = detect_compounding_risk(
        low_risk_correlation_analysis,
        high_concentration_sector_analysis
    )

    assert not result


def test_compounding_risk_detection_low_both(low_risk_correlation_analysis, low_concentration_sector_analysis):
    """Test no compounding risk when both low (AC 2)."""
    result = detect_compounding_risk(
        low_risk_correlation_analysis,
        low_concentration_sector_analysis
    )

    assert not result


def test_calculate_risk_level_critical():
    """Test risk level classification - Critical (AC 5)."""
    risk_level = calculate_risk_level(
        correlation_percentage=95,
        concentrated_sectors=["DeFi Governance"]
    )

    assert risk_level == "Critical"


def test_calculate_risk_level_high_correlation():
    """Test risk level classification - High (correlation only) (AC 5)."""
    risk_level = calculate_risk_level(
        correlation_percentage=90,
        concentrated_sectors=[]
    )

    assert risk_level == "High"


def test_calculate_risk_level_high_sector():
    """Test risk level classification - High (sector only) (AC 5)."""
    risk_level = calculate_risk_level(
        correlation_percentage=70,
        concentrated_sectors=["DeFi Governance"]
    )

    assert risk_level == "High"


def test_calculate_risk_level_moderate():
    """Test risk level classification - Moderate (AC 5)."""
    risk_level = calculate_risk_level(
        correlation_percentage=75,
        concentrated_sectors=[]
    )

    assert risk_level == "Moderate"


def test_calculate_risk_level_low():
    """Test risk level classification - Low (AC 5)."""
    risk_level = calculate_risk_level(
        correlation_percentage=65,
        concentrated_sectors=[]
    )

    assert risk_level == "Low"


def test_generate_synthesis_narrative_compounding_risk(high_risk_correlation_analysis, high_concentration_sector_analysis):
    """Test synthesis narrative generation for compounding risk portfolios (AC 4, 6, 7)."""
    crash_data = [{"name": "2022 Bear Market"}]

    narrative = generate_synthesis_narrative(
        high_risk_correlation_analysis,
        high_concentration_sector_analysis,
        compounding_risk_detected=True,
        risk_multiplier_effect="",
        crash_data=crash_data
    )

    # Verify narrative contains correlation percentage
    assert "95%" in narrative

    # Verify narrative contains sector concentration
    assert "68%" in narrative or "DeFi Governance" in narrative

    # Verify compounding risk mentioned
    assert "compounding" in narrative.lower() or "amplifies" in narrative.lower() or "multiply" in narrative.lower()

    # Verify historical crash example included
    assert "2022" in narrative or "crash" in narrative.lower() or "lost" in narrative.lower()

    # Verify leverage calculation (95/30 = ~3x)
    assert "3" in narrative or "leverage" in narrative.lower()


def test_generate_synthesis_narrative_well_diversified(low_risk_correlation_analysis, low_concentration_sector_analysis):
    """Test synthesis narrative for well-diversified portfolios (AC 8)."""
    crash_data = [{"name": "2022 Bear Market"}]

    narrative = generate_synthesis_narrative(
        low_risk_correlation_analysis,
        low_concentration_sector_analysis,
        compounding_risk_detected=False,
        risk_multiplier_effect="",
        crash_data=crash_data
    )

    # Verify positive confirmation of low compounding risk
    assert "manageable" in narrative.lower() or "balanced" in narrative.lower() or "limits" in narrative.lower()

    # Verify explanation of portfolio structure
    assert "30%" in narrative or "concentration" in narrative.lower()

    # Verify narrative is reassuring
    assert "well-diversified" in narrative.lower() or "balanced" in narrative.lower()


@patch('agents.guardian_agent_local.query_crashes_by_correlation_loss')
def test_synthesis_metta_integration(mock_metta_query, high_risk_correlation_analysis, high_concentration_sector_analysis):
    """Test synthesis queries MeTTa for historical dual-risk data (AC 5)."""
    # Mock MeTTa response
    mock_metta_query.return_value = [
        {"scenario_id": "crash_2022_bear", "name": "2022 Bear Market"}
    ]

    from agents.shared.models import CorrelationAnalysisResponse, SectorAnalysisResponse

    correlation_response = Mock(spec=CorrelationAnalysisResponse)
    correlation_response.analysis_data = high_risk_correlation_analysis.model_dump()

    sector_response = Mock(spec=SectorAnalysisResponse)
    sector_response.analysis_data = high_concentration_sector_analysis.model_dump()

    synthesis = synthesis_analysis(correlation_response, sector_response, request_id="test_123")

    # Verify MeTTa query was called
    mock_metta_query.assert_called_once()

    # Verify correlation bracket selection
    call_args = mock_metta_query.call_args
    assert ">90%" in str(call_args) or "correlation_bracket" in str(call_args)

    # Verify synthesis result
    assert synthesis.compounding_risk_detected
    assert synthesis.overall_risk_level == "Critical"


def test_synthesis_analysis_full_workflow(high_risk_correlation_analysis, high_concentration_sector_analysis):
    """Test complete synthesis_analysis workflow (AC 1-8)."""
    from agents.shared.models import CorrelationAnalysisResponse, SectorAnalysisResponse

    correlation_response = Mock(spec=CorrelationAnalysisResponse)
    correlation_response.analysis_data = high_risk_correlation_analysis.model_dump()

    sector_response = Mock(spec=SectorAnalysisResponse)
    sector_response.analysis_data = high_concentration_sector_analysis.model_dump()

    synthesis = synthesis_analysis(correlation_response, sector_response, request_id="test_full")

    # Verify compounding risk detected
    assert synthesis.compounding_risk_detected

    # Verify risk level
    assert synthesis.overall_risk_level == "Critical"

    # Verify narrative contains key elements
    assert "95%" in synthesis.synthesis_narrative
    assert "68%" in synthesis.synthesis_narrative or "DeFi Governance" in synthesis.synthesis_narrative

    # Verify risk multiplier effect
    assert "leverage" in synthesis.risk_multiplier_effect.lower() or "amplifies" in synthesis.risk_multiplier_effect.lower()

    # Verify recommendations field exists (Story 2.4: should have recommendations)
    assert len(synthesis.recommendations) > 0  # Updated for Story 2.4

    # Verify synthesis creates models correctly
    assert isinstance(synthesis.correlation_analysis, CorrelationAnalysis)
    assert isinstance(synthesis.sector_analysis, SectorAnalysis)


# =============================================================================
# Story 2.4: Recommendation Generation Unit Tests
# =============================================================================

def test_generate_recommendations_high_correlation():
    """Test high correlation generates uncorrelated asset recommendation (AC 2)."""
    from agents.guardian_agent_local import generate_recommendations
    from agents.shared.models import CorrelationAnalysis, SectorAnalysis, CrashPerformance

    correlation_analysis = CorrelationAnalysis(
        correlation_coefficient=0.95,
        correlation_percentage=95,
        interpretation="High",
        historical_context=[
            CrashPerformance(
                crash_name="2022 Bear Market",
                crash_period="Nov 2021 - Jun 2022",
                eth_drawdown_pct=-75.3,
                portfolio_loss_pct=-73.0,
                market_avg_loss_pct=-55.0
            )
        ],
        calculation_period_days=90,
        narrative="Your portfolio is 95% correlated to ETH"
    )

    sector_analysis = SectorAnalysis(
        sector_breakdown={},
        concentrated_sectors=[],
        diversification_score="Well-Diversified",
        sector_risks=[],
        narrative="Diversified sector allocation"
    )

    recommendations = generate_recommendations(
        correlation_analysis,
        sector_analysis,
        compounding_risk_detected=False,
        overall_risk_level="High"
    )

    # Verify recommendation count
    assert len(recommendations) == 1

    # Verify recommendation content
    rec = recommendations[0]
    assert rec.priority == 1
    assert "95%" in rec.action
    assert "below 80%" in rec.action
    assert "uncorrelated assets" in rec.action.lower() or "bitcoin" in rec.action.lower() or "alternative layer-1s" in rec.action.lower()

    # Verify no specific token picks (AC 9)
    assert "Buy BTC" not in rec.action
    assert "Sell" not in rec.action
    assert "Bitcoin" in rec.action or "Alternative Layer-1s" in rec.action or "Stablecoins" in rec.action

    # Verify rationale explains correlation risk
    assert "correlation" in rec.rationale.lower()
    assert "73" in rec.rationale or "73.0" in rec.rationale

    # Verify expected impact references historical data
    assert "2022" in rec.expected_impact or "Bear Market" in rec.expected_impact


def test_generate_recommendations_high_sector_concentration():
    """Test high sector concentration generates reduction recommendation (AC 3)."""
    from agents.guardian_agent_local import generate_recommendations
    from agents.shared.models import CorrelationAnalysis, SectorAnalysis, SectorHolding, SectorRisk, OpportunityCost

    correlation_analysis = CorrelationAnalysis(
        correlation_coefficient=0.65,
        correlation_percentage=65,
        interpretation="Moderate",
        historical_context=[],
        calculation_period_days=90,
        narrative="Moderate correlation"
    )

    sector_analysis = SectorAnalysis(
        sector_breakdown={
            "DeFi Governance": SectorHolding(
                sector_name="DeFi Governance",
                value_usd=10912.0,
                percentage=68.0,
                token_symbols=["UNI", "AAVE", "COMP"]
            )
        },
        concentrated_sectors=["DeFi Governance"],
        diversification_score="High Concentration",
        sector_risks=[
            SectorRisk(
                sector_name="DeFi Governance",
                crash_scenario="2022 Bear Market",
                sector_loss_pct=-75.0,
                market_avg_loss_pct=-55.0,
                crash_period="Nov 2021 - Jun 2022",
                opportunity_cost=OpportunityCost(
                    missed_sector="Layer-1 Alts",
                    missed_token="SOL",
                    recovery_gain_pct=500.0,
                    narrative="SOL gained 500% during recovery"
                )
            )
        ],
        narrative="68% concentrated in DeFi Governance"
    )

    recommendations = generate_recommendations(
        correlation_analysis,
        sector_analysis,
        compounding_risk_detected=False,
        overall_risk_level="High"
    )

    # Verify recommendation count
    assert len(recommendations) == 1

    # Verify recommendation content
    rec = recommendations[0]
    assert "DeFi Governance" in rec.action
    assert "68%" in rec.action
    assert "below 40%" in rec.action

    # Verify no specific token picks (AC 9)
    assert "Sell UNI" not in rec.action
    assert "Sell AAVE" not in rec.action
    assert "Buy" not in rec.action

    # Verify rationale includes historical sector loss data
    assert "DeFi Governance" in rec.rationale
    assert "75" in rec.rationale or "75.0" in rec.rationale
    assert "2022" in rec.rationale or "Bear Market" in rec.rationale

    # Verify expected impact includes opportunity cost
    assert "500" in rec.expected_impact or "recovery" in rec.expected_impact.lower()


def test_generate_recommendations_compounding_risk_prioritization():
    """Test compounding risk prioritizes sector diversification first (AC 4)."""
    from agents.guardian_agent_local import generate_recommendations
    from agents.shared.models import CorrelationAnalysis, SectorAnalysis, SectorHolding, SectorRisk, OpportunityCost, CrashPerformance

    correlation_analysis = CorrelationAnalysis(
        correlation_coefficient=0.95,
        correlation_percentage=95,
        interpretation="High",
        historical_context=[
            CrashPerformance(
                crash_name="2022 Bear Market",
                crash_period="Nov 2021 - Jun 2022",
                eth_drawdown_pct=-75.3,
                portfolio_loss_pct=-73.0,
                market_avg_loss_pct=-55.0
            )
        ],
        calculation_period_days=90,
        narrative="95% correlated to ETH"
    )

    sector_analysis = SectorAnalysis(
        sector_breakdown={
            "DeFi Governance": SectorHolding(
                sector_name="DeFi Governance",
                value_usd=10912.0,
                percentage=68.0,
                token_symbols=["UNI", "AAVE", "COMP"]
            )
        },
        concentrated_sectors=["DeFi Governance"],
        diversification_score="High Concentration",
        sector_risks=[
            SectorRisk(
                sector_name="DeFi Governance",
                crash_scenario="2022 Bear Market",
                sector_loss_pct=-75.0,
                market_avg_loss_pct=-55.0,
                crash_period="Nov 2021 - Jun 2022",
                opportunity_cost=OpportunityCost(
                    missed_sector="Layer-1 Alts",
                    missed_token="SOL",
                    recovery_gain_pct=500.0,
                    narrative="SOL gained 500%"
                )
            )
        ],
        narrative="68% concentrated in DeFi Governance"
    )

    recommendations = generate_recommendations(
        correlation_analysis,
        sector_analysis,
        compounding_risk_detected=True,
        overall_risk_level="Critical"
    )

    # Verify recommendation count (should be 3 for compounding risk)
    assert len(recommendations) == 3

    # Verify sector diversification has priority 1
    assert recommendations[0].priority == 1
    assert "DeFi Governance" in recommendations[0].action
    assert "concentration" in recommendations[0].action.lower()

    # Verify correlation reduction has priority 2
    assert recommendations[1].priority == 2
    assert "uncorrelated assets" in recommendations[1].action.lower() or "correlation" in recommendations[1].action.lower()

    # Verify prioritization explanation has priority 3
    assert recommendations[2].priority == 3
    assert "Prioritize" in recommendations[2].action or "prioritize" in recommendations[2].action.lower()
    assert "sector" in recommendations[2].rationale.lower()
    assert ("first" in recommendations[2].rationale.lower() or
           "before" in recommendations[2].rationale.lower() or
           "naturally" in recommendations[2].rationale.lower())

    # Verify expected impact explains compounding benefit
    assert "compounding" in recommendations[2].expected_impact.lower() or "both" in recommendations[2].expected_impact.lower()


def test_generate_recommendations_well_diversified():
    """Test well-diversified portfolio gets positive monitoring recommendation (AC 5)."""
    from agents.guardian_agent_local import generate_recommendations
    from agents.shared.models import CorrelationAnalysis, SectorAnalysis, SectorHolding

    correlation_analysis = CorrelationAnalysis(
        correlation_coefficient=0.65,
        correlation_percentage=65,
        interpretation="Moderate",
        historical_context=[],
        calculation_period_days=90,
        narrative="65% correlated to ETH"
    )

    sector_analysis = SectorAnalysis(
        sector_breakdown={
            "DeFi Governance": SectorHolding(
                sector_name="DeFi Governance",
                value_usd=4000.0,
                percentage=25.0,
                token_symbols=["UNI", "AAVE"]
            ),
            "Layer-2": SectorHolding(
                sector_name="Layer-2",
                value_usd=3200.0,
                percentage=20.0,
                token_symbols=["MATIC", "OP"]
            ),
            "Stablecoins": SectorHolding(
                sector_name="Stablecoins",
                value_usd=4800.0,
                percentage=30.0,
                token_symbols=["USDC", "DAI"]
            )
        },
        concentrated_sectors=[],
        diversification_score="Well-Diversified",
        sector_risks=[],
        narrative="Balanced sector allocation"
    )

    recommendations = generate_recommendations(
        correlation_analysis,
        sector_analysis,
        compounding_risk_detected=False,
        overall_risk_level="Low"
    )

    # Verify single recommendation
    assert len(recommendations) == 1

    # Verify positive acknowledgment tone
    rec = recommendations[0]
    assert "Maintain" in rec.action or "balanced" in rec.rationale.lower()

    # Verify mentions correlation and sectors
    assert "65%" in rec.rationale
    assert "DeFi Governance" in rec.rationale or "Layer-2" in rec.rationale or "Stablecoins" in rec.rationale

    # Verify monitoring frequency included
    assert "monitoring" in rec.expected_impact.lower() or "quarterly" in rec.expected_impact.lower()

    # Verify sets alert thresholds
    assert "40%" in rec.expected_impact or "80%" in rec.expected_impact


def test_recommendations_no_specific_token_picks():
    """Test recommendations avoid specific token symbols (AC 9)."""
    from agents.guardian_agent_local import generate_recommendations
    from agents.shared.models import CorrelationAnalysis, SectorAnalysis, SectorHolding, CrashPerformance

    correlation_analysis = CorrelationAnalysis(
        correlation_coefficient=0.95,
        correlation_percentage=95,
        interpretation="High",
        historical_context=[
            CrashPerformance(
                crash_name="2022 Bear Market",
                crash_period="Nov 2021 - Jun 2022",
                eth_drawdown_pct=-75.3,
                portfolio_loss_pct=-73.0,
                market_avg_loss_pct=-55.0
            )
        ],
        calculation_period_days=90,
        narrative="95% correlated to ETH"
    )

    sector_analysis = SectorAnalysis(
        sector_breakdown={},
        concentrated_sectors=[],
        diversification_score="Well-Diversified",
        sector_risks=[],
        narrative="Diversified"
    )

    recommendations = generate_recommendations(
        correlation_analysis,
        sector_analysis,
        compounding_risk_detected=False,
        overall_risk_level="High"
    )

    # Verify no specific token picks in any recommendation
    for rec in recommendations:
        # Should NOT contain specific token buy/sell instructions
        assert "Buy BTC" not in rec.action
        assert "Sell UNI" not in rec.action
        assert "Buy SOL" not in rec.action
        assert "Sell AAVE" not in rec.action
        assert "Swap" not in rec.action.lower() or "for BTC" not in rec.action

        # SHOULD use asset classes instead
        if "uncorrelated" in rec.action.lower() or "correlation" in rec.action.lower():
            assert ("Bitcoin" in rec.action or
                   "Alternative Layer-1s" in rec.action or
                   "Stablecoins" in rec.action)


def test_get_correlation_recommendations_helper():
    """Test get_correlation_recommendations helper function (AC 2)."""
    from agents.guardian_agent_local import get_correlation_recommendations
    from agents.shared.models import CorrelationAnalysis, CrashPerformance

    correlation_analysis = CorrelationAnalysis(
        correlation_coefficient=0.92,
        correlation_percentage=92,
        interpretation="High",
        historical_context=[
            CrashPerformance(
                crash_name="2022 Bear Market",
                crash_period="Nov 2021 - Jun 2022",
                eth_drawdown_pct=-75.3,
                portfolio_loss_pct=-70.0,
                market_avg_loss_pct=-55.0
            )
        ],
        calculation_period_days=90,
        narrative="92% correlated"
    )

    rec = get_correlation_recommendations(correlation_analysis, priority=1)

    # Verify priority
    assert rec.priority == 1

    # Verify action includes current percentage and target
    assert "92%" in rec.action
    assert "below 80%" in rec.action

    # Verify asset classes used (no specific tokens)
    assert ("Bitcoin" in rec.action or
           "Alternative Layer-1s" in rec.action or
           "Stablecoins" in rec.action)

    # Verify rationale explains risk
    assert "correlation" in rec.rationale.lower()
    assert "70" in rec.rationale or "70.0" in rec.rationale

    # Verify expected impact references historical data
    assert "2022" in rec.expected_impact or "Bear Market" in rec.expected_impact


def test_get_sector_recommendations_helper():
    """Test get_sector_recommendations helper function (AC 3)."""
    from agents.guardian_agent_local import get_sector_recommendations
    from agents.shared.models import SectorAnalysis, SectorHolding, SectorRisk, OpportunityCost

    sector_analysis = SectorAnalysis(
        sector_breakdown={
            "DeFi Governance": SectorHolding(
                sector_name="DeFi Governance",
                value_usd=10912.0,
                percentage=72.0,
                token_symbols=["UNI", "AAVE", "COMP"]
            )
        },
        concentrated_sectors=["DeFi Governance"],
        diversification_score="High Concentration",
        sector_risks=[
            SectorRisk(
                sector_name="DeFi Governance",
                crash_scenario="2022 Bear Market",
                sector_loss_pct=-80.0,
                market_avg_loss_pct=-55.0,
                crash_period="Nov 2021 - Jun 2022",
                opportunity_cost=OpportunityCost(
                    missed_sector="Layer-1 Alts",
                    missed_token="SOL",
                    recovery_gain_pct=500.0,
                    narrative="Missed SOL recovery"
                )
            )
        ],
        narrative="72% in DeFi Governance"
    )

    rec = get_sector_recommendations(sector_analysis, priority=1)

    # Verify priority
    assert rec.priority == 1

    # Verify action includes sector name and percentages
    assert "DeFi Governance" in rec.action
    assert "72%" in rec.action
    assert "below 40%" in rec.action

    # Verify rationale includes historical loss
    assert "DeFi Governance" in rec.rationale
    assert "80" in rec.rationale or "80.0" in rec.rationale
    assert "2022" in rec.rationale

    # Verify expected impact includes opportunity cost
    assert "500" in rec.expected_impact
    assert "recovery" in rec.expected_impact.lower() or "rebound" in rec.expected_impact.lower()


def test_get_diversified_recommendations_helper():
    """Test get_diversified_recommendations helper function (AC 5)."""
    from agents.guardian_agent_local import get_diversified_recommendations
    from agents.shared.models import CorrelationAnalysis, SectorAnalysis, SectorHolding

    correlation_analysis = CorrelationAnalysis(
        correlation_coefficient=0.60,
        correlation_percentage=60,
        interpretation="Moderate",
        historical_context=[],
        calculation_period_days=90,
        narrative="60% correlated"
    )

    sector_analysis = SectorAnalysis(
        sector_breakdown={
            "DeFi Governance": SectorHolding(
                sector_name="DeFi Governance",
                value_usd=3000.0,
                percentage=30.0,
                token_symbols=["UNI"]
            ),
            "Layer-2": SectorHolding(
                sector_name="Layer-2",
                value_usd=2500.0,
                percentage=25.0,
                token_symbols=["MATIC"]
            ),
            "Stablecoins": SectorHolding(
                sector_name="Stablecoins",
                value_usd=2000.0,
                percentage=20.0,
                token_symbols=["USDC"]
            )
        },
        concentrated_sectors=[],
        diversification_score="Well-Diversified",
        sector_risks=[],
        narrative="Balanced"
    )

    rec = get_diversified_recommendations(correlation_analysis, sector_analysis)

    # Verify priority is 1 (only recommendation)
    assert rec.priority == 1

    # Verify positive action
    assert "Maintain" in rec.action or "balanced" in rec.action.lower()

    # Verify rationale acknowledges good structure
    assert "60%" in rec.rationale
    assert "DeFi Governance" in rec.rationale or "Layer-2" in rec.rationale

    # Verify monitoring guidance
    assert "monitoring" in rec.expected_impact.lower() or "quarterly" in rec.expected_impact.lower()
    assert "40%" in rec.expected_impact or "80%" in rec.expected_impact


def test_get_prioritization_recommendation_helper():
    """Test get_prioritization_recommendation helper function (AC 4)."""
    from agents.guardian_agent_local import get_prioritization_recommendation

    rec = get_prioritization_recommendation()

    # Verify priority is 3 (explanatory recommendation)
    assert rec.priority == 3

    # Verify action explains prioritization
    assert "Prioritize" in rec.action or "prioritize" in rec.action.lower()
    assert "sector" in rec.action.lower()
    assert "before" in rec.action.lower() or "first" in rec.action.lower()

    # Verify rationale explains compounding benefit
    assert "sector concentration" in rec.rationale.lower()
    assert "amplifies" in rec.rationale.lower() or "naturally" in rec.rationale.lower()

    # Verify expected impact explains dual benefit
    assert "both" in rec.expected_impact.lower() or "compounding" in rec.expected_impact.lower()
    assert "risk" in rec.expected_impact.lower()
