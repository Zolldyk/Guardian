"""
SectorAgent - Agentverse Hosted Version with ASI1 LLM Integration

This version is compatible with Agentverse hosted platform constraints:
- Uses only supported libraries (requests, no pandas/numpy)
- Integrates chat protocol for ASI1 LLM compatibility
- Includes AI-powered parameter extraction via OpenAI/Claude agents
- Fetches sector mapping data from GitHub repository

Deployment Instructions:
1. Create agent on Agentverse → Agents → Launch an Agent → Blank Agent
2. Copy this entire file into agent.py
3. Add comprehensive README in Overview section for ASI1 discoverability
4. Click "Start" to deploy
5. Copy agent address from logs and update .env file

Environment Variables (set in Agentverse dashboard - NO COMMENTS):
- SECTOR_AGENT_SEED=<your_secret_seed_phrase>
- CONCENTRATION_THRESHOLD=60
- LOG_LEVEL=INFO
- AI_AGENT_CHOICE=openai (or "claude")
"""

import os
import time
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, Dict, List

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
    if not value and key == "SECTOR_AGENT_SEED":
        print(f"⚠️ {key} not set, using default seed (NOT SECURE for production)")
        return "sector_agent_insecure_default_seed_change_me"
    # Strip inline comments and whitespace (handles "60 # comment" -> "60")
    if "#" in value:
        value = value.split("#")[0].strip()
    return value.strip()

# Agent configuration
SECTOR_AGENT_SEED = get_env_var("SECTOR_AGENT_SEED")

# AI Agent selection for parameter extraction
AI_AGENT_CHOICE = get_env_var("AI_AGENT_CHOICE", "openai")
OPENAI_AGENT = 'agent1qtlpfshtlcxekgrfcpmv7m9zpajuwu7d5jfyachvpa4u3dkt6k0uwwp2lct'
CLAUDE_AGENT = 'agent1qvk7q2av3e2y5gf5s90nfzkc8a48q3wdqeevwrtgqfdl0k78rspd6f2l4dx'
AI_AGENT_ADDRESS = OPENAI_AGENT if AI_AGENT_CHOICE == "openai" else CLAUDE_AGENT

# Sector concentration configuration
CONCENTRATION_THRESHOLD = float(get_env_var("CONCENTRATION_THRESHOLD", "60"))

# GitHub raw data URLs
GITHUB_SECTOR_MAPPINGS_URL = "https://raw.githubusercontent.com/Zolldyk/Guardian/main/data/sector-mappings.json"
GITHUB_DEMO_WALLETS_URL = "https://raw.githubusercontent.com/Zolldyk/Guardian/main/data/demo-wallets.json"
GITHUB_HISTORICAL_CRASHES_URL = "https://raw.githubusercontent.com/Zolldyk/Guardian/main/data/historical-crashes.json"

# Default crash scenario to analyze
DEFAULT_CRASH_SCENARIO = "crash_2022_bear"

print(f"✅ Configuration loaded: CONCENTRATION_THRESHOLD={CONCENTRATION_THRESHOLD}%")

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


class SectorHolding(BaseModel):
    """Portfolio allocation to a specific sector."""
    sector_name: str
    value_usd: float
    percentage: float
    token_symbols: List[str] = []


class OpportunityCost(BaseModel):
    """Opportunity cost from over-concentration in a sector."""
    missed_sector: str
    missed_token: str
    recovery_gain_pct: float
    narrative: str


class SectorRisk(BaseModel):
    """Historical risk and opportunity cost for a concentrated sector."""
    sector_name: str
    crash_scenario: str
    sector_loss_pct: float
    market_avg_loss_pct: float
    crash_period: str
    opportunity_cost: OpportunityCost


class SectorAnalysis(BaseModel):
    """Sector concentration analysis results from SectorAgent."""
    sector_breakdown: dict  # Dict[str, SectorHolding]
    concentrated_sectors: List[str] = []
    diversification_score: str
    sector_risks: List[SectorRisk] = []
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


