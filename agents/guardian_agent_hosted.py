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


def generate_synthesis_narrative(
    correlation_analysis: dict,
    sector_analysis: dict,
    compounding_risk_detected: bool,
    crash_data: list
) -> str:
    """
    Generate synthesis narrative (pure Python).

    Args:
        correlation_analysis: Correlation analysis dict
        sector_analysis: Sector analysis dict
        compounding_risk_detected: Whether compounding risk detected
        crash_data: Historical crash data

    Returns:
        Cohesive narrative string
    """
    correlation_pct = correlation_analysis.get('correlation_percentage', 0)
    concentrated_sectors = sector_analysis.get('concentrated_sectors', [])

    if compounding_risk_detected:
        concentrated_sector = concentrated_sectors[0] if concentrated_sectors else "Unknown"
        sector_breakdown = sector_analysis.get('sector_breakdown', {})
        concentration_pct = 0

        if concentrated_sector in sector_breakdown:
            concentration_pct = sector_breakdown[concentrated_sector].get('percentage', 0)

        leverage = round(correlation_pct / 30.0, 1)

        narrative = (
            f"Your {correlation_pct}% ETH correlation + {concentration_pct:.0f}% "
            f"{concentrated_sector} concentration creates compounding risk. "
            f"This structure acts like {leverage}x leverage to ETH movements. "
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

        return narrative

    else:
        narrative = (
            f"Your {correlation_pct}% ETH correlation is manageable, "
            f"and no sector exceeds 30% concentration. "
            f"This balanced structure limits compounding risks. "
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


def format_combined_response(
    request_id: str,
    wallet_address: str,
    correlation_response: dict | None,
    sector_response: dict | None,
    synthesis: dict | None,
    total_time_ms: int
) -> str:
    """
    Format combined analysis response for user.

    Args:
        request_id: Request identifier
        wallet_address: Wallet address analyzed
        correlation_response: CorrelationAgent response data (or None)
        sector_response: SectorAgent response data (or None)
        synthesis: GuardianSynthesis dict (or None)
        total_time_ms: Total processing time in milliseconds

    Returns:
        Formatted narrative text for user
    """
    lines = [
        "🛡️ Guardian Portfolio Risk Analysis\n",
        f"Wallet: {wallet_address}\n",
        f"Request ID: {request_id}\n",
        "\n"
    ]

    # CorrelationAgent Analysis Section
    if correlation_response:
        lines.append("📊 CorrelationAgent Analysis:\n")
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

        lines.append(f"\n(Agent: {correlation_response.get('agent_address', 'N/A')}, "
                    f"Processing: {correlation_response.get('processing_time_ms', 0)}ms)\n\n")
    else:
        lines.append("📊 CorrelationAgent Analysis:\n")
        lines.append("⚠️ Correlation analysis unavailable (agent timeout)\n\n")

    # SectorAgent Analysis Section
    if sector_response:
        lines.append("🏛️ SectorAgent Analysis:\n")
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

        lines.append(f"\n(Agent: {sector_response.get('agent_address', 'N/A')}, "
                    f"Processing: {sector_response.get('processing_time_ms', 0)}ms)\n\n")
    else:
        lines.append("🏛️ SectorAgent Analysis:\n")
        lines.append("⚠️ Sector analysis unavailable (agent timeout)\n\n")

    # Guardian Synthesis Section (Story 2.3)
    if synthesis:
        lines.append("🔮 Guardian Synthesis:\n")
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
    else:
        if correlation_response and sector_response:
            lines.append("🔮 Guardian Synthesis:\n")
            lines.append("⚠️ Synthesis analysis unavailable (synthesis error)\n\n")

    # Summary section
    lines.append("⚙️ Agents Consulted:\n")
    if correlation_response:
        lines.append(f"- CorrelationAgent ({correlation_response.get('agent_address', 'N/A')})\n")
    if sector_response:
        lines.append(f"- SectorAgent ({sector_response.get('agent_address', 'N/A')})\n")

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

            # Store query text for potential regex fallback
            ctx.storage.set(f"query_{ctx.session}", content.text)

            # Forward to AI agent for structured parameter extraction
            try:
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
            except Exception as e:
                # AI agent unavailable - fall back to regex extraction
                ctx.logger.warning(f"⚠️ AI extraction failed: {e}, falling back to regex")
                wallet_address = extract_wallet_address_regex(content.text)

                if not wallet_address:
                    error_response = ChatMessage(
                        content=[TextContent(
                            text="Sorry, I couldn't find a valid Ethereum wallet address in your request. "
                                 "Please provide a wallet address in the format: 0x... (40 hex characters)\n\n"
                                 "(Note: AI parameter extraction is temporarily unavailable, using pattern matching)"
                        )],
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

        # Store analysis state
        ctx.storage.set(f"request_{request_id}_start_time", start_time)
        ctx.storage.set(f"request_{request_id}_wallet", wallet_address)

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
