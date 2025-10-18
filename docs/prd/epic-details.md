# Epic Details

## Epic 1: Foundation & Specialized Agent Intelligence

**Epic Goal:** Establish project infrastructure, learn the uAgents framework, and implement two specialized analysis agents (CorrelationAgent and SectorAgent) that can independently analyze portfolio structure and deliver basic risk insights. By the end of this epic, both agents are deployed to Agentverse testnet and can be invoked independently to analyze demo portfolios.

---

### Story 1.1: Project Setup and uAgents Framework Learning

**As a** developer,
**I want** a working development environment with uAgents framework configured and basic "hello world" agent tested,
**so that** I can build production agents confidently and understand framework capabilities before implementing Guardian's business logic.

**Acceptance Criteria:**

1. Python 3.10+ virtual environment created with all dependencies installed (uAgents, Pandas, NumPy, pytest)
2. GitHub repository initialized with monorepo structure (agents/, data/, tests/, docs/ folders)
3. requirements.txt file documents all Python dependencies with pinned versions
4. .env.example file created with all required environment variables documented (agent addresses, timeouts, thresholds, logging configuration)
5. GitHub Actions workflow configured (.github/workflows/ci.yml) to run automated tests on push and pull requests
6. GitHub Actions workflow includes linting (ruff), type checking (mypy), and pytest execution with coverage reporting
7. "Hello World" agent successfully created following Innovation Lab guide and deployed to Agentverse testnet
8. Basic inter-agent communication example from Innovation Lab works (two test agents exchange messages successfully)
9. Git repository has initial commit with project structure and working hello world example
10. README.md includes environment setup instructions and links to uAgents documentation
11. Developer can explain uAgents message-passing pattern and agent registration process

---

### Story 1.2: Portfolio Data Structure and Demo Wallet Configuration

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

### Story 1.3: CorrelationAgent ETH Correlation Calculation

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

### Story 1.4: CorrelationAgent Historical Crash Context

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

### Story 1.5: SectorAgent Token-to-Sector Mapping

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

### Story 1.6: SectorAgent Sector-Specific Historical Performance

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

### Story 1.7: Specialized Agent Integration Testing

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

## Epic 2: Multi-Agent Orchestration & Historical Intelligence

**Epic Goal:** Implement Guardian orchestrator agent, enable inter-agent communication via uAgents message-passing, integrate MeTTa knowledge graph with historical crash scenarios, and create synthesis logic that reveals compounding risks from combining correlation and sector analysis. By the end of this epic, Guardian can consult both specialized agents and return synthesized analysis showing risks neither agent revealed alone.

---

### Story 2.1: MeTTa Knowledge Graph Setup and Historical Data Population

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

### Story 2.2: Guardian Orchestrator Agent Foundation

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

### Story 2.3: Guardian Synthesis Logic - Compounding Risk Detection

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

### Story 2.4: Guardian Actionable Recommendations Generation

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

### Story 2.5: Multi-Agent Response Transparency and Logging

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

### Story 2.6: End-to-End Multi-Agent Integration Testing

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

## Epic 3: Production Deployment & User Experience

**Epic Goal:** Integrate Chat Protocol for ASI:One conversational interface, deploy all agents to Agentverse production environment, create polished demo scenarios and comprehensive documentation, and produce demo video and submission materials for hackathon judging. By the end of this epic, Guardian is accessible via ASI:One, judges can test independently, and hackathon submission is complete.

---

### Story 3.1: Chat Protocol Integration for ASI:One Interface

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

### Story 3.2: Production Deployment to Agentverse

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

### Story 3.3: Demo Wallet Scenarios and Expected Analysis Refinement

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

### Story 3.4: Comprehensive Documentation for Judge Self-Service

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

### Story 3.5: Demo Video Production

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

### Story 3.6: Final Integration Testing and Bug Fixing

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