class SectorAnalysisResponse(Model):
    """Response message from SectorAgent with analysis results."""
    request_id: str
    wallet_address: str
    analysis_data: dict  # SectorAnalysis serialized as dict
    agent_address: str
    processing_time_ms: int


class SectorErrorMessage(Model):
    """Error message for sector analysis failures."""
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
# SECTOR CLASSIFICATION FUNCTIONS (Pure Python)
# =============================================================================

def load_sector_mappings_from_github() -> Dict[str, Dict[str, Any]]:
    """
    Load sector mapping data from GitHub repository.

    Returns:
        Dictionary mapping token symbols to sector information

    Raises:
        ValueError: If data cannot be fetched or parsed
    """
    try:
        print(f"Fetching sector mappings from GitHub...")
        response = requests.get(GITHUB_SECTOR_MAPPINGS_URL, timeout=10)
        response.raise_for_status()

        sector_map = response.json()
        print(f"✅ Loaded {len(sector_map)} sector mappings")
        return sector_map

    except Exception as e:
        raise ValueError(f"Failed to load sector mappings from GitHub: {str(e)}")


def load_demo_wallet_from_github(wallet_address: str) -> Dict[str, Any]:
    """
    Load demo wallet data from GitHub repository.

    Args:
        wallet_address: Ethereum wallet address

    Returns:
        Dictionary containing wallet data

    Raises:
        ValueError: If wallet not found or data cannot be fetched
    """
    try:
        print(f"Fetching demo wallets from GitHub...")
        response = requests.get(GITHUB_DEMO_WALLETS_URL, timeout=10)
        response.raise_for_status()

        wallets_data = response.json()

        # Find matching wallet
        for wallet in wallets_data.get("wallets", []):
            if wallet["wallet_address"].lower() == wallet_address.lower():
                print(f"✅ Found demo wallet: {wallet['name']}")
                return wallet

        raise ValueError(f"Wallet address {wallet_address} not found in demo wallets")

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to load demo wallet from GitHub: {str(e)}")


def load_historical_crashes_from_github() -> List[Dict[str, Any]]:
    """
    Load historical crash data from GitHub repository using pure Python.

    Returns:
        List of crash scenario dictionaries

    Raises:
        ValueError: If data cannot be fetched or parsed
    """
    try:
        print(f"Fetching historical crashes from GitHub...")
        response = requests.get(GITHUB_HISTORICAL_CRASHES_URL, timeout=10)
        response.raise_for_status()

        crashes_data = response.json()
        crashes_list = crashes_data.get("crashes", [])
        print(f"✅ Loaded {len(crashes_list)} historical crash scenarios")
        return crashes_list

    except Exception as e:
        raise ValueError(f"Failed to load historical crashes from GitHub: {str(e)}")


def get_sector_crash_performance_pure_python(
    sector_name: str,
    crash_scenario: str = DEFAULT_CRASH_SCENARIO
) -> Dict[str, Any]:
    """
    Query historical sector performance for a specific crash scenario using pure Python.

    Args:
        sector_name: Sector name (e.g., "DeFi Governance")
        crash_scenario: Crash scenario ID (default: "crash_2022_bear")

    Returns:
        Dictionary containing crash performance data

    Raises:
        ValueError: If crash scenario or sector not found
    """
    try:
        crashes_list = load_historical_crashes_from_github()
    except ValueError as e:
        print(f"❌ Historical crashes unavailable: {str(e)}")
        raise

    # Find the crash scenario using pure Python
    crash = None
    for c in crashes_list:
        if c.get("scenario_id") == crash_scenario:
            crash = c
            break

    if not crash:
        raise ValueError(f"Crash scenario '{crash_scenario}' not found")

    sector_performance = crash.get("sector_performance", {})

    # Check if sector exists in crash data
    if sector_name not in sector_performance:
        raise ValueError(f"Sector '{sector_name}' not found in crash scenario '{crash_scenario}'")

    return {
        "sector_name": sector_name,
        "sector_loss_pct": sector_performance[sector_name],
        "market_avg_loss_pct": crash.get("market_avg_loss_pct", 0.0),
        "crash_period": crash.get("period", ""),
        "crash_name": crash.get("name", "")
    }


