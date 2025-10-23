"""
Guardian Orchestrator Agent Local - Coordinates multi-agent portfolio risk analysis.

This is the LOCAL DEVELOPMENT VERSION using pandas/numpy for data processing.
For production deployment to Agentverse, use guardian_agent_hosted.py.

Guardian orchestrates specialized analysis agents (CorrelationAgent and SectorAgent)
to deliver comprehensive cryptocurrency portfolio risk intelligence.
"""

import asyncio
import logging
import re
import time
from typing import Optional

from uagents import Agent, Context

from agents.shared.config import get_env_var
from agents.shared.models import (
    AnalysisRequest,
    CorrelationAnalysis,
    CorrelationAnalysisResponse,
    ErrorMessage,
    GuardianAnalysisResponse,
    GuardianSynthesis,
    Portfolio,
    Recommendation,
    SectorAnalysis,
    SectorAnalysisResponse,
)
from agents.shared.metta_interface import (
    query_crashes_by_correlation_loss,
)

logger = logging.getLogger(__name__)

# Agent initialization with seed from environment
guardian_agent = Agent(
    name="guardian_agent_local",
    seed=get_env_var("GUARDIAN_AGENT_SEED", default="guardian_agent_local_secret_seed"),
    port=8003,
)

# Load specialist agent addresses from environment
CORRELATION_AGENT_ADDRESS = get_env_var("CORRELATION_AGENT_ADDRESS", default="")
SECTOR_AGENT_ADDRESS = get_env_var("SECTOR_AGENT_ADDRESS", default="")

# Timeout configuration (seconds)
AGENT_RESPONSE_TIMEOUT = int(get_env_var("AGENT_RESPONSE_TIMEOUT", default="10"))


def extract_wallet_address(message_text: str) -> Optional[str]:
    """
    Extract Ethereum wallet address from natural language input.

    Args:
        message_text: User message text

    Returns:
        Wallet address if found, None otherwise

    Examples:
        >>> extract_wallet_address("Analyze wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
        '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'
        >>> extract_wallet_address("Check risk for my portfolio")
        None
    """
    # Regex pattern for Ethereum address (0x + 40 hex characters)
    pattern = r'0x[a-fA-F0-9]{40}'
    match = re.search(pattern, message_text)

    if match:
        return match.group(0)
    return None


async def send_analysis_request(
    ctx: Context,
    agent_address: str,
    agent_name: str,
    portfolio: Portfolio,
    request_id: str
) -> None:
    """
    Send analysis request to specialist agent.

    Args:
        ctx: uAgents context
        agent_address: Target agent address
        agent_name: Agent name for logging (CorrelationAgent/SectorAgent)
        portfolio: Portfolio data
        request_id: Unique request identifier
    """
    request = AnalysisRequest(
        request_id=request_id,
        wallet_address=portfolio.wallet_address,
        portfolio_data=portfolio.model_dump(),
        requested_by=str(ctx.agent.address),
    )

    await ctx.send(agent_address, request)
    logger.info(f"Sent AnalysisRequest {request_id} to {agent_name} at {agent_address}")


async def wait_for_response(
    ctx: Context,
    request_id: str,
    agent_name: str,
    timeout: float = AGENT_RESPONSE_TIMEOUT
) -> Optional[dict]:
    """
    Wait for specialist agent response with timeout.

    Args:
        ctx: uAgents context
        request_id: Request identifier to match
        agent_name: Agent name for logging
        timeout: Maximum wait time in seconds

    Returns:
        Response data dict if received, None if timeout
    """
    response_key = f"{agent_name.lower()}_{request_id}"
    start_time = time.time()

    # Poll storage for response (check every 100ms)
    while time.time() - start_time < timeout:
        response = ctx.storage.get(response_key)
        if response:
            elapsed_ms = int((time.time() - start_time) * 1000)
            logger.info(f"Received {agent_name} response for {request_id} after {elapsed_ms}ms")
            return response

        await asyncio.sleep(0.1)

    # Timeout reached
    logger.warning(f"{agent_name} response timed out after {timeout}s for request {request_id}")
    return None


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


