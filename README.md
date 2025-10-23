# Guardian

**AI-powered crypto portfolio risk analysis using multi-agent systems**

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

Guardian is a sophisticated portfolio risk assessment tool built on the Fetch.ai uAgents framework. It analyzes cryptocurrency portfolios for systemic risks by detecting high asset correlations and sector concentration issues that could lead to cascading losses during market downturns.

## The Problem: Portfolio Risk Blindness

Most crypto investors suffer from **risk blindness**—they see their portfolio as a collection of individual tokens without understanding the hidden correlations and sector concentrations that can amplify losses during market crashes.

**Real-world scenario:**
- An investor holds UNI, AAVE, MKR, and COMP (all DeFi governance tokens)
- They believe they're diversified because they own "4 different tokens"
- During the 2022 bear market, all 4 tokens crashed together (-75% vs -55% market average)
- The portfolio suffered **compounding risk**: 95% ETH correlation + 68% DeFi governance concentration

Traditional portfolio trackers only show token prices and total value. They don't reveal:
- How correlated your assets are to ETH (crash risk multiplier)
- Whether you're dangerously concentrated in one sector
- How your portfolio would perform in historical crash scenarios

**Guardian solves this by detecting compounding risks that individual analysis would miss.**

## The Solution: Multi-Agent Intelligence

Guardian uses a **distributed multi-agent architecture** to identify risks that no single agent could detect alone:

- **Guardian Agent**: Main orchestrator that coordinates risk analysis and detects compounding risks
- **CorrelationAgent**: Analyzes portfolio correlation to ETH using historical crash data
- **SectorAgent**: Evaluates sector concentration and identifies dangerous patterns
- **MeTTa Knowledge Graph**: Stores historical market crash scenarios and semantic relationships

### Multi-Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          User                                   │
│                  via ASI:One Chat Interface                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Guardian Agent│
                    │  (Orchestrator)│
                    └────────┬───────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Correlation  │ │   Sector     │ │    MeTTa     │
    │    Agent     │ │    Agent     │ │  Knowledge   │
    │              │ │              │ │    Graph     │
    └──────────────┘ └──────────────┘ └──────────────┘
            │                │                │
            └────────────────┼────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │   Guardian     │
                    │   Synthesis    │
                    │ (Compounding   │
                    │  Risk Detection)│
                    └────────────────┘
