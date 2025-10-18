"""
CorrelationAgent - Analyzes portfolio correlation to ETH.

This agent calculates the Pearson correlation coefficient between a portfolio's
weighted returns and ETH returns over a 90-day historical window.
"""

import logging
import time
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from uagents import Agent, Context

from agents.shared.config import (
    get_env_var,
    HIGH_CORRELATION_THRESHOLD,
    MODERATE_CORRELATION_THRESHOLD,
    MIN_REQUIRED_DATA_DAYS,
    MAX_EXCLUDED_VALUE_RATIO,
)
from agents.shared.models import (
    AnalysisRequest,
    CorrelationAnalysis,
    CorrelationAnalysisResponse,
    ErrorMessage,
    Portfolio,
)

logger = logging.getLogger(__name__)

# Path to historical price data
HISTORICAL_PRICES_DIR = Path(__file__).parent.parent / "data" / "historical_prices"

# Agent initialization with seed from environment
correlation_agent = Agent(
    name="correlation_agent",
    seed=get_env_var("CORRELATION_AGENT_SEED", default="correlation_agent_secret_seed"),
    port=8001,
)


def load_price_data(symbol: str, days: int) -> pd.DataFrame:
    """
    Load historical price data for a token from CSV file.

    Args:
        symbol: Token symbol (e.g., 'ETH', 'UNI')
        days: Number of days of historical data to load

    Returns:
        DataFrame with columns: date, price_usd, volume_usd

    Raises:
        FileNotFoundError: If CSV file for symbol doesn't exist
        ValueError: If insufficient data available
    """
    csv_path = HISTORICAL_PRICES_DIR / f"{symbol}.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Price data not found for {symbol} at {csv_path}")

    # Load CSV
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Get last N days
    df = df.tail(days + 1).reset_index(drop=True)  # +1 for calculating returns

    if len(df) < days:
        raise ValueError(f"Insufficient data for {symbol}: found {len(df)} days, need {days}")

    return df


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

    Raises:
        FileNotFoundError: If ETH.csv doesn't exist
        ValueError: If insufficient data available
    """
    df = load_price_data("ETH", days)
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
            df = load_price_data(symbol, days)
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
        Correlation coefficient (0.0 to 1.0)
    """
    # Align the two series to have the same dates
    # Use inner join to get only dates present in both series
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
    logger.info(f"Received AnalysisRequest {msg.request_id} from {sender}")

    start_time = time.time()

    try:
        # Convert portfolio_data dict to Portfolio model
        portfolio = Portfolio(**msg.portfolio_data)

        # Validate portfolio data
        if not portfolio or len(portfolio.tokens) == 0:
            raise ValueError("Portfolio must contain at least one token")

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

        logger.info(f"Sent CorrelationAnalysisResponse for {msg.request_id} ({processing_time_ms}ms)")

    except Exception as e:
        # Error handling: send ErrorMessage, never crash silently
        logger.error(f"Error processing {msg.request_id}: {str(e)}")

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

        logger.info(f"Sent ErrorMessage for {msg.request_id} ({processing_time_ms}ms)")


if __name__ == "__main__":
    correlation_agent.run()