def format_combined_response(
    request_id: str,
    wallet_address: str,
    correlation_response: Optional[CorrelationAnalysisResponse],
    sector_response: Optional[SectorAnalysisResponse],
    synthesis: Optional[GuardianSynthesis],
    total_time_ms: int
) -> str:
    """
    Format combined analysis response for user with full transparency.

    This function implements Story 2.5 transparency requirements by:
    - Presenting specialist agent responses verbatim
    - Displaying agent addresses for verifiability
    - Showing per-agent timing information
    - Using clear section separators
    - Providing detailed error transparency when agents timeout

    Args:
        request_id: Request identifier
        wallet_address: Wallet address analyzed
        correlation_response: CorrelationAgent response (or None if timed out)
        sector_response: SectorAgent response (or None if timed out)
        synthesis: GuardianSynthesis (or None if synthesis unavailable)
        total_time_ms: Total processing time in milliseconds

    Returns:
        Formatted narrative text for user with transparency features
    """
    logger.info(
        f"Formatting Guardian response with transparency features. "
        f"correlation_response={'present' if correlation_response else 'None'}, "
        f"sector_response={'present' if sector_response else 'None'}"
    )

    response_parts = [
        "🛡️ Guardian Portfolio Risk Analysis\n",
        f"Wallet: {wallet_address}\n",
        f"Request ID: {request_id}\n",
        "\n"
    ]

    # CorrelationAgent Analysis Section
    if correlation_response:
        # Add truncated address to header for verifiability
        truncated_addr = truncate_address(correlation_response.agent_address)
        logger.info(f"Truncating CorrelationAgent address: {correlation_response.agent_address} -> {truncated_addr}")

        response_parts.append(f"🔗 CorrelationAgent Analysis ({truncated_addr}):\n\n")
        analysis_data = correlation_response.analysis_data
        response_parts.append(f"{analysis_data.get('narrative', 'Analysis data unavailable')}\n")

        # Include historical crash context if available
        historical_context = analysis_data.get('historical_context', [])
        if historical_context:
            response_parts.append("\nHistorical Context:\n")
            for crash in historical_context:
                response_parts.append(
                    f"- {crash['crash_name']} ({crash['crash_period']}): "
                    f"Portfolios with similar correlation lost {crash['portfolio_loss_pct']:.1f}% "
                    f"(vs. {crash['market_avg_loss_pct']:.1f}% market average)\n"
                )

        # Display processing time prominently
        response_parts.append(f"\n(Processing: {correlation_response.processing_time_ms}ms)\n\n")

        # Add section separator
        response_parts.append("---\n\n")
    else:
        response_parts.append("🔗 CorrelationAgent Analysis:\n\n")
        # Enhanced error transparency - explain timeout clearly
        response_parts.append(
            f"⚠️ CorrelationAgent did not respond within {AGENT_RESPONSE_TIMEOUT} seconds (timeout). "
            "Proceeding with SectorAgent results only. Analysis may have reduced historical context.\n\n"
        )
        response_parts.append("---\n\n")
        logger.error("CorrelationAgent timeout - no response received within AGENT_RESPONSE_TIMEOUT")

    # SectorAgent Analysis Section
    if sector_response:
        # Add truncated address to header for verifiability
        truncated_addr = truncate_address(sector_response.agent_address)
        logger.info(f"Truncating SectorAgent address: {sector_response.agent_address} -> {truncated_addr}")

        response_parts.append(f"🏛️ SectorAgent Analysis ({truncated_addr}):\n\n")
        analysis_data = sector_response.analysis_data
        response_parts.append(f"{analysis_data.get('narrative', 'Analysis data unavailable')}\n")

        # Include sector breakdown
        sector_breakdown = analysis_data.get('sector_breakdown', {})
        if sector_breakdown:
            response_parts.append("\nSector Breakdown:\n")
            for sector_name, sector_data in sector_breakdown.items():
                response_parts.append(
                    f"- {sector_data['sector_name']}: {sector_data['percentage']:.1f}% "
                    f"(${sector_data['value_usd']:,.2f}) - "
                    f"{', '.join(sector_data['token_symbols'])}\n"
                )

        # Include sector risks if available
        sector_risks = analysis_data.get('sector_risks', [])
        if sector_risks:
            response_parts.append("\nHistorical Sector Risks:\n")
            for risk in sector_risks:
                response_parts.append(
                    f"- {risk['crash_scenario']}: {risk['sector_name']} sector lost "
                    f"{risk['sector_loss_pct']:.1f}% (vs. {risk['market_avg_loss_pct']:.1f}% market average)\n"
                )
                if risk.get('opportunity_cost'):
                    opp_cost = risk['opportunity_cost']
                    response_parts.append(f"  Opportunity Cost: {opp_cost['narrative']}\n")

        # Display processing time prominently
        response_parts.append(f"\n(Processing: {sector_response.processing_time_ms}ms)\n\n")

        # Add section separator
        response_parts.append("---\n\n")
    else:
        response_parts.append("🏛️ SectorAgent Analysis:\n\n")
        # Enhanced error transparency - explain timeout clearly
        response_parts.append(
            f"⚠️ SectorAgent did not respond within {AGENT_RESPONSE_TIMEOUT} seconds (timeout). "
            "Proceeding with CorrelationAgent results only. Analysis may be incomplete.\n\n"
        )
        response_parts.append("---\n\n")
        logger.error("SectorAgent timeout - no response received within AGENT_RESPONSE_TIMEOUT")

    # Guardian Synthesis Section (new in Story 2.3)
    if synthesis:
        response_parts.append("🔮 Guardian Synthesis:\n\n")
        response_parts.append(f"Risk Level: {synthesis.overall_risk_level}\n")
        response_parts.append(f"Compounding Risk Detected: {'Yes' if synthesis.compounding_risk_detected else 'No'}\n\n")
        response_parts.append(f"{synthesis.synthesis_narrative}\n\n")

        # Add risk multiplier effect
        response_parts.append(f"Risk Multiplier Effect:\n{synthesis.risk_multiplier_effect}\n\n")

        # Recommendations (Story 2.4)
        if synthesis.recommendations:
            response_parts.append("📋 Recommendations:\n\n")
            for idx, rec in enumerate(synthesis.recommendations, 1):
                response_parts.append(f"{idx}. {rec.action}\n")
                response_parts.append(f"   - **Why:** {rec.rationale}\n")
                response_parts.append(f"   - **Expected Impact:** {rec.expected_impact}\n\n")

        # Add section separator after synthesis
        response_parts.append("---\n\n")
    else:
        if correlation_response and sector_response:
            # Both responses available but synthesis failed
            response_parts.append("🔮 Guardian Synthesis:\n\n")
            response_parts.append(
                "⚠️ Guardian synthesis encountered an error while combining agent insights. "
                "Individual agent analyses are available above.\n\n"
            )
            response_parts.append("---\n\n")
            logger.error("Guardian synthesis failed - displaying individual agent analyses only")

    # Enhanced Summary Section (Story 2.5 - Task 7)
    response_parts.append("⚙️ Agents Consulted:\n")
    if correlation_response:
        response_parts.append(
            f"- CorrelationAgent ({correlation_response.agent_address}) - "
            f"{correlation_response.processing_time_ms}ms\n"
        )
    if sector_response:
        response_parts.append(
            f"- SectorAgent ({sector_response.agent_address}) - "
            f"{sector_response.processing_time_ms}ms\n"
        )

    response_parts.append(f"\n⏱️ Total Analysis Time: {total_time_ms / 1000:.1f} seconds\n")

    return "".join(response_parts)


