"""
CorrelationAgent - Standalone Deployment Version for Agentverse

This is a self-contained version that includes all dependencies and fetches
historical price data from GitHub. Ready for single-file Agentverse deployment.

Deployment Instructions:
1. Upload this file to Agentverse
2. Set environment variables in Agentverse dashboard:
   - CORRELATION_AGENT_SEED (required - your secret seed phrase)
   - HIGH_CORRELATION_THRESHOLD=85
   - MODERATE_CORRELATION_THRESHOLD=70
   - MIN_REQUIRED_DATA_DAYS=60
   - MAX_EXCLUDED_VALUE_RATIO=50
   - LOG_LEVEL=INFO
3. Deploy and copy your agent address
"""

import logging
import os
import time
from datetime import datetime, timezone
from io import StringIO
from typing import Dict, List

import numpy as np
import pandas as pd
import requests
from pydantic import BaseModel, ConfigDict, Field, model_validator
from uagents import Agent, Context, Model

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION (from environment variables)
# =============================================================================

def get_env_var(key: str, default: str = "") -> str:
    """Get environment variable with optional default value."""
    value = os.getenv(key, default)
    if not value and key == "CORRELATION_AGENT_SEED":
        logger.warning(f"⚠️ {key} not set, using default seed (NOT SECURE for production)")
        return "correlation_agent_insecure_default_seed_change_me"
    return value


# Agent configuration
CORRELATION_AGENT_SEED = get_env_var("CORRELATION_AGENT_SEED")

# Correlation calculation configuration (percentages converted to decimals)
HIGH_CORRELATION_THRESHOLD = float(get_env_var("HIGH_CORRELATION_THRESHOLD", "85")) / 100
MODERATE_CORRELATION_THRESHOLD = float(get_env_var("MODERATE_CORRELATION_THRESHOLD", "70")) / 100
MIN_REQUIRED_DATA_DAYS = int(get_env_var("MIN_REQUIRED_DATA_DAYS", "60"))
MAX_EXCLUDED_VALUE_RATIO = float(get_env_var("MAX_EXCLUDED_VALUE_RATIO", "50")) / 100

# GitHub raw data URLs (fetches historical prices from repository)
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/Zolldyk/Guardian/main/data/historical_prices"

logger.info(f"✅ Configuration loaded: HIGH_THRESHOLD={HIGH_CORRELATION_THRESHOLD}, MIN_DAYS={MIN_REQUIRED_DATA_DAYS}")

# =============================================================================
# PYDANTIC DATA MODELS (inlined from agents/shared/models.py)
# =============================================================================

class TokenHolding(BaseModel):
    """Represents a single token holding within a portfolio."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symbol": "UNI",
                "amount": 1250.0,
                "price_usd": 6.42,
                "value_usd": 8025.0,
            }
        }
    )

    symbol: str = Field(..., description="Token symbol (e.g., 'ETH', 'UNI', 'AAVE')")
    amount: float = Field(..., gt=0, description="Amount of tokens held")
    price_usd: float = Field(..., gt=0, description="Current price per token in USD")
    value_usd: float = Field(..., gt=0, description="Total value (amount * price_usd)")


class Portfolio(BaseModel):
    """Complete portfolio data structure passed between agents."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
                "tokens": [
                    {"symbol": "UNI", "amount": 1250.0, "price_usd": 6.42, "value_usd": 8025.0}
                ],
                "total_value_usd": 16040.5,
                "analysis_timestamp": "2025-10-18T14:32:00Z",
            }
        }
    )

    wallet_address: str = Field(
        ...,
        pattern=r"^0x[a-fA-F0-9]{40}$",
        description="Ethereum wallet address",
    )
    tokens: List[TokenHolding] = Field(..., min_length=1, description="List of token holdings")
    total_value_usd: float = Field(..., gt=0, description="Total portfolio value in USD")
    analysis_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Snapshot timestamp"
    )

    @model_validator(mode="after")
    def validate_total_value(self) -> "Portfolio":
        """Verify total_value_usd matches sum of token values."""
        calculated_total = sum(token.value_usd for token in self.tokens)
        if abs(self.total_value_usd - calculated_total) > 0.01:
            raise ValueError(
                f"total_value_usd ({self.total_value_usd}) does not match sum of token values ({calculated_total})"
            )
        return self