def get_opportunity_cost_pure_python(
    concentrated_sectors: List[str],
    crash_scenario: str = DEFAULT_CRASH_SCENARIO
) -> List[OpportunityCost]:
    """
    Calculate opportunity cost for concentrated portfolios using pure Python.

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
        crashes_list = load_historical_crashes_from_github()
    except ValueError as e:
        print(f"⚠️ Historical crashes unavailable: {str(e)}")
        return []

    # Find the crash scenario
    crash = None
    for c in crashes_list:
        if c.get("scenario_id") == crash_scenario:
            crash = c
            break

    if not crash:
        raise ValueError(f"Crash scenario '{crash_scenario}' not found")

    opportunity_sectors = crash.get("opportunity_cost_sectors", {})

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
                    missed_token=opp_data.get("best_performer", ""),
                    recovery_gain_pct=opp_data.get("recovery_gain_pct", 0.0),
                    narrative=opp_data.get("reason", "")
                )
            )

    # Return top opportunity (highest recovery gain)
    if opportunity_costs:
        opportunity_costs.sort(key=lambda x: x.recovery_gain_pct, reverse=True)
        return [opportunity_costs[0]]  # Return only the best opportunity

    return []


def generate_sector_risk_narrative_pure_python(sector_risks: List[SectorRisk]) -> str:
    """
    Generate plain English narrative explaining sector crash performance and opportunity cost.

    Args:
        sector_risks: List of SectorRisk objects with historical crash data

    Returns:
        Plain English narrative string
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


def classify_tokens_pure_python(portfolio_data: dict, sector_map: Dict[str, Dict[str, Any]]) -> Dict[str, Dict]:
    """
    Classify portfolio tokens into sectors using pure Python.

    Args:
        portfolio_data: Portfolio dictionary with tokens list
        sector_map: Dictionary mapping token symbols to sector info

    Returns:
        Dictionary mapping sector names to sector holdings
    """
    # Initialize sector accumulator
    sector_data: Dict[str, Dict] = {}

    # Track unknown tokens
    unknown_tokens = []
    unknown_value = 0.0

    total_value = portfolio_data["total_value_usd"]

    # Classify each token
    for token in portfolio_data["tokens"]:
        symbol = token["symbol"]
        value_usd = token["value_usd"]

        # Look up sector for this token
        if symbol in sector_map:
            sector_name = sector_map[symbol]["sector"]
        else:
            # Unknown token - add to "Unknown Sector"
            print(f"⚠️ Token {symbol} not found in sector mappings, categorizing as Unknown Sector")
            sector_name = "Unknown Sector"
            unknown_tokens.append(symbol)
            unknown_value += value_usd

        # Add token value to sector total
        if sector_name not in sector_data:
            sector_data[sector_name] = {
                "sector_name": sector_name,
                "value_usd": 0.0,
                "percentage": 0.0,
                "token_symbols": []
            }

        sector_data[sector_name]["value_usd"] += value_usd
        sector_data[sector_name]["token_symbols"].append(symbol)

    # Calculate percentages
    for sector_name in sector_data:
        sector_data[sector_name]["percentage"] = (
            sector_data[sector_name]["value_usd"] / total_value * 100
        )

    print(f"✅ Classified portfolio into {len(sector_data)} sectors")
    if unknown_tokens:
        print(
            f"⚠️ Unknown tokens: {unknown_tokens} "
            f"(${unknown_value:.2f} USD, {unknown_value/total_value*100:.1f}%)"
        )

    return sector_data


def identify_concentrated_sectors_pure_python(
    sector_breakdown: Dict[str, Dict],
    threshold: float
) -> List[str]:
    """
    Identify sectors exceeding concentration threshold using pure Python.

    Args:
        sector_breakdown: Dictionary mapping sector names to sector data
        threshold: Concentration threshold percentage

    Returns:
        List of sector names exceeding threshold
    """
    concentrated = [
        sector_name
        for sector_name, data in sector_breakdown.items()
        if data["percentage"] > threshold
    ]

    print(f"✅ Identified {len(concentrated)} concentrated sectors (>{threshold}%): {concentrated}")
    return concentrated