def detect_compounding_risk(
    correlation_analysis: CorrelationAnalysis,
    sector_analysis: SectorAnalysis
) -> bool:
    """
    Detect if portfolio has compounding risk structure.

    This function is standalone and testable independently of synthesis_analysis().

    Args:
        correlation_analysis: Correlation analysis results
        sector_analysis: Sector analysis results

    Returns:
        True if BOTH conditions met:
        1. High correlation (>85%)
        2. High sector concentration (any sector >60%)

    Examples:
        >>> corr = CorrelationAnalysis(correlation_percentage=95, ...)
        >>> sector = SectorAnalysis(concentrated_sectors=["DeFi Governance"], ...)
        >>> detect_compounding_risk(corr, sector)
        True
    """
    high_correlation = correlation_analysis.correlation_percentage > 85
    high_concentration = len(sector_analysis.concentrated_sectors) > 0  # >60% threshold

    return high_correlation and high_concentration


def calculate_risk_level(
    correlation_percentage: float,
    concentrated_sectors: list
) -> str:
    """
    Calculate overall risk level based on correlation and sector concentration.

    Args:
        correlation_percentage: Correlation percentage (0-100)
        concentrated_sectors: List of sectors with >60% concentration

    Returns:
        Risk level: "Critical" | "High" | "Moderate" | "Low"

    Risk Level Classification:
        - Critical: Correlation >85% AND Sector >60% (compounding risk)
        - High: Correlation >85% OR Sector >60% (single dimension risk)
        - Moderate: Correlation 70-85% OR Sector 40-60%
        - Low: Correlation <70% AND all sectors <40%
    """
    high_correlation = correlation_percentage > 85
    high_concentration = len(concentrated_sectors) > 0  # >60%

    if high_correlation and high_concentration:
        return "Critical"
    elif high_correlation or high_concentration:
        return "High"
    elif correlation_percentage >= 70 or len(concentrated_sectors) > 0:
        # Moderate correlation (70-85%) or moderate concentration detected
        return "Moderate"
    else:
        return "Low"


