"""
Guardian Orchestrator Agent - Agentverse Hosted Version with ASI1 LLM Integration

This version is compatible with Agentverse hosted platform constraints:
- Uses only supported libraries (requests, no pandas/numpy)
- Integrates chat protocol for ASI1 LLM compatibility
- Includes AI-powered parameter extraction via OpenAI/Claude agents
- Fetches demo wallet data from GitHub repository

Deployment Instructions:
1. Create agent on Agentverse → Agents → Launch an Agent → Blank Agent
2. Copy this entire file into agent.py
3. Add comprehensive README in Overview section for ASI1 discoverability
4. Click "Start" to deploy
5. Copy agent address from logs and update .env file

Environment Variables (set in Agentverse dashboard - NO COMMENTS):
- GUARDIAN_AGENT_SEED=<your_secret_seed_phrase>
- CORRELATION_AGENT_ADDRESS=agent1qw...
- SECTOR_AGENT_ADDRESS=agent1qx...
- AGENT_RESPONSE_TIMEOUT=10
- AI_AGENT_CHOICE=openai (or "claude")
- LOG_LEVEL=INFO
"""

import os
import time
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, List

import requests
from pydantic import BaseModel
from uagents import Agent, Context, Model, Protocol

# Import chat protocol components for ASI1 LLM integration
from uagents_core.contrib.protocols.chat import (
    chat_protocol_spec,
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    StartSessionContent,
    EndSessionContent,
)

# Import shared models for inter-agent communication
# Import MeTTa interface for historical crash queries
try:
    from agents.shared.metta_interface import query_crashes_by_correlation_loss
except ImportError:
    # MeTTa interface may not be available in Agentverse sandbox
    def query_crashes_by_correlation_loss(correlation_bracket, min_loss_pct):
        """Fallback MeTTa query function."""
        return []

# =============================================================================
# CONFIGURATION
# =============================================================================

def get_env_var(key: str, default: str = "") -> str:
    """Get environment variable with optional default value."""
    value = os.getenv(key, default)
    if not value and key == "GUARDIAN_AGENT_SEED":
        print(f"⚠️ {key} not set, using default seed (NOT SECURE for production)")
        return "guardian_agent_insecure_default_seed_change_me"
    # Strip inline comments and whitespace
    if "#" in value:
        value = value.split("#")[0].strip()
    return value.strip()

# Agent configuration
GUARDIAN_AGENT_SEED = get_env_var("GUARDIAN_AGENT_SEED")

# Specialist agent addresses
CORRELATION_AGENT_ADDRESS = get_env_var("CORRELATION_AGENT_ADDRESS")
SECTOR_AGENT_ADDRESS = get_env_var("SECTOR_AGENT_ADDRESS")

# AI Agent selection for parameter extraction
AI_AGENT_CHOICE = get_env_var("AI_AGENT_CHOICE", "openai")
OPENAI_AGENT = 'agent1qtlpfshtlcxekgrfcpmv7m9zpajuwu7d5jfyachvpa4u3dkt6k0uwwp2lct'
CLAUDE_AGENT = 'agent1qvk7q2av3e2y5gf5s90nfzkc8a48q3wdqeevwrtgqfdl0k78rspd6f2l4dx'
AI_AGENT_ADDRESS = OPENAI_AGENT if AI_AGENT_CHOICE == "openai" else CLAUDE_AGENT

# Timeout configuration
AGENT_RESPONSE_TIMEOUT = int(get_env_var("AGENT_RESPONSE_TIMEOUT", "10"))

# GitHub raw data URLs
GITHUB_DEMO_WALLETS_URL = "https://raw.githubusercontent.com/Zolldyk/Guardian/main/data/demo-wallets.json"

print("✅ Guardian configuration loaded")
print(f"   CorrelationAgent: {CORRELATION_AGENT_ADDRESS}")
print(f"   SectorAgent: {SECTOR_AGENT_ADDRESS}")
print(f"   Timeout: {AGENT_RESPONSE_TIMEOUT}s")

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


# =============================================================================
# uAGENTS MESSAGE MODELS
# =============================================================================

class AnalysisRequest(Model):
    """Request message sent from Guardian to specialist agents."""
    request_id: str
    wallet_address: str
    portfolio_data: dict
    requested_by: str


class CorrelationAnalysisResponse(Model):
    """Response message from CorrelationAgent with analysis results."""
    request_id: str
    wallet_address: str
    analysis_data: dict
    agent_address: str
    processing_time_ms: int


class SectorAnalysisResponse(Model):
    """Response message from SectorAgent with analysis results."""
    request_id: str
    wallet_address: str
    analysis_data: dict
    agent_address: str
    processing_time_ms: int


class GuardianAnalysisResponse(Model):
    """Response message from Guardian with combined analysis."""
    request_id: str
    wallet_address: str
    correlation_analysis: dict | None
    sector_analysis: dict | None
    response_text: str
    agent_addresses: dict
    total_processing_time_ms: int


# AI Parameter Extraction Models
class StructuredOutputPrompt(Model):
    """Prompt sent to AI agent for parameter extraction."""
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    """Response from AI agent with extracted parameters."""
    output: dict[str, Any]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def extract_wallet_address_regex(text: str) -> str | None:
    """
    Extract Ethereum wallet address from text using regex pattern.

    This is a fallback mechanism when AI parameter extraction fails
    due to rate limiting or other errors.

    Args:
        text: Input text potentially containing wallet address

    Returns:
        Wallet address if found, None otherwise
    """
    import re
    pattern = r'0x[a-fA-F0-9]{40}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def load_demo_wallet_from_github(wallet_address: str) -> dict:
    """
    Load demo wallet data from GitHub repository.

    Args:
        wallet_address: Ethereum wallet address

    Returns:
        Portfolio data dict

    Raises:
        ValueError: If wallet not found or data unavailable
    """
    try:
        print("Fetching demo wallet data from GitHub...")
        response = requests.get(GITHUB_DEMO_WALLETS_URL, timeout=10)
        response.raise_for_status()

        data = response.json()
        wallets = data.get("demo_wallets", [])

        # Find matching wallet
        for wallet in wallets:
            if wallet["wallet_address"].lower() == wallet_address.lower():
                print(f"✅ Found demo wallet: {wallet['name']}")
                return wallet

        # Wallet not found
        available = [w["wallet_address"] for w in wallets]
        raise ValueError(
            f"Wallet {wallet_address} not found in demo wallets. "
            f"Available demo wallets: {', '.join(available)}"
        )

    except Exception as e:
        raise ValueError(f"Failed to load demo wallet data: {str(e)}")


def detect_compounding_risk(
    correlation_analysis: dict,
    sector_analysis: dict
) -> bool:
    """
    Detect if portfolio has compounding risk structure (pure Python).

    Args:
        correlation_analysis: Correlation analysis data dict
        sector_analysis: Sector analysis data dict

    Returns:
        True if BOTH correlation >85% AND sector >60%
    """
    high_correlation = correlation_analysis.get('correlation_percentage', 0) > 85
    high_concentration = len(sector_analysis.get('concentrated_sectors', [])) > 0

    return high_correlation and high_concentration


def calculate_risk_level(
    correlation_percentage: float,
    concentrated_sectors: list
) -> str:
    """
    Calculate overall risk level (pure Python).

    Args:
        correlation_percentage: Correlation percentage (0-100)
        concentrated_sectors: List of sectors with >60% concentration

    Returns:
        "Critical" | "High" | "Moderate" | "Low"
    """
    high_correlation = correlation_percentage > 85
    high_concentration = len(concentrated_sectors) > 0

    if high_correlation and high_concentration:
        return "Critical"
    elif high_correlation or high_concentration:
        return "High"
    elif correlation_percentage >= 70:
        return "Moderate"
    else:
        return "Low"


