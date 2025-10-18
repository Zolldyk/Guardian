# Requirements

## Functional Requirements

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

## Non-Functional Requirements

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