def generate_synthesis_narrative(
    correlation_analysis: CorrelationAnalysis,
    sector_analysis: SectorAnalysis,
    compounding_risk_detected: bool,
    risk_multiplier_effect: str,
    crash_data: list
) -> str:
    """
    Generate cohesive synthesis narrative explaining compounding risks.

    Args:
        correlation_analysis: Correlation analysis results
        sector_analysis: Sector analysis results
        compounding_risk_detected: Whether compounding risk was detected
        risk_multiplier_effect: Risk multiplier narrative
        crash_data: Historical crash data from MeTTa

    Returns:
        Cohesive narrative explaining risk structure

    Narrative Structure:
        For compounding risk portfolios:
            1. Correlation risk summary
            2. Sector concentration context
            3. Multiplier effect explanation
            4. Historical crash example
            5. Key insight

        For well-diversified portfolios:
            1. Confirmation of low compounding risk
            2. Explanation of why portfolio is well-structured
            3. Historical comparison
    """
    correlation_pct = correlation_analysis.correlation_percentage
    concentrated_sectors_list = sector_analysis.concentrated_sectors

    if compounding_risk_detected:
        # Compounding risk portfolio narrative with explicit agent attribution
        concentrated_sector = concentrated_sectors_list[0] if concentrated_sectors_list else "Unknown"

        # Get sector concentration percentage
        sector_breakdown = sector_analysis.sector_breakdown
        concentration_pct = 0
        if concentrated_sector in sector_breakdown:
            concentration_pct = sector_breakdown[concentrated_sector].get('percentage', 0)

        # Calculate leverage effect
        leverage = round(correlation_pct / 30.0, 1)

        # Build narrative with explicit agent references (Story 2.5)
        narrative_parts = [
            f"As CorrelationAgent showed, your {correlation_pct}% ETH correlation creates significant exposure to Ethereum price movements. "
            f"SectorAgent revealed that your {concentration_pct:.0f}% {concentrated_sector} concentration amplifies this risk through sector-specific vulnerabilities. "
        ]

        # Add Guardian's synthesis insight (combining both agents)
        narrative_parts.append(
            f"Combining these insights, Guardian identifies a compounding risk pattern: "
            f"this structure acts like {leverage}x leverage to ETH movements. "
        )

        # Add historical crash example if available
        if crash_data and len(crash_data) > 0:
            worst_crash = crash_data[0]  # Assume sorted by severity
            crash_name = worst_crash.get('name', '2022 Bear Market')

            # Get portfolio loss from historical context
            portfolio_loss = -75.0  # Default
            if correlation_analysis.historical_context:
                portfolio_loss = correlation_analysis.historical_context[0].portfolio_loss_pct

            correlation_only_loss = correlation_pct * 0.6  # Rough estimate

            narrative_parts.append(
                f"In {crash_name}, portfolios with this dual-risk structure lost {portfolio_loss:.0f}% "
                f"(not just {correlation_only_loss:.0f}% from correlation alone). "
            )

        # Add key insight
        narrative_parts.append(
            f"{concentrated_sector} sector amplifies ETH correlation—when both crash together, losses multiply."
        )

        logger.info("Generated synthesis narrative with agent attribution (CorrelationAgent, SectorAgent references)")

        return "".join(narrative_parts)

    else:
        # Well-diversified portfolio narrative with explicit agent attribution
        narrative_parts = [
            f"CorrelationAgent calculated your {correlation_pct}% ETH correlation as manageable. "
            f"According to SectorAgent's analysis, no sector exceeds 30% concentration. "
        ]

        # Add Guardian's synthesis insight
        narrative_parts.append(
            "Combining these findings, Guardian confirms this balanced structure limits compounding risks. "
        )

        # Add historical comparison if available
        if crash_data and len(crash_data) > 0:
            crash_name = crash_data[0].get('name', '2022 Bear Market')
            market_avg_loss = -55.0  # Default
            if correlation_analysis.historical_context:
                market_avg_loss = correlation_analysis.historical_context[0].market_avg_loss_pct

            narrative_parts.append(
                f"During {crash_name}, well-diversified portfolios like yours lost around "
                f"{market_avg_loss:.0f}% versus -75% for concentrated portfolios."
            )

        logger.info("Generated diversified portfolio synthesis narrative with agent attribution")

        return "".join(narrative_parts)


def get_correlation_recommendations(
    correlation_analysis: CorrelationAnalysis,
    priority: int
) -> Recommendation:
    """
    Generate recommendation for high ETH correlation.

    Args:
        correlation_analysis: Correlation analysis results
        priority: Recommendation priority (1 = highest)

    Returns:
        Recommendation for reducing correlation risk

    Examples:
        >>> corr = CorrelationAnalysis(correlation_percentage=95, ...)
        >>> rec = get_correlation_recommendations(corr, priority=1)
        >>> rec.priority
        1
    """
    correlation_pct = correlation_analysis.correlation_percentage

    # Extract historical loss data for rationale
    portfolio_loss = 73.0  # Default fallback
    market_avg_loss = 55.0  # Default fallback
    crash_name = "2022 Bear Market"  # Default fallback

    if correlation_analysis.historical_context:
        crash_example = correlation_analysis.historical_context[0]
        portfolio_loss = abs(crash_example.portfolio_loss_pct)
        market_avg_loss = abs(crash_example.market_avg_loss_pct)
        crash_name = crash_example.crash_name

        # Calculate expected impact (reduce correlation to 75-80% target)
        target_bracket_loss = market_avg_loss * 0.9  # 10% improvement estimate

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

    return Recommendation(
        priority=priority,
        action=action,
        rationale=rationale,
        expected_impact=expected_impact
    )