def truncate_address(address: str) -> str:
    """
    Truncate agent address for readability in headers.

    Args:
        address: Full agent address (e.g., "agent1qw2e3r4t5y6u7i8o9p0a1s2d3f4g5h6j7k8l9z0")

    Returns:
        Truncated address (e.g., "agent1qw2e...z0")

    Examples:
        >>> truncate_address("agent1qw2e3r4t5y6u7i8o9p0a1s2d3f4g5h6j7k8l9z0")
        'agent1qw2e...z0'
    """
    if len(address) <= 15:
        return address  # Already short, no truncation needed
    return f"{address[:10]}...{address[-3:]}"


def generate_synthesis_narrative(
    correlation_analysis: dict,
    sector_analysis: dict,
    compounding_risk_detected: bool,
    crash_data: list
) -> str:
    """
    Generate synthesis narrative with explicit agent attribution (pure Python, Story 2.5).

    Args:
        correlation_analysis: Correlation analysis dict
        sector_analysis: Sector analysis dict
        compounding_risk_detected: Whether compounding risk detected
        crash_data: Historical crash data

    Returns:
        Cohesive narrative string with agent references
    """
    correlation_pct = correlation_analysis.get('correlation_percentage', 0)
    concentrated_sectors = sector_analysis.get('concentrated_sectors', [])

    if compounding_risk_detected:
        # Compounding risk portfolio narrative with explicit agent attribution
        concentrated_sector = concentrated_sectors[0] if concentrated_sectors else "Unknown"
        sector_breakdown = sector_analysis.get('sector_breakdown', {})
        concentration_pct = 0

        if concentrated_sector in sector_breakdown:
            concentration_pct = sector_breakdown[concentrated_sector].get('percentage', 0)

        leverage = round(correlation_pct / 30.0, 1)

        # Build narrative with explicit agent references (Story 2.5)
        narrative = (
            f"As CorrelationAgent showed, your {correlation_pct}% ETH correlation creates significant exposure to Ethereum price movements. "
            f"SectorAgent revealed that your {concentration_pct:.0f}% {concentrated_sector} concentration amplifies this risk through sector-specific vulnerabilities. "
        )

        # Add Guardian's synthesis insight (combining both agents)
        narrative += (
            f"Combining these insights, Guardian identifies a compounding risk pattern: "
            f"this structure acts like {leverage}x leverage to ETH movements. "
        )

        if crash_data and len(crash_data) > 0:
            crash_name = crash_data[0].get('name', '2022 Bear Market')
            historical_context = correlation_analysis.get('historical_context', [])
            portfolio_loss = -75.0

            if historical_context:
                portfolio_loss = historical_context[0].get('portfolio_loss_pct', -75.0)

            correlation_only_loss = correlation_pct * 0.6

            narrative += (
                f"In {crash_name}, portfolios with this dual-risk structure lost {portfolio_loss:.0f}% "
                f"(not just {correlation_only_loss:.0f}% from correlation alone). "
            )

        narrative += f"{concentrated_sector} sector amplifies ETH correlation—when both crash together, losses multiply."

        print("Generated synthesis narrative with agent attribution (CorrelationAgent, SectorAgent references)")

        return narrative

    else:
        # Well-diversified portfolio narrative with explicit agent attribution
        narrative = (
            f"CorrelationAgent calculated your {correlation_pct}% ETH correlation as manageable. "
            f"According to SectorAgent's analysis, no sector exceeds 30% concentration. "
        )

        # Add Guardian's synthesis insight
        narrative += (
            "Combining these findings, Guardian confirms this balanced structure limits compounding risks. "
        )

        if crash_data and len(crash_data) > 0:
            crash_name = crash_data[0].get('name', '2022 Bear Market')
            historical_context = correlation_analysis.get('historical_context', [])
            market_avg_loss = -55.0

            if historical_context:
                market_avg_loss = historical_context[0].get('market_avg_loss_pct', -55.0)

            narrative += (
                f"During {crash_name}, well-diversified portfolios like yours lost around "
                f"{market_avg_loss:.0f}% versus -75% for concentrated portfolios."
            )

        print("Generated diversified portfolio synthesis narrative with agent attribution")

        return narrative


def get_correlation_recommendations(
    correlation_analysis: dict,
    priority: int
) -> dict:
    """
    Generate recommendation for high ETH correlation (pure Python).

    Args:
        correlation_analysis: Correlation analysis dict
        priority: Recommendation priority (1 = highest)

    Returns:
        Recommendation dict
    """
    correlation_pct = correlation_analysis.get('correlation_percentage', 0)

    # Extract historical loss data for rationale
    portfolio_loss = 73.0
    market_avg_loss = 55.0
    crash_name = "2022 Bear Market"

    historical_context = correlation_analysis.get('historical_context', [])
    if historical_context:
        crash_example = historical_context[0]
        portfolio_loss = abs(crash_example.get('portfolio_loss_pct', portfolio_loss))
        market_avg_loss = abs(crash_example.get('market_avg_loss_pct', market_avg_loss))
        crash_name = crash_example.get('crash_name', crash_name)

        target_bracket_loss = market_avg_loss * 0.9
        expected_impact = (
            f"Reducing correlation to 75-80% would have limited {crash_name} losses to "
            f"~{target_bracket_loss:.0f}% vs. {portfolio_loss:.0f}% for portfolios with "
            f">{correlation_pct-5}% correlation"
        )
    else:
        expected_impact = (
            "Reducing correlation to 75-80% would have limited 2022 losses to 60% vs. 73% "
            "for >90% correlated portfolios"
        )

    # CRITICAL: No specific token picks - stay in risk analysis domain
    action = (
        f"Add uncorrelated assets (Bitcoin, Alternative Layer-1s, or Stablecoins) to reduce "
        f"ETH correlation from {correlation_pct}% to below 80%"
    )

    rationale = (
        f"High ETH correlation means your portfolio moves in lockstep with ETH price. "
        f"Your {correlation_pct}% correlation means you lose {portfolio_loss:.0f}% when ETH crashes."
    )

    return {
        'priority': priority,
        'action': action,
        'rationale': rationale,
        'expected_impact': expected_impact
    }


def get_sector_recommendations(
    sector_analysis: dict,
    priority: int
) -> dict:
    """
    Generate recommendation for high sector concentration (pure Python).

    Args:
        sector_analysis: Sector analysis dict
        priority: Recommendation priority (1 = highest)

    Returns:
        Recommendation dict
    """
    concentrated_sectors = sector_analysis.get('concentrated_sectors', [])
    if not concentrated_sectors:
        return {}

    concentrated_sector = concentrated_sectors[0]
    sector_breakdown = sector_analysis.get('sector_breakdown', {})
    concentration_pct = 0

    if concentrated_sector in sector_breakdown:
        concentration_pct = sector_breakdown[concentrated_sector].get('percentage', 0)

    # Extract historical sector loss data for rationale
    sector_loss = 75.0
    crash_scenario = "2022 Bear Market"
    missed_gain = 500.0

    sector_risks = sector_analysis.get('sector_risks', [])
    sector_risk = next(
        (risk for risk in sector_risks if risk.get('sector_name') == concentrated_sector),
        None
    )

    if sector_risk:
        sector_loss = abs(sector_risk.get('sector_loss_pct', sector_loss))
        crash_scenario = sector_risk.get('crash_scenario', crash_scenario)

        opportunity_cost = sector_risk.get('opportunity_cost')
        if opportunity_cost:
            missed_gain = opportunity_cost.get('recovery_gain_pct', missed_gain)

    # CRITICAL: No specific token picks - stay in risk analysis domain
    action = (
        f"Reduce {concentrated_sector} token concentration from {concentration_pct:.0f}% to below 40%"
    )

    rationale = (
        f"Over-concentration in {concentrated_sector} means single-sector crashes "
        f"disproportionately impact your portfolio. {concentrated_sector} lost "
        f"{sector_loss:.0f}% in the {crash_scenario}."
    )

    expected_impact = (
        f"Reducing sector concentration would have limited losses and positioned portfolio for "
        f"{missed_gain:.0f}% recovery gains missed during 2023 rebound"
    )

    return {
        'priority': priority,
        'action': action,
        'rationale': rationale,
        'expected_impact': expected_impact
    }