```

**Why Multi-Agent?**
- **Specialization**: Each agent is an expert in one dimension of risk (correlation, sector, historical context)
- **Compounding Risk Detection**: Guardian synthesizes specialist insights to identify risks neither agent would detect alone
- **Transparency**: Users see each agent's analysis verbatim, building trust through verifiable multi-agent collaboration
- **Scalability**: Additional risk agents (liquidity, smart contract, governance) can be added without modifying existing agents

## Agent Addresses (Deployed on Agentverse)

Guardian's multi-agent system consists of three specialized agents deployed on the Fetch.ai Agentverse platform. You can interact with Guardian directly via ASI:One.

| Agent | Address | Purpose |
|-------|---------|---------|
| **Guardian** | agent1qvq7grn2njv8a4tnxn6cnpvh9236gu42l6pf9cvmdya5yw8lnan25fxz7w0 ; Handle: `@guardianagent` (deployed) | Main orchestrator—send portfolio queries here |
| **CorrelationAgent** | agent1qg5y0arw0yvt45v6q5c9tx8symzt5ls2w5m245daz78q3yz9pqr756r5svn ; Handle: `@correlationagent` (deployed) | Calculates ETH correlation and crash risk |
| **SectorAgent** | agent1qws0dupy87yd0egny8uz0gmftrcjalnewf9hpynxgp442473jnhn5uded8e ; `@sectoragent` (deployed) | Analyzes sector concentration patterns |

**How to Query Guardian via ASI:One:**

1. Navigate to [ASI:One Chat Interface](https://asi.one)
2. Search for "Guardian" or "portfolio risk analysis"
3. Select **Guardian** agent from search results
4. Send a natural language query:
   - "Analyze wallet `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58`"
   - "What are the risks in portfolio `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`?"
   - "Give me a risk assessment for `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8`"
5. Guardian will respond within ~4 seconds with full multi-agent analysis
   

## Demo Wallets (Test Guardian Yourself)

Guardian includes three pre-configured demo wallets representing different risk profiles. Use these addresses to test Guardian via ASI:One:

### Demo Wallet 1: High Risk DeFi Whale
**Address:** `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58`

**Expected Risk Profile:**
- **ETH Correlation:** >90% (High Risk)
- **Sector Concentration:** 73% in DeFi Governance tokens
- **Guardian Alert Level:** Critical Risk
- **Key Insight:** Compounding risk detected—high correlation + high sector concentration creates 3.2x leverage effect

**Holdings:** UNI (23.7%), COMP (17.6%), AAVE (17.4%), MKR (14.0%), OP (10.3%), MATIC (6.9%), SNX (5.1%), CRV (3.4%), BAL (1.5%)

**Why This is High Risk:** All major holdings are ETH-based DeFi governance tokens. During the 2022 bear market, portfolios with this structure lost 73% (vs 55% market average) due to compounding correlation + sector concentration.

---

### Demo Wallet 2: Moderate Risk Balanced Portfolio
**Address:** `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`

**Expected Risk Profile:**
- **ETH Correlation:** 80-85% (Moderate Risk)
- **Sector Concentration:** 40-50% (Balanced)
- **Guardian Alert Level:** Moderate Risk
- **Key Insight:** Reasonable diversification with stablecoin cushion, but still ETH-dependent

**Holdings:** ETH (25.1%), LINK (12.7%), UNI (10.7%), AAVE (10.5%), ARB (10.0%), DAI (8.9%), OP (7.3%), USDC (7.2%), SUSHI (4.0%), GRT (3.6%)

**Why This is Moderate Risk:** Balanced sector allocation with 16% stablecoins provides some downside protection. Still exposed to ETH ecosystem but with better risk management than Wallet 1.

---

### Demo Wallet 3: Well-Diversified Conservative
**Address:** `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8`

**Expected Risk Profile:**
- **ETH Correlation:** <70% (Low Risk)
- **Sector Concentration:** No sector >30% (Excellent)
- **Guardian Alert Level:** Low Risk
- **Key Insight:** Cross-chain diversification with BTC and alternative Layer-1s

**Holdings:** BTC (20.3%), SOL (17.2%), AVAX (11.4%), ETH (10.6%), USDC (10.0%), DAI (8.0%), LINK (5.7%), ATOM (4.1%), DOT (3.5%), UNI (3.4%), AAVE (2.8%), LDO (2.8%)

**Why This is Low Risk:** Significant allocation to uncorrelated assets (BTC, SOL, AVAX). Stablecoins provide stability. No single sector dominates. This portfolio would have significantly outperformed ETH-only portfolios during 2022 bear market.

---

**Try These Queries in ASI:One:**
- "Analyze wallet `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58`" (High Risk)
- "What risks exist in `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`?" (Moderate Risk)
- "Assess portfolio `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8`" (Low Risk)

## Sample Conversation: Full Analysis Flow

Here's what a complete Guardian analysis looks like when you query Demo Wallet 1 via ASI:One:

**User Query (via ASI:One):**
```
Analyze wallet 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58
```

**Guardian Response:**
```
Guardian Portfolio Risk Analysis
Wallet: 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58
Request ID: demo-wallet-1-example

CorrelationAgent Analysis (agent1qw2e...9z0):

Your portfolio is 95% correlated to ETH. Portfolios with >90% correlation
lost an average of 73% in the 2022 crash versus 55% market average.

Historical Context:
- 2022 Bear Market (2022-05 to 2022-12): Portfolios with similar correlation
  lost 73.0% (vs. 55.0% market average)
- 2021 May Flash Crash (2021-05-12 to 2021-05-23): Portfolios with similar
  correlation lost 56.0% (vs. 38.0% market average)

(Processing: 1234ms)

---

SectorAgent Analysis (agent2qa3w...7h8):

68% of your portfolio is concentrated in DeFi Governance tokens. This
sector lost 75% in the 2022 crash.

Sector Breakdown:
- DeFi Governance: 68.0% ($68,000) - UNI, AAVE, MKR
- Layer-1 Platforms: 15.0% ($15,000) - ETH
- DeFi Lending: 12.0% ($12,000) - COMP
- Stablecoins: 5.0% ($5,000) - USDC

Historical Sector Risks:
- 2022 Bear Market: DeFi Governance sector lost 75.0% (vs. 55.0% market average)
  Opportunity Cost: Diversified portfolios gained 500.0% during 2023 recovery
  while DeFi Governance only recovered 250.0%

(Processing: 2345ms)

---

Guardian Synthesis:

Risk Level: Critical
Compounding Risk Detected: Yes

As CorrelationAgent showed, your 95% ETH correlation creates significant
exposure to Ethereum price movements. SectorAgent revealed that your 68%
DeFi Governance concentration amplifies this risk through sector-specific
vulnerabilities.

Combining these insights, Guardian identifies a compounding risk pattern:
this structure acts like 3.2x leverage to ETH movements. In 2022 Bear Market,
portfolios with this dual-risk structure lost 73% (not just 57% from
correlation alone). DeFi Governance sector amplifies ETH correlation—when
both crash together, losses multiply.

