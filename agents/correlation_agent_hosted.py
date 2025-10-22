"""
CorrelationAgent - Agentverse Hosted Version with ASI1 LLM Integration

This version is compatible with Agentverse hosted platform constraints:
- Uses only supported libraries (requests, statistics, no pandas/numpy)
- Integrates chat protocol for ASI1 LLM compatibility
- Includes AI-powered parameter extraction via OpenAI/Claude agents
- Fetches historical price data from GitHub repository

Deployment Instructions:
1. Create agent on Agentverse → Agents → Launch an Agent → Blank Agent
2. Copy this entire file into agent.py
3. Add comprehensive README in Overview section for ASI1 discoverability
4. Click "Start" to deploy
5. Copy agent address from logs and update .env file

Environment Variables (set in Agentverse dashboard - NO COMMENTS):
- CORRELATION_AGENT_SEED=<your_secret_seed_phrase>
- HIGH_CORRELATION_THRESHOLD=85
- MODERATE_CORRELATION_THRESHOLD=70
- MIN_REQUIRED_DATA_DAYS=60
- MAX_EXCLUDED_VALUE_RATIO=50
- LOG_LEVEL=INFO
- AI_AGENT_CHOICE=openai (or "claude")
"""

import os
import time
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, Dict, List
from statistics import correlation as pearson_correlation
from math import sqrt

import requests
from pydantic import BaseModel
from uagents import Agent, Context, Model, Protocol
from uagents_core.models import ErrorMessage