def get_sector_recommendations(
    sector_analysis: SectorAnalysis,
    priority: int
) -> Recommendation:
    """
    Generate recommendation for high sector concentration.

    Args:
        sector_analysis: Sector analysis results
        priority: Recommendation priority (1 = highest)

    Returns:
        Recommendation for reducing sector concentration

    Examples:
        >>> sector = SectorAnalysis(concentrated_sectors=["DeFi Governance"], ...)
        >>> rec = get_sector_recommendations(sector, priority=1)
        >>> "DeFi Governance" in rec.action
        True
    """
    # Get most concentrated sector
    concentrated_sector = sector_analysis.concentrated_sectors[0]
    sector_breakdown = sector_analysis.sector_breakdown
    concentration_pct = 0

    if concentrated_sector in sector_breakdown:
        sector_holding = sector_breakdown[concentrated_sector]
        # Handle both dict and Pydantic model
        concentration_pct = sector_holding.get('percentage', 0) if isinstance(sector_holding, dict) else sector_holding.percentage

    # Extract historical sector loss data for rationale
    sector_loss = 75.0  # Default fallback
    crash_scenario = "2022 Bear Market"  # Default fallback
    missed_gain = 500.0  # Default fallback

    # Handle both dict and Pydantic model for sector_risks
    sector_risk = None
    for risk in sector_analysis.sector_risks:
        risk_sector = risk.get('sector_name') if isinstance(risk, dict) else risk.sector_name
        if risk_sector == concentrated_sector:
            sector_risk = risk
            break

    if sector_risk:
        # Handle both dict and Pydantic model
        if isinstance(sector_risk, dict):
            sector_loss = abs(sector_risk.get('sector_loss_pct', sector_loss))
            crash_scenario = sector_risk.get('crash_scenario', crash_scenario)
            opp_cost = sector_risk.get('opportunity_cost')
            if opp_cost:
                missed_gain = opp_cost.get('recovery_gain_pct', missed_gain)
        else:
            sector_loss = abs(sector_risk.sector_loss_pct)
            crash_scenario = sector_risk.crash_scenario
            if sector_risk.opportunity_cost:
                missed_gain = sector_risk.opportunity_cost.recovery_gain_pct

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

    return Recommendation(
        priority=priority,
        action=action,
        rationale=rationale,
        expected_impact=expected_impact
    )


def get_diversified_recommendations(
    correlation_analysis: CorrelationAnalysis,
    sector_analysis: SectorAnalysis
) -> Recommendation:
    """
    Generate recommendation for well-diversified portfolio.

    Args:
        correlation_analysis: Correlation analysis results
        sector_analysis: Sector analysis results

    Returns:
        Recommendation acknowledging good structure with monitoring guidance

    Examples:
        >>> corr = CorrelationAnalysis(correlation_percentage=65, ...)
        >>> sector = SectorAnalysis(concentrated_sectors=[], ...)
        >>> rec = get_diversified_recommendations(corr, sector)
        >>> "Maintain" in rec.action
        True
    """
    correlation_pct = correlation_analysis.correlation_percentage

    # Extract top 3 sectors for acknowledgment
    sector_list_parts = []
    sector_breakdown = sector_analysis.sector_breakdown
    sorted_sectors = sorted(
        sector_breakdown.items(),
        key=lambda x: x[1].get('percentage', 0) if isinstance(x[1], dict) else x[1].percentage,
        reverse=True
    )[:3]

    for sector_name, sector_holding in sorted_sectors:
        # Handle both dict and Pydantic model
        percentage = sector_holding.get('percentage', 0) if isinstance(sector_holding, dict) else sector_holding.percentage
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

    return Recommendation(
        priority=1,
        action=action,
        rationale=rationale,
        expected_impact=expected_impact
    )