def get_diversified_recommendations(
    correlation_analysis: dict,
    sector_analysis: dict
) -> dict:
    """
    Generate recommendation for well-diversified portfolio (pure Python).

    Args:
        correlation_analysis: Correlation analysis dict
        sector_analysis: Sector analysis dict

    Returns:
        Recommendation dict
    """
    correlation_pct = correlation_analysis.get('correlation_percentage', 0)

    # Extract top 3 sectors for acknowledgment
    sector_breakdown = sector_analysis.get('sector_breakdown', {})
    sorted_sectors = sorted(
        sector_breakdown.items(),
        key=lambda x: x[1].get('percentage', 0),
        reverse=True
    )[:3]

    sector_list_parts = []
    for sector_name, sector_holding in sorted_sectors:
        percentage = sector_holding.get('percentage', 0)
        sector_list_parts.append(f"{sector_name} ({percentage:.0f}%)")

    sector_list = ", ".join(sector_list_parts)

    action = "Maintain current balanced portfolio structure"

    rationale = (
        f"Your {correlation_pct}% ETH correlation and diversified sector allocation "
        f"({sector_list}) limit compounding risks. This balanced structure performed well historically."
    )

    expected_impact = (
        "Continue monitoring correlation and sector concentration quarterly to maintain risk balance. "
        "Set alerts if any sector exceeds 40% or correlation exceeds 80%."
    )

    return {
        'priority': 1,
        'action': action,
        'rationale': rationale,
        'expected_impact': expected_impact
    }


def get_prioritization_recommendation() -> dict:
    """
    Generate recommendation explaining compounding risk prioritization (pure Python).

    Returns:
        Recommendation dict
    """
    action = "Prioritize sector diversification before correlation reduction"

    rationale = (
        "When both high correlation and high sector concentration are present, sector concentration "
        "amplifies correlation risk. Reducing sector concentration to <40% will also naturally reduce "
        "ETH correlation as you add diversified assets."
    )

    expected_impact = (
        "Addressing sector concentration first provides compounding benefit by reducing both risk "
        "dimensions simultaneously, maximizing portfolio resilience"
    )

    return {
        'priority': 3,
        'action': action,
        'rationale': rationale,
        'expected_impact': expected_impact
    }


def generate_recommendations(
    correlation_analysis: dict,
    sector_analysis: dict,
    compounding_risk_detected: bool,
    overall_risk_level: str
) -> list:
    """
    Generate 1-3 actionable recommendations based on identified risks (pure Python).

    Args:
        correlation_analysis: Correlation analysis dict
        sector_analysis: Sector analysis dict
        compounding_risk_detected: Whether compounding risk detected
        overall_risk_level: Overall risk level (Critical/High/Moderate/Low)

    Returns:
        List of recommendation dicts, sorted by priority (1 = highest)
    """
    try:
        print(f"Generating recommendations for risk_level={overall_risk_level}")

        recommendations = []

        # Scenario 1: Well-diversified portfolio (Low risk)
        if overall_risk_level == "Low":
            recommendations.append(
                get_diversified_recommendations(correlation_analysis, sector_analysis)
            )
            print("Generated diversified portfolio recommendation")

        # Scenario 2: Compounding risk (Critical risk - both dimensions high)
        elif compounding_risk_detected:
            # Priority 1: Sector diversification (bigger impact)
            recommendations.append(
                get_sector_recommendations(sector_analysis, priority=1)
            )
            # Priority 2: Correlation reduction
            recommendations.append(
                get_correlation_recommendations(correlation_analysis, priority=2)
            )
            # Priority 3: Prioritization explanation
            recommendations.append(
                get_prioritization_recommendation()
            )
            print("Generated 3 recommendations for compounding risk")

        # Scenario 3: High correlation only
        elif correlation_analysis.get('correlation_percentage', 0) > 85:
            recommendations.append(
                get_correlation_recommendations(correlation_analysis, priority=1)
            )
            print("Generated correlation recommendation (high correlation only)")

        # Scenario 4: High sector concentration only
        elif len(sector_analysis.get('concentrated_sectors', [])) > 0:
            recommendations.append(
                get_sector_recommendations(sector_analysis, priority=1)
            )
            print("Generated sector recommendation (high concentration only)")

        # Scenario 5: Moderate risk
        else:
            if correlation_analysis.get('correlation_percentage', 0) >= 70:
                recommendations.append(
                    get_correlation_recommendations(correlation_analysis, priority=1)
                )
                print("Generated correlation recommendation for moderate risk")

            # Check for moderate sector concentration (40-60%)
            sector_breakdown = sector_analysis.get('sector_breakdown', {})
            moderate_sectors = [
                sector_name for sector_name, sector_holding in sector_breakdown.items()
                if sector_holding.get('percentage', 0) > 40
            ]

            if moderate_sectors and len(recommendations) == 0:
                temp_sector_analysis = sector_analysis.copy()
                temp_sector_analysis['concentrated_sectors'] = moderate_sectors
                recommendations.append(
                    get_sector_recommendations(temp_sector_analysis, priority=len(recommendations) + 1)
                )
                print("Generated sector recommendation for moderate concentration")

        # Sort by priority (1 = highest)
        recommendations.sort(key=lambda rec: rec.get('priority', 1))

        print(f"Generated {len(recommendations)} recommendations")

        return recommendations

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return []


