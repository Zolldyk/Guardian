"""
SectorAgent Local - Analyzes portfolio sector concentration and diversification.

This is the LOCAL DEVELOPMENT VERSION using pandas for data processing.
For production deployment to Agentverse, use sector_agent_hosted.py.

This agent classifies tokens into sector categories, calculates sector concentration
percentages, identifies dangerous concentration (>60% in any sector), and provides
diversification score and risk narrative.
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List

import pandas as pd
from uagents import Agent, Context

from agents.shared.config import get_env_var
from agents.shared.models import (
    AnalysisRequest,
    SectorAnalysis,
    SectorAnalysisResponse,
    SectorHolding,
    SectorRisk,
    OpportunityCost,
    ErrorMessage,
    Portfolio,
)

logger = logging.getLogger(__name__)

# Path to sector mapping data
SECTOR_MAPPINGS_PATH = Path(__file__).parent.parent / "data" / "sector-mappings.json"

# Path to historical crashes data
HISTORICAL_CRASHES_PATH = Path(__file__).parent.parent / "data" / "historical-crashes.json"

# Concentration threshold (percentage)
CONCENTRATION_THRESHOLD = 60.0

# Default crash scenario to analyze
DEFAULT_CRASH_SCENARIO = "crash_2022_bear"

# Agent initialization with seed from environment
sector_agent = Agent(
    name="sector_agent_local",
    seed=get_env_var("SECTOR_AGENT_SEED", default="sector_agent_local_secret_seed"),
    port=8002,
)


def load_sector_mappings() -> pd.DataFrame:
    """
    Load sector mapping data from JSON file using pandas.

    Returns:
        DataFrame with token-to-sector mappings

    Raises:
        FileNotFoundError: If sector-mappings.json doesn't exist
        ValueError: If JSON is malformed
    """
    if not SECTOR_MAPPINGS_PATH.exists():
        raise FileNotFoundError(f"Sector mappings not found at {SECTOR_MAPPINGS_PATH}")

    try:
        # Load JSON and convert to DataFrame
        df = pd.read_json(SECTOR_MAPPINGS_PATH, orient="index")
        logger.info(f"Loaded {len(df)} sector mappings")
        return df
    except Exception as e:
        raise ValueError(f"Failed to load sector mappings: {str(e)}")


def load_historical_crashes() -> pd.DataFrame:
    """
    Load historical crash data from JSON file using pandas.

    Returns:
        DataFrame with historical crash scenarios including sector-specific performance

    Raises:
        FileNotFoundError: If historical-crashes.json doesn't exist
        ValueError: If JSON is malformed
    """
    if not HISTORICAL_CRASHES_PATH.exists():
        raise FileNotFoundError(f"Historical crashes not found at {HISTORICAL_CRASHES_PATH}")

    try:
        # Load JSON file
        with open(HISTORICAL_CRASHES_PATH, 'r') as f:
            data = json.load(f)

        # Convert crashes list to DataFrame
        df = pd.DataFrame(data["crashes"])
        logger.info(f"Loaded {len(df)} historical crash scenarios")
        return df
    except Exception as e:
        raise ValueError(f"Failed to load historical crashes: {str(e)}")


def get_sector_crash_performance(sector_name: str, crash_scenario: str = DEFAULT_CRASH_SCENARIO) -> Dict:
    """
    Query historical sector performance for a specific crash scenario.

    Args:
        sector_name: Sector name (e.g., "DeFi Governance")
        crash_scenario: Crash scenario ID (default: "crash_2022_bear")

    Returns:
        Dictionary containing:
        - sector_name: str
        - sector_loss_pct: float
        - market_avg_loss_pct: float
        - crash_period: str
        - crash_name: str

    Raises:
        ValueError: If crash scenario or sector not found
    """
    try:
        crashes_df = load_historical_crashes()
    except FileNotFoundError as e:
        logger.error(f"Historical crashes unavailable: {str(e)}")
        raise

    # Find the crash scenario
    crash = crashes_df[crashes_df["scenario_id"] == crash_scenario]

    if crash.empty:
        raise ValueError(f"Crash scenario '{crash_scenario}' not found")

    crash_row = crash.iloc[0]
    sector_performance = crash_row["sector_performance"]

    # Check if sector exists in crash data
    if sector_name not in sector_performance:
        raise ValueError(f"Sector '{sector_name}' not found in crash scenario '{crash_scenario}'")

    return {
        "sector_name": sector_name,
        "sector_loss_pct": sector_performance[sector_name],
        "market_avg_loss_pct": crash_row["market_avg_loss_pct"],
        "crash_period": crash_row["period"],
        "crash_name": crash_row["name"]
    }


def get_opportunity_cost(
    concentrated_sectors: List[str],
    crash_scenario: str = DEFAULT_CRASH_SCENARIO
) -> List[OpportunityCost]:
    """
    Calculate opportunity cost for concentrated portfolios by identifying missed recovery gains.

    Args:
        concentrated_sectors: List of sectors with high concentration (>60%)
        crash_scenario: Crash scenario ID (default: "crash_2022_bear")

    Returns:
        List of OpportunityCost objects representing missed opportunities

    Raises:
        ValueError: If crash scenario not found
    """
    if not concentrated_sectors:
        # No concentration, no opportunity cost
        return []

    try:
        crashes_df = load_historical_crashes()
    except FileNotFoundError as e:
        logger.error(f"Historical crashes unavailable: {str(e)}")
        return []

    # Find the crash scenario
    crash = crashes_df[crashes_df["scenario_id"] == crash_scenario]

    if crash.empty:
        raise ValueError(f"Crash scenario '{crash_scenario}' not found")

    crash_row = crash.iloc[0]
    opportunity_sectors = crash_row.get("opportunity_cost_sectors", {})

    if not opportunity_sectors:
        return []

    # Find best opportunity NOT in concentrated sectors
    opportunity_costs = []

    for sector_name, opp_data in opportunity_sectors.items():
        # Only show opportunity cost for sectors NOT heavily represented in portfolio
        if sector_name not in concentrated_sectors:
            opportunity_costs.append(
                OpportunityCost(
                    missed_sector=sector_name,
                    missed_token=opp_data["best_performer"],
                    recovery_gain_pct=opp_data["recovery_gain_pct"],
                    narrative=opp_data["reason"]
                )
            )

    # Return top opportunity (highest recovery gain)
    if opportunity_costs:
        opportunity_costs.sort(key=lambda x: x.recovery_gain_pct, reverse=True)
        return [opportunity_costs[0]]  # Return only the best opportunity

    return []


def generate_sector_risk_narrative(sector_risks: List[SectorRisk]) -> str:
    """
    Generate plain English narrative explaining sector crash performance and opportunity cost.

    Args:
        sector_risks: List of SectorRisk objects with historical crash data

    Returns:
        Plain English narrative string

    Examples:
        - Well-diversified: "Well-diversified across sectors, no concentration warnings."
        - Concentrated with risk: "Your 68% DeFi Governance concentration lost 75% in 2022..."
    """
    if not sector_risks:
        return "Well-diversified across sectors, no concentration warnings."

    narrative_parts = []

    for risk in sector_risks:
        # Crash performance
        crash_text = (
            f"Your {risk.sector_name} concentration lost {abs(risk.sector_loss_pct):.0f}% "
            f"during the {risk.crash_scenario} ({risk.crash_period}), "
            f"compared to {abs(risk.market_avg_loss_pct):.0f}% market average."
        )

        # Opportunity cost
        opp_cost = risk.opportunity_cost
        opp_text = (
            f" Meanwhile, {opp_cost.missed_sector} tokens like {opp_cost.missed_token} "
            f"gained {opp_cost.recovery_gain_pct:.0f}% during recovery. {opp_cost.narrative}"
        )

        narrative_parts.append(f"\n\n📉 Historical Risk:\n{crash_text}{opp_text}")

    return "".join(narrative_parts)


def classify_tokens(portfolio: Portfolio) -> Dict[str, Dict]:
    """
    Classify portfolio tokens into sectors and calculate sector concentrations.

    Args:
        portfolio: Portfolio model containing token holdings

    Returns:
        Dictionary mapping sector names to sector holdings with:
        - sector_name: str
        - value_usd: float
        - percentage: float
        - token_symbols: List[str]

    Raises:
        FileNotFoundError: If sector mappings file missing
    """
    try:
        sector_map = load_sector_mappings()
    except FileNotFoundError as e:
        logger.error(f"Sector mappings unavailable: {str(e)}")
        raise

    # Initialize sector accumulator
    sector_data: Dict[str, Dict] = {}

    # Track unknown tokens
    unknown_tokens = []
    unknown_value = 0.0

    # Classify each token in the portfolio
    for token in portfolio.tokens:
        symbol = token.symbol

        # Look up sector for this token
        if symbol in sector_map.index:
            sector_name = sector_map.loc[symbol, "sector"]
        else:
            # Unknown token - add to "Unknown Sector"
            logger.warning(f"Token {symbol} not found in sector mappings, categorizing as Unknown Sector")
            sector_name = "Unknown Sector"
            unknown_tokens.append(symbol)
            unknown_value += token.value_usd

        # Add token value to sector total
        if sector_name not in sector_data:
            sector_data[sector_name] = {
                "sector_name": sector_name,
                "value_usd": 0.0,
                "percentage": 0.0,
                "token_symbols": []
            }

        sector_data[sector_name]["value_usd"] += token.value_usd
        sector_data[sector_name]["token_symbols"].append(symbol)

    # Calculate percentages
    for sector_name in sector_data:
        sector_data[sector_name]["percentage"] = (
            sector_data[sector_name]["value_usd"] / portfolio.total_value_usd * 100
        )

    logger.info(f"Classified portfolio into {len(sector_data)} sectors")
    if unknown_tokens:
        logger.warning(
            f"Unknown tokens: {unknown_tokens} "
            f"(${unknown_value:.2f} USD, {unknown_value/portfolio.total_value_usd*100:.1f}%)"
        )

    return sector_data


def identify_concentrated_sectors(
    sector_breakdown: Dict[str, Dict],
    threshold: float = CONCENTRATION_THRESHOLD
) -> List[str]:
    """
    Identify sectors that exceed the concentration threshold.

    Args:
        sector_breakdown: Dictionary mapping sector names to sector data
        threshold: Concentration threshold percentage (default: 60.0)

    Returns:
        List of sector names that exceed the threshold
    """
    concentrated = [
        sector_name
        for sector_name, data in sector_breakdown.items()
        if data["percentage"] > threshold
    ]

    logger.info(f"Identified {len(concentrated)} concentrated sectors (>{threshold}%): {concentrated}")
    return concentrated


def calculate_diversification_score(concentrated_sectors: List[str]) -> str:
    """
    Calculate diversification score based on number of concentrated sectors.

    Args:
        concentrated_sectors: List of concentrated sector names

    Returns:
        Diversification score: "Well-Diversified" | "Moderate Concentration" | "High Concentration"
    """
    num_concentrated = len(concentrated_sectors)

    if num_concentrated == 0:
        score = "Well-Diversified"
    elif num_concentrated == 1:
        score = "Moderate Concentration"
    else:
        score = "High Concentration"

    logger.info(f"Diversification score: {score} ({num_concentrated} concentrated sectors)")
    return score


def generate_sector_narrative(
    sector_breakdown: Dict[str, Dict],
    concentrated_sectors: List[str],
    diversification_score: str,
    portfolio_total_value: float
) -> str:
    """
    Generate plain English narrative explaining sector concentration.

    Args:
        sector_breakdown: Dictionary mapping sector names to sector data
        concentrated_sectors: List of concentrated sector names
        diversification_score: Diversification score string
        portfolio_total_value: Total portfolio value in USD

    Returns:
        Plain English narrative with sector breakdown and concentration warnings
    """
    narrative_parts = []

    # Header
    num_sectors = len(sector_breakdown)
    if diversification_score == "Well-Diversified":
        narrative_parts.append(f"Your portfolio is well-diversified across {num_sectors} sectors:\n")
    else:
        narrative_parts.append(f"Your portfolio is distributed across {num_sectors} sectors:\n")

    # Sector breakdown (sorted by percentage descending)
    sorted_sectors = sorted(
        sector_breakdown.items(),
        key=lambda x: x[1]["percentage"],
        reverse=True
    )

    for sector_name, data in sorted_sectors:
        tokens_str = ", ".join(data["token_symbols"])
        narrative_parts.append(
            f"\n- {sector_name}: {data['percentage']:.1f}% (${data['value_usd']:.2f} USD) - {tokens_str}"
        )

    # Concentration warnings
    if concentrated_sectors:
        narrative_parts.append("\n")
        for sector_name in concentrated_sectors:
            sector_pct = sector_breakdown[sector_name]["percentage"]
            narrative_parts.append(
                f"\n⚠️ HIGH CONCENTRATION: {sector_pct:.1f}% of your portfolio is in {sector_name} tokens. "
                f"This creates dangerous sector risk - if {sector_name} crashes, your entire portfolio is exposed."
            )

    # Diversification assessment
    narrative_parts.append(f"\n\nDiversification Score: {diversification_score}")

    # Risk implication based on score
    if diversification_score == "Well-Diversified":
        narrative_parts.append(
            "\n\nNo sector exceeds 60% concentration. Your portfolio structure demonstrates good sector "
            "diversification, which reduces the risk of a single-sector crash wiping out your holdings."
        )
    elif diversification_score == "Moderate Concentration":
        narrative_parts.append(
            "\n\nOne sector exceeds 60% concentration. Consider diversifying into uncorrelated sectors "
            "to reduce this compounding risk."
        )
    else:  # High Concentration
        narrative_parts.append(
            "\n\nMultiple sectors exceed 60% concentration or you have extreme concentration in one sector. "
            "Consider diversifying into uncorrelated sectors like Stablecoins, Layer-1 Alts, or different "
            "DeFi categories to reduce this compounding risk."
        )

    return "".join(narrative_parts)


@sector_agent.on_message(model=AnalysisRequest)
async def handle_analysis_request(ctx: Context, sender: str, msg: AnalysisRequest):
    """
    Handle incoming AnalysisRequest message and return sector concentration analysis.

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

        # Classify tokens into sectors
        sector_breakdown = classify_tokens(portfolio)

        # Identify concentrated sectors
        concentrated_sectors = identify_concentrated_sectors(sector_breakdown)

        # Calculate diversification score
        diversification_score = calculate_diversification_score(concentrated_sectors)

        # Generate plain English narrative (sector breakdown)
        narrative = generate_sector_narrative(
            sector_breakdown,
            concentrated_sectors,
            diversification_score,
            portfolio.total_value_usd
        )

        # Build sector_risks list with historical crash performance (Story 1.6)
        sector_risks = []
        if concentrated_sectors:
            try:
                # Get opportunity cost once (same for all concentrated sectors)
                opportunity_costs = get_opportunity_cost(concentrated_sectors)

                # For each concentrated sector, get crash performance
                for sector_name in concentrated_sectors:
                    # Get sector crash performance
                    crash_perf = get_sector_crash_performance(sector_name)

                    # Build SectorRisk object
                    if opportunity_costs:
                        sector_risk = SectorRisk(
                            sector_name=sector_name,
                            crash_scenario=crash_perf["crash_name"],
                            sector_loss_pct=crash_perf["sector_loss_pct"],
                            market_avg_loss_pct=crash_perf["market_avg_loss_pct"],
                            crash_period=crash_perf["crash_period"],
                            opportunity_cost=opportunity_costs[0]
                        )
                        sector_risks.append(sector_risk)

                        # Break after first sector (avoid duplicate opportunity costs)
                        break

            except (ValueError, FileNotFoundError) as e:
                # If historical data unavailable, log warning but continue without sector_risks
                logger.warning(f"Could not load historical crash data: {str(e)}")
                sector_risks = []

        # Append historical risk narrative to main narrative
        historical_narrative = generate_sector_risk_narrative(sector_risks)
        narrative = narrative + historical_narrative

        # Build SectorAnalysis model
        analysis = SectorAnalysis(
            sector_breakdown=sector_breakdown,
            concentrated_sectors=concentrated_sectors,
            diversification_score=diversification_score,
            sector_risks=sector_risks,  # NOW POPULATED with historical data
            narrative=narrative
        )

        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Send response
        response = SectorAnalysisResponse(
            request_id=msg.request_id,
            wallet_address=msg.wallet_address,
            analysis_data=analysis.model_dump(),
            agent_address=ctx.agent.address,
            processing_time_ms=processing_time_ms
        )

        await ctx.send(sender, response)
        logger.info(
            f"Sent SectorAnalysisResponse {msg.request_id} to {sender} "
            f"(processed in {processing_time_ms}ms)"
        )

    except ValueError as e:
        # Invalid portfolio data or insufficient data
        logger.error(f"ValueError processing request {msg.request_id}: {str(e)}")

        error_response = ErrorMessage(
            request_id=msg.request_id,
            error_type="invalid_data",
            error_message=str(e),
            agent_address=ctx.agent.address,
            retry_recommended=False
        )

        await ctx.send(sender, error_response)

    except FileNotFoundError as e:
        # Sector mappings file missing
        logger.error(f"FileNotFoundError processing request {msg.request_id}: {str(e)}")

        error_response = ErrorMessage(
            request_id=msg.request_id,
            error_type="insufficient_data",
            error_message=f"Sector mapping data unavailable: {str(e)}",
            agent_address=ctx.agent.address,
            retry_recommended=True
        )

        await ctx.send(sender, error_response)

    except Exception as e:
        # Unexpected error
        logger.exception(f"Unexpected error processing request {msg.request_id}: {str(e)}")

        error_response = ErrorMessage(
            request_id=msg.request_id,
            error_type="agent_unavailable",
            error_message=f"Internal error: {str(e)}",
            agent_address=ctx.agent.address,
            retry_recommended=True
        )

        await ctx.send(sender, error_response)


if __name__ == "__main__":
    logger.info("Starting SectorAgent Local...")
    sector_agent.run()
