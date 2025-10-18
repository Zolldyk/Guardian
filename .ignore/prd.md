# Guardian Product Requirements Document (PRD)

**DeFi Portfolio Intelligence Agent**

**Version:** 1.0
**Date:** October 18, 2025
**Status:** Draft - In Progress
**Author:** John (PM Agent)

---

## Goals and Background Context

### Goals

- Win ASI Alliance Hackathon top prize by demonstrating best-in-class multi-agent collaboration
- Reveal hidden portfolio risks (correlation blindness and sector concentration) that standard trackers miss
- Transform abstract risk metrics into visceral understanding through historical crash simulations
- Validate product-market fit for DeFi portfolio intelligence through demo feedback
- Build extensible foundation for post-hackathon product evolution

### Background Context

DeFi investors face a dangerous illusion: they believe holding 10-15 different tokens means they're diversified, but during market crashes discover everything drops together. A typical scenario: "I thought I was diversified but everything crashed 70% overnight." This risk blindness stems from two hidden structural problems—portfolios that are 95% correlated to ETH (creating 3x leveraged exposure) and dangerous sector concentration (68% in governance tokens that collapse together).

Guardian solves this through multi-agent intelligence: specialized agents analyze correlation structure and sector concentration independently, then an orchestrator synthesizes findings to reveal compounding risks that neither dimension shows alone. Using the "time machine" approach, Guardian transforms abstract statistics into concrete insights: "Your portfolio is 95% correlated to ETH—portfolios with this structure lost 73% in the 2022 crash versus 55% market average." Built for the ASI Alliance Hackathon, Guardian demonstrates how specialized agents collaborating through the Fetch.ai/SingularityNET ecosystem can provide judgment and interpretation, not just data dashboards.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| October 18, 2025 | v1.0 | Initial PRD creation from project brief | John (PM Agent) |

---

## Requirements

### Functional Requirements

**FR1:** Guardian orchestrator agent accepts wallet address input via ASI:One Chat Protocol and initiates portfolio risk analysis workflow.

**FR2:** CorrelationAgent calculates portfolio correlation coefficient to ETH using historical price data and returns numerical correlation score (0-100%).

**FR3:** CorrelationAgent queries MeTTa knowledge graph to retrieve historical crash performance for portfolios matching the calculated correlation pattern.

**FR4:** CorrelationAgent returns correlation analysis with historical context (e.g., "95% correlated to ETH. In 2022 crash, portfolios with this structure lost 73% vs. 55% market average").

**FR5:** SectorAgent maps each token in portfolio to predefined sector classification (DeFi governance, layer-2, yield protocols, etc.).

**FR6:** SectorAgent calculates sector concentration percentages and identifies if any sector exceeds dangerous threshold (>60%).

**FR7:** SectorAgent queries MeTTa knowledge graph to retrieve sector-specific crash performance and opportunity cost data for concentrated sectors.

**FR8:** SectorAgent returns sector analysis with historical context and missed opportunities (e.g., "68% in DeFi governance tokens. This sector lost 75% in 2022 while SOL gained 500% in 2023").

**FR9:** Guardian synthesizes CorrelationAgent and SectorAgent responses to identify compounding risk effects (how correlation + sector concentration multiply risk).

**FR10:** Guardian presents synthesis showing how the two risk dimensions interact (e.g., "Your 3x ETH leverage + governance concentration creates compounding risk—this structure would have lost 75% in 2022, not just 60%").

**FR11:** Guardian generates 2-3 actionable recommendations based on identified risks (e.g., "Reduce governance token concentration below 40%", "Add SOL or BTC for uncorrelated exposure").

**FR12:** All agent responses are visible to users showing individual agent contributions (CorrelationAgent response, SectorAgent response, Guardian synthesis) for transparency.

**FR13:** System supports 2-3 hardcoded demo wallet addresses with pre-analyzed portfolio data (no real-time blockchain fetching).

**FR14:** System returns analysis results within 60 seconds of wallet input for demo scenarios.

**FR15:** MeTTa knowledge graph contains pre-populated data for 3 major crash scenarios (2022 bear market, 2021 correction, 2020 COVID crash).

**FR16:** MeTTa knowledge graph contains sector classifications and historical performance for top 20-30 DeFi tokens.

**FR17:** For tokens not in MeTTa knowledge graph, system returns "insufficient data" message rather than incorrect analysis.

**FR18:** Guardian supports natural language queries beyond initial wallet input (follow-up questions about specific risks or recommendations).

### Non-Functional Requirements

**NFR1:** All three agents (Guardian, CorrelationAgent, SectorAgent) must be deployed to Agentverse with unique public addresses accessible via ASI:One.

**NFR2:** Inter-agent communication must complete successfully with >95% reliability across test scenarios.

**NFR3:** Individual agent response time must be <5 seconds per query.

**NFR4:** End-to-end analysis time (wallet input to final synthesis) must be <60 seconds.

**NFR5:** System must support minimum 10 concurrent users during demo/testing phase without degradation.

**NFR6:** MeTTa query execution must complete in <1 second per historical lookup.