def synthesis_analysis(
    correlation_response: dict,
    sector_response: dict,
    request_id: str = "unknown"
) -> dict:
    """
    Synthesize correlation and sector analysis (pure Python for Agentverse).

    Args:
        correlation_response: CorrelationAgent response dict
        sector_response: SectorAgent response dict
        request_id: Request ID for logging

    Returns:
        GuardianSynthesis dict
    """
    try:
        print(f"Starting synthesis analysis for request {request_id}")

        # Extract analysis data
        correlation_analysis = correlation_response.get('analysis_data', {})
        sector_analysis = sector_response.get('analysis_data', {})

        correlation_pct = correlation_analysis.get('correlation_percentage', 0)
        concentrated_sectors = sector_analysis.get('concentrated_sectors', [])

        # Detect compounding risk
        compounding_detected = detect_compounding_risk(correlation_analysis, sector_analysis)
        print(f"Compounding risk detected: {compounding_detected}")

        # Query MeTTa for historical crash data
        crash_data = []
        if compounding_detected:
            try:
                correlation_bracket = ">90%" if correlation_pct > 90 else "80-90%"
                crash_data = query_crashes_by_correlation_loss(
                    correlation_bracket=correlation_bracket,
                    min_loss_pct=-70.0
                )
                print(f"MeTTa query returned {len(crash_data)} crash scenarios")
            except Exception as e:
                print(f"MeTTa query failed: {e}")
                crash_data = []

        # Calculate risk multiplier effect
        leverage = round(correlation_pct / 30.0, 1)
        if compounding_detected and concentrated_sectors:
            concentrated_sector = concentrated_sectors[0]
            sector_breakdown = sector_analysis.get('sector_breakdown', {})
            concentration_pct = 0

            if concentrated_sector in sector_breakdown:
                concentration_pct = sector_breakdown[concentrated_sector].get('percentage', 0)

            risk_multiplier_effect = (
                f"Your {correlation_pct}% ETH correlation acts like {leverage}x leverage, "
                f"and {concentration_pct:.0f}% {concentrated_sector} concentration means "
                f"when {concentrated_sector} crashes, your entire portfolio amplifies the loss."
            )
        else:
            risk_multiplier_effect = (
                f"Your {correlation_pct}% correlation creates moderate ETH exposure, "
                f"but diversified sector allocation limits amplification risk."
            )

        # Calculate risk level
        overall_risk_level = calculate_risk_level(correlation_pct, concentrated_sectors)

        # Generate narrative
        synthesis_narrative = generate_synthesis_narrative(
            correlation_analysis,
            sector_analysis,
            compounding_detected,
            crash_data
        )

        # Generate actionable recommendations (Story 2.4)
        recommendations = generate_recommendations(
            correlation_analysis,
            sector_analysis,
            compounding_detected,
            overall_risk_level
        )
        print(f"Generated {len(recommendations)} recommendations for risk_level={overall_risk_level}")

        # Return synthesis dict
        synthesis = {
            'compounding_risk_detected': compounding_detected,
            'risk_multiplier_effect': risk_multiplier_effect,
            'recommendations': recommendations,  # Story 2.4: Populated with actionable recommendations
            'overall_risk_level': overall_risk_level,
            'synthesis_narrative': synthesis_narrative
        }

        print(f"Synthesis complete: risk_level={overall_risk_level}")

        return synthesis

    except Exception as e:
        print(f"Synthesis error: {e}")
        raise


# =============================================================================
# MULTI-TURN CONVERSATION CONTEXT MANAGEMENT (Story 3.1)
# =============================================================================

def init_conversation_state(session_id: str, wallet_address: str, portfolio_data: dict) -> dict:
    """
    Initialize conversation state for a new analysis session.

    Args:
        session_id: Unique session identifier
        wallet_address: Ethereum wallet address
        portfolio_data: Portfolio data dict from demo wallet

    Returns:
        Initialized conversation state dict
    """
    return {
        "session_id": session_id,
        "wallet_address": wallet_address,
        "portfolio_data": portfolio_data,
        "correlation_analysis": None,
        "sector_analysis": None,
        "synthesis": None,
        "conversation_history": [],
        "last_update": datetime.utcnow().isoformat()
    }


def get_conversation_state(ctx: Context) -> dict | None:
    """
    Retrieve conversation state from session storage.

    Args:
        ctx: uAgents context

    Returns:
        Conversation state dict or None if not found
    """
    session_key = f"conversation_{ctx.session}"
    state = ctx.storage.get(session_key)

    if state:
        ctx.logger.info(f"Session {ctx.session}: Retrieved conversation state for wallet {state.get('wallet_address', 'unknown')}")

    return state


def update_conversation_state(
    ctx: Context,
    state: dict,
    user_message: str,
    guardian_response: str,
    correlation_response: dict | None = None,
    sector_response: dict | None = None,
    synthesis: dict | None = None
) -> dict:
    """
    Update conversation state with new exchange and analysis results.

    Args:
        ctx: uAgents context
        state: Current conversation state
        user_message: User's message text
        guardian_response: Guardian's response text
        correlation_response: Optional CorrelationAgent response
        sector_response: Optional SectorAgent response
        synthesis: Optional synthesis results

    Returns:
        Updated conversation state dict
    """
    # Update analysis results if provided
    if correlation_response:
        state["correlation_analysis"] = correlation_response.get('analysis_data', {})

    if sector_response:
        state["sector_analysis"] = sector_response.get('analysis_data', {})

    if synthesis:
        state["synthesis"] = synthesis

    # Add to conversation history
    exchange = {
        "user_message": user_message,
        "guardian_response": guardian_response,
        "timestamp": datetime.utcnow().isoformat()
    }
    state["conversation_history"].append(exchange)

    # Prune history to max 10 exchanges
    if len(state["conversation_history"]) > 10:
        state["conversation_history"] = state["conversation_history"][-10:]
        ctx.logger.info(f"Session {ctx.session}: Pruned conversation history to 10 exchanges")

    # Update timestamp
    state["last_update"] = datetime.utcnow().isoformat()

    # Store updated state
    session_key = f"conversation_{ctx.session}"
    ctx.storage.set(session_key, state)

    ctx.logger.info(f"Session {ctx.session}: Updated conversation state (total exchanges: {len(state['conversation_history'])})")

    return state


def classify_follow_up_question(message_text: str) -> str:
    """
    Classify follow-up question type for response routing.

    Args:
        message_text: User's message text

    Returns:
        Question type: "correlation" | "sector" | "recommendation" | "crash_context" | "unclear"
    """
    message_lower = message_text.lower()

    # Correlation questions
    if any(keyword in message_lower for keyword in ["correlation", "correlated", "eth correlation", "eth price"]):
        return "correlation"

    # Sector questions
    if any(keyword in message_lower for keyword in ["sector", "concentration", "governance", "defi", "gaming"]):
        return "sector"

    # Recommendation questions
    if any(keyword in message_lower for keyword in ["what should", "how can", "recommend", "what do", "should i"]):
        return "recommendation"

    # Crash context questions
    if any(keyword in message_lower for keyword in ["2022", "2021", "2020", "crash", "historical", "bear market"]):
        return "crash_context"

    # Unclear
    return "unclear"


def is_unclear_question(message_text: str) -> bool:
    """
    Detect unclear or unsupported questions.

    Args:
        message_text: User's message text

    Returns:
        True if question is unclear or unsupported
    """
    message_lower = message_text.lower().strip()

    # Empty or very short
    if len(message_text) < 3:
        return True

    # Off-topic requests (investment advice)
    off_topic_keywords = ["price prediction", "investment advice", "buy", "sell", "trade", "moon", "wen"]
    if any(keyword in message_lower for keyword in off_topic_keywords):
        return True

    # Gibberish detection (no vowels)
    if not any(c in 'aeiou' for c in message_lower):
        return True

    return False


def generate_correlation_followup_response(correlation_analysis: dict, user_question: str) -> str:
    """
    Generate follow-up response for correlation questions.

    Args:
        correlation_analysis: Stored correlation analysis data
        user_question: User's follow-up question

    Returns:
        Formatted response text
    """
    correlation_pct = correlation_analysis.get('correlation_percentage', 0)
    interpretation = correlation_analysis.get('interpretation', 'unknown')

    # Build response with contextual reference
    response_parts = [
        f"As I mentioned, your portfolio has {correlation_pct}% correlation to ETH. "
        f"This is considered {interpretation} correlation.\n\n"
    ]

    # Add explanation based on question
    if "high" in user_question.lower() or "why" in user_question.lower():
        response_parts.append(
            "This means your portfolio moves very closely with Ethereum's price. "
            "When ETH drops, your portfolio typically drops by a similar percentage. "
        )

    # Add historical context if available
    historical_context = correlation_analysis.get('historical_context', [])
    if historical_context:
        crash = historical_context[0]
        response_parts.append(
            f"\n\nBased on historical data from {crash.get('crash_name', '2022 Bear Market')}:\n"
            f"- Portfolios with {correlation_pct}% correlation lost approximately {crash.get('portfolio_loss_pct', -75)}%\n"
            f"- Market average loss was {crash.get('market_avg_loss_pct', -55)}%\n"
        )

    # Add recommendation hint
    response_parts.append(
        "\n\nTo reduce correlation risk, consider adding uncorrelated assets like Bitcoin, "
        "Alternative Layer-1s, or Stablecoins to your portfolio."
    )

    return "".join(response_parts)