def calculate_diversification_score_pure_python(concentrated_sectors: List[str]) -> str:
    """
    Calculate diversification score using pure Python.

    Args:
        concentrated_sectors: List of concentrated sector names

    Returns:
        Diversification score string
    """
    num_concentrated = len(concentrated_sectors)

    if num_concentrated == 0:
        score = "Well-Diversified"
    elif num_concentrated == 1:
        score = "Moderate Concentration"
    else:
        score = "High Concentration"

    print(f"✅ Diversification score: {score} ({num_concentrated} concentrated sectors)")
    return score


def generate_sector_narrative_pure_python(
    sector_breakdown: Dict[str, Dict],
    concentrated_sectors: List[str],
    diversification_score: str,
    portfolio_total_value: float
) -> str:
    """
    Generate plain English narrative using pure Python.

    Args:
        sector_breakdown: Dictionary mapping sector names to sector data
        concentrated_sectors: List of concentrated sector names
        diversification_score: Diversification score string
        portfolio_total_value: Total portfolio value in USD

    Returns:
        Plain English narrative
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

    # Risk implication
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


def process_sector_analysis(portfolio_data: dict) -> SectorAnalysis:
    """
    Main processing function for sector concentration analysis.

    Args:
        portfolio_data: Portfolio dictionary containing token holdings

    Returns:
        SectorAnalysis model with complete analysis results

    Raises:
        ValueError: If sector mappings unavailable or data invalid
    """
    print(f"🔍 Processing sector analysis for portfolio...")

    # Load sector mappings
    sector_map = load_sector_mappings_from_github()

    # Classify tokens into sectors
    sector_breakdown = classify_tokens_pure_python(portfolio_data, sector_map)

    # Identify concentrated sectors
    concentrated_sectors = identify_concentrated_sectors_pure_python(
        sector_breakdown,
        CONCENTRATION_THRESHOLD
    )

    # Calculate diversification score
    diversification_score = calculate_diversification_score_pure_python(concentrated_sectors)

    # Generate narrative (sector breakdown)
    narrative = generate_sector_narrative_pure_python(
        sector_breakdown,
        concentrated_sectors,
        diversification_score,
        portfolio_data["total_value_usd"]
    )

    # Build sector_risks list with historical crash performance (Story 1.6)
    sector_risks = []
    if concentrated_sectors:
        try:
            # Get opportunity cost once (same for all concentrated sectors)
            opportunity_costs = get_opportunity_cost_pure_python(concentrated_sectors)

            # For each concentrated sector, get crash performance
            for sector_name in concentrated_sectors:
                # Get sector crash performance
                crash_perf = get_sector_crash_performance_pure_python(sector_name)

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

        except (ValueError, Exception) as e:
            # If historical data unavailable, log warning but continue without sector_risks
            print(f"⚠️ Could not load historical crash data: {str(e)}")
            sector_risks = []

    # Append historical risk narrative to main narrative
    historical_narrative = generate_sector_risk_narrative_pure_python(sector_risks)
    narrative = narrative + historical_narrative

    # Build analysis model
    analysis = SectorAnalysis(
        sector_breakdown=sector_breakdown,
        concentrated_sectors=concentrated_sectors,
        diversification_score=diversification_score,
        sector_risks=sector_risks,  # NOW POPULATED with historical data
        narrative=narrative,
    )

    return analysis


# =============================================================================
# AGENT INITIALIZATION
# =============================================================================

# IMPORTANT: Agentverse provides a pre-created 'agent' instance
# We don't create our own Agent() - just use the provided one
# The seed is set via Agentverse environment variables

print(f"✅ SectorAgent initializing...")

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
    Processes sector analysis and sends result back to user.
    """
    session_sender = ctx.storage.get(str(ctx.session))

    if session_sender is None:
        ctx.logger.error("❌ No session sender found in storage")
        return

    # Check if AI couldn't extract parameters
    if "<UNKNOWN>" in str(msg.output):
        error_response = ChatMessage(
            content=[TextContent(
                text="Sorry, I couldn't understand your request. Please provide a wallet address from the demo wallets:\n\n"
                     "1. High Risk DeFi Whale: `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58`\n"
                     "2. Moderate Risk Balanced: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`\n"
                     "3. Well-Diversified Conservative: `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8`"
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

        # Load demo wallet data from GitHub
        wallet_data = load_demo_wallet_from_github(wallet_address)

        # Construct portfolio data
        portfolio_data = {
            "wallet_address": wallet_data["wallet_address"],
            "tokens": wallet_data["tokens"],
            "total_value_usd": wallet_data["total_value_usd"],
            "analysis_timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Perform sector analysis
        analysis = process_sector_analysis(portfolio_data)

        processing_time_ms = int((time.time() - start_time) * 1000)

        ctx.logger.info(f"✅ Analysis complete: {analysis.diversification_score} in {processing_time_ms}ms")

        # Send narrative response to user
        response = ChatMessage(
            content=[TextContent(
                text=f"## Sector Concentration Analysis\n\n"
                     f"**Wallet:** `{wallet_address}`\n\n"
                     f"{analysis.narrative}\n\n"
                     f"---\n"
                     f"*Analysis completed in {processing_time_ms}ms*"
            )],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, response)
        ctx.logger.info(f"📤 Sent analysis response to {session_sender}")

    except ValueError as err:
        ctx.logger.error(f"❌ ValueError: {err}")

        processing_time_ms = int((time.time() - start_time) * 1000)

        error_response = ChatMessage(
            content=[TextContent(
                text=f"Sorry, I couldn't analyze that wallet address. {str(err)}\n\n"
                     f"Please use one of the demo wallet addresses:\n"
                     f"1. High Risk DeFi Whale: `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58`\n"
                     f"2. Moderate Risk Balanced: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`\n"
                     f"3. Well-Diversified Conservative: `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8`"
            )],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, error_response)

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
        # Perform sector analysis
        analysis = process_sector_analysis(msg.portfolio_data)

        processing_time_ms = int((time.time() - start_time) * 1000)

        ctx.logger.info(f"✅ Analysis complete: {analysis.diversification_score} in {processing_time_ms}ms")

        # Send response back to sender
        await ctx.send(
            sender,
            SectorAnalysisResponse(
                request_id=msg.request_id,
                wallet_address=msg.wallet_address,
                analysis_data=analysis.model_dump(),
                agent_address=ctx.agent.address,
                processing_time_ms=processing_time_ms,
            ),
        )

        ctx.logger.info(f"📤 Sent SectorAnalysisResponse for {msg.request_id}")

    except Exception as e:
        ctx.logger.error(f"❌ Error processing {msg.request_id}: {str(e)}")

        processing_time_ms = int((time.time() - start_time) * 1000)

        await ctx.send(
            sender,
            SectorErrorMessage(
                request_id=msg.request_id,
                error_type="insufficient_data" if "mappings" in str(e).lower() else "invalid_data",
                error_message=f"Sector analysis failed: {str(e)}",
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
    ctx.logger.info("🚀 SectorAgent (Agentverse Hosted) Started Successfully!")
    ctx.logger.info(f"📍 Agent Address: {ctx.agent.address}")
    ctx.logger.info(f"⚙️  Configuration:")
    ctx.logger.info(f"   - AI Agent: {AI_AGENT_CHOICE.upper()}")
    ctx.logger.info(f"   - Concentration Threshold: {CONCENTRATION_THRESHOLD}%")
    ctx.logger.info(f"📊 Data Source: GitHub ({GITHUB_SECTOR_MAPPINGS_URL})")
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
    print("Starting SectorAgent (Agentverse Hosted Version)...")
    agent.run()