📋 Recommendations:

1. Reduce DeFi Governance token concentration from 68% to below 40%
   - Why: Over-concentration in DeFi Governance means single-sector crashes
     disproportionately impact your portfolio
   - Expected Impact: Reducing sector concentration would have limited losses
     and positioned portfolio for 500% recovery gains during 2023 rebound

2. Add uncorrelated assets (Bitcoin, Alternative Layer-1s, or Stablecoins)
   to reduce ETH correlation from 95% to below 80%
   - Why: High ETH correlation means your portfolio moves in lockstep with
     ETH price
   - Expected Impact: Reducing correlation to 75-80% would have limited 2022
     Bear Market losses to ~50% vs. 73% for portfolios with >90% correlation

3. Prioritize sector diversification before correlation reduction
   - Why: When both high correlation and high sector concentration are present,
     sector concentration amplifies correlation risk
   - Expected Impact: Addressing sector concentration first provides compounding
     benefit by reducing both risk dimensions simultaneously

---

Agents Consulted:
- CorrelationAgent (agent1qw2e...9z0) - 1234ms
- SectorAgent (agent2qa3w...7h8) - 2345ms

Total Analysis Time: 3.6 seconds
```

**What This Demonstrates:**
- **Multi-Agent Collaboration:** Three separate agents (CorrelationAgent, SectorAgent, Guardian) working together
- **Transparency:** Each agent's response shown verbatim with addresses and timing
- **Compounding Risk Detection:** Guardian identifies that 95% correlation + 68% sector concentration = 3.2x leverage effect
- **Historical Context:** References actual market events (2022 bear market, 2021 May crash)
- **Actionable Recommendations:** Prioritized suggestions with expected impact

For complete sample responses for all three demo wallets, see `docs/sample-responses/`.

## Limitations

Guardian is designed for **crypto portfolio risk analysis** and has specific limitations judges should be aware of:

**What Guardian Can Do:**
- Analyze ETH correlation for crypto portfolios
- Detect sector concentration risks across DeFi sectors
- Identify compounding risks (correlation + sector concentration)
- Provide historical context from 2021-2022 market crashes
- Generate prioritized recommendations with expected impact

**What Guardian Cannot Do:**
- **Real-time portfolio tracking:** Guardian analyzes static demo wallets, not live on-chain data
- **Custom wallet support:** MVP supports 3 pre-configured demo wallets only (not arbitrary addresses)
- **Traditional finance analysis:** Designed for crypto assets only (no stocks, bonds, forex)
- **Smart contract risk:** Does not analyze smart contract vulnerabilities or exploit risks
- **Liquidity analysis:** Does not assess token liquidity or slippage risk
- **Tax optimization:** No tax-loss harvesting or regulatory compliance advice
- **Automated rebalancing:** Provides recommendations but does not execute trades

**MVP Scope:**
- **Demo Wallets Only:** Test using provided addresses (`0x9aab...`, `0x742d...`, `0xBE0e...`)
- **Historical Correlation:** Uses 2021-2024 price data (not real-time feeds)
- **Agentverse Deployment:** Requires agents to be deployed and online
- **Response Time:** 3-6 seconds typical; may be slower under high platform load

**Future possibilities:**
- Support custom wallet addresses via on-chain queries (Etherscan API integration)
- Add smart contract risk analysis (separate agent)
- Add liquidity risk analysis (DEX depth queries)
- Real-time price feeds for live correlation calculations
- Multi-chain support beyond Ethereum ecosystem

## Prerequisites

- **Python 3.10+** (tested with Python 3.13.5)
- **Git** 2.51.1+
- **pip** 25.2+
- **Agentverse account** (for agent deployment)

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Zolldyk/Guardian.git
cd Guardian
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- `uagents==0.22.10` - Fetch.ai agent framework
- `pandas==2.3.3` - Data analysis
- `numpy==2.3.4` - Numerical computing
- `pytest==8.4.2` - Testing framework
- `ruff` - Code linting
- `mypy==1.18.2` - Type checking
- `python-dotenv==1.1.1` - Environment variable management

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and configure:
- Agent addresses (populated after Agentverse deployment)
- MeTTa knowledge path
- Logging level
- Timeout settings

See `.env.example` for detailed variable documentation.

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=agents --cov-report=html
open htmlcov/index.html  # View coverage report

# Run specific test file
pytest tests/test_hello_world.py -v
```

### Code Quality Checks

```bash
# Lint code
ruff check agents/

# Type checking
mypy agents/ --ignore-missing-imports

# Format code
ruff format agents/
```

### Running Agents Locally