def generate_sector_followup_response(sector_analysis: dict, user_question: str) -> str:
    """
    Generate follow-up response for sector questions.

    Args:
        sector_analysis: Stored sector analysis data
        user_question: User's follow-up question

    Returns:
        Formatted response text
    """
    concentrated_sectors = sector_analysis.get('concentrated_sectors', [])

    if not concentrated_sectors:
        return "Building on the sector analysis, your portfolio has no significant sector concentration (all sectors <60%)."

    sector_name = concentrated_sectors[0]
    sector_breakdown = sector_analysis.get('sector_breakdown', {})
    sector_pct = 0

    if sector_name in sector_breakdown:
        sector_pct = sector_breakdown[sector_name].get('percentage', 0)

    # Build response with contextual reference
    response_parts = [
        f"Building on the sector analysis, your portfolio has {sector_pct:.0f}% "
        f"concentrated in {sector_name}.\n\n"
    ]

    # Add risk explanation
    response_parts.append(
        f"This concentration is risky because:\n"
    )

    # Add sector-specific risks if available
    sector_risks = sector_analysis.get('sector_risks', [])
    sector_risk = next(
        (risk for risk in sector_risks if risk.get('sector_name') == sector_name),
        None
    )

    if sector_risk:
        response_parts.append(
            f"- In {sector_risk.get('crash_scenario', '2022 Bear Market')}, "
            f"{sector_name} sector lost {sector_risk.get('sector_loss_pct', -75):.0f}%\n"
        )

        opportunity_cost = sector_risk.get('opportunity_cost')
        if opportunity_cost:
            response_parts.append(
                f"- You missed {opportunity_cost.get('recovery_gain_pct', 500):.0f}% recovery gains "
                f"during the rebound\n"
            )

    # Add recommendation hint
    response_parts.append(
        f"\n\nTo reduce sector risk, consider reducing {sector_name} concentration to below 40%."
    )

    return "".join(response_parts)


def generate_recommendation_followup_response(synthesis: dict, user_question: str) -> str:
    """
    Generate follow-up response for recommendation questions.

    Args:
        synthesis: Stored synthesis data with recommendations
        user_question: User's follow-up question

    Returns:
        Formatted response text
    """
    recommendations = synthesis.get('recommendations', [])

    if not recommendations:
        return "Based on your portfolio's risk profile, I recommend maintaining your current balanced structure."

    # Build response with context
    response_parts = [
        "Based on your portfolio's risk profile, here are my prioritized recommendations:\n\n"
    ]

    # Format recommendations with priority
    for idx, rec in enumerate(recommendations, 1):
        response_parts.append(
            f"{idx}. {rec.get('action', '')}\n"
            f"   - **Why:** {rec.get('rationale', '')}\n"
            f"   - **Expected Impact:** {rec.get('expected_impact', '')}\n\n"
        )

    # Add note about addressing user's concern if mentioned in question
    if "correlation" in user_question.lower():
        response_parts.append(
            "These recommendations specifically address your correlation risk concerns."
        )
    elif "sector" in user_question.lower() or "concentration" in user_question.lower():
        response_parts.append(
            "These recommendations specifically address your sector concentration concerns."
        )

    return "".join(response_parts)


def generate_crash_context_followup_response(correlation_analysis: dict, user_question: str) -> str:
    """
    Generate follow-up response for crash context questions.

    Args:
        correlation_analysis: Stored correlation analysis data
        user_question: User's follow-up question

    Returns:
        Formatted response text
    """
    historical_context = correlation_analysis.get('historical_context', [])

    if not historical_context:
        return (
            "I don't have specific historical crash data for your correlation level. "
            "Generally, high ETH correlation means your portfolio closely follows ETH's price movements."
        )

    # Build response with crash details
    response_parts = []

    for crash in historical_context:
        crash_name = crash.get('crash_name', '2022 Bear Market')
        crash_period = crash.get('crash_period', '2022-Q2')
        portfolio_loss = crash.get('portfolio_loss_pct', -75)
        market_avg_loss = crash.get('market_avg_loss_pct', -55)

        response_parts.append(
            f"**{crash_name}** ({crash_period}):\n"
            f"- Portfolios with your correlation level lost approximately {portfolio_loss:.0f}%\n"
            f"- Market average loss was {market_avg_loss:.0f}%\n"
            f"- Your portfolio would have underperformed the market by {abs(portfolio_loss - market_avg_loss):.0f}%\n\n"
        )

    response_parts.append(
        "This historical context shows why reducing correlation is important for portfolio resilience."
    )

    return "".join(response_parts)


def generate_clarification_response(conversation_state: dict | None) -> str:
    """
    Generate clarification prompt for unclear questions.

    Args:
        conversation_state: Current conversation state (if any)

    Returns:
        Clarification prompt text
    """
    if conversation_state and conversation_state.get('synthesis'):
        # User has existing analysis - suggest relevant follow-ups
        return (
            "I'm not sure I understood your question. Here are some things I can help with:\n\n"
            "- Explain correlation analysis: \"Why is my correlation high?\"\n"
            "- Explain sector concentration: \"Why is governance concentration risky?\"\n"
            "- Provide recommendations: \"What should I do about this risk?\"\n"
            "- Explain crash context: \"What happened in the 2022 crash?\"\n\n"
            "What would you like to know?"
        )
    else:
        # No existing analysis - prompt for wallet analysis
        return (
            "I'm not sure I understood your request. I specialize in portfolio risk analysis.\n\n"
            "To get started, please provide a wallet address to analyze:\n"
            "Example: \"Analyze wallet 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58\"\n\n"
            "I can help you understand correlation risks, sector concentration, and historical crash performance."
        )


def generate_offtopic_response() -> str:
    """
    Generate response for off-topic requests.

    Returns:
        Off-topic response text
    """
    return (
        "I specialize in portfolio risk analysis, not investment advice or price predictions.\n\n"
        "I can help you understand:\n"
        "- Your portfolio's correlation to ETH\n"
        "- Sector concentration risks\n"
        "- Historical crash performance\n"
        "- Risk reduction strategies\n\n"
        "Would you like to analyze a wallet address?"
    )