# Import chat protocol components for ASI1 LLM integration
from uagents_core.contrib.protocols.chat import (
    chat_protocol_spec,
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    StartSessionContent,
    EndSessionContent,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

def get_env_var(key: str, default: str = "") -> str:
    """Get environment variable with optional default value."""
    value = os.getenv(key, default)
    if not value and key == "CORRELATION_AGENT_SEED":
        print(f"⚠️ {key} not set, using default seed (NOT SECURE for production)")
        return "correlation_agent_insecure_default_seed_change_me"
    # Strip inline comments and whitespace (handles "85 # comment" -> "85")
    if "#" in value:
        value = value.split("#")[0].strip()
    return value.strip()

# Agent configuration
CORRELATION_AGENT_SEED = get_env_var("CORRELATION_AGENT_SEED")

# AI Agent selection for parameter extraction
AI_AGENT_CHOICE = get_env_var("AI_AGENT_CHOICE", "openai")
OPENAI_AGENT = 'agent1qtlpfshtlcxekgrfcpmv7m9zpajuwu7d5jfyachvpa4u3dkt6k0uwwp2lct'
CLAUDE_AGENT = 'agent1qvk7q2av3e2y5gf5s90nfzkc8a48q3wdqeevwrtgqfdl0k78rspd6f2l4dx'
AI_AGENT_ADDRESS = OPENAI_AGENT if AI_AGENT_CHOICE == "openai" else CLAUDE_AGENT

# Correlation calculation configuration
HIGH_CORRELATION_THRESHOLD = float(get_env_var("HIGH_CORRELATION_THRESHOLD", "85")) / 100
MODERATE_CORRELATION_THRESHOLD = float(get_env_var("MODERATE_CORRELATION_THRESHOLD", "70")) / 100
MIN_REQUIRED_DATA_DAYS = int(get_env_var("MIN_REQUIRED_DATA_DAYS", "60"))
MAX_EXCLUDED_VALUE_RATIO = float(get_env_var("MAX_EXCLUDED_VALUE_RATIO", "50")) / 100

# GitHub raw data URLs
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/Zolldyk/Guardian/main/data/historical_prices"
GITHUB_CRASH_DATA_URL = "https://raw.githubusercontent.com/Zolldyk/Guardian/main/data/historical-crashes.json"

print(f"✅ Configuration loaded: HIGH_THRESHOLD={HIGH_CORRELATION_THRESHOLD}, MIN_DAYS={MIN_REQUIRED_DATA_DAYS}")

# =============================================================================
# DATA MODELS (Pydantic)
# =============================================================================

class TokenHolding(BaseModel):
    """Represents a single token holding within a portfolio."""
    symbol: str
    amount: float
    price_usd: float
    value_usd: float


class Portfolio(BaseModel):
    """Complete portfolio data structure passed between agents."""
    wallet_address: str
    tokens: List[TokenHolding]
    total_value_usd: float
    analysis_timestamp: datetime


class CrashPerformance(BaseModel):
    """Historical crash performance for a given correlation bracket."""
    crash_name: str
    crash_period: str
    eth_drawdown_pct: float
    portfolio_loss_pct: float
    market_avg_loss_pct: float


class CorrelationAnalysis(BaseModel):
    """Correlation analysis results from CorrelationAgent."""
    correlation_coefficient: float
    correlation_percentage: int
    interpretation: str
    historical_context: List[CrashPerformance] = []
    calculation_period_days: int = 90
    narrative: str


# =============================================================================
# uAGENTS MESSAGE MODELS
# =============================================================================

class AnalysisRequest(Model):
    """Request message sent from Guardian or via chat protocol."""
    request_id: str
    wallet_address: str
    portfolio_data: dict
    requested_by: str


class CorrelationAnalysisResponse(Model):
    """Response message from CorrelationAgent with analysis results."""
    request_id: str
    wallet_address: str
    analysis_data: dict  # CorrelationAnalysis serialized as dict
    agent_address: str
    processing_time_ms: int


class CorrelationErrorMessage(Model):
    """Error message for correlation analysis failures."""
    request_id: str
    error_type: str
    error_message: str
    agent_address: str
    retry_recommended: bool


# AI Parameter Extraction Models
class StructuredOutputPrompt(Model):
    """Prompt sent to AI agent for parameter extraction."""
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    """Response from AI agent with extracted parameters."""
    output: dict[str, Any]


# =============================================================================
# CORRELATION CALCULATION FUNCTIONS (Pure Python)
# =============================================================================

def load_price_data_from_github(symbol: str, days: int) -> List[Dict[str, Any]]:
    """
    Load historical price data from GitHub repository.

    Args:
        symbol: Token symbol (e.g., 'ETH', 'UNI')
        days: Number of days of historical data to load

    Returns:
        List of dicts with keys: date, price_usd, volume_usd

    Raises:
        FileNotFoundError: If CSV file for symbol doesn't exist
        ValueError: If insufficient data available
    """
    url = f"{GITHUB_RAW_BASE_URL}/{symbol}.csv"

    try:
        print(f"Fetching price data for {symbol} from GitHub...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse CSV manually (no pandas)
        lines = response.text.strip().split("\n")
        headers = lines[0].split(",")

        prices = []
        for line in lines[1:]:  # Skip header
            values = line.split(",")
            if len(values) >= 3:
                prices.append({
                    "date": values[0],
                    "price_usd": float(values[1]),
                    "volume_usd": float(values[2]) if len(values) > 2 else 0.0
                })

        # Get last N+1 days (need extra for returns calculation)
        prices = prices[-(days + 1):]

        if len(prices) < days:
            raise ValueError(f"Insufficient data for {symbol}: found {len(prices)} days, need {days}")

        print(f"✅ Loaded {len(prices)} days of price data for {symbol}")
        return prices

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise FileNotFoundError(f"Price data not found for {symbol} at {url}")
        raise
    except Exception as e:
        print(f"❌ Failed to load price data for {symbol}: {e}")
        raise


def calculate_daily_returns(prices: List[float]) -> List[float]:
    """
    Calculate daily returns from price list.

    Args:
        prices: List of daily prices

    Returns:
        List of daily returns (pct_change)
    """
    returns = []
    for i in range(1, len(prices)):
        pct_change = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(pct_change)
    return returns


def load_eth_returns(days: int) -> List[float]:
    """
    Load ETH price data and calculate daily returns.

    Args:
        days: Number of days for historical window

    Returns:
        List of daily ETH returns
    """
    price_data = load_price_data_from_github("ETH", days)
    prices = [row["price_usd"] for row in price_data]
    returns = calculate_daily_returns(prices)
    return returns


def calculate_portfolio_returns(portfolio: Portfolio, days: int) -> List[float]:
    """
    Calculate portfolio weighted average returns.

    Args:
        portfolio: Portfolio containing tokens and their allocations
        days: Number of days for historical window

    Returns:
        List of daily weighted portfolio returns

    Raises:
        ValueError: If insufficient data or no valid tokens
    """
    # Calculate weight for each token
    total_value = portfolio.total_value_usd
    token_weights: Dict[str, float] = {}
    token_returns: Dict[str, List[float]] = {}

    excluded_tokens = []
    excluded_value = 0.0

    for token in portfolio.tokens:
        symbol = token.symbol
        weight = token.value_usd / total_value
        token_weights[symbol] = weight

        try:
            # Load price data and calculate returns
            price_data = load_price_data_from_github(symbol, days)
            prices = [row["price_usd"] for row in price_data]
            returns = calculate_daily_returns(prices)

            # Check if we have enough data
            if len(returns) < MIN_REQUIRED_DATA_DAYS:
                print(f"Token {symbol} has insufficient data ({len(returns)} days), excluding")
                excluded_tokens.append(symbol)
                excluded_value += token.value_usd
                continue

            token_returns[symbol] = returns

        except FileNotFoundError:
            print(f"Token {symbol} not found in historical data, excluding")
            excluded_tokens.append(symbol)
            excluded_value += token.value_usd
            continue
        except Exception as e:
            print(f"Error loading {symbol}: {e}, excluding")
            excluded_tokens.append(symbol)
            excluded_value += token.value_usd
            continue

    # Check if we excluded too much of the portfolio
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

    # Find common dates (intersection of all return series)
    # Assume all return series have same length since we fetched same number of days
    num_days = min(len(returns) for returns in token_returns.values())

    if num_days < MIN_REQUIRED_DATA_DAYS:
        raise ValueError(f"Insufficient overlapping data: only {num_days} common dates")

    # Calculate weighted portfolio returns
    portfolio_returns = [0.0] * num_days

    for symbol, returns in token_returns.items():
        weight = adjusted_weights[symbol]
        # Ensure we only use the common number of days
        for i in range(num_days):
            portfolio_returns[i] += weight * returns[i]

    return portfolio_returns


def calculate_pearson_correlation_pure_python(portfolio_returns: List[float], eth_returns: List[float]) -> float:
    """
    Compute Pearson correlation coefficient using pure Python (no numpy).

    Args:
        portfolio_returns: List of daily portfolio returns
        eth_returns: List of daily ETH returns

    Returns:
        Correlation coefficient (-1.0 to +1.0)
    """
    # Ensure same length
    min_length = min(len(portfolio_returns), len(eth_returns))
    portfolio_returns = portfolio_returns[:min_length]
    eth_returns = eth_returns[:min_length]

    # Use Python's statistics module
    try:
        correlation_coef = pearson_correlation(portfolio_returns, eth_returns)
    except Exception as e:
        print(f"⚠️ Correlation calculation failed: {e}, returning 0.0")
        return 0.0

    # Handle edge cases
    if correlation_coef != correlation_coef:  # NaN check
        print("⚠️ Correlation resulted in NaN, returning 0.0")
        return 0.0

    return correlation_coef


# =============================================================================
# HISTORICAL CRASH CONTEXT FUNCTIONS (Pure Python)
# =============================================================================

def load_historical_crashes() -> dict:
    """
    Load historical crash data from GitHub using pure Python (no pandas).

    Returns:
        Dict with crash scenario data

    Raises:
        FileNotFoundError: If historical-crashes.json doesn't exist
        ValueError: If JSON is malformed
    """
    try:
        print(f"Fetching historical crash data from GitHub...")
        response = requests.get(GITHUB_CRASH_DATA_URL, timeout=10)
        response.raise_for_status()

        # Parse JSON using native json module
        import json
        data = json.loads(response.text)

        print(f"✅ Loaded {len(data.get('crashes', []))} crash scenarios")
        return data

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise FileNotFoundError(f"Historical crash data not found at {GITHUB_CRASH_DATA_URL}")
        raise
    except Exception as e:
        print(f"❌ Failed to load historical crash data: {e}")
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
        data = load_historical_crashes()
    except (FileNotFoundError, ValueError):
        # Graceful fallback: return empty list if data unavailable
        print("⚠️ Historical crash data unavailable, returning empty context")
        return []

    # Determine correlation bracket using pure Python conditionals
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

    for crash in data.get("crashes", []):
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

    print(f"📊 Loaded crash context for {bracket} correlation bracket: {len(crash_performances)} scenarios")
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


def process_correlation_analysis(portfolio_data: dict) -> CorrelationAnalysis:
    """
    Main correlation analysis function with historical crash context.

    Args:
        portfolio_data: Portfolio data dict

    Returns:
        CorrelationAnalysis result with crash context

    Raises:
        ValueError: If analysis cannot be completed
    """
    # Convert portfolio_data dict to Portfolio model
    portfolio = Portfolio(**portfolio_data)

    # Validate portfolio data
    if not portfolio or len(portfolio.tokens) == 0:
        raise ValueError("Portfolio must contain at least one token")

    print(f"🔍 Analyzing portfolio with {len(portfolio.tokens)} tokens, ${portfolio.total_value_usd:,.2f} total value")

    # Perform correlation calculation
    portfolio_returns = calculate_portfolio_returns(portfolio, days=90)
    eth_returns = load_eth_returns(days=90)
    correlation_coef = calculate_pearson_correlation_pure_python(portfolio_returns, eth_returns)

    # Build response
    correlation_pct = int(abs(correlation_coef) * 100)
    interpretation = (
        "High" if abs(correlation_coef) > HIGH_CORRELATION_THRESHOLD
        else "Moderate" if abs(correlation_coef) >= MODERATE_CORRELATION_THRESHOLD
        else "Low"
    )

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

    return analysis


# =============================================================================
# AGENT INITIALIZATION
# =============================================================================

# IMPORTANT: Agentverse provides a pre-created 'agent' instance
# We don't create our own Agent() - just use the provided one
# The seed is set via Agentverse environment variables

print(f"✅ CorrelationAgent initializing...")

# Create protocols
chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_proto = Protocol(
    name="StructuredOutputClientProtocol",
    version="0.1.0"
)

# =============================================================================
# CHAT PROTOCOL HANDLERS (ASI1 LLM Integration)
# =============================================================================

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle incoming ChatMessage from ASI1 LLM.
    Extracts user query and forwards to AI agent for parameter extraction.
    """
    ctx.logger.info(f"📨 Received ChatMessage from {sender}")

    # Store session sender for response routing
    ctx.storage.set(str(ctx.session), sender)

    # Send acknowledgement
    await ctx.send(
        sender,
        ChatAcknowledgement(
            acknowledged_msg_id=msg.msg_id,
            timestamp=datetime.now(timezone.utc)
        ),
    )

    # Process message content
    for content in msg.content:
        if isinstance(content, StartSessionContent):
            ctx.logger.info(f"🟢 Session started with {sender}")
            continue

        elif isinstance(content, EndSessionContent):
            ctx.logger.info(f"🔴 Session ended with {sender}")
            continue

        elif isinstance(content, TextContent):
            ctx.logger.info(f"💬 User query: {content.text}")

            # Forward to AI agent for structured parameter extraction
            # Use simplified schema dict for Agentverse compatibility
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=content.text,
                    output_schema={
                        "type": "object",
                        "properties": {
                            "wallet_address": {
                                "type": "string",
                                "description": "Ethereum wallet address starting with 0x (40 hex characters)"
                            }
                        },
                        "required": ["wallet_address"]
                    }
                ),
            )


@chat_proto.on_message(ChatAcknowledgement)
async def handle_chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle chat acknowledgements."""
    ctx.logger.info(f"✅ Message {msg.acknowledged_msg_id} acknowledged by {sender}")


# =============================================================================
# AI PARAMETER EXTRACTION HANDLER
# =============================================================================

@struct_output_proto.on_message(StructuredOutputResponse)
async def handle_structured_output(ctx: Context, sender: str, msg: StructuredOutputResponse):
    """
    Handle AI agent response with extracted parameters.
    Processes correlation analysis and sends result back to user.
    """
    session_sender = ctx.storage.get(str(ctx.session))

    if session_sender is None:
        ctx.logger.error("❌ No session sender found in storage")
        return

    # Check if AI couldn't extract parameters
    if "<UNKNOWN>" in str(msg.output):
        error_response = ChatMessage(
            content=[TextContent(
                text="Sorry, I couldn't understand your request. Please provide a wallet address or portfolio data."
            )],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, error_response)
        return

    start_time = time.time()

    try:
        # Extract wallet address from AI response
        wallet_address = msg.output.get("wallet_address")

        if not wallet_address:
            raise ValueError("Could not extract wallet address from query")

        ctx.logger.info(f"🔍 Extracted wallet address: {wallet_address}")

        # NOTE: For Chat Protocol, we need portfolio data to perform analysis
        # This demo version doesn't integrate with blockchain APIs
        # In production, you would fetch portfolio data from Alchemy/Moralis/etc.

        error_response = ChatMessage(
            content=[TextContent(
                text=f"I've identified wallet address: `{wallet_address}`\n\n"
                     f"However, to analyze your portfolio correlation with ETH, I need portfolio data "
                     f"(token holdings, amounts, and current prices).\n\n"
                     f"**For direct agent-to-agent analysis**, send an `AnalysisRequest` message with full portfolio data.\n\n"
                     f"**For production deployment**, this agent would integrate with blockchain data providers "
                     f"(Alchemy, Moralis, Covalent) to automatically fetch your portfolio holdings.\n\n"
                     f"This is a demo version showing the Chat Protocol integration pattern."
            )],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, error_response)
        ctx.logger.info(f"📤 Sent portfolio data request to {session_sender}")
        return

    except Exception as err:
        ctx.logger.error(f"❌ Error processing analysis: {err}")

        processing_time_ms = int((time.time() - start_time) * 1000)

        error_response = ChatMessage(
            content=[TextContent(
                text=f"Sorry, I encountered an error analyzing your portfolio: {str(err)}. Please try again or contact support."
            )],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, error_response)


# =============================================================================
# DIRECT MESSAGE HANDLER (Agent-to-Agent Communication)
# =============================================================================

@agent.on_message(model=AnalysisRequest)
async def handle_direct_analysis_request(ctx: Context, sender: str, msg: AnalysisRequest):
    """
    Handle direct AnalysisRequest from other agents (e.g., Guardian).
    Bypasses chat protocol and AI extraction for agent-to-agent communication.
    """
    ctx.logger.info(f"📨 Received direct AnalysisRequest {msg.request_id} from {sender}")

    start_time = time.time()

    try:
        # Perform correlation analysis
        analysis = process_correlation_analysis(msg.portfolio_data)

        processing_time_ms = int((time.time() - start_time) * 1000)

        ctx.logger.info(f"✅ Analysis complete: {analysis.correlation_percentage}% correlation in {processing_time_ms}ms")

        # Send response back to sender
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

        ctx.logger.info(f"📤 Sent CorrelationAnalysisResponse for {msg.request_id}")

    except Exception as e:
        ctx.logger.error(f"❌ Error processing {msg.request_id}: {str(e)}")

        processing_time_ms = int((time.time() - start_time) * 1000)

        await ctx.send(
            sender,
            CorrelationErrorMessage(
                request_id=msg.request_id,
                error_type="insufficient_data" if "insufficient" in str(e).lower() else "invalid_data",
                error_message=f"Correlation analysis failed: {str(e)}",
                agent_address=ctx.agent.address,
                retry_recommended=False,
            ),
        )

        ctx.logger.info(f"📤 Sent ErrorMessage for {msg.request_id}")


# =============================================================================
# STARTUP HANDLER
# =============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    """Log startup information."""
    ctx.logger.info("=" * 70)
    ctx.logger.info("🚀 CorrelationAgent (Agentverse Hosted) Started Successfully!")
    ctx.logger.info(f"📍 Agent Address: {ctx.agent.address}")
    ctx.logger.info(f"⚙️  Configuration:")
    ctx.logger.info(f"   - AI Agent: {AI_AGENT_CHOICE.upper()}")
    ctx.logger.info(f"   - High Correlation Threshold: {HIGH_CORRELATION_THRESHOLD * 100}%")
    ctx.logger.info(f"   - Moderate Correlation Threshold: {MODERATE_CORRELATION_THRESHOLD * 100}%")
    ctx.logger.info(f"   - Min Required Data Days: {MIN_REQUIRED_DATA_DAYS}")
    ctx.logger.info(f"   - Max Excluded Value Ratio: {MAX_EXCLUDED_VALUE_RATIO * 100}%")
    ctx.logger.info(f"📊 Data Source: GitHub ({GITHUB_RAW_BASE_URL})")
    ctx.logger.info(f"💬 ASI1 LLM Integration: ✅ Enabled")
    ctx.logger.info(f"✅ Ready to receive messages (Chat Protocol + Direct)")
    ctx.logger.info("=" * 70)


# =============================================================================
# REGISTER PROTOCOLS
# =============================================================================

# Only publish chat_proto manifest (for ASI:One discoverability)
# struct_output_proto is internal communication only
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_proto, publish_manifest=False)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("Starting CorrelationAgent (Agentverse Hosted Version)...")
    agent.run()