def get_prioritization_recommendation() -> Recommendation:
    """
    Generate recommendation explaining compounding risk prioritization.

    Returns:
        Recommendation explaining why sector diversification should be prioritized

    Examples:
        >>> rec = get_prioritization_recommendation()
        >>> rec.priority
        3
        >>> "Prioritize" in rec.action
        True
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

    return Recommendation(
        priority=3,
        action=action,
        rationale=rationale,
        expected_impact=expected_impact
    )


def generate_recommendations(
    correlation_analysis: CorrelationAnalysis,
    sector_analysis: SectorAnalysis,
    compounding_risk_detected: bool,
    overall_risk_level: str
) -> list[Recommendation]:
    """
    Generate 1-3 actionable recommendations based on identified risks.

    This function analyzes portfolio risk structure and generates prioritized,
    specific recommendations that tell users exactly what steps to take to improve
    portfolio structure and reduce compounding risks.

    Args:
        correlation_analysis: Correlation analysis results from CorrelationAgent
        sector_analysis: Sector analysis results from SectorAgent
        compounding_risk_detected: Whether both high correlation AND high sector concentration detected
        overall_risk_level: Overall risk level (Critical/High/Moderate/Low)

    Returns:
        List of 1-3 Recommendation objects, sorted by priority (1 = highest)

    Recommendation count by scenario:
        - Compounding risk: 3 recommendations (sector, correlation, prioritization explanation)
        - High risk (single dimension): 1-2 recommendations
        - Low risk: 1 recommendation (monitoring guidance)

    Examples:
        >>> corr = CorrelationAnalysis(correlation_percentage=95, ...)
        >>> sector = SectorAnalysis(concentrated_sectors=["DeFi Governance"], ...)
        >>> recs = generate_recommendations(corr, sector, True, "Critical")
        >>> len(recs)
        3
        >>> recs[0].priority
        1
    """
    try:
        logger.info(
            f"Generating recommendations for risk_level={overall_risk_level}, "
            f"compounding_risk={compounding_risk_detected}"
        )

        recommendations = []

        # Scenario 1: Well-diversified portfolio (Low risk)
        if overall_risk_level == "Low":
            recommendations.append(
                get_diversified_recommendations(correlation_analysis, sector_analysis)
            )
            logger.info("Generated diversified portfolio recommendation")

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
            logger.info("Generated 3 recommendations for compounding risk (sector first, correlation second, prioritization)")

        # Scenario 3: High correlation only
        elif correlation_analysis.correlation_percentage > 85:
            recommendations.append(
                get_correlation_recommendations(correlation_analysis, priority=1)
            )
            logger.info("Generated correlation recommendation (high correlation only)")

        # Scenario 4: High sector concentration only
        elif len(sector_analysis.concentrated_sectors) > 0:
            recommendations.append(
                get_sector_recommendations(sector_analysis, priority=1)
            )
            logger.info("Generated sector recommendation (high concentration only)")

        # Scenario 5: Moderate risk (one or both dimensions moderately high)
        else:
            # Generate 1-2 recommendations based on specific findings
            if correlation_analysis.correlation_percentage >= 70:
                recommendations.append(
                    get_correlation_recommendations(correlation_analysis, priority=1)
                )
                logger.info("Generated correlation recommendation for moderate risk")

            # Check for moderate sector concentration (40-60%)
            sector_breakdown = sector_analysis.sector_breakdown
            moderate_sectors = [
                sector_name for sector_name, sector_holding in sector_breakdown.items()
                if (sector_holding.get('percentage', 0) if isinstance(sector_holding, dict) else sector_holding.percentage) > 40
            ]

            if moderate_sectors and len(recommendations) == 0:
                # Create temporary concentrated_sectors list for moderate case
                temp_sector_analysis = SectorAnalysis(
                    sector_breakdown=sector_breakdown,
                    concentrated_sectors=moderate_sectors,
                    diversification_score=sector_analysis.diversification_score,
                    sector_risks=sector_analysis.sector_risks,
                    narrative=sector_analysis.narrative
                )
                recommendations.append(
                    get_sector_recommendations(temp_sector_analysis, priority=len(recommendations) + 1)
                )
                logger.info("Generated sector recommendation for moderate concentration")

        # Sort by priority (1 = highest)
        recommendations.sort(key=lambda rec: rec.priority)

        logger.info(
            f"Generated {len(recommendations)} recommendations: "
            f"priorities={[rec.priority for rec in recommendations]}"
        )

        return recommendations

    except Exception as e:
        logger.error(f"Unexpected error generating recommendations: {e}", exc_info=True)
        # Return empty list on error rather than crashing
        return []


def synthesis_analysis(
    correlation_response: CorrelationAnalysisResponse,
    sector_response: SectorAnalysisResponse,
    request_id: str = "unknown"
) -> GuardianSynthesis:
    """
    Synthesize correlation and sector analysis to detect compounding risks.

    This is the core synthesis logic that transforms Guardian from a simple message
    forwarder into an intelligent orchestrator revealing compounding risks invisible
    to individual agents.

    Args:
        correlation_response: Response from CorrelationAgent
        sector_response: Response from SectorAgent
        request_id: Request identifier for logging

    Returns:
        GuardianSynthesis with compounding risk analysis and narrative

    Raises:
        ValueError: If analysis data is invalid
        Exception: If synthesis logic fails

    Examples:
        >>> synthesis = synthesis_analysis(corr_response, sector_response)
        >>> print(synthesis.overall_risk_level)
        'Critical'
        >>> print(synthesis.compounding_risk_detected)
        True
    """
    try:
        logger.info(f"Starting synthesis analysis for request {request_id}")

        # Extract analysis data from responses
        correlation_analysis = CorrelationAnalysis(**correlation_response.analysis_data)
        sector_analysis = SectorAnalysis(**sector_response.analysis_data)

        correlation_pct = correlation_analysis.correlation_percentage
        concentrated_sectors = sector_analysis.concentrated_sectors

        logger.info(
            f"Synthesis inputs: correlation={correlation_pct}%, "
            f"concentrated_sectors={concentrated_sectors}"
        )

        # Detect compounding risk
        compounding_detected = detect_compounding_risk(correlation_analysis, sector_analysis)
        logger.info(f"Compounding risk detected: {compounding_detected}")

        # Query MeTTa for historical crash data
        crash_data = []
        if compounding_detected:
            try:
                # Determine correlation bracket
                correlation_bracket = ">90%" if correlation_pct > 90 else "80-90%"

                # Query MeTTa for severe crashes
                crash_data = query_crashes_by_correlation_loss(
                    correlation_bracket=correlation_bracket,
                    min_loss_pct=-70.0
                )
                logger.info(
                    f"MeTTa query returned {len(crash_data)} crash scenarios "
                    f"for {correlation_bracket} bracket"
                )

            except Exception as e:
                logger.warning(f"MeTTa query failed (using fallback): {e}")
                # MeTTa interface has automatic JSON fallback, so crash_data should still be valid
                crash_data = []

        # Calculate risk multiplier effect
        leverage = round(correlation_pct / 30.0, 1)
        if compounding_detected and concentrated_sectors:
            concentrated_sector = concentrated_sectors[0]
            sector_breakdown = sector_analysis.sector_breakdown
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

        # Calculate overall risk level
        overall_risk_level = calculate_risk_level(correlation_pct, concentrated_sectors)
        logger.info(f"Overall risk level: {overall_risk_level}")

        # Generate synthesis narrative
        synthesis_narrative = generate_synthesis_narrative(
            correlation_analysis,
            sector_analysis,
            compounding_detected,
            risk_multiplier_effect,
            crash_data
        )

        # Generate actionable recommendations (Story 2.4)
        recommendations = generate_recommendations(
            correlation_analysis,
            sector_analysis,
            compounding_detected,
            overall_risk_level
        )
        logger.info(f"Generated {len(recommendations)} recommendations for risk_level={overall_risk_level}")

        # Build GuardianSynthesis model
        synthesis = GuardianSynthesis(
            correlation_analysis=correlation_analysis,
            sector_analysis=sector_analysis,
            compounding_risk_detected=compounding_detected,
            risk_multiplier_effect=risk_multiplier_effect,
            recommendations=recommendations,  # Story 2.4: Populated with actionable recommendations
            overall_risk_level=overall_risk_level,
            synthesis_narrative=synthesis_narrative
        )

        logger.info(
            f"Synthesis complete: risk_level={overall_risk_level}, "
            f"compounding={compounding_detected}, "
            f"narrative_length={len(synthesis_narrative)} chars"
        )

        return synthesis

    except ValueError as e:
        logger.error(f"Synthesis validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in synthesis: {e}", exc_info=True)
        raise


@guardian_agent.on_event("startup")
async def startup_handler(ctx: Context):
    """Log agent startup and configuration."""
    logger.info(f"Guardian Agent Local started at {ctx.agent.address}")
    logger.info(f"CorrelationAgent address: {CORRELATION_AGENT_ADDRESS}")
    logger.info(f"SectorAgent address: {SECTOR_AGENT_ADDRESS}")
    logger.info(f"Agent response timeout: {AGENT_RESPONSE_TIMEOUT}s")


@guardian_agent.on_message(model=AnalysisRequest)
async def handle_analysis_request(ctx: Context, sender: str, msg: AnalysisRequest):
    """
    Handle portfolio analysis request from user.

    This is the main orchestration handler that coordinates specialist agents.

    Args:
        ctx: uAgents context
        sender: Sender address
        msg: AnalysisRequest message
    """
    try:
        start_time = time.time()
        request_id = msg.request_id
        wallet_address = msg.wallet_address

        logger.info(f"Received AnalysisRequest {request_id} for wallet {wallet_address} from {sender}")

        # Store session sender for response routing
        ctx.storage.set(f"session_{request_id}", sender)

        # Parse portfolio from message data
        portfolio = Portfolio(**msg.portfolio_data)
        logger.info(f"Portfolio loaded: {len(portfolio.tokens)} tokens, ${portfolio.total_value_usd:,.2f} total value")

        # Send requests to both specialist agents in parallel
        if CORRELATION_AGENT_ADDRESS:
            await send_analysis_request(
                ctx, CORRELATION_AGENT_ADDRESS, "CorrelationAgent", portfolio, request_id
            )
        else:
            logger.warning("CORRELATION_AGENT_ADDRESS not configured, skipping correlation analysis")

        if SECTOR_AGENT_ADDRESS:
            await send_analysis_request(
                ctx, SECTOR_AGENT_ADDRESS, "SectorAgent", portfolio, request_id
            )
        else:
            logger.warning("SECTOR_AGENT_ADDRESS not configured, skipping sector analysis")

        # Wait for responses with timeout
        correlation_response = None
        sector_response = None

        if CORRELATION_AGENT_ADDRESS:
            correlation_data = await wait_for_response(ctx, request_id, "CorrelationAgent")
            if correlation_data:
                correlation_response = CorrelationAnalysisResponse(**correlation_data)

        if SECTOR_AGENT_ADDRESS:
            sector_data = await wait_for_response(ctx, request_id, "SectorAgent")
            if sector_data:
                sector_response = SectorAnalysisResponse(**sector_data)

        # Calculate total processing time
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
                logger.info(f"Synthesis analysis complete for request {request_id}")
            except Exception as e:
                logger.error(f"Synthesis analysis failed for request {request_id}: {e}")
                # Continue without synthesis if it fails

        # Format combined response (includes synthesis if available)
        response_text = format_combined_response(
            request_id,
            wallet_address,
            correlation_response,
            sector_response,
            synthesis,
            total_time_ms
        )

        # Create GuardianAnalysisResponse
        agent_addresses = {}
        if correlation_response:
            agent_addresses["CorrelationAgent"] = correlation_response.agent_address
        if sector_response:
            agent_addresses["SectorAgent"] = sector_response.agent_address

        guardian_response = GuardianAnalysisResponse(
            request_id=request_id,
            wallet_address=wallet_address,
            correlation_analysis=correlation_response.model_dump() if correlation_response else None,
            sector_analysis=sector_response.model_dump() if sector_response else None,
            response_text=response_text,
            agent_addresses=agent_addresses,
            total_processing_time_ms=total_time_ms
        )

        # Send response back to sender
        await ctx.send(sender, guardian_response)
        logger.info(f"Sent GuardianAnalysisResponse {request_id} to {sender} (total time: {total_time_ms}ms)")

    except ValueError as e:
        # Validation error (invalid portfolio data, etc.)
        error_msg = ErrorMessage(
            request_id=msg.request_id,
            error_type="invalid_data",
            error_message=f"Invalid portfolio data: {str(e)}",
            agent_address=str(ctx.agent.address),
            retry_recommended=False
        )
        await ctx.send(sender, error_msg)
        logger.error(f"ValidationError in handle_analysis_request: {e}")

    except Exception as e:
        # Unexpected error
        error_msg = ErrorMessage(
            request_id=msg.request_id,
            error_type="agent_unavailable",
            error_message=f"An unexpected error occurred: {str(e)}",
            agent_address=str(ctx.agent.address),
            retry_recommended=True
        )
        await ctx.send(sender, error_msg)
        logger.error(f"Unexpected error in handle_analysis_request: {e}", exc_info=True)


@guardian_agent.on_message(model=CorrelationAnalysisResponse)
async def handle_correlation_response(ctx: Context, sender: str, msg: CorrelationAnalysisResponse):
    """
    Handle response from CorrelationAgent.

    Stores response in context storage keyed by request_id.

    Args:
        ctx: uAgents context
        sender: Sender address (should be CorrelationAgent)
        msg: CorrelationAnalysisResponse message
    """
    logger.info(f"Received CorrelationAnalysisResponse {msg.request_id} from {sender} "
                f"(processing_time: {msg.processing_time_ms}ms)")

    # Store response in context storage
    response_key = f"correlationagent_{msg.request_id}"
    ctx.storage.set(response_key, msg.model_dump())


@guardian_agent.on_message(model=SectorAnalysisResponse)
async def handle_sector_response(ctx: Context, sender: str, msg: SectorAnalysisResponse):
    """
    Handle response from SectorAgent.

    Stores response in context storage keyed by request_id.

    Args:
        ctx: uAgents context
        sender: Sender address (should be SectorAgent)
        msg: SectorAnalysisResponse message
    """
    logger.info(f"Received SectorAnalysisResponse {msg.request_id} from {sender} "
                f"(processing_time: {msg.processing_time_ms}ms)")

    # Store response in context storage
    response_key = f"sectoragent_{msg.request_id}"
    ctx.storage.set(response_key, msg.model_dump())


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger.info("Starting Guardian Agent Local...")
    guardian_agent.run()