def format_combined_response(
    request_id: str,
    wallet_address: str,
    correlation_response: dict | None,
    sector_response: dict | None,
    synthesis: dict | None,
    total_time_ms: int
) -> str:
    """
    Format combined analysis response for user with full transparency (Story 2.5).

    This function implements Story 2.5 transparency requirements by:
    - Presenting specialist agent responses verbatim
    - Displaying agent addresses for verifiability
    - Showing per-agent timing information
    - Using clear section separators
    - Providing detailed error transparency when agents timeout

    Args:
        request_id: Request identifier
        wallet_address: Wallet address analyzed
        correlation_response: CorrelationAgent response data (or None)
        sector_response: SectorAgent response data (or None)
        synthesis: GuardianSynthesis dict (or None)
        total_time_ms: Total processing time in milliseconds

    Returns:
        Formatted narrative text for user with transparency features
    """
    print(
        f"Formatting Guardian response with transparency features. "
        f"correlation_response={'present' if correlation_response else 'None'}, "
        f"sector_response={'present' if sector_response else 'None'}"
    )

    lines = [
        "🛡️ Guardian Portfolio Risk Analysis\n",
        f"Wallet: {wallet_address}\n",
        f"Request ID: {request_id}\n",
        "\n"
    ]

    # CorrelationAgent Analysis Section
    if correlation_response:
        # Add truncated address to header for verifiability
        agent_addr = correlation_response.get('agent_address', 'N/A')
        truncated_addr = truncate_address(agent_addr)
        print(f"Truncating CorrelationAgent address: {agent_addr} -> {truncated_addr}")

        lines.append(f"🔗 CorrelationAgent Analysis ({truncated_addr}):\n\n")
        analysis_data = correlation_response.get("analysis_data", {})
        lines.append(f"{analysis_data.get('narrative', 'Analysis data unavailable')}\n")

        # Include historical crash context if available
        historical_context = analysis_data.get('historical_context', [])
        if historical_context:
            lines.append("\nHistorical Context:\n")
            for crash in historical_context:
                lines.append(
                    f"- {crash['crash_name']} ({crash['crash_period']}): "
                    f"Portfolios with similar correlation lost {crash['portfolio_loss_pct']:.1f}% "
                    f"(vs. {crash['market_avg_loss_pct']:.1f}% market average)\n"
                )

        # Display processing time prominently
        lines.append(f"\n(Processing: {correlation_response.get('processing_time_ms', 0)}ms)\n\n")

        # Add section separator
        lines.append("---\n\n")
    else:
        lines.append("🔗 CorrelationAgent Analysis:\n\n")
        # Enhanced error transparency - explain timeout clearly
        lines.append(
            f"⚠️ CorrelationAgent did not respond within {AGENT_RESPONSE_TIMEOUT} seconds (timeout). "
            "Proceeding with SectorAgent results only. Analysis may have reduced historical context.\n\n"
        )
        lines.append("---\n\n")
        print("ERROR: CorrelationAgent timeout - no response received within AGENT_RESPONSE_TIMEOUT")

    # SectorAgent Analysis Section
    if sector_response:
        # Add truncated address to header for verifiability
        agent_addr = sector_response.get('agent_address', 'N/A')
        truncated_addr = truncate_address(agent_addr)
        print(f"Truncating SectorAgent address: {agent_addr} -> {truncated_addr}")

        lines.append(f"🏛️ SectorAgent Analysis ({truncated_addr}):\n\n")
        analysis_data = sector_response.get("analysis_data", {})
        lines.append(f"{analysis_data.get('narrative', 'Analysis data unavailable')}\n")

        # Include sector breakdown
        sector_breakdown = analysis_data.get('sector_breakdown', {})
        if sector_breakdown:
            lines.append("\nSector Breakdown:\n")
            for sector_name, sector_data in sector_breakdown.items():
                lines.append(
                    f"- {sector_data['sector_name']}: {sector_data['percentage']:.1f}% "
                    f"(${sector_data['value_usd']:,.2f}) - "
                    f"{', '.join(sector_data['token_symbols'])}\n"
                )

        # Include sector risks if available
        sector_risks = analysis_data.get('sector_risks', [])
        if sector_risks:
            lines.append("\nHistorical Sector Risks:\n")
            for risk in sector_risks:
                lines.append(
                    f"- {risk['crash_scenario']}: {risk['sector_name']} sector lost "
                    f"{risk['sector_loss_pct']:.1f}% (vs. {risk['market_avg_loss_pct']:.1f}% market average)\n"
                )
                if risk.get('opportunity_cost'):
                    opp_cost = risk['opportunity_cost']
                    lines.append(f"  Opportunity Cost: {opp_cost['narrative']}\n")

        # Display processing time prominently
        lines.append(f"\n(Processing: {sector_response.get('processing_time_ms', 0)}ms)\n\n")

        # Add section separator
        lines.append("---\n\n")
    else:
        lines.append("🏛️ SectorAgent Analysis:\n\n")
        # Enhanced error transparency - explain timeout clearly
        lines.append(
            f"⚠️ SectorAgent did not respond within {AGENT_RESPONSE_TIMEOUT} seconds (timeout). "
            "Proceeding with CorrelationAgent results only. Analysis may be incomplete.\n\n"
        )
        lines.append("---\n\n")
        print("ERROR: SectorAgent timeout - no response received within AGENT_RESPONSE_TIMEOUT")

    # Guardian Synthesis Section (Story 2.3)
    if synthesis:
        lines.append("🔮 Guardian Synthesis:\n\n")
        lines.append(f"Risk Level: {synthesis.get('overall_risk_level', 'Unknown')}\n")
        lines.append(f"Compounding Risk Detected: {'Yes' if synthesis.get('compounding_risk_detected') else 'No'}\n\n")
        lines.append(f"{synthesis.get('synthesis_narrative', '')}\n\n")
        lines.append(f"Risk Multiplier Effect:\n{synthesis.get('risk_multiplier_effect', '')}\n\n")

        # Recommendations (Story 2.4)
        if synthesis.get('recommendations'):
            lines.append("📋 Recommendations:\n\n")
            for idx, rec in enumerate(synthesis['recommendations'], 1):
                lines.append(f"{idx}. {rec.get('action', '')}\n")
                lines.append(f"   - **Why:** {rec.get('rationale', '')}\n")
                lines.append(f"   - **Expected Impact:** {rec.get('expected_impact', '')}\n\n")

        # Add section separator after synthesis
        lines.append("---\n\n")
    else:
        if correlation_response and sector_response:
            # Both responses available but synthesis failed
            lines.append("🔮 Guardian Synthesis:\n\n")
            lines.append(
                "⚠️ Guardian synthesis encountered an error while combining agent insights. "
                "Individual agent analyses are available above.\n\n"
            )
            lines.append("---\n\n")
            print("ERROR: Guardian synthesis failed - displaying individual agent analyses only")

    # Enhanced Summary Section (Story 2.5 - Task 7)
    lines.append("⚙️ Agents Consulted:\n")
    if correlation_response:
        lines.append(
            f"- CorrelationAgent ({correlation_response.get('agent_address', 'N/A')}) - "
            f"{correlation_response.get('processing_time_ms', 0)}ms\n"
        )
    if sector_response:
        lines.append(
            f"- SectorAgent ({sector_response.get('agent_address', 'N/A')}) - "
            f"{sector_response.get('processing_time_ms', 0)}ms\n"
        )

    lines.append(f"\n⏱️ Total Analysis Time: {total_time_ms / 1000:.1f} seconds\n")

    return "".join(lines)


# =============================================================================
# AGENT INITIALIZATION
# =============================================================================

agent = Agent(
    name="guardian_agent_hosted",
    seed=GUARDIAN_AGENT_SEED,
)

# Create chat protocol for ASI1 LLM integration
chat_proto = Protocol(spec=chat_protocol_spec)