class CrashPerformance(BaseModel):
    """Historical crash performance for a given correlation bracket."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "crash_name": "2022 Bear Market",
                "crash_period": "Nov 2021 - Jun 2022",
                "eth_drawdown_pct": -75.3,
                "portfolio_loss_pct": -68.2,
                "market_avg_loss_pct": -62.5,
            }
        }
    )

    crash_name: str = Field(..., description="Crash scenario name")
    crash_period: str = Field(..., description="Date range of crash")
    eth_drawdown_pct: float = Field(..., description="ETH drawdown percentage during crash")
    portfolio_loss_pct: float = Field(..., description="Avg portfolio loss for this correlation bracket")
    market_avg_loss_pct: float = Field(..., description="Market average loss for comparison")


class CorrelationAnalysis(BaseModel):
    """Correlation analysis results from CorrelationAgent."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "correlation_coefficient": 0.95,
                "correlation_percentage": 95,
                "interpretation": "High",
                "historical_context": [],
                "calculation_period_days": 90,
                "narrative": "Your portfolio is 95% correlated to ETH over the past 90 days.",
            }
        }
    )

    correlation_coefficient: float = Field(..., ge=-1.0, le=1.0, description="Pearson correlation (-1 to +1)")
    correlation_percentage: int = Field(..., ge=0, le=100, description="Correlation as percentage (absolute value)")
    interpretation: str = Field(..., description="High (>85%), Moderate (70-85%), Low (<70%)")
    historical_context: List[CrashPerformance] = Field(default_factory=list, description="Historical crash data")
    calculation_period_days: int = Field(default=90, description="Historical window in days")
    narrative: str = Field(..., description="Plain English explanation of correlation risk")


# =============================================================================
# uAGENTS MESSAGE MODELS
# =============================================================================

class AnalysisRequest(Model):
    """Request message sent from Guardian to CorrelationAgent."""
    request_id: str
    wallet_address: str
    portfolio_data: dict  # Portfolio serialized as dict
    requested_by: str


class CorrelationAnalysisResponse(Model):
    """Response message from CorrelationAgent with analysis results."""
    request_id: str
    wallet_address: str
    analysis_data: dict  # CorrelationAnalysis serialized as dict
    agent_address: str
    processing_time_ms: int


class ErrorMessage(Model):
    """Universal error message for communicating failures."""
    request_id: str
    error_type: str  # "timeout" | "invalid_data" | "insufficient_data" | "agent_unavailable"
    error_message: str
    agent_address: str
    retry_recommended: bool


# =============================================================================
# CORRELATION CALCULATION FUNCTIONS
# =============================================================================

