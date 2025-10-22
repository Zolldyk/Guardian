"""
CorrelationAgent Local - Analyzes portfolio correlation to ETH with historical crash context.

This is the LOCAL DEVELOPMENT VERSION using pandas/numpy for data processing.
For production deployment to Agentverse, use correlation_agent_hosted.py.

This agent calculates the Pearson correlation coefficient between a portfolio's
weighted returns and ETH returns over a 90-day historical window, and includes
historical crash performance context for the portfolio's correlation level.
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List

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
    CrashPerformance,
    ErrorMessage,
    Portfolio,
)

logger = logging.getLogger(__name__)

# Path to historical price data
HISTORICAL_PRICES_DIR = Path(__file__).parent.parent / "data" / "historical_prices"
HISTORICAL_CRASHES_PATH = Path(__file__).parent.parent / "data" / "historical-crashes.json"

# Agent initialization with seed from environment
correlation_agent = Agent(
    name="correlation_agent_local",
    seed=get_env_var("CORRELATION_AGENT_SEED", default="correlation_agent_local_secret_seed"),
    port=8001,
)


def load_historical_crashes() -> pd.DataFrame:
    """
    Load historical crash data from JSON file using pandas.

    Returns:
        DataFrame with crash scenario data

    Raises:
        FileNotFoundError: If historical-crashes.json doesn't exist
        ValueError: If JSON is malformed
    """
    if not HISTORICAL_CRASHES_PATH.exists():
        raise FileNotFoundError(f"Historical crash data not found at {HISTORICAL_CRASHES_PATH}")

    try:
        with open(HISTORICAL_CRASHES_PATH) as f:
            data = json.load(f)

        # Convert to DataFrame
        df = pd.DataFrame(data["crashes"])
        return df
    except Exception as e:
        raise ValueError(f"Failed to load historical crash data: {str(e)}")


def get_crash_context(correlation_pct: int) -> List[CrashPerformance]:
    """
    Query historical crash data based on calculated correlation coefficient.

    Args:
        correlation_pct: Portfolio correlation percentage (0-100)

    Returns:
        List of CrashPerformance models for all 3 crash scenarios

    Raises:
        FileNotFoundError: If crash data file missing
    """
    try:
        df = load_historical_crashes()
    except FileNotFoundError:
        # Graceful fallback: return empty list if data unavailable
        logger.warning("Historical crash data unavailable, returning empty context")
        return []

    # Determine correlation bracket
    if correlation_pct > 90:
        bracket = ">90%"
    elif correlation_pct >= 80:
        bracket = "80-90%"
    elif correlation_pct >= 70:
        bracket = "70-80%"
    else:
        bracket = "<70%"

    # Extract crash performance for this bracket from all 3 scenarios
    crash_performances = []

    for _, crash in df.iterrows():
        portfolio_loss = crash["correlation_brackets"][bracket]

        crash_performances.append(
            CrashPerformance(
                crash_name=crash["name"],
                crash_period=crash["period"],
                eth_drawdown_pct=crash["eth_drawdown_pct"],
                portfolio_loss_pct=portfolio_loss,
                market_avg_loss_pct=crash["market_avg_loss_pct"],
            )
        )

    return crash_performances


def generate_narrative_with_crash_context(
    correlation_coef: float,
    correlation_pct: int,
    interpretation: str,
    crash_context: List[CrashPerformance]
) -> str:
    """
    Generate plain English narrative explaining correlation with historical crash context.

    Args:
        correlation_coef: Raw correlation coefficient (-1 to 1)
        correlation_pct: Correlation percentage (0-100)
        interpretation: Interpretation level (High/Moderate/Low)
        crash_context: List of historical crash performances

    Returns:
        Plain English narrative with crash context
    """
    # Direction of correlation
    direction = "positively" if correlation_coef >= 0 else "negatively"

    # Base correlation statement
    narrative_parts = [
        f"Your portfolio is {correlation_pct}% {direction} correlated to ETH over the past 90 days. "
        f"This is {interpretation} correlation."
    ]

    # Add historical crash context if available
    if crash_context:
        narrative_parts.append("\n\nHistorical crash performance for portfolios at your correlation level:")

        for crash in crash_context:
            narrative_parts.append(
                f"\n- {crash.crash_name} ({crash.crash_period}): "
                f"Portfolios at your correlation level lost an average of {crash.portfolio_loss_pct:.0f}% "
                f"(ETH dropped {crash.eth_drawdown_pct:.0f}%), compared to {crash.market_avg_loss_pct:.0f}% market average."
            )

        # Add risk implication based on interpretation
        if interpretation == "High":
            narrative_parts.append(
                "\n\nThis high correlation means your portfolio moves almost identically to ETH, "
                "amplifying both gains and losses. When ETH crashes, your portfolio will likely crash equally hard. "
                "Diversifying with uncorrelated assets (BTC, stablecoins, Layer-1 alternatives) could reduce this compounding risk."
            )
        elif interpretation == "Moderate":
            narrative_parts.append(
                "\n\nThis moderate correlation means your portfolio has some diversification from ETH movements, "
                "but still experiences significant exposure. Continue balancing ETH-correlated DeFi positions "
                "with uncorrelated assets to improve risk-adjusted returns."
            )
        else:  # Low
            narrative_parts.append(
                "\n\nYour portfolio structure demonstrates good diversification from ETH movements. "
                "Continue maintaining exposure to uncorrelated assets to preserve this risk-reduction benefit."
            )
    else:
        # Fallback narrative if crash data unavailable
        narrative_parts.append(
            f" This indicates {interpretation.lower()} {direction.rstrip('ly')} correlation. "
            "Historical crash data unavailable."
        )

    return "".join(narrative_parts)


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
        Correlation coefficient (-1.0 to 1.0)
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
    Handle incoming AnalysisRequest message and return correlation analysis with crash context.

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

        # Get historical crash context for this correlation level
        crash_context = get_crash_context(correlation_pct)

        # Generate narrative with crash context
        narrative = generate_narrative_with_crash_context(
            correlation_coef,
            correlation_pct,
            interpretation,
            crash_context
        )

        analysis = CorrelationAnalysis(
            correlation_coefficient=correlation_coef,
            correlation_percentage=correlation_pct,
            interpretation=interpretation,
            historical_context=crash_context,
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