# Create structured output protocol for AI parameter extraction
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
    Handle incoming ChatMessage from ASI1 LLM with multi-turn support (Story 3.1).
    Detects follow-up questions and routes to appropriate response generation.
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
            # Clear conversation state on session end
            session_key = f"conversation_{ctx.session}"
            ctx.storage.set(session_key, None)
            ctx.logger.info(f"Session {ctx.session}: Cleared conversation state")
            continue

        elif isinstance(content, TextContent):
            user_message = content.text
            ctx.logger.info(f"💬 User query: {user_message}")

            # Store query text for potential regex fallback
            ctx.storage.set(f"query_{ctx.session}", user_message)

            # Check for existing conversation state (Story 3.1)
            conversation_state = get_conversation_state(ctx)

            # Check for unclear or off-topic questions (Story 3.1 - Error Recovery)
            if is_unclear_question(user_message):
                ctx.logger.info(f"Session {ctx.session}: Unclear question detected")

                # Check if this is an off-topic request
                if any(keyword in user_message.lower() for keyword in ["price prediction", "investment advice", "buy", "sell", "trade"]):
                    response_text = generate_offtopic_response()
                else:
                    response_text = generate_clarification_response(conversation_state)

                # Send clarification response
                clarification_msg = ChatMessage(
                    content=[TextContent(text=response_text)],
                    msg_id=uuid4(),
                    timestamp=datetime.now(timezone.utc)
                )
                await ctx.send(sender, clarification_msg)

                # Update conversation history if state exists
                if conversation_state:
                    update_conversation_state(ctx, conversation_state, user_message, response_text)

                return

            # Follow-up question handling (Story 3.1)
            if conversation_state:
                ctx.logger.info(f"Session {ctx.session}: Detected existing conversation state - checking for follow-up question")

                # Classify question type
                question_type = classify_follow_up_question(user_message)
                ctx.logger.info(f"Session {ctx.session}: Classified question as '{question_type}'")

                # Generate follow-up response if applicable
                followup_response = None

                if question_type == "correlation" and conversation_state.get('correlation_analysis'):
                    followup_response = generate_correlation_followup_response(
                        conversation_state['correlation_analysis'],
                        user_message
                    )
                elif question_type == "sector" and conversation_state.get('sector_analysis'):
                    followup_response = generate_sector_followup_response(
                        conversation_state['sector_analysis'],
                        user_message
                    )
                elif question_type == "recommendation" and conversation_state.get('synthesis'):
                    followup_response = generate_recommendation_followup_response(
                        conversation_state['synthesis'],
                        user_message
                    )
                elif question_type == "crash_context" and conversation_state.get('correlation_analysis'):
                    followup_response = generate_crash_context_followup_response(
                        conversation_state['correlation_analysis'],
                        user_message
                    )

                # Send follow-up response if generated
                if followup_response:
                    start_time = time.time()

                    followup_msg = ChatMessage(
                        content=[TextContent(text=followup_response)],
                        msg_id=uuid4(),
                        timestamp=datetime.now(timezone.utc)
                    )
                    await ctx.send(sender, followup_msg)

                    elapsed_ms = int((time.time() - start_time) * 1000)
                    ctx.logger.info(f"Session {ctx.session}: Generated follow-up response in {elapsed_ms}ms")

                    # Update conversation history
                    update_conversation_state(ctx, conversation_state, user_message, followup_response)

                    return

                # If not a follow-up or classification unclear, check for new wallet analysis request

            # Check if this is a new wallet analysis request (initial or follow-up)
            # Extract wallet address for analysis
            wallet_address_extracted = False

            # Forward to AI agent for structured parameter extraction
            try:
                await ctx.send(
                    AI_AGENT_ADDRESS,
                    StructuredOutputPrompt(
                        prompt=user_message,
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
                wallet_address_extracted = True
            except Exception as e:
                # AI agent unavailable - fall back to regex extraction
                ctx.logger.warning(f"⚠️ AI extraction failed: {e}, falling back to regex")
                wallet_address = extract_wallet_address_regex(user_message)

                if not wallet_address:
                    # No wallet address found - send context loss message
                    if conversation_state:
                        error_text = (
                            "I don't have your portfolio analysis in this session. "
                            "Please provide a wallet address to analyze.\n\n"
                            "Example: \"Analyze wallet 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58\""
                        )
                    else:
                        error_text = (
                            "Sorry, I couldn't find a valid Ethereum wallet address in your request. "
                            "Please provide a wallet address in the format: 0x... (40 hex characters)\n\n"
                            "(Note: AI parameter extraction is temporarily unavailable, using pattern matching)"
                        )

                    error_response = ChatMessage(
                        content=[TextContent(text=error_text)],
                        msg_id=uuid4(),
                        timestamp=datetime.now(timezone.utc)
                    )
                    await ctx.send(sender, error_response)
                    return

                # Continue with extracted wallet address
                ctx.logger.info(f"✅ Extracted via regex fallback: {wallet_address}")
                ctx.storage.set(f"fallback_wallet_{ctx.session}", wallet_address)


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
    Orchestrates analysis and sends result back to user.
    Implements regex fallback for AI rate limit scenarios.
    """
    session_sender = ctx.storage.get(str(ctx.session))

    if session_sender is None:
        ctx.logger.error("❌ No session sender found in storage")
        return

    # Check if AI couldn't extract parameters (rate limit or parsing failure)
    if "<UNKNOWN>" in str(msg.output):
        ctx.logger.warning("⚠️ AI extraction returned <UNKNOWN>, attempting regex fallback")

        # Try regex fallback using stored query text
        query_text = ctx.storage.get(f"query_{ctx.session}")
        if query_text:
            wallet_address = extract_wallet_address_regex(query_text)

            if wallet_address:
                ctx.logger.info(f"✅ Regex fallback successful: {wallet_address}")
                # Store for later use and continue with analysis
                ctx.storage.set(f"fallback_wallet_{ctx.session}", wallet_address)
                ctx.storage.set(f"ai_rate_limited_{ctx.session}", True)

                # Continue to analysis logic below (replace msg.output)
                msg.output = {"wallet_address": wallet_address}
            else:
                # No wallet address found even with regex
                error_response = ChatMessage(
                    content=[TextContent(
                        text="Sorry, I couldn't find a valid Ethereum wallet address in your request. "
                             "Please provide a wallet address in the format: 0x... (40 hex characters)\n\n"
                             "(Note: AI parameter extraction is temporarily unavailable)"
                    )],
                    msg_id=uuid4(),
                    timestamp=datetime.now(timezone.utc)
                )
                await ctx.send(session_sender, error_response)
                return
        else:
            # No query text stored
            error_response = ChatMessage(
                content=[TextContent(
                    text="Sorry, I couldn't find a valid Ethereum wallet address in your request. "
                         "Please provide a wallet address in the format: 0x... (40 hex characters)"
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

        # Load demo wallet data
        try:
            portfolio_data = load_demo_wallet_from_github(wallet_address)
        except ValueError as e:
            error_response = ChatMessage(
                content=[TextContent(
                    text=f"❌ {str(e)}\n\nThis is a demo version using pre-configured portfolios. "
                         f"Please use one of the available demo wallet addresses."
                )],
                msg_id=uuid4(),
                timestamp=datetime.now(timezone.utc)
            )
            await ctx.send(session_sender, error_response)
            return

        # Generate unique request ID
        request_id = str(uuid4())

        # Initialize or update conversation state (Story 3.1)
        conversation_state = get_conversation_state(ctx)
        if not conversation_state:
            conversation_state = init_conversation_state(
                session_id=str(ctx.session),
                wallet_address=wallet_address,
                portfolio_data=portfolio_data
            )
            session_key = f"conversation_{ctx.session}"
            ctx.storage.set(session_key, conversation_state)
            ctx.logger.info(f"Session {ctx.session}: Initialized new conversation state for wallet {wallet_address}")
        else:
            # Update existing state with new wallet data
            conversation_state["wallet_address"] = wallet_address
            conversation_state["portfolio_data"] = portfolio_data
            session_key = f"conversation_{ctx.session}"
            ctx.storage.set(session_key, conversation_state)
            ctx.logger.info(f"Session {ctx.session}: Updated conversation state with new wallet {wallet_address}")

        # Store analysis state
        ctx.storage.set(f"request_{request_id}_start_time", start_time)
        ctx.storage.set(f"request_{request_id}_wallet", wallet_address)

        # Store user message for conversation history
        user_query = ctx.storage.get(f"query_{ctx.session}")
        ctx.storage.set(f"request_{request_id}_user_message", user_query or f"Analyze wallet {wallet_address}")

        # Send analysis requests to specialist agents
        if CORRELATION_AGENT_ADDRESS:
            correlation_request = AnalysisRequest(
                request_id=request_id,
                wallet_address=wallet_address,
                portfolio_data=portfolio_data,
                requested_by=str(ctx.agent.address),
            )
            await ctx.send(CORRELATION_AGENT_ADDRESS, correlation_request)
            ctx.logger.info(f"📤 Sent AnalysisRequest to CorrelationAgent ({request_id})")
        else:
            ctx.logger.warning("⚠️ CORRELATION_AGENT_ADDRESS not configured")

        if SECTOR_AGENT_ADDRESS:
            sector_request = AnalysisRequest(
                request_id=request_id,
                wallet_address=wallet_address,
                portfolio_data=portfolio_data,
                requested_by=str(ctx.agent.address),
            )
            await ctx.send(SECTOR_AGENT_ADDRESS, sector_request)
            ctx.logger.info(f"📤 Sent AnalysisRequest to SectorAgent ({request_id})")
        else:
            ctx.logger.warning("⚠️ SECTOR_AGENT_ADDRESS not configured")

        # Note: Response aggregation happens in specialist agent response handlers

    except Exception as err:
        ctx.logger.error(f"❌ Error processing analysis: {err}")

        error_response = ChatMessage(
            content=[TextContent(
                text=f"Sorry, I encountered an error analyzing your portfolio: {str(err)}. "
                     f"Please try again or contact support."
            )],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, error_response)


# =============================================================================
# SPECIALIST AGENT RESPONSE HANDLERS
# =============================================================================

@agent.on_message(model=CorrelationAnalysisResponse)
async def handle_correlation_response(ctx: Context, sender: str, msg: CorrelationAnalysisResponse):
    """Handle response from CorrelationAgent."""
    ctx.logger.info(f"📥 Received CorrelationAnalysisResponse {msg.request_id} from {sender}")

    # Store response
    ctx.storage.set(f"correlation_{msg.request_id}", msg.dict())

    # Check if we have both responses (or timeout)
    await check_and_send_combined_response(ctx, msg.request_id)


@agent.on_message(model=SectorAnalysisResponse)
async def handle_sector_response(ctx: Context, sender: str, msg: SectorAnalysisResponse):
    """Handle response from SectorAgent."""
    ctx.logger.info(f"📥 Received SectorAnalysisResponse {msg.request_id} from {sender}")

    # Store response
    ctx.storage.set(f"sector_{msg.request_id}", msg.dict())

    # Check if we have both responses (or timeout)
    await check_and_send_combined_response(ctx, msg.request_id)


async def check_and_send_combined_response(ctx: Context, request_id: str):
    """
    Check if both specialist agent responses received, then send combined response.
    Also handles timeout scenarios.
    """
    # Check if already sent
    if ctx.storage.get(f"sent_{request_id}"):
        return

    # Get stored responses
    correlation_response = ctx.storage.get(f"correlation_{request_id}")
    sector_response = ctx.storage.get(f"sector_{request_id}")
    start_time = ctx.storage.get(f"request_{request_id}_start_time")
    wallet_address = ctx.storage.get(f"request_{request_id}_wallet")

    if start_time is None or wallet_address is None:
        ctx.logger.error(f"❌ Missing request metadata for {request_id}")
        return

    # Check if both responses received OR timeout exceeded
    elapsed_time = time.time() - start_time
    has_both = correlation_response is not None and sector_response is not None
    timeout_exceeded = elapsed_time >= AGENT_RESPONSE_TIMEOUT * 2  # Wait for both agents

    if not (has_both or timeout_exceeded):
        return  # Still waiting

    # Mark as sent
    ctx.storage.set(f"sent_{request_id}", True)

    # Calculate total time
    total_time_ms = int((time.time() - start_time) * 1000)

    # Perform synthesis analysis if both responses available
    synthesis = None
    if correlation_response and sector_response:
        try:
            synthesis = synthesis_analysis(
                correlation_response,
                sector_response,
                request_id=request_id
            )
            ctx.logger.info(f"Synthesis analysis complete for {request_id}")
        except Exception as e:
            ctx.logger.error(f"Synthesis analysis failed: {e}")
            # Continue without synthesis

    # Format combined response (includes synthesis if available)
    response_text = format_combined_response(
        request_id,
        wallet_address,
        correlation_response,
        sector_response,
        synthesis,
        total_time_ms
    )

    # Add AI rate limit notification if regex fallback was used
    if ctx.storage.get(f"ai_rate_limited_{ctx.session}"):
        response_text = (
            "ℹ️ Note: AI parameter extraction temporarily unavailable (rate limit), "
            "using pattern matching fallback.\n\n"
        ) + response_text
        # Clear the flag
        ctx.storage.set(f"ai_rate_limited_{ctx.session}", None)

    # Get session sender
    session_sender = ctx.storage.get(str(ctx.session))

    if session_sender is None:
        ctx.logger.error("❌ No session sender found")
        return

    # Send response via Chat Protocol
    chat_response = ChatMessage(
        content=[TextContent(text=response_text)],
        msg_id=uuid4(),
        timestamp=datetime.now(timezone.utc)
    )
    await ctx.send(session_sender, chat_response)
    ctx.logger.info(f"📤 Sent combined analysis to {session_sender} ({total_time_ms}ms)")

    # Update conversation state with analysis results (Story 3.1)
    conversation_state = get_conversation_state(ctx)
    if conversation_state:
        user_message = ctx.storage.get(f"request_{request_id}_user_message")
        if user_message:
            update_conversation_state(
                ctx,
                conversation_state,
                user_message,
                response_text,
                correlation_response,
                sector_response,
                synthesis
            )
            ctx.logger.info(f"Session {ctx.session}: Updated conversation state with analysis results")


# =============================================================================
# DIRECT MESSAGE HANDLER (Agent-to-Agent Communication)
# =============================================================================

@agent.on_message(model=AnalysisRequest)
async def handle_direct_analysis_request(ctx: Context, sender: str, msg: AnalysisRequest):
    """
    Handle direct AnalysisRequest from other agents.
    This enables agent-to-agent orchestration without Chat Protocol.
    """
    ctx.logger.info(f"📨 Received direct AnalysisRequest {msg.request_id} from {sender}")

    start_time = time.time()
    request_id = msg.request_id
    wallet_address = msg.wallet_address

    # Store request metadata
    ctx.storage.set(f"request_{request_id}_start_time", start_time)
    ctx.storage.set(f"request_{request_id}_wallet", wallet_address)
    ctx.storage.set(f"request_{request_id}_direct_sender", sender)

    # Send requests to specialist agents
    if CORRELATION_AGENT_ADDRESS:
        await ctx.send(CORRELATION_AGENT_ADDRESS, msg)
        ctx.logger.info("📤 Forwarded to CorrelationAgent")

    if SECTOR_AGENT_ADDRESS:
        await ctx.send(SECTOR_AGENT_ADDRESS, msg)
        ctx.logger.info("📤 Forwarded to SectorAgent")


# =============================================================================
# AGENT STARTUP
# =============================================================================

# Include protocols
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_proto)

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    """Log agent startup and configuration."""
    ctx.logger.info(f"🛡️ Guardian Agent Hosted started at {ctx.agent.address}")
    ctx.logger.info(f"   CorrelationAgent: {CORRELATION_AGENT_ADDRESS}")
    ctx.logger.info(f"   SectorAgent: {SECTOR_AGENT_ADDRESS}")
    ctx.logger.info(f"   AI Agent: {AI_AGENT_ADDRESS} ({AI_AGENT_CHOICE})")
    ctx.logger.info(f"   Timeout: {AGENT_RESPONSE_TIMEOUT}s")


if __name__ == "__main__":
    agent.run()