```bash
# Run hello world agent (for learning/testing)
python agents/hello_world_agent.py

# Run test client agent (in separate terminal)
python agents/test_client_agent.py

# Run Guardian agent (future implementation)
python agents/guardian.py
```

## uAgents Framework Concepts

### Message-Passing Pattern

uAgents uses asynchronous message-passing for inter-agent communication:

1. **Agents are autonomous entities** - Each agent runs independently with its own logic
2. **Message models define contracts** - Pydantic models define message structure
3. **Handlers process messages** - Decorated functions handle incoming messages
4. **Addresses enable routing** - Each agent has a unique address (agent1q...)

### Agent Registration

Agents are registered with Agentverse using a seed phrase:

```python
agent = Agent(
    name="my_agent",
    seed="unique_seed_phrase",  # Generates deterministic address
    port=8000,
    endpoint=["http://localhost:8000/submit"],
)
```

The seed phrase generates a deterministic address that enables other agents to discover and communicate with it.

### Message Handlers

Message handlers are defined using decorators:

```python
@agent.on_message(model=MyRequest)
async def handle_request(ctx: Context, sender: str, msg: MyRequest):
    # Process message
    response = MyResponse(data="result")
    await ctx.send(sender, response)
```

### Communication Flow

1. Agent A sends a message to Agent B's address
2. Message is routed through Agentverse infrastructure
3. Agent B's handler processes the message
4. Agent B sends a response back to Agent A
5. Agent A's handler processes the response

All communication is **asynchronous** - agents don't block waiting for responses.

## Project Structure

```
guardian/
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── hello_world_agent.py     # Learning example
│   ├── test_client_agent.py     # Test client for hello world
│   ├── guardian.py              # Main orchestrator (future)
│   ├── correlation_agent.py     # Correlation specialist (future)
│   ├── sector_agent.py          # Sector specialist (future)
│   └── shared/                  # Shared utilities
│       └── __init__.py
├── data/                        # Data files
├── tests/                       # Test suite
│   ├── __init__.py
│   └── test_hello_world.py      # Unit tests
├── scripts/                     # Utility scripts
├── .github/workflows/           # CI/CD configuration
│   └── ci.yml                   # GitHub Actions workflow
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

## Agentverse Deployment

### Prerequisites

1. Create account at [Agentverse](https://agentverse.ai/)
2. Generate API key (Settings → API Keys)
3. Add API key to `.env`:

```bash
AGENTVERSE_API_KEY=your_api_key_here
```

### Deployment Steps

1. **Test locally first**:
```bash
python agents/hello_world_agent.py
```

2. **Deploy to Agentverse**:
   - Option A: Use Agentverse web UI (upload agent code)

3. **Update agent addresses**:
   - Copy deployed agent addresses from Agentverse dashboard
   - Update `.env` with actual addresses

4. **Verify deployment**:
   - Check agent status in Agentverse dashboard
   - Test inter-agent communication

## Testing Hello World Agents

1. **Start hello world agent**:
```bash
source venv/bin/activate
python agents/hello_world_agent.py
```

2. **Copy the agent address** from console output

3. **Update test client** (already configured):
```python
# In agents/test_client_agent.py
HELLO_WORLD_AGENT_ADDRESS = "agent1qdv6858m9mfa3tlf2erjcz7tt7v224hrmyendyaw0r6369k3xj8lkjnrzym"
```

4. **Run test client** (in new terminal):
```bash
source venv/bin/activate
python agents/test_client_agent.py
```

5. **Observe message exchange** in both terminal windows

## CI/CD Pipeline

GitHub Actions automatically runs on push/PR to `main` or `develop`:

- **Linting**: `ruff check .`
- **Type Checking**: `mypy agents/`
- **Unit Tests**: `pytest --cov=agents`
- **Integration Tests**: `pytest tests/test_integration.py`

View pipeline results: [Actions tab](https://github.com/Zolldyk/Guardian/actions)

## Resources

### uAgents Documentation

- [Fetch.ai Innovation Lab](https://fetch.ai/docs) - Official documentation
- [uAgents GitHub](https://github.com/fetchai/uAgents) - Framework repository
- [Agentverse Platform](https://agentverse.ai/) - Agent hosting platform


## Development Commands Cheat Sheet

```bash
# Environment setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Testing
pytest tests/ -v                           # All tests
pytest --cov=agents --cov-report=html      # With coverage
pytest tests/test_hello_world.py -v        # Specific test

# Code quality
ruff check agents/                         # Lint
mypy agents/ --ignore-missing-imports      # Type check
ruff format agents/                        # Format

# Run agents
python agents/hello_world_agent.py         # Hello world
python agents/test_client_agent.py         # Test client
```
