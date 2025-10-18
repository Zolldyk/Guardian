# Components

This section defines the three core agents that comprise Guardian's multi-agent system. Each agent is an independent service with clear responsibilities and interfaces.

## Guardian Orchestrator Agent

**Responsibility:** Central coordinator that receives user queries via ASI:One Chat Protocol, delegates analysis to specialized agents, synthesizes results to identify compounding risks, and generates actionable recommendations.

**Key Interfaces:**
- **Incoming:** `ChatMessage` from ASI:One (user natural language queries)
- **Outgoing:** `AnalysisRequest` to CorrelationAgent and SectorAgent
- **Incoming:** `CorrelationAnalysisResponse` and `SectorAnalysisResponse` from specialized agents
- **Outgoing:** `ChatResponse` to ASI:One (synthesized narrative analysis)

**Dependencies:**
- CorrelationAgent (via uAgents address)
- SectorAgent (via uAgents address)
- `agents/shared/portfolio_utils.py` (portfolio parsing from demo wallet data)
- `data/demo_wallets.json` (hardcoded demo portfolios)

**Technology Stack:**
- Python 3.10+, uAgents framework, Pydantic models
- ASI:One Chat Protocol integration
- Python logging for inter-agent message tracing

**Core Logic:**
```python
# Guardian agent structure (agents/guardian.py)
from uagents import Agent, Context
from agents.shared.models import ChatMessage, AnalysisRequest, GuardianSynthesis
import uuid

guardian = Agent(name="guardian", seed=os.getenv("GUARDIAN_SEED"))

@guardian.on_message(model=ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    # 1. Parse wallet address from natural language
    wallet_address = extract_wallet_address(msg.message_text)

    # 2. Load portfolio data from demo_wallets.json
    portfolio = load_demo_portfolio(wallet_address)

    # 3. Generate request ID for tracking
    request_id = str(uuid.uuid4())

    # 4. Send parallel requests to specialized agents
    await ctx.send(CORRELATION_AGENT_ADDRESS, AnalysisRequest(
        request_id=request_id,
        wallet_address=wallet_address,
        portfolio=portfolio,
        requested_by=ctx.agent.address
    ))
    await ctx.send(SECTOR_AGENT_ADDRESS, AnalysisRequest(
        request_id=request_id,
        wallet_address=wallet_address,
        portfolio=portfolio,
        requested_by=ctx.agent.address
    ))

    # 5. Store session context for response handling
    ctx.storage.set(request_id, {
        "session_id": msg.session_id,
        "wallet_address": wallet_address,
        "timestamp": msg.timestamp
    })

@guardian.on_message(model=CorrelationAnalysisResponse)
async def handle_correlation_response(ctx: Context, sender: str, msg: CorrelationAnalysisResponse):
    # Store correlation results, check if sector results ready
    # If both complete, trigger synthesis
    pass

def synthesize_analysis(correlation: CorrelationAnalysis, sector: SectorAnalysis) -> GuardianSynthesis:
    # Detect compounding risk: correlation >85% AND sector concentration >60%
    compounding = correlation.correlation_percentage > 85 and len(sector.concentrated_sectors) > 0

    # Generate risk multiplier narrative
    # Generate 2-3 prioritized recommendations
    # Return complete synthesis
    pass
```

---

## CorrelationAgent

**Responsibility:** Calculate portfolio correlation to ETH using historical price data, query MeTTa for historical crash performance patterns, and return correlation analysis with "time machine" context.

**Key Interfaces:**
- **Incoming:** `AnalysisRequest` from Guardian
- **Outgoing:** `CorrelationAnalysisResponse` to Guardian
- **External:** MeTTa knowledge graph queries (via Hyperon Python bindings)

**Dependencies:**
- `agents/shared/metta_interface.py` (MeTTa query abstraction)
- `data/historical_crashes.json` (fallback if MeTTa unavailable)
- Pandas, NumPy (correlation calculations)
- Historical price data (embedded CSV files)

**Technology Stack:**
- Python 3.10+, uAgents framework
- Pandas for portfolio time-series analysis
- NumPy for Pearson correlation coefficient calculation
- Hyperon Python for MeTTa queries