**NFR7:** All agents must be implemented using uAgents framework (Fetch.ai's Python multi-agent system).

**NFR8:** Historical data and correlation calculations must use Python ecosystem (Pandas, NumPy).

**NFR9:** Documentation must be complete enough for hackathon judges to test system without creator assistance.

**NFR10:** Agent deployment must be production-ready on Agentverse (not local development environment).

**NFR11:** System must handle edge cases gracefully (empty wallet, single token, unknown tokens) with clear error messages.

**NFR12:** Code must be maintainable and extensible for post-hackathon feature additions (80% reusable for production version).

**NFR13:** Historical crash simulation accuracy must be within ±10% of actual historical performance.

**NFR14:** Risk identification accuracy must be 100% for demo wallets and >90% for unseen test portfolios.

**NFR15:** System must include disclaimers that Guardian provides analysis, not investment advice.

---

## User Interface Design Goals

### Overall UX Vision

Guardian is designed as a **conversational intelligence agent**, not a traditional dashboard or visualization tool. The user experience centers on natural language interaction where users ask questions in plain English and receive narrative responses that synthesize complex risk analysis into clear insights. The UX philosophy is "show me what matters, not everything"—Guardian proactively reveals risks users didn't know to ask about rather than overwhelming with raw data.

The interaction feels like consulting a knowledgeable financial advisor who has deeply analyzed your portfolio: thoughtful, educational, and action-oriented. Users should experience progressive revelation—starting with surface understanding, then correlation risk, then sector risk, then the synthesis that shows how these dimensions compound. Each revelation builds toward the "lean forward moment" where the user realizes their portfolio structure is riskier than they thought.

**Key UX Principles:**
- **Intelligence over information:** Judgment and interpretation, not data dumps
- **Visceral over abstract:** Historical crash simulations make risk concrete
- **Transparent reasoning:** Users see which agents contributed what insights
- **Conversational flow:** Natural back-and-forth, not form filling
- **Actionable outcomes:** Every analysis ends with clear next steps

### Key Interaction Paradigms

**1. Natural Language Query Input**
Users interact via text-based conversational interface through ASI:One. Primary entry point is wallet address submission: "Analyze 0xabc123..." or "How risky is my portfolio at 0xabc123". System also supports follow-up questions: "Why is governance token concentration dangerous?" or "What should I do about this?"

**2. Progressive Risk Disclosure**
Information is revealed in layers rather than all at once:
- Layer 1: Surface acknowledgment ("Analyzing your portfolio...")
- Layer 2: Correlation risk reveal with historical context
- Layer 3: Sector concentration reveal with opportunity cost
- Layer 4: Synthesis showing compounding effects
- Layer 5: Actionable recommendations

This structure creates narrative tension and makes the synthesis feel like an earned insight rather than just another data point.

**3. Multi-Agent Transparency**
Individual agent contributions are visible to users, not hidden in backend processing. When Guardian consults CorrelationAgent or SectorAgent, users see the specific responses from each agent. This demonstrates the multi-agent collaboration explicitly—critical for hackathon judging and for building user trust in the analysis.

**4. Contextual Education**
Guardian doesn't assume users understand correlation coefficients or sector dynamics. Responses include brief educational context: "95% correlation means your portfolio moves almost identically to ETH—like 3x leveraged exposure" before diving into implications.

### Core Screens and Views

*Note: Guardian is chat-based via ASI:One, so "screens" are conversation stages rather than traditional UI screens.*

**1. Initial Query/Wallet Input Stage**
User provides wallet address in natural language. System confirms receipt and initiates analysis.

**2. Analysis In-Progress Stage**
Guardian shows which agents are being consulted and what they're analyzing. Example: "Consulting CorrelationAgent to analyze your portfolio structure..." This makes wait time feel purposeful and shows multi-agent collaboration.

**3. Correlation Risk Reveal Stage**
CorrelationAgent's response is presented with correlation coefficient, interpretation, and historical crash performance. Includes clear explanation of what the numbers mean.

**4. Sector Concentration Reveal Stage**
SectorAgent's response shows sector breakdown, concentration percentages, sector-specific crash performance, and opportunity cost (what was missed by over-concentrating).

**5. Synthesis & Compounding Risk Stage**
Guardian's synthesis explains how correlation + sector risks multiply. This is the "lean forward moment"—the insight neither individual agent revealed.

**6. Recommendations Stage**
2-3 specific, actionable recommendations based on identified risks. Includes rationale for each recommendation.

**7. Follow-Up Q&A Stage**
User can ask clarifying questions, drill into specific risks, or request alternative strategies. Guardian maintains context from previous analysis.

### Accessibility: **None** (MVP), WCAG AA (Post-MVP)

**MVP Stance:** Guardian's MVP relies entirely on ASI:One's accessibility features. As a text-based conversational interface, ASI:One should be inherently more accessible than visual dashboards (screen reader friendly, keyboard navigable). However, no Guardian-specific accessibility testing or enhancements are in scope for the 10-day hackathon build.

**Assumption:** ASI:One platform provides baseline accessibility compliance. Guardian doesn't introduce additional accessibility barriers since responses are plain text narratives.

**Post-MVP Goal:** When building standalone web dashboard (Phase 2), target WCAG AA compliance with proper semantic HTML, ARIA labels, keyboard navigation, and sufficient color contrast for any visualizations added.

### Branding

**MVP Approach: Minimal/Functional Branding**

Guardian is a hackathon proof-of-concept, not a consumer brand. Branding elements are functional and trust-building rather than marketing-focused:

- **Name:** "Guardian" conveys protection and vigilance—appropriate for risk analysis
- **Tagline:** "DeFi Portfolio Intelligence Agent" (descriptive, communicates purpose immediately)
- **Agent Persona:** Investigative, analytical, direct but supportive. Like a concerned financial advisor who tells you hard truths.
- **Visual Identity:** None required for MVP (ASI:One handles all UI rendering). If needed, simple text-based identifier: "🛡️ Guardian" with shield emoji.
- **Tone of Voice:** Professional but not alarmist. Educational without being condescending. Clear warnings about risk without creating panic.

### Target Device and Platforms: **Web Responsive** (ASI:One Interface)

**Primary Platform:** Web browser access via ASI:One conversational interface. Users access Guardian through ASI:One's web platform on desktop or mobile browsers.

**Device Support:**
- **Desktop browsers:** Chrome, Firefox, Safari, Edge (whatever ASI:One supports)
- **Mobile browsers:** Responsive web interface, no native mobile app
- **Tablets:** Supported via responsive web (ASI:One's responsibility)

**No Platform-Specific Optimization:** Guardian doesn't control the UI rendering—ASI:One does. As a conversational agent, Guardian's output is plain text narrative that adapts to any screen size naturally.

---

## Technical Assumptions

### Repository Structure: **Monorepo**

Guardian will use a **monorepo structure** with all three agents (Guardian orchestrator, CorrelationAgent, SectorAgent), shared utilities, data files, tests, and documentation in a single repository.

**Rationale:**
- **Solo developer efficiency:** Single repo means one place to track all code, no cross-repo dependency management, simpler version control
- **Shared code reuse:** All agents need common utilities (MeTTa interface, portfolio parsing, data structures). Monorepo makes sharing code across agents trivial via relative imports.
- **Atomic commits:** Changes that span multiple agents (e.g., updating MeTTa query interface) can be committed atomically rather than coordinated across repos
- **Simplified deployment:** Single deployment workflow pushes all three agents from one codebase
- **Hackathon judges:** Easier for judges to review—one GitHub URL, one README, all code visible in single place

**Repository Structure:**
```
guardian/
├── agents/
│   ├── guardian.py              # Main orchestrator agent
│   ├── correlation_agent.py     # Correlation analysis agent
│   ├── sector_agent.py          # Sector concentration agent
│   └── shared/
│       ├── metta_interface.py   # MeTTa query utilities
│       └── portfolio_utils.py   # Shared portfolio parsing
├── data/
│   ├── demo_wallets.json        # Hardcoded demo portfolios
│   ├── historical_crashes.json  # Crash scenario data
│   ├── sector_mappings.json     # Token-to-sector classifications
│   └── metta_knowledge/         # MeTTa knowledge graph files
├── tests/
│   ├── test_agents.py           # Agent unit tests
│   ├── test_integration.py      # Inter-agent communication tests
│   └── test_metta_queries.py    # MeTTa query accuracy tests
├── docs/
│   ├── README.md                # Main documentation
│   ├── ARCHITECTURE.md          # Architecture explanation
│   └── DEMO.md                  # Demo instructions
└── requirements.txt             # Python dependencies
```

### Service Architecture: **Distributed Multi-Agent System (Message-Passing)**

Guardian uses a **distributed multi-agent architecture** where each agent is deployed independently to Agentverse with its own unique address, and agents communicate via asynchronous message-passing through the uAgents protocol.

**Architectural Pattern:**
- **Not monolithic:** This is not a single application with internal modules. Each agent is a separate service.
- **Not microservices (traditional):** Agents don't expose REST APIs or use HTTP. Communication is via uAgents' native message protocol.
- **Agent-oriented architecture:** Agents are autonomous entities that maintain their own logic and data, collaborate through messages, and can be discovered/invoked via addresses.

**Communication Flow:**
1. User → ASI:One → Guardian orchestrator (via Chat Protocol)
2. Guardian → CorrelationAgent (via uAgents message with portfolio data)
3. CorrelationAgent → Guardian (response with correlation analysis)
4. Guardian → SectorAgent (via uAgents message with portfolio data)
5. SectorAgent → Guardian (response with sector analysis)
6. Guardian synthesizes both responses → User (via Chat Protocol)

**State Management:**
- **Stateless agents for MVP:** Agents don't maintain session state between requests. Each analysis is independent.
- **Context passed in messages:** All necessary context (portfolio data, wallet address) is included in messages between agents.
- **Post-MVP consideration:** May need stateful conversations if adding multi-turn dialogue with context retention.

**Deployment Model:**
- Each agent deployed separately to Agentverse
- Agents run continuously, listening for messages
- Guardian orchestrator also implements Chat Protocol for ASI:One integration
- No shared database or state store—data is embedded in agents or queried from MeTTa

### Testing Requirements: **Unit + Integration (Time-Boxed)**

Given 10-day solo timeline, testing strategy prioritizes **confidence over coverage**—focus on critical paths and agent communication reliability.

**Testing Levels:**

**1. Unit Tests (Essential - 20% of test time)**
- **Agent logic tests:** Each agent's core logic (correlation calculation, sector mapping, synthesis rules) tested independently with mocked dependencies
- **MeTTa query tests:** Verify MeTTa queries return expected results for known scenarios
- **Portfolio parsing tests:** Ensure portfolio data structures are parsed correctly
- **Target:** 70% code coverage on critical business logic, not 100% coverage

**2. Integration Tests (Critical - 60% of test time)**
- **Inter-agent communication:** Guardian → CorrelationAgent → response flow works reliably
- **End-to-end scenarios:** Full analysis workflow for each demo wallet completes successfully
- **Error handling:** Test timeout scenarios, unknown tokens, empty wallets
- **MeTTa integration:** Real queries against MeTTa knowledge graph return accurate results
- **Target:** 100% of demo scenarios pass integration tests

**3. Manual Testing (Essential - 20% of test time)**
- **ASI:One interface testing:** Real human interaction via Chat Protocol to verify UX flow
- **Demo rehearsal:** Run through complete demo script multiple times to catch UX issues
- **Judge perspective testing:** Can someone unfamiliar with the code run the demo successfully?

**Out of Scope for MVP:**
- E2E automated UI tests, load/performance tests, security testing, comprehensive edge case testing

### Additional Technical Assumptions and Requests

**1. Programming Language & Runtime**
- **Python 3.10+** for all agents and supporting code
- **Rationale:** uAgents framework is Python-based, ecosystem has mature libraries for financial analysis (Pandas, NumPy)

**2. Agent Framework & Platform**
- **uAgents framework** (Fetch.ai) for agent implementation
- **Agentverse** (Fetch.ai platform) for agent deployment and hosting
- **ASI:One Chat Protocol** for user-facing conversational interface
- **Rationale:** Mandatory for ASI Alliance hackathon eligibility

**3. Knowledge Representation**
- **MeTTa** (SingularityNET) for historical crash data and sector knowledge storage
- **Hyperon Python bindings** for querying MeTTa from agents
- **Fallback:** If Hyperon bindings prove problematic, can store knowledge as JSON and do dictionary lookups

**4. Data Processing & Analysis**
- **Pandas** for portfolio data manipulation and analysis
- **NumPy** for correlation calculations and numerical operations

**5. Data Storage**
- **Local JSON files** embedded with agents for demo wallet data, sector mappings, and configuration
- **MeTTa knowledge graph files** for historical crash data
- **No database server** (no PostgreSQL, MongoDB, Redis)
- **Post-MVP:** Migrate to PostgreSQL for user portfolio persistence, Redis for caching

**6. Version Control & Collaboration**
- **Git** for version control
- **GitHub** for code hosting and judge review

**7. Documentation**
- **Markdown** for all documentation (README, ARCHITECTURE, DEMO)
- **Inline code comments** for complex logic
- **Architecture diagrams:** Hand-drawn or simple tool (Excalidraw, diagrams.net)

**8. External Dependencies**
- **No blockchain APIs** for MVP (no Etherscan, Alchemy, The Graph)
- **No Web3 wallet connection** (no MetaMask, WalletConnect)
- **Pre-downloaded historical price data** (CSV from CoinGecko or similar)

**9. Error Handling & Monitoring**
- **Basic error handling:** Try/catch blocks for agent communication failures, timeouts, unknown tokens
- **Logging:** Python logging module for debugging
- **Monitoring:** Agentverse built-in monitoring for agent health

**10. Security & Privacy**
- **Read-only analysis:** No wallet connections, no transaction signing, no private key handling
- **Public demo wallets:** Using publicly visible wallet addresses, no PII
- **No authentication:** No user accounts, no login
- **Disclaimers:** Include disclaimer that Guardian provides analysis, not investment advice

**11. Performance Targets**
- Individual agent response: <5 seconds
- End-to-end analysis: <60 seconds
- Concurrent users: 10 minimum
- MeTTa query execution: <1 second

**12. Deployment Environment**
- **Production deployment:** Agentverse platform (managed by Fetch.ai)
- **No custom infrastructure:** No cloud servers (AWS, GCP), no containers, no orchestration

---

## Epic List

### Epic 1: Foundation & Specialized Agent Intelligence
Establish project infrastructure and implement two specialized analysis agents (CorrelationAgent and SectorAgent) that can independently analyze portfolio structure, delivering basic risk insights without multi-agent coordination.

### Epic 2: Multi-Agent Orchestration & Historical Intelligence
Implement Guardian orchestrator agent, enable inter-agent communication via uAgents message-passing, integrate MeTTa knowledge graph with historical crash scenarios, and create synthesis logic that reveals compounding risks from multi-agent collaboration.

### Epic 3: Production Deployment & User Experience
Integrate Chat Protocol for ASI:One conversational interface, deploy all agents to Agentverse production environment, create demo wallet scenarios, and produce comprehensive documentation and demo materials for hackathon submission.

---

## Epic Details

### Epic 1: Foundation & Specialized Agent Intelligence

**Epic Goal:** Establish project infrastructure, learn the uAgents framework, and implement two specialized analysis agents (CorrelationAgent and SectorAgent) that can independently analyze portfolio structure and deliver basic risk insights. By the end of this epic, both agents are deployed to Agentverse testnet and can be invoked independently to analyze demo portfolios.

---

#### Story 1.1: Project Setup and uAgents Framework Learning

**As a** developer,
**I want** a working development environment with uAgents framework configured and basic "hello world" agent tested,
**so that** I can build production agents confidently and understand framework capabilities before implementing Guardian's business logic.

**Acceptance Criteria:**

1. Python 3.10+ virtual environment created with all dependencies installed (uAgents, Pandas, NumPy, pytest)
2. GitHub repository initialized with monorepo structure (agents/, data/, tests/, docs/ folders)
3. requirements.txt file documents all Python dependencies with pinned versions
4. "Hello World" agent successfully created following Innovation Lab guide and deployed to Agentverse testnet
5. Basic inter-agent communication example from Innovation Lab works (two test agents exchange messages successfully)
6. Git repository has initial commit with project structure and working hello world example
7. README.md includes environment setup instructions and links to uAgents documentation
8. Developer can explain uAgents message-passing pattern and agent registration process

---

#### Story 1.2: Portfolio Data Structure and Demo Wallet Configuration

**As a** CorrelationAgent and SectorAgent,
**I want** a standardized portfolio data structure and pre-configured demo wallets with known holdings,
**so that** I can parse portfolio data consistently and have reliable test cases for analysis development.

**Acceptance Criteria:**

1. Portfolio data structure defined as JSON schema (wallet address, list of token holdings with symbol/amount/price)
2. Historical price data (90-day window) pre-downloaded from CoinGecko for top 30 DeFi tokens and stored as CSV
3. data/demo_wallets.json contains 3 demo portfolios with different risk profiles (high correlation+concentration, moderate risk, well-diversified)
4. Demo wallet addresses are real Ethereum addresses (verifiable on Etherscan)
5. Each demo portfolio includes 8-15 token holdings representing realistic DeFi investor allocation
6. portfolio_utils.py module provides parse_portfolio() function that converts JSON to internal data structure
7. Unit tests verify portfolio parsing handles valid input and raises clear errors for invalid data
8. Documentation explains demo wallet selection rationale and expected risk profiles

---

#### Story 1.3: CorrelationAgent ETH Correlation Calculation

**As a** portfolio analyst,
**I want** CorrelationAgent to calculate my portfolio's correlation coefficient to ETH using historical price data,
**so that** I can understand how closely my portfolio moves with the Ethereum market anchor.

**Acceptance Criteria:**

1. CorrelationAgent implemented as uAgents agent with unique identifier
2. Agent accepts message containing portfolio data (tokens, amounts, current prices)
3. Agent calculates portfolio weighted average returns over 90-day historical window
4. Agent calculates ETH returns over same 90-day window using pre-downloaded price data
5. Agent computes Pearson correlation coefficient between portfolio returns and ETH returns
6. Agent returns correlation result as percentage (0-100%) with interpretation (e.g., ">90% = high correlation")
7. Correlation calculation accuracy validated against manually calculated test cases (within ±2% tolerance)
8. Agent handles edge cases: single-token portfolio, empty portfolio, tokens with insufficient price history
9. Unit tests cover correlation calculation logic with known input/output pairs
10. Agent deployed to Agentverse testnet and responds to direct message queries within 5 seconds

---

#### Story 1.4: CorrelationAgent Historical Crash Context

**As a** portfolio analyst,
**I want** CorrelationAgent to include historical crash performance context alongside correlation coefficient,
**so that** I understand what this correlation level meant during real market events (the "time machine" approach).

**Acceptance Criteria:**

1. data/historical_crashes.json contains performance data for 3 crash scenarios (2022 bear market, 2021 correction, 2020 COVID crash)
2. Each crash scenario includes: date range, ETH drawdown %, average portfolio loss by correlation bracket (>90%, 80-90%, 70-80%, <70%)
3. CorrelationAgent queries historical crash data based on calculated correlation coefficient
4. Agent response includes correlation % AND historical context (e.g., "95% correlated. Portfolios with >90% correlation lost avg 73% in 2022 vs. 55% market avg")
5. Historical context is included for all 3 crash scenarios when relevant to portfolio's correlation level
6. Agent response uses plain English narrative, not raw JSON data dumps
7. Unit tests verify correct historical data retrieval for each correlation bracket
8. Historical performance claims are within ±10% of actual market data (validated against CoinGecko historical prices)

---

#### Story 1.5: SectorAgent Token-to-Sector Mapping

**As a** portfolio analyst,
**I want** SectorAgent to classify each token in my portfolio into sector categories and calculate concentration percentages,
**so that** I can see if I'm over-concentrated in high-risk sectors like DeFi governance tokens.

**Acceptance Criteria:**

1. data/sector_mappings.json maps top 30 DeFi tokens to sectors (DeFi Governance, Layer-2, Yield Protocols, DEX, Lending, Stablecoins, Layer-1 Alts)
2. SectorAgent implemented as uAgents agent with unique identifier
3. Agent accepts message containing portfolio data (tokens, amounts, values)
4. Agent maps each token to its sector using sector_mappings.json
5. Agent calculates sector concentration as % of total portfolio value in each sector
6. Agent identifies if any sector exceeds 60% concentration threshold (flagged as dangerous)
7. Agent returns sector breakdown with percentages and concentration warnings
8. Agent handles unknown tokens gracefully (returns "Unknown Sector: 15%" and logs warning)
9. Unit tests verify sector mapping accuracy and concentration calculation with known portfolios
10. Agent deployed to Agentverse testnet and responds to queries within 5 seconds

---

#### Story 1.6: SectorAgent Sector-Specific Historical Performance

**As a** portfolio analyst,
**I want** SectorAgent to show how concentrated sectors performed during historical crashes and what opportunities were missed,
**so that** I understand both the downside risk (sector crash performance) and opportunity cost (what I missed by over-concentrating).

**Acceptance Criteria:**

1. data/historical_crashes.json includes sector-specific performance for each crash scenario (% loss by sector during 2022 bear, 2021 correction, 2020 COVID)
2. data/historical_crashes.json includes opportunity cost data (best-performing sectors/tokens during recovery periods)
3. SectorAgent queries historical data for concentrated sectors (those >60% of portfolio)
4. Agent response includes sector concentration % AND historical performance (e.g., "68% in DeFi Governance. This sector lost 75% in 2022")
5. Agent response includes opportunity cost for concentrated portfolios (e.g., "While SOL gained 500% in 2023 recovery, governance tokens remained down 60%")
6. Agent response uses narrative format explaining trade-offs, not raw percentages
7. Historical claims validated against market data (±10% accuracy)
8. Unit tests verify correct historical retrieval for each sector category
9. Agent handles portfolios with no dangerous concentration (returns "Well-diversified across sectors, no concentration warnings")

---

#### Story 1.7: Specialized Agent Integration Testing

**As a** developer,
**I want** comprehensive integration tests for CorrelationAgent and SectorAgent to verify they work reliably with demo portfolios,
**so that** I have confidence both agents are production-ready before building the orchestrator.

**Acceptance Criteria:**

1. Integration test suite (tests/test_integration.py) created using pytest
2. Test invokes CorrelationAgent with each of 3 demo wallets and verifies response structure and correlation accuracy
3. Test invokes SectorAgent with each of 3 demo wallets and verifies sector breakdown and concentration detection
4. Test validates response times (<5 seconds per agent query) for all demo scenarios
5. Test verifies error handling: empty portfolio, single token, unknown tokens
6. Test confirms agents are accessible via Agentverse testnet addresses (not just local testing)
7. All 3 demo wallets return expected risk profiles (high/moderate/low risk) from both agents
8. Test logs agent responses for manual review of narrative quality
9. 100% of integration tests pass before proceeding to Epic 2
10. Test results documented in tests/README.md with sample agent responses

---

### Epic 2: Multi-Agent Orchestration & Historical Intelligence

**Epic Goal:** Implement Guardian orchestrator agent, enable inter-agent communication via uAgents message-passing, integrate MeTTa knowledge graph with historical crash scenarios, and create synthesis logic that reveals compounding risks from combining correlation and sector analysis. By the end of this epic, Guardian can consult both specialized agents and return synthesized analysis showing risks neither agent revealed alone.

---

#### Story 2.1: MeTTa Knowledge Graph Setup and Historical Data Population

**As a** Guardian orchestrator,
**I want** a MeTTa knowledge graph populated with historical crash scenarios and sector performance data,
**so that** all agents can query semantic knowledge about past market events and I can demonstrate SingularityNET technology integration.

**Acceptance Criteria:**

1. MeTTa schema designed for crash scenarios (entities: Crash, Sector, Token, CorrelationBracket; relationships: performed, during, with-correlation)
2. Hyperon Python library installed and basic MeTTa query execution tested ("hello world" query works)
3. data/metta_knowledge/ directory contains MeTTa files (.metta format) with knowledge graph data
4. Knowledge graph includes 3 crash scenarios: 2022-bear-market, 2021-correction, 2020-covid-crash
5. Each crash scenario includes: ETH drawdown, avg portfolio loss by correlation bracket, sector performance, recovery patterns
6. Sample MeTTa queries documented (e.g., "find crashes where correlation >90% AND sector-concentration >60%")
7. shared/metta_interface.py module provides query_historical_performance() function that wraps Hyperon API
8. Unit tests verify MeTTa queries return accurate results for known scenarios
9. Fallback documented: If MeTTa integration fails, can use JSON dictionary lookups (maintain functionality, lose sophistication)
10. MeTTa knowledge graph validates successfully and agents can query it programmatically

---

#### Story 2.2: Guardian Orchestrator Agent Foundation

**As a** user,
**I want** Guardian orchestrator agent that can accept portfolio input and coordinate analysis by calling specialized agents,
**so that** I get comprehensive multi-dimensional risk analysis instead of consulting individual agents separately.

**Acceptance Criteria:**

1. Guardian agent implemented as uAgents agent with unique identifier
2. Agent accepts message containing portfolio data (wallet address, token holdings)
3. Agent has registered addresses for CorrelationAgent and SectorAgent (can send messages to them)
4. Agent sends portfolio data to CorrelationAgent via uAgents message protocol
5. Agent waits for CorrelationAgent response (with timeout handling: 10-second max wait)
6. Agent sends portfolio data to SectorAgent via uAgents message protocol (can be parallel or sequential)
7. Agent waits for SectorAgent response (with timeout handling: 10-second max wait)
8. Agent logs all inter-agent messages for debugging and transparency
9. Agent returns both specialized agent responses to user (not yet synthesized, just forwarding)
10. Integration test confirms Guardian successfully calls both agents and receives responses for demo portfolios

---

#### Story 2.3: Guardian Synthesis Logic - Compounding Risk Detection

**As a** portfolio analyst,
**I want** Guardian to synthesize correlation and sector analysis to reveal compounding risks that multiply when both dimensions are dangerous,
**so that** I understand my portfolio isn't just risky on two fronts—the risks amplify each other.

**Acceptance Criteria:**

1. Guardian implements synthesis_analysis() function that takes CorrelationAgent and SectorAgent responses as input
2. Synthesis logic identifies compounding risk pattern: high correlation (>85%) + high sector concentration (>60%) = amplified risk
3. Synthesis calculates risk multiplier effect (not just additive): correlation risk × sector risk = compounding effect
4. Synthesis generates narrative explaining interaction: "Your 3x ETH leverage + 68% governance concentration creates compounding risk. In 2022, this structure lost 75% (not just 60% from correlation alone)"
5. Synthesis queries MeTTa for portfolios with similar dual-risk structure during historical crashes
6. Synthesis response is presented as cohesive narrative, not bullet points from two agents
7. Synthesis highlights insights not visible in individual agent responses (the "lean forward moment")
8. For well-diversified portfolios, synthesis confirms low compounding risk and explains why
9. Unit tests verify synthesis correctly identifies compounding risk patterns with test data
10. Manual testing confirms synthesis creates "aha moment" where user realizes hidden risk structure

---

#### Story 2.4: Guardian Actionable Recommendations Generation

**As a** portfolio analyst,
**I want** Guardian to conclude analysis with 2-3 specific, actionable recommendations based on identified risks,
**so that** I know exactly what steps to take to improve my portfolio structure.

**Acceptance Criteria:**

1. Guardian implements generate_recommendations() function based on risk findings
2. For high correlation: recommend adding uncorrelated assets (BTC, SOL, stablecoins) with specific allocation suggestions
3. For high sector concentration: recommend reducing overweighted sector below 40% threshold
4. For compounding risk: recommend prioritizing sector diversification first (bigger impact than correlation reduction)
5. For well-diversified portfolios: acknowledge good structure and recommend monitoring frequency
6. Recommendations are specific (e.g., "Reduce governance token concentration from 68% to <40%") not vague ("diversify more")
7. Each recommendation includes brief rationale explaining why it reduces specific risk
8. Recommendations numbered (1, 2, 3) for clarity and prioritized by impact
9. Recommendations avoid specific token picks or investment advice (stays in risk analysis domain)
10. Integration tests verify appropriate recommendations generated for each demo wallet's risk profile

---

#### Story 2.5: Multi-Agent Response Transparency and Logging

**As a** user and hackathon judge,
**I want** to see individual agent contributions (CorrelationAgent response, SectorAgent response) alongside Guardian's synthesis,
**so that** I understand how multi-agent collaboration produced the final analysis and can trust the reasoning.

**Acceptance Criteria:**

1. Guardian response structure includes three sections: (1) CorrelationAgent Analysis, (2) SectorAgent Analysis, (3) Guardian Synthesis & Recommendations
2. Each specialized agent response is presented verbatim (not summarized or paraphrased by Guardian)
3. Response formatting clearly delineates which agent contributed what (using headers or labels)
4. Guardian synthesis section explicitly references insights from both agents: "As CorrelationAgent showed... and SectorAgent revealed..."
5. Agent addresses included in response (e.g., "Consulted CorrelationAgent at agent1qw...") for verifiability
6. Response timing logged: time taken by each agent, total analysis duration
7. Error transparency: if an agent fails or times out, Guardian explains what happened rather than silently omitting it
8. Manual testing confirms judges can clearly see multi-agent collaboration (not black box)
9. Documentation includes sample response showing transparency structure
10. Response format is readable and engaging (narrative flow), not robotic message passing logs

---

#### Story 2.6: End-to-End Multi-Agent Integration Testing

**As a** developer,
**I want** comprehensive end-to-end tests covering full Guardian orchestration workflow with both specialized agents and MeTTa queries,
**so that** I have confidence the complete multi-agent system works reliably before deploying to production.

**Acceptance Criteria:**

1. Integration test suite tests/test_integration.py expanded with Guardian orchestration scenarios
2. Test sends portfolio to Guardian and verifies it calls both CorrelationAgent and SectorAgent
3. Test confirms Guardian synthesis contains insights not present in individual agent responses
4. Test verifies MeTTa queries execute successfully and historical data appears in responses
5. Test validates end-to-end timing: <60 seconds from portfolio input to final recommendations
6. Test covers timeout scenario: if CorrelationAgent doesn't respond in 10 seconds, Guardian proceeds with SectorAgent only
7. Test covers partial data scenario: unknown tokens don't crash analysis, "insufficient data" message appears gracefully
8. Test confirms all 3 demo wallets produce expected risk narratives (high/moderate/low risk synthesis)
9. Test logs complete responses for manual review of synthesis quality and narrative coherence
10. 100% of critical path integration tests pass with all agents deployed on Agentverse testnet

---

### Epic 3: Production Deployment & User Experience

**Epic Goal:** Integrate Chat Protocol for ASI:One conversational interface, deploy all agents to Agentverse production environment, create polished demo scenarios and comprehensive documentation, and produce demo video and submission materials for hackathon judging. By the end of this epic, Guardian is accessible via ASI:One, judges can test independently, and hackathon submission is complete.

---

#### Story 3.1: Chat Protocol Integration for ASI:One Interface

**As a** user,
**I want** to interact with Guardian via natural language conversation through ASI:One interface,
**so that** I can ask about portfolio risk in plain English without learning API formats or agent addresses.

**Acceptance Criteria:**

1. Guardian agent implements Fetch.ai Chat Protocol following ASI:One compatibility guide from Innovation Lab
2. Guardian accepts conversational text input: "Analyze my portfolio at 0xabc123..." or "How risky is wallet 0xabc123?"
3. Guardian parses natural language input to extract wallet address (basic regex or keyword matching)
4. Guardian responds with conversational narrative (not JSON or structured data dumps)
5. Guardian supports follow-up questions in same session: "Why is governance concentration dangerous?" or "What should I do?"
6. Guardian maintains context from previous analysis within conversation session (stateless per-session, not persistent)
7. Guardian handles unclear input gracefully: "I need a wallet address to analyze. Please provide an Ethereum address (0x...)"
8. Guardian can be discovered in ASI:One agent directory (proper README and metadata for discoverability)
9. Manual testing via ASI:One interface confirms conversational flow feels natural
10. Documentation includes sample conversation transcript showing user queries and Guardian responses

---

#### Story 3.2: Production Deployment to Agentverse

**As a** hackathon judge and user,
**I want** all three agents deployed to Agentverse production environment with stable public addresses,
**so that** I can interact with Guardian reliably without depending on developer's local environment.

**Acceptance Criteria:**

1. CorrelationAgent deployed to Agentverse production with unique public address (agent1qw...)
2. SectorAgent deployed to Agentverse production with unique public address (agent1qx...)
3. Guardian deployed to Agentverse production with unique public address (agent1qy...)
4. All agents configured with production data (demo wallets, historical crashes, sector mappings, MeTTa knowledge)
5. Agent addresses documented in README.md and DEMO.md for judge access
6. Smoke tests confirm all agents are online and responding (query each agent directly as sanity check)
7. Inter-agent communication verified in production: Guardian successfully calls CorrelationAgent and SectorAgent on Agentverse
8. Chat Protocol verified in production: Guardian accessible via ASI:One interface and responds to queries
9. Performance verified: end-to-end analysis completes in <60 seconds for demo wallets
10. Production deployment does not require developer intervention (agents run autonomously on Agentverse)

---

#### Story 3.3: Demo Wallet Scenarios and Expected Analysis Refinement

**As a** developer and presenter,
**I want** 3 polished demo wallet scenarios with pre-validated expected analysis outcomes,
**so that** I can confidently demonstrate Guardian during judging and ensure the analysis narratives showcase the "lean forward moment."

**Acceptance Criteria:**

1. Demo Wallet 1 (High Risk): Portfolio with >90% ETH correlation + >65% DeFi governance concentration, demonstrates clear compounding risk
2. Demo Wallet 2 (Moderate Risk): Portfolio with 80-85% correlation + moderate sector concentration (40-50%), shows some risk but not alarming
3. Demo Wallet 3 (Well-Diversified): Portfolio with <70% correlation + no sector >30%, demonstrates Guardian confirms good structure
4. Each demo wallet is a real Ethereum address (verifiable on Etherscan) with historically held positions
5. Expected analysis outcomes documented for each wallet: correlation %, sector breakdown, synthesis insight, recommendations
6. Actual Guardian analysis tested and compared to expected outcomes (accuracy validated)
7. Narrative quality manually reviewed: does synthesis create "aha moment"? Are recommendations clear and actionable?
8. Demo wallet documentation includes backstory: why this portfolio structure is common among DeFi investors
9. Timing validated: each demo wallet analysis completes in 45-60 seconds consistently
10. Demo script written: exact queries to run, expected responses, points to highlight during judging

---

#### Story 3.4: Comprehensive Documentation for Judge Self-Service

**As a** hackathon judge,
**I want** complete documentation covering architecture, agent addresses, sample interactions, and testing instructions,
**so that** I can evaluate Guardian independently without creator assistance.

**Acceptance Criteria:**

1. README.md includes project overview, value proposition (risk blindness problem), multi-agent architecture diagram
2. README.md includes agent addresses (Guardian, CorrelationAgent, SectorAgent) with instructions to query via ASI:One
3. README.md includes 3 demo wallet addresses and what risk profile to expect from each
4. README.md includes sample conversation showing full analysis flow with actual agent responses
5. ARCHITECTURE.md explains multi-agent design: why distributed, how agents communicate, MeTTa integration, synthesis logic
6. ARCHITECTURE.md includes architecture diagram (hand-drawn or simple tool) showing user → Guardian → CorrelationAgent/SectorAgent → MeTTa
7. DEMO.md provides step-by-step testing instructions: how to access ASI:One, what to type, what Guardian should respond
8. docs/sample-responses/ directory includes full agent responses for each demo wallet (judges can compare their results)
9. All documentation follows Innovation Lab README best practices for agent discoverability
10. Documentation reviewed by someone unfamiliar with project—can they test Guardian successfully?

---

#### Story 3.5: Demo Video Production

**As a** hackathon judge,
**I want** a 3-5 minute demo video showing Guardian's complete user experience and multi-agent collaboration,
**so that** I can understand the product vision and see it working even if live system has issues during judging.

**Acceptance Criteria:**

1. Demo video script written covering: (1) problem intro (risk blindness), (2) solution (multi-agent intelligence), (3) live demo, (4) architecture, (5) impact
2. Screen recording shows ASI:One interface with Guardian conversation for one demo wallet (high-risk portfolio)
3. Video shows progressive disclosure: correlation reveal → sector reveal → synthesis "aha moment" → recommendations
4. Video includes brief architecture explanation: show code/agent structure, explain multi-agent collaboration
5. Video shows transparency: individual agent responses visible before synthesis
6. Video includes MeTTa query example (show knowledge graph being queried for historical context)
7. Voiceover explains what's happening at each step (not just silent screen recording)
8. Video duration: 3-5 minutes (concise, respects judges' time)
9. Video quality: clear audio, readable text, smooth pacing (not rushed)
10. Video uploaded to YouTube/Vimeo and link included in README.md

---

#### Story 3.6: Final Integration Testing and Bug Fixing

**As a** developer,
**I want** dedicated time for end-to-end testing, edge case exploration, and bug fixing before submission,
**so that** judges encounter a polished, reliable system without crashes or confusing errors.

**Acceptance Criteria:**

1. Complete end-to-end test runs for all 3 demo wallets via ASI:One interface (not just agent-to-agent testing)
2. Edge cases tested: empty portfolio, single token, all unknown tokens, extremely high/low correlation
3. Error messages validated: are they helpful? Do they explain what went wrong and what to do?
4. Response quality reviewed: narrative coherent? Grammar/spelling correct? Synthesis creates "aha moment"?
5. Performance validated: all demo analyses complete in <60 seconds consistently (run 10 times each)
6. Inter-agent communication reliability tested: run 20+ analyses back-to-back, confirm >95% success rate
7. Timeout handling validated: if an agent is slow, Guardian doesn't crash, provides partial analysis or clear error
8. Documentation accuracy verified: do agent addresses work? Are sample responses up-to-date?
9. Bug list triaged: critical bugs fixed (crash, wrong analysis), minor bugs documented as known issues
10. Submission readiness checklist completed: code committed, documentation finalized, demo video uploaded, all agents online

---

## Checklist Results Report

*[This section will be populated after executing the pm-checklist]*

---

## Next Steps

### UX Expert Prompt

*[This section will contain the prompt for the UX Expert to create architecture using this document as input]*

### Architect Prompt

*[This section will contain the prompt for the Architect to create architecture using this document as input]*