def load_price_data_from_github(symbol: str, days: int) -> pd.DataFrame:
    """
    Load historical price data from GitHub repository.

    Args:
        symbol: Token symbol (e.g., 'ETH', 'UNI')
        days: Number of days of historical data to load

    Returns:
        DataFrame with columns: date, price_usd, volume_usd

    Raises:
        FileNotFoundError: If CSV file for symbol doesn't exist
        ValueError: If insufficient data available
    """
    url = f"{GITHUB_RAW_BASE_URL}/{symbol}.csv"

    try:
        logger.debug(f"Fetching price data for {symbol} from GitHub...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse CSV from response text
        df = pd.read_csv(StringIO(response.text))
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        # Get last N days
        df = df.tail(days + 1).reset_index(drop=True)  # +1 for calculating returns

        if len(df) < days:
            raise ValueError(f"Insufficient data for {symbol}: found {len(df)} days, need {days}")

        logger.debug(f"✅ Loaded {len(df)} days of price data for {symbol}")
        return df

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise FileNotFoundError(f"Price data not found for {symbol} at {url}")
        raise
    except Exception as e:
        logger.error(f"❌ Failed to load price data for {symbol}: {e}")
        raise


def calculate_daily_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate daily returns from price series.

    Args:
        prices: Series of daily prices

    Returns:
        Series of daily returns (price_today - price_yesterday) / price_yesterday
    """
    returns = prices.pct_change().dropna()
    return returns


def load_eth_returns(days: int) -> pd.Series:
    """
    Load ETH price data and calculate daily returns over specified window.

    Args:
        days: Number of days for historical window

    Returns:
        Series of daily ETH returns
    """
    df = load_price_data_from_github("ETH", days)
    returns = calculate_daily_returns(df["price_usd"])
    return returns


def calculate_portfolio_returns(portfolio: Portfolio, days: int) -> pd.Series:
    """
    Calculate portfolio weighted average returns over specified window.

    Args:
        portfolio: Portfolio containing tokens and their allocations
        days: Number of days for historical window

    Returns:
        Series of daily weighted portfolio returns

    Raises:
        ValueError: If insufficient data or no valid tokens
    """
    # Calculate weight for each token
    total_value = portfolio.total_value_usd
    token_weights: Dict[str, float] = {}
    token_returns: Dict[str, pd.Series] = {}

    excluded_tokens = []
    excluded_value = 0.0

    for token in portfolio.tokens:
        symbol = token.symbol
        weight = token.value_usd / total_value
        token_weights[symbol] = weight

        try:
            # Load price data and calculate returns
            df = load_price_data_from_github(symbol, days)
            returns = calculate_daily_returns(df["price_usd"])

            # Check if we have enough data (minimum required days from config)
            if len(returns) < MIN_REQUIRED_DATA_DAYS:
                logger.warning(f"Token {symbol} has insufficient data ({len(returns)} days), excluding from calculation")
                excluded_tokens.append(symbol)
                excluded_value += token.value_usd
                continue

            token_returns[symbol] = returns

        except FileNotFoundError:
            logger.warning(f"Token {symbol} not found in historical data, excluding from calculation")
            excluded_tokens.append(symbol)
            excluded_value += token.value_usd
            continue
        except Exception as e:
            logger.warning(f"Error loading {symbol}: {e}, excluding from calculation")
            excluded_tokens.append(symbol)
            excluded_value += token.value_usd
            continue

    # Check if we excluded too much of the portfolio (from config)
    if excluded_value / total_value > MAX_EXCLUDED_VALUE_RATIO:
        raise ValueError(
            f"Insufficient data: {len(excluded_tokens)} tokens ({excluded_value / total_value:.1%} of portfolio) excluded"
        )

    if len(token_returns) == 0:
        raise ValueError("No valid tokens with sufficient historical data")

    # Recalculate weights for remaining tokens
    remaining_value = total_value - excluded_value
    adjusted_weights = {
        symbol: (token_weights[symbol] * total_value) / remaining_value
        for symbol in token_returns.keys()
    }

    # Align all return series to have the same dates
    # Use the intersection of all dates
    all_dates = None
    for returns in token_returns.values():
        if all_dates is None:
            all_dates = set(returns.index)
        else:
            all_dates = all_dates.intersection(set(returns.index))

    if not all_dates or len(all_dates) < MIN_REQUIRED_DATA_DAYS:
        raise ValueError(f"Insufficient overlapping data: only {len(all_dates) if all_dates else 0} common dates")

    # Calculate weighted portfolio returns
    portfolio_returns = pd.Series(0.0, index=sorted(all_dates))

    for symbol, returns in token_returns.items():
        weight = adjusted_weights[symbol]
        # Filter returns to common dates
        aligned_returns = returns[returns.index.isin(all_dates)]
        portfolio_returns += weight * aligned_returns

    return portfolio_returns.sort_index()


def calculate_pearson_correlation(portfolio_returns: pd.Series, eth_returns: pd.Series) -> float:
    """
    Compute Pearson correlation coefficient between portfolio and ETH returns.

    Args:
        portfolio_returns: Series of daily portfolio returns
        eth_returns: Series of daily ETH returns

    Returns:
        Correlation coefficient (-1.0 to +1.0)
    """
    # Align the two series to have the same dates
    aligned_portfolio = portfolio_returns[portfolio_returns.index.isin(eth_returns.index)].sort_index()
    aligned_eth = eth_returns[eth_returns.index.isin(portfolio_returns.index)].sort_index()

    # Ensure same length and order
    common_dates = sorted(set(aligned_portfolio.index).intersection(set(aligned_eth.index)))
    aligned_portfolio = aligned_portfolio[common_dates]
    aligned_eth = aligned_eth[common_dates]

    # Calculate correlation using NumPy
    correlation_matrix = np.corrcoef(aligned_portfolio, aligned_eth)
    correlation_coef = correlation_matrix[0, 1]

    # Handle NaN (can happen if returns are constant)
    if np.isnan(correlation_coef):
        logger.warning("Correlation calculation resulted in NaN, returning 0.0")
        return 0.0

    # Return correlation coefficient directly (can be negative for inverse correlation)
    # Note: Crypto assets are typically positively correlated, but negative correlation
    # represents inverse movement (hedging) and should be preserved
    return correlation_coef


# =============================================================================
# AGENT INITIALIZATION
# =============================================================================

correlation_agent = Agent(
    name="correlation_agent",
    seed=CORRELATION_AGENT_SEED,
    port=8001,
)

logger.info(f"✅ CorrelationAgent initialized with address: {correlation_agent.address}")


# =============================================================================
# MESSAGE HANDLER
# =============================================================================

@correlation_agent.on_message(model=AnalysisRequest)
async def handle_analysis_request(ctx: Context, sender: str, msg: AnalysisRequest):
    """
    Handle incoming AnalysisRequest message and return correlation analysis.

    Args:
        ctx: uAgents context for sending responses
        sender: Address of the requesting agent (Guardian)
        msg: AnalysisRequest message containing portfolio data
    """
    # Log incoming request (CRITICAL: must log all messages)
    logger.info(f"📨 Received AnalysisRequest {msg.request_id} from {sender}")

    start_time = time.time()

    try:
        # Convert portfolio_data dict to Portfolio model
        portfolio = Portfolio(**msg.portfolio_data)

        # Validate portfolio data
        if not portfolio or len(portfolio.tokens) == 0:
            raise ValueError("Portfolio must contain at least one token")

        logger.info(f"🔍 Analyzing portfolio with {len(portfolio.tokens)} tokens, ${portfolio.total_value_usd:,.2f} total value")

        # Perform correlation calculation
        portfolio_returns = calculate_portfolio_returns(portfolio, days=90)
        eth_returns = load_eth_returns(days=90)
        correlation_coef = calculate_pearson_correlation(portfolio_returns, eth_returns)

        # Build response
        # Use absolute value for percentage display and interpretation (thresholds from config)
        correlation_pct = int(abs(correlation_coef) * 100)
        interpretation = "High" if abs(correlation_coef) > HIGH_CORRELATION_THRESHOLD else "Moderate" if abs(correlation_coef) >= MODERATE_CORRELATION_THRESHOLD else "Low"

        # Include direction in narrative (positive/negative correlation)
        direction = "positively" if correlation_coef >= 0 else "negatively"
        narrative = f"Your portfolio is {correlation_pct}% {direction} correlated to ETH over the past 90 days. This indicates {interpretation.lower()} {direction.rstrip('ly')} correlation."

        analysis = CorrelationAnalysis(
            correlation_coefficient=correlation_coef,
            correlation_percentage=correlation_pct,
            interpretation=interpretation,
            historical_context=[],  # Empty for Story 1.3, populated in Story 1.4
            calculation_period_days=90,
            narrative=narrative,
        )

        processing_time_ms = int((time.time() - start_time) * 1000)

        logger.info(f"✅ Analysis complete: {correlation_pct}% correlation ({interpretation}) in {processing_time_ms}ms")

        # Send response back to sender (convert analysis to dict for uAgents compatibility)
        await ctx.send(
            sender,
            CorrelationAnalysisResponse(
                request_id=msg.request_id,
                wallet_address=msg.wallet_address,
                analysis_data=analysis.model_dump(),
                agent_address=ctx.agent.address,
                processing_time_ms=processing_time_ms,
            ),
        )

        logger.info(f"📤 Sent CorrelationAnalysisResponse for {msg.request_id}")

    except Exception as e:
        # Error handling: send ErrorMessage, never crash silently
        logger.error(f"❌ Error processing {msg.request_id}: {str(e)}")

        processing_time_ms = int((time.time() - start_time) * 1000)

        await ctx.send(
            sender,
            ErrorMessage(
                request_id=msg.request_id,
                error_type="insufficient_data" if "insufficient" in str(e).lower() else "invalid_data",
                error_message=f"Correlation analysis failed: {str(e)}",
                agent_address=ctx.agent.address,
                retry_recommended=False,
            ),
        )

        logger.info(f"📤 Sent ErrorMessage for {msg.request_id} ({processing_time_ms}ms)")


# =============================================================================
# STARTUP MESSAGE
# =============================================================================

@correlation_agent.on_event("startup")
async def startup(ctx: Context):
    """Log startup information."""
    logger.info("=" * 70)
    logger.info("🚀 CorrelationAgent Started Successfully!")
    logger.info(f"📍 Agent Address: {ctx.agent.address}")
    logger.info(f"⚙️  Configuration:")
    logger.info(f"   - High Correlation Threshold: {HIGH_CORRELATION_THRESHOLD * 100}%")
    logger.info(f"   - Moderate Correlation Threshold: {MODERATE_CORRELATION_THRESHOLD * 100}%")
    logger.info(f"   - Min Required Data Days: {MIN_REQUIRED_DATA_DAYS}")
    logger.info(f"   - Max Excluded Value Ratio: {MAX_EXCLUDED_VALUE_RATIO * 100}%")
    logger.info(f"📊 Data Source: GitHub ({GITHUB_RAW_BASE_URL})")
    logger.info(f"✅ Ready to receive AnalysisRequest messages")
    logger.info("=" * 70)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    logger.info("Starting CorrelationAgent...")
    correlation_agent.run()