**Core Logic:**
```python
# CorrelationAgent structure (agents/correlation_agent.py)
from uagents import Agent, Context
import pandas as pd
import numpy as np

correlation_agent = Agent(name="correlation_agent", seed=os.getenv("CORRELATION_AGENT_SEED"))

@correlation_agent.on_message(model=AnalysisRequest)
async def analyze_correlation(ctx: Context, sender: str, msg: AnalysisRequest):
    start_time = time.time()

    # 1. Calculate portfolio weighted returns (90-day window)
    portfolio_returns = calculate_portfolio_returns(msg.portfolio, days=90)

    # 2. Get ETH returns over same period
    eth_returns = load_eth_returns(days=90)

    # 3. Calculate Pearson correlation coefficient
    correlation_coef = np.corrcoef(portfolio_returns, eth_returns)[0, 1]
    correlation_pct = int(correlation_coef * 100)

    # 4. Interpret correlation level
    if correlation_pct > 85:
        interpretation = "High"
    elif correlation_pct > 70:
        interpretation = "Moderate"
    else:
        interpretation = "Low"

    # 5. Query MeTTa for historical crash performance
    historical_context = query_metta_crash_data(correlation_pct)

    # 6. Generate narrative explanation
    narrative = generate_correlation_narrative(correlation_pct, historical_context)

    # 7. Build and send response
    analysis = CorrelationAnalysis(
        correlation_coefficient=correlation_coef,
        correlation_percentage=correlation_pct,
        interpretation=interpretation,
        historical_context=historical_context,
        narrative=narrative
    )

    processing_time = int((time.time() - start_time) * 1000)

    await ctx.send(sender, CorrelationAnalysisResponse(
        request_id=msg.request_id,
        wallet_address=msg.wallet_address,
        analysis=analysis,
        agent_address=ctx.agent.address,
        processing_time_ms=processing_time
    ))
```

---

## SectorAgent

**Responsibility:** Map portfolio tokens to sector classifications, calculate sector concentration percentages, identify dangerous concentration (>60%), query MeTTa for sector-specific crash performance and opportunity cost.

**Key Interfaces:**
- **Incoming:** `AnalysisRequest` from Guardian
- **Outgoing:** `SectorAnalysisResponse` to Guardian
- **External:** MeTTa knowledge graph queries (sector performance data)

**Dependencies:**
- `agents/shared/metta_interface.py` (MeTTa query abstraction)
- `data/sector_mappings.json` (token-to-sector classifications)
- `data/historical_crashes.json` (fallback sector performance data)

**Technology Stack:**
- Python 3.10+, uAgents framework
- JSON file parsing for sector mappings
- Hyperon Python for MeTTa queries

**Core Logic:**
```python
# SectorAgent structure (agents/sector_agent.py)
from uagents import Agent, Context
from collections import defaultdict

sector_agent = Agent(name="sector_agent", seed=os.getenv("SECTOR_AGENT_SEED"))

@sector_agent.on_message(model=AnalysisRequest)
async def analyze_sectors(ctx: Context, sender: str, msg: AnalysisRequest):
    start_time = time.time()

    # 1. Load sector mappings
    sector_map = load_sector_mappings()  # from data/sector_mappings.json

    # 2. Classify tokens and calculate sector breakdown
    sector_breakdown = {}
    unknown_tokens = []

    for holding in msg.portfolio.tokens:
        if holding.symbol in sector_map:
            sector_name = sector_map[holding.symbol]["sector"]
            if sector_name not in sector_breakdown:
                sector_breakdown[sector_name] = SectorHolding(
                    sector_name=sector_name,
                    value_usd=0.0,
                    percentage=0.0,
                    token_symbols=[]
                )
            sector_breakdown[sector_name].value_usd += holding.value_usd
            sector_breakdown[sector_name].token_symbols.append(holding.symbol)
        else:
            unknown_tokens.append(holding.symbol)

    # 3. Calculate percentages
    for sector_holding in sector_breakdown.values():
        sector_holding.percentage = (sector_holding.value_usd / msg.portfolio.total_value_usd) * 100

    # 4. Identify concentrated sectors (>60%)
    concentrated_sectors = [
        sector for sector, holding in sector_breakdown.items()
        if holding.percentage > 60
    ]

    # 5. Query MeTTa for sector-specific crash performance
    sector_risks = []
    for sector_name in concentrated_sectors:
        crash_perf = query_metta_sector_performance(sector_name)
        opportunity_cost = query_metta_opportunity_cost(sector_name)
        sector_risks.append(SectorRisk(
            sector_name=sector_name,
            crash_performance=crash_perf,
            opportunity_cost=opportunity_cost
        ))

    # 6. Generate narrative
    narrative = generate_sector_narrative(sector_breakdown, concentrated_sectors, sector_risks)

    # 7. Build and send response
    analysis = SectorAnalysis(
        sector_breakdown=sector_breakdown,
        concentrated_sectors=concentrated_sectors,
        diversification_score="High Concentration" if concentrated_sectors else "Well-Diversified",
        sector_risks=sector_risks,
        narrative=narrative
    )

    processing_time = int((time.time() - start_time) * 1000)

    await ctx.send(sender, SectorAnalysisResponse(
        request_id=msg.request_id,
        wallet_address=msg.wallet_address,
        analysis=analysis,
        agent_address=ctx.agent.address,
        processing_time_ms=processing_time,
        unknown_tokens=unknown_tokens
    ))
```

---
