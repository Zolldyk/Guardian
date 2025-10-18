# Project Brief: Guardian

**DeFi Portfolio Intelligence Agent**

**Version:** 1.0
**Date:** October 18, 2025
**Status:** Ready for Execution

---

## Executive Summary

Guardian is a DeFi portfolio intelligence agent that reveals hidden risks in cryptocurrency portfolios through multi-agent collaboration. Built for the ASI Alliance Hackathon, Guardian uses three specialized agents (Guardian orchestrator, CorrelationAgent, SectorAgent) to expose risk blindness—the dangerous illusion of diversification when portfolios are actually highly correlated and concentrated.

**The Problem:** DeFi investors believe they're diversified by holding 10-15 different tokens, but discover during market crashes that everything drops together. The typical scenario: "I thought I was diversified but everything crashed 70% overnight."

**The Solution:** Guardian analyzes portfolios through two dimensions—correlation structure and sector concentration—revealing compounding risks that traditional portfolio trackers miss. Using historical crash simulations (the "time-machine approach"), Guardian shows what would have happened to your exact portfolio structure during past market events.

**Target Market:** DeFi investors managing self-custody portfolios who need judgment and interpretation, not just data dashboards.

**Key Value Proposition:** Guardian transforms abstract risk metrics into visceral understanding through multi-agent intelligence that synthesizes correlation exposure, sector concentration, and historical context into a single actionable insight: "Your portfolio looks diversified but you're actually 3x leveraged on ETH with 68% concentration in the worst-performing sector."

---

## Problem Statement

### Current State: The Illusion of Diversification

DeFi investors face a critical knowledge gap: they believe portfolio diversification means holding multiple different tokens, when in reality, most DeFi portfolios are structurally identical. A typical investor holds 10-15 tokens across different protocols and thinks they're protected from market downturns. They check their portfolio and see variety: governance tokens, DeFi protocols, layer-2 solutions, and yield optimizers.

Then a market crash happens. Ethereum drops 20%. Their "diversified" portfolio drops 60-75%. The painful realization: "I thought I was diversified, but everything crashed together."

### The Impact: Catastrophic Losses from Hidden Risk

This isn't a minor inconvenience—it's the difference between surviving market cycles and catastrophic losses:

- **Correlation blindness:** Investors don't realize that 95% correlation to ETH means 3x leveraged exposure. A 20% ETH drop becomes a 60% portfolio drop.
- **Sector concentration:** Holding 12 different tokens means nothing if 9 of them are DeFi governance tokens that all collapse together. Historical data shows portfolios with >60% governance token concentration lost an average of 75% during the 2022 bear market.
- **Compounding risk:** These two dimensions multiply. High ETH correlation + high sector concentration doesn't add risk—it compounds it. The same portfolio structure that would lose 60% from correlation alone loses 75% when sector concentration amplifies the damage.

The financial impact is measurable: investors following this pattern routinely experience 70%+ drawdowns in corrections where Bitcoin drops 40%. They're taking 2x the risk without understanding why.

### Why Existing Solutions Fall Short

Current portfolio tools fail because they treat this as a data problem when it's actually a judgment problem:

- **Portfolio trackers** (Zerion, Zapper, DeBank) show what you own but not what it means. They display token lists and total value but provide no structural analysis of correlation or concentration.
- **Analytics platforms** (Dune, Nansen) provide sophisticated data for researchers but require users to build their own queries and interpret raw statistics. The insight gap remains.
- **Traditional portfolio tools** (Morningstar, Personal Capital) don't understand crypto correlation structures or DeFi-specific sector dynamics.

None of these tools answer the fundamental question: "What does my portfolio structure actually mean for my risk exposure?"

### Why This Matters Now

The DeFi ecosystem is maturing, with institutional capital entering and retail investors managing increasingly large self-custody portfolios. The stakes are higher—individual portfolios worth $50K-$500K are common. But portfolio intelligence hasn't evolved beyond "track your tokens and show pretty charts."

Meanwhile, market volatility remains extreme. The tools to prevent 70% portfolio crashes exist (correlation analysis, sector mapping, historical simulation), but they're not accessible to the investors who need them most. Risk blindness isn't a data availability problem—it's an intelligence gap.

---

## Proposed Solution

### Core Concept: Multi-Agent Intelligence for Two-Dimensional Risk Analysis

Guardian solves risk blindness by transforming portfolio analysis from a data display problem into an intelligence synthesis problem. Instead of showing users what they own, Guardian reveals what their portfolio structure means through coordinated analysis across two critical dimensions:

1. **Correlation Structure Analysis:** Exposing hidden leverage through correlation to market anchors (primarily ETH)
2. **Sector Concentration Analysis:** Identifying dangerous concentration in high-risk categories (governance tokens, yield protocols, etc.)
3. **Synthesis:** Revealing how these two dimensions compound during market stress

Guardian achieves this through a multi-agent architecture where specialized agents analyze different risk dimensions, then an orchestrator synthesizes findings into a single coherent narrative. This isn't just architectural elegance—it's necessary because correlation analysis and sector classification require fundamentally different knowledge domains.

### Key Differentiators

#### 1. The "Time Machine" Approach: Historical Context as Default

Guardian doesn't present risk as abstract statistics. Instead, every analysis includes historical simulation: "Your portfolio is 95% correlated to ETH" becomes "Your portfolio is 95% correlated to ETH. In the 2022 crash, portfolios with this correlation structure lost 73% compared to 55% for the market."

This approach:
- Makes abstract risk visceral and urgent
- Provides concrete reference points users can verify
- Shows both what happened (past crashes) and what didn't happen (opportunity cost from missed gains)
- Embeds intelligence directly in agent responses rather than requiring separate analysis

#### 2. Judgment Engine, Not Data Dashboard

Guardian interprets rather than displays. The value proposition isn't "here's more data" but "here's what this data means for YOUR specific situation."

Where existing tools show:
- "Portfolio value: $47,382"
- "12 tokens across 8 protocols"
- "30-day return: -12%"

Guardian reveals:
- "Your portfolio LOOKS diversified (12 tokens) but IS 3x leveraged on ETH"
- "68% concentrated in DeFi governance tokens—the worst-performing sector in 2022"
- "These risks compound: when ETH drops 20%, you don't lose 60% (from leverage alone), you lose 75% because your sector amplifies the damage"

#### 3. Compounding Risk Synthesis

The critical innovation is synthesis. Correlation analysis alone shows half the picture. Sector analysis alone misses structural dependencies. Guardian's orchestrator combines both dimensions to reveal compounding effects that neither agent could identify alone.

This creates the "lean forward moment": users think they understand their portfolio (or assume tools have already told them everything), then Guardian shows them a risk structure they didn't know existed.

#### 4. Multi-Agent Collaboration with Specialized Knowledge

Each agent maintains domain-specific knowledge:
- **CorrelationAgent:** Historical crash data, correlation patterns, leverage calculations
- **SectorAgent:** Token-to-sector mappings, sector performance history, opportunity cost analysis
- **Guardian Orchestrator:** Synthesis logic, narrative construction, user interaction via conversational interface

This distribution of intelligence means insights emerge from collaboration, not from a single monolithic analysis engine. The architecture demonstrates the ASI Alliance vision: specialized agents working together to produce intelligence greater than any single agent could achieve.

### Why This Solution Will Succeed

Guardian succeeds where others fail because it addresses the root cause: existing tools assume users need more data when they actually need better judgment applied to existing data.

The solution is designed around three user truths:
1. **Users don't know what they don't know:** You can't search for "correlation risk" if you don't know it exists. Guardian reveals risks proactively.
2. **Abstract statistics don't change behavior:** Telling someone "95% correlation" doesn't create urgency. Telling them "you would have lost 73% in 2022" does.
3. **Synthesis is more valuable than raw analysis:** The insight isn't in knowing your correlation OR your sector concentration—it's in understanding how they interact.

### High-Level Product Vision

Guardian is a conversational intelligence agent accessible through the ASI:One chat interface. Users connect their wallet, ask "How risky is my portfolio?", and Guardian orchestrates a real-time analysis by consulting specialized risk agents, then synthesizes findings into a clear narrative with historical context.

The experience is:
1. **Conversational:** Natural language interaction, not forms or dashboards
2. **Proactive:** Guardian identifies risks users didn't ask about
3. **Contextual:** Every metric includes "what this means for you" interpretation
4. **Actionable:** Analysis concludes with specific recommendations, not just observations
5. **Transparent:** Users can see which agents were consulted and what each contributed

The MVP proves the core concept: multi-agent risk intelligence that reveals hidden portfolio structure. Post-MVP, Guardian evolves into a continuous monitoring system, proactive alerting engine, and eventually an execution layer for rebalancing recommendations.

---

## Target Users

### Primary User Segment: Self-Directed DeFi Investors

**Demographic/Profile:**
- Age: 25-45 years old
- Technical comfort: High (comfortable with MetaMask, DEXs, smart contract interaction)
- Crypto experience: 2-5 years in the space
- Portfolio size: $50K-$500K in self-custody DeFi positions
- Location: Global, but concentrated in crypto-friendly regions (US, Europe, Asia)
- Occupation: Tech workers, entrepreneurs, finance professionals who manage crypto as side portfolio

**Current Behaviors and Workflows:**
- Manages 8-20 different token positions across multiple protocols (Aave, Uniswap, Compound, etc.)
- Checks portfolio daily using tools like Zerion, Zapper, or DeBank to see total value and individual holdings
- Makes investment decisions based on Twitter/CT (Crypto Twitter) research, Discord communities, and protocol documentation
- Rebalances manually 1-2 times per month based on gut feel or price movements
- Tracks positions in spreadsheets or notes apps to remember cost basis and strategy rationale
- Experiences anxiety during market volatility but lacks framework for evaluating actual risk exposure

**Specific Needs and Pain Points:**
- **"I don't know what I don't know":** Aware that portfolio might be risky but lacks tools to identify hidden structural risks
- **Analysis paralysis:** Has access to endless data (Dune dashboards, on-chain analytics) but struggles to synthesize it into actionable decisions
- **False confidence from diversification:** Believes holding 12+ different tokens provides safety, unaware of correlation and sector concentration
- **Missed the 2022 crash lessons:** Either experienced catastrophic losses and wants to prevent recurrence, or got lucky and doesn't understand why others suffered
- **Time constraints:** Can't spend 10+ hours per week doing sophisticated portfolio analysis; needs intelligence, not more raw data
- **Trust gap with centralized tools:** Prefers self-custody and decentralized solutions but acknowledges need for smarter analysis tools

**Goals They're Trying to Achieve:**
- **Primary goal:** Preserve capital during market downturns while maintaining upside exposure
- **Secondary goal:** Make informed rebalancing decisions based on risk assessment, not emotions
- **Tertiary goal:** Understand portfolio structure well enough to explain it to others (or themselves in 6 months)
- **Aspiration:** Build a portfolio that survives multiple market cycles and compounds wealth over 3-5 year timeframe

---

### Secondary User Segment: Crypto-Native Financial Advisors

**Demographic/Profile:**
- Age: 28-50 years old
- Professional role: Independent financial advisors, crypto portfolio managers, or Web3 consultants serving 5-50 clients
- Portfolio under management: $500K-$10M across client wallets
- Location: Global, operating remotely
- Background: Traditional finance + crypto expertise, or crypto-native building advisory practices

**Current Behaviors and Workflows:**
- Manages multiple client wallets with varying risk profiles and investment theses
- Conducts manual portfolio reviews monthly or quarterly, producing reports in Google Docs/Notion
- Uses combination of portfolio trackers, spreadsheets, and custom Python scripts for analysis
- Struggles to scale personalized analysis—each client review takes 2-4 hours
- Seeks differentiation from traditional advisors who don't understand DeFi correlation dynamics
- Needs tools that produce client-ready explanations, not just internal analytics

**Specific Needs and Pain Points:**
- **Scalability challenge:** Can't manually analyze correlation and sector concentration for 20+ client portfolios
- **Client education burden:** Spends significant time explaining why diversification ≠ holding multiple tokens
- **Competitive differentiation:** Needs sophisticated analysis to justify advisory fees versus "just use Zapper"
- **Regulatory/fiduciary concerns:** Must demonstrate due diligence in risk assessment for client protection
- **Standardization vs. personalization:** Wants consistent framework (correlation + sector analysis) but customized insights per client

**Goals They're Trying to Achieve:**
- **Primary goal:** Provide defensible risk analysis that protects clients and demonstrates professional value
- **Secondary goal:** Scale advisory practice without linearly increasing analysis time per client
- **Tertiary goal:** Educate clients about DeFi portfolio dynamics in clear, compelling terms
- **Aspiration:** Build reputation as the "sophisticated DeFi portfolio advisor" who prevents client disasters

---

## Goals & Success Metrics

### Business Objectives

- **Win ASI Alliance Hackathon top prize** by demonstrating best-in-class multi-agent collaboration and meaningful use of the full ASI Alliance tech stack (uAgents, MeTTa, Agentverse, Chat Protocol) - Target: Top 3 placement by November 2025

- **Validate product-market fit for DeFi risk intelligence** through demo feedback and post-hackathon user interest - Target: 50+ requests for beta access or 10+ substantive conversations with potential users within 2 weeks of hackathon conclusion

- **Establish Guardian as reference implementation** for multi-agent financial analysis in the ASI ecosystem - Target: Mention in ASI Alliance documentation or community showcases within 3 months post-hackathon

- **Build foundation for post-hackathon product development** by creating clean, extensible architecture that can evolve from demo to production - Target: 80% of MVP codebase reusable for production version

### User Success Metrics

- **Risk revelation rate:** % of analyzed portfolios where Guardian identifies hidden correlation or sector concentration risks not visible in standard portfolio trackers - Target: 85%+ of demo scenarios show meaningful risk insights

- **Comprehension improvement:** Users understand their portfolio risk structure after Guardian analysis - Measured by ability to articulate "my portfolio is X% correlated to ETH" or similar structural insights - Target: 90%+ comprehension in user testing

- **"Lean forward" moment creation:** Analysis produces at least one insight that surprises or concerns the user - Target: 100% of demo sessions include user reaction indicating new awareness

- **Actionability:** Users can state specific next steps based on Guardian's analysis (e.g., "I need to reduce governance token exposure" or "I should add uncorrelated assets") - Target: 100% of sessions conclude with clear action items

- **Time to insight:** Complete risk analysis delivered within 60 seconds of wallet submission - Target: <60 seconds for demo scenarios with pre-loaded data

### Key Performance Indicators (KPIs)

**Hackathon Technical KPIs:**
- **Agent deployment success:** All 3 agents (Guardian, CorrelationAgent, SectorAgent) successfully deployed to Agentverse and accessible via unique addresses - Target: 100% deployment success
- **Inter-agent communication reliability:** Messages between Guardian and specialized agents complete without errors - Target: 100% success rate across 20+ test scenarios
- **MeTTa query execution:** Historical context queries return accurate results with reasoning - Target: 100% accuracy for pre-defined crash scenarios (2022 bear, 2021 correction, 2020 COVID)
- **Chat Protocol integration:** Guardian responds correctly to user queries via ASI:One interface - Target: 100% response rate with <5 second latency

**Demo Quality KPIs:**
- **Video demo completion:** 3-5 minute demo video showing complete user flow from wallet input to actionable recommendations - Target: Completed by Day 8, duration 3-5 minutes
- **Narrative arc clarity:** Demo shows clear progression: surface analysis → first reveal (correlation) → second reveal (sector) → synthesis → recommendations - Target: 100% of test viewers can describe the arc
- **Technical demonstration:** Demo clearly shows multi-agent collaboration (not black box) with visible agent responses - Target: All 3 agents' contributions visible in demo
- **Documentation completeness:** README with agent addresses, interaction instructions, and architecture explanation - Target: 100% completeness (can be used by judges without creator assistance)

**Product Validation KPIs:**
- **Risk identification accuracy:** % of known risky portfolios (high correlation + high sector concentration) correctly identified by Guardian - Target: 100% for demo wallets, 90%+ for unseen test cases
- **Historical simulation accuracy:** Crash scenario results match actual historical performance within ±10% - Target: ±10% accuracy for 2022 bear market simulation
- **Synthesis quality:** Guardian's combined analysis (correlation + sector → compounding risk) is non-obvious and adds value beyond individual agent outputs - Target: 100% of test cases show synthesis insights not present in individual analyses
- **False positive rate:** % of well-diversified portfolios incorrectly flagged as high-risk - Target: <10% false positives

**Post-Hackathon Traction KPIs:**
- **Community engagement:** GitHub stars, Twitter mentions, or ASI community discussion - Target: 50+ GitHub stars or 100+ social mentions within 30 days
- **Beta interest:** Number of users requesting access to production version - Target: 50+ beta requests within 2 weeks
- **Partnership conversations:** Engagement from potential partners (portfolio tools, protocols, advisors) - Target: 5+ substantive conversations within 1 month

---

## MVP Scope

### Core Features (Must Have)

- **Three-Agent Architecture:** Guardian orchestrator + CorrelationAgent + SectorAgent deployed to Agentverse with real inter-agent communication, not mocked. Each agent has distinct address and can be queried independently. Rationale: Multi-agent collaboration is the core hackathon differentiator and technical requirement.

- **Correlation Risk Analysis:** CorrelationAgent calculates portfolio correlation to ETH using historical price data and returns correlation coefficient + historical crash performance. Example output: "95% correlated to ETH. In 2022 crash, portfolios with this structure lost 73% vs. 55% market average." Rationale: Reveals hidden leverage that users can't see in standard trackers.

- **Sector Concentration Analysis:** SectorAgent maps tokens to sectors (DeFi governance, layer-2, yield, etc.) and identifies dangerous concentration. Example output: "68% in DeFi governance tokens. This sector lost 75% in 2022 while SOL gained 500% in 2023." Rationale: Shows opportunity cost and sector-specific amplification risk.

- **Compounding Risk Synthesis:** Guardian combines correlation + sector insights to reveal how risks multiply. Example output: "Your correlation (3x ETH leverage) + sector concentration creates compounding risk. In 2022, this exact structure would have lost 75%, not just 60%." Rationale: The synthesis is the core intelligence that neither individual agent provides.

- **MeTTa Historical Intelligence:** Pre-populated MeTTa knowledge graph with 3 major crash scenarios (2022 bear market, 2021 correction, 2020 COVID crash) including correlation performance, sector performance, and opportunity cost data. Agents query MeTTa to ground responses in historical patterns. Rationale: Demonstrates meaningful SingularityNET tech usage and creates the "time machine" signature move.

- **Chat Protocol Integration:** Guardian accessible via ASI:One conversational interface. Users input wallet address, ask questions in natural language, receive narrative responses (not JSON or raw data). Rationale: Shows Fetch.ai Chat Protocol integration and creates user-friendly interaction model.

- **Demo Wallet Scenarios:** 2-3 hardcoded wallet addresses with pre-analyzed portfolios representing clear risk patterns (high correlation + high sector concentration, well-diversified portfolio, moderate risk). Portfolio data stored locally, not fetched from blockchain APIs. Rationale: Ensures reliable demo, eliminates API dependencies, allows crafting perfect narrative arc.

- **Agent Response Transparency:** When Guardian consults CorrelationAgent or SectorAgent, the individual agent responses are visible to users (not hidden in backend). Users can see what each agent contributed to the final synthesis. Rationale: Demonstrates multi-agent collaboration visibly, important for hackathon judging.

- **Actionable Recommendations:** Every analysis concludes with 2-3 specific recommendations based on risk findings. Example: "Reduce governance token concentration below 40%", "Add SOL or BTC for uncorrelated exposure", "Consider this portfolio high-risk for holding through volatility." Rationale: Ensures analysis is actionable, not just informational.

- **Documentation & Deployment:** Complete README with agent addresses, sample queries, architecture diagram, and instructions for interacting via ASI:One. All agents deployed to Agentverse with publicly accessible addresses. Rationale: Judges must be able to test without creator assistance; production-ready deployment proves technical competence.

### Out of Scope for MVP

- **Real-time blockchain data fetching:** No integration with Etherscan, Alchemy, or other blockchain APIs. Portfolio data is hardcoded for demo scenarios. (Post-MVP: Days/weeks of API integration work)

- **User authentication or wallet connection:** No MetaMask integration, no wallet signing. Users provide wallet address as text input. (Post-MVP: Can add Web3 wallet connection)

- **Continuous monitoring or alerting:** Guardian analyzes on-demand only, no background monitoring or push notifications when risk thresholds are crossed. (Post-MVP: Requires persistent monitoring infrastructure)

- **Rebalancing execution:** No ability to execute trades or connect to DEXs. Recommendations are advisory only. (Post-MVP: 4th agent for execution with significant complexity)

- **Multi-chain support:** Ethereum/ERC-20 tokens only. No Solana, Polygon, Arbitrum, or other chains. (Post-MVP: Requires multi-chain data sources and correlation models)

- **Unlimited token coverage:** MeTTa knowledge limited to top 20-30 DeFi tokens with pre-defined sector classifications. Unknown/obscure tokens return "insufficient data" message. (Post-MVP: Can expand knowledge graph incrementally)

- **Custom portfolio hypotheticals:** Users can't input "what if I had X% in Y token" scenarios. Analysis is for actual wallet addresses only. (Post-MVP: Portfolio simulation feature)

- **Gas optimization analysis:** No analysis of transaction costs or optimal rebalancing strategies considering gas fees. (Post-MVP: Requires DEX integration and gas modeling)

- **Historical backtesting UI:** No interactive timeline or slider to explore "what if you held this portfolio during X crash." Historical context is embedded in responses only. (Post-MVP: Rich visualization feature)

- **Social/collaborative features:** No ability to compare your portfolio to others, no community insights, no shared analysis. Single-user analysis only. (Post-MVP: Requires privacy considerations and data aggregation)

### MVP Success Criteria

The MVP is successful when:

1. **All 3 agents are deployed to Agentverse** with unique addresses and respond to queries independently
2. **Inter-agent communication works reliably** with Guardian calling CorrelationAgent and SectorAgent in real-time (not pre-cached)
3. **MeTTa queries return accurate historical context** for all pre-defined crash scenarios
4. **Demo shows complete narrative arc** from wallet input → correlation reveal → sector reveal → synthesis → recommendations in under 2 minutes
5. **Judges can interact with Guardian via ASI:One** using the demo wallet addresses without creator assistance
6. **Documentation is complete** with architecture explanation, agent addresses, and sample interaction flows
7. **At least one demo scenario produces the "lean forward moment"** where synthesis reveals compounding risk not obvious from individual analyses

The MVP demonstrates that multi-agent DeFi risk intelligence is viable, valuable, and built on the ASI Alliance tech stack. It proves the concept while maintaining realistic scope for 10-day solo development.

---

## Post-MVP Vision

### Phase 2 Features (Next 3-6 Months)

**Real-Time Portfolio Fetching**
Replace hardcoded demo wallets with live blockchain data integration. Users can input any Ethereum wallet address and receive analysis within 60 seconds. Requires integration with blockchain data providers (Alchemy, QuickNode, or The Graph), rate limiting, caching strategy, and error handling for edge cases (empty wallets, unknown tokens, incomplete price data).

Timeline: 2-3 weeks of focused development
Impact: Transforms from demo to usable product for real portfolios

**Proactive Monitoring & Alerts**
Guardian continuously monitors connected wallets and sends alerts when risk thresholds are crossed. Example: "Your governance token concentration just crossed 60% after today's ETH drop. Based on 2022 patterns, portfolios like yours are entering high-risk territory." Requires persistent monitoring infrastructure, trigger system, push notifications (email, Telegram, or Discord), and user preference management.

Timeline: 3-4 weeks of development
Impact: Shifts from reactive analysis to proactive risk management

**Expanded Token & Sector Coverage**
Grow MeTTa knowledge graph from top 20-30 tokens to top 200+ tokens with comprehensive sector classifications. Add new sectors (gaming, NFT infrastructure, liquid staking derivatives, etc.) and more granular sub-sectors within DeFi. Include historical performance across multiple time periods (bull markets, bear markets, sector rotations).

Timeline: Ongoing, 20-30 tokens per week
Impact: Increases percentage of real portfolios that can be fully analyzed from ~60% to ~95%

**Portfolio Comparison & Benchmarking**
Show users how their portfolio structure compares to anonymized aggregates. Example: "Portfolios with your risk profile (high correlation + high sector concentration) represent 23% of DeFi investors but experienced 80% of catastrophic losses in 2022." Requires privacy-preserving data aggregation and statistical analysis infrastructure.

Timeline: 4-6 weeks of development
Impact: Adds social proof and relative context to risk assessment

**Multi-Chain Support (Phase 2B)**
Expand beyond Ethereum to include Solana, Polygon, Arbitrum, Optimism, and other major chains. Analyze cross-chain correlation patterns (e.g., "Your Solana portfolio is 87% correlated to your Ethereum portfolio, eliminating cross-chain diversification benefits"). Requires multi-chain data sources, cross-chain correlation models, and unified sector taxonomy.

Timeline: 6-8 weeks of development
Impact: Addresses reality that DeFi investors operate across multiple chains

### Long-Term Vision (1-2 Years)

**From Reactive Intelligence to Predictive Intelligence**
Guardian evolves from analyzing current portfolio structure to predicting future risk based on market conditions. Using advanced MeTTa reasoning over historical patterns, Guardian identifies early warning signals: "Your portfolio structure is similar to those that suffered in previous flash crashes. Current market conditions (high volatility + low liquidity) suggest elevated risk in the next 7 days."

This shifts Guardian from "here's your risk" to "here's what's likely to happen" — transforming portfolio intelligence from diagnostic to predictive. Requires sophisticated pattern matching, machine learning integration with MeTTa, and careful handling of prediction uncertainty.

**Social Intelligence & Collective Learning**
Guardian learns from analyzing thousands of portfolios to identify patterns invisible at individual level. Example: "Portfolios holding both Token A and Token B experienced 40% higher correlation during crashes than expected from individual token correlations. This suggests hidden relationship not captured in standard analysis."

The ASI network's collective intelligence becomes Guardian's knowledge base, with insights emerging from cross-portfolio pattern recognition while maintaining individual privacy. This creates network effects: more users → better insights for everyone.

**Autonomous Rebalancing Agent**
Introduce 4th agent (ExecutionAgent) that can execute rebalancing trades based on Guardian's recommendations. User sets risk preferences and approval thresholds. When Guardian identifies dangerous concentration, ExecutionAgent proposes specific trades (e.g., "Sell 30% of governance tokens, add 20% BTC and 10% stablecoin"). User approves with single signature, agent executes optimally across DEXs considering gas costs and slippage.

This closes the loop from intelligence → recommendation → execution, making Guardian a complete portfolio management system.

**DAO Treasury Management**
Expand from individual portfolios to DAO treasury analysis. DAOs managing $1M-$100M in assets face same correlation and concentration risks but at larger scale. Guardian analyzes treasury composition, reveals correlation to protocol's native token (e.g., "Your treasury is 80% correlated to your governance token, creating existential risk if protocol faces crisis"), and recommends diversification strategies.

Adds new user segment (DAO operators, treasury managers) with higher value propositions and more sophisticated requirements.

### Expansion Opportunities

**Integration Partnerships**
- **Embed Guardian in existing portfolio trackers:** Zerion, Zapper, DeBank add "Risk Analysis by Guardian" button that launches ASI:One conversation
- **Protocol partnerships:** DeFi protocols integrate Guardian to help users understand risks before depositing into high-risk strategies
- **Financial advisor tools:** Guardian becomes portfolio analysis module for crypto-native wealth advisors serving clients
- **Educational platforms:** Crypto education platforms use Guardian to teach portfolio risk concepts with real examples

**Enterprise Version**
Build Guardian for institutional DeFi investors (family offices, hedge funds, venture DAOs) with advanced features:
- Multi-wallet portfolio aggregation
- Custom risk models and thresholds
- Compliance reporting and audit trails
- Team collaboration features
- Historical backtesting and scenario analysis

Pricing model shifts from free/freemium to B2B SaaS with premium tiers.

**Guardian Analytics Platform**
Aggregate anonymized insights from portfolio analysis into market intelligence product. Example reports:
- "Q3 2025 DeFi Portfolio Risk Report: 67% of portfolios show dangerous governance token concentration"
- "Correlation Trends: ETH correlation increasing across all DeFi sectors"
- "Early Warning: Portfolios matching pre-crash patterns up 34% this month"

New revenue stream from data/insights sales to protocols, researchers, and media.

**Regulatory Compliance Module**
As crypto regulation matures, Guardian adds compliance features:
- Automated tax-loss harvesting recommendations
- Regulatory reporting for diversification requirements
- Risk disclosure generation for registered advisors
- Audit trail for fiduciary duty documentation

Positions Guardian as infrastructure for regulated DeFi portfolio management.

---

## Technical Considerations

### Platform Requirements

- **Target Platforms:** ASI Alliance ecosystem (Agentverse for agent deployment, ASI:One for user interaction via Chat Protocol)
- **Browser/OS Support:** Platform-agnostic access via ASI:One web interface. No native mobile apps or desktop clients for MVP. Users access through any modern browser (Chrome, Firefox, Safari, Edge) on desktop or mobile.
- **Performance Requirements:**
  - Agent response time: <5 seconds per individual agent query (CorrelationAgent, SectorAgent)
  - End-to-end analysis time: <60 seconds from wallet input to complete synthesis
  - Inter-agent communication latency: <2 seconds per message
  - MeTTa query execution: <1 second per historical lookup
  - Concurrent user support: Minimum 10 simultaneous users for demo/testing phase (can scale post-MVP)

### Technology Preferences

**Frontend:**
- **Primary Interface:** ASI:One Chat Protocol (no custom frontend development required for MVP)
- **Future Consideration:** Web dashboard for visualizations post-MVP, likely React/Next.js with Web3 integration (MetaMask, WalletConnect)
- **Rationale:** Chat-first approach minimizes development time, aligns with hackathon requirements, and validates conversational AI value proposition before building traditional UI

**Backend:**
- **Agent Framework:** uAgents (Fetch.ai's Python framework for multi-agent systems)
- **Language:** Python 3.10+ for all agents (Guardian, CorrelationAgent, SectorAgent)
- **Knowledge Representation:** MeTTa (SingularityNET's knowledge graph language) for historical crash data, sector classifications, and correlation patterns
- **Data Processing:** Pandas for portfolio analysis, NumPy for correlation calculations
- **Rationale:** Full ASI Alliance stack usage maximizes hackathon scoring; Python ecosystem provides mature libraries for financial analysis

**Database:**
- **MVP:** Local JSON files or Python dictionaries for hardcoded demo wallet data and MeTTa knowledge graph
- **Post-MVP:** PostgreSQL or MongoDB for persistent storage of user portfolios, analysis history, and expanded token database
- **Caching:** Redis for caching agent responses and historical price data post-MVP
- **Rationale:** Simplest possible data storage for MVP; can upgrade to production database when adding real-time features

**Hosting/Infrastructure:**
- **Agent Deployment:** Agentverse (Fetch.ai's agent hosting platform) for all 3 agents
- **Data Storage:** Local to agents for MVP (no separate cloud storage infrastructure)
- **Post-MVP Hosting:** Cloud infrastructure (AWS, GCP, or Heroku) for backend services when adding real-time blockchain data fetching
- **Monitoring:** Agentverse built-in monitoring for agent health and message logs
- **Rationale:** Agentverse required for hackathon; proven platform for agent deployment; reduces DevOps complexity

### Architecture Considerations

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

**Service Architecture:**
- **Pattern:** Distributed multi-agent system (not monolithic)
- **Communication:** Message-passing between agents via uAgents protocol
- **Deployment:** Each agent deployed independently to Agentverse with unique address
- **State Management:** Stateless agents (no session persistence for MVP)
- **Rationale:** True multi-agent architecture proves hackathon concept; independent deployment shows scalability; stateless keeps complexity low

**Integration Requirements:**
- **Chat Protocol Integration:** Guardian agent implements Fetch.ai Chat Protocol for ASI:One conversation interface
- **MeTTa Integration:** Python bindings for MeTTa queries (hyperon Python library)
- **Historical Data Source:** Pre-downloaded CSV from CoinGecko or CryptoCompare API for price history (avoid real-time API dependency for MVP)
- **Future Integrations:** Blockchain data APIs (Alchemy, The Graph), Web3 wallet connection, notification services (SendGrid, Telegram Bot API)
- **Rationale:** Minimize external dependencies for MVP reliability; API integrations are Phase 2 priority

**Security/Compliance:**
- **MVP Security Posture:** Read-only analysis (no wallet connections, no transaction signing, no private key handling)
- **Data Privacy:** Demo wallets are public addresses (no PII collection)
- **Rate Limiting:** None required for MVP (hardcoded data, no external APIs)
- **Post-MVP Security Requirements:**
  - Secure API key management for blockchain data providers
  - User authentication if saving portfolio preferences
  - Rate limiting to prevent abuse
  - No storage of private keys or sensitive wallet data
- **Compliance Considerations:** Financial advice disclaimers (Guardian provides analysis, not investment advice); GDPR considerations if expanding to EU users with saved preferences
- **Rationale:** MVP's read-only, demo-only scope minimizes security surface; production version requires standard Web3 security practices

**Scalability Considerations:**
- **MVP Bottlenecks:** Single agent instance per type (1 Guardian, 1 CorrelationAgent, 1 SectorAgent); potential message queue buildup if >10 concurrent users
- **Horizontal Scaling Path:** Deploy multiple instances of each agent type with load balancer; Agentverse supports agent scaling
- **Data Scaling:** MeTTa knowledge graph limited to top 30 tokens for MVP; post-MVP can expand incrementally without architecture changes
- **Cost Implications:** Agentverse free tier for hackathon; production deployment may require paid tier depending on usage volume
- **Rationale:** MVP scale sufficient for demo and initial user testing; architecture supports horizontal scaling when needed

---

## Constraints & Assumptions

### Constraints

**Budget:**
- **Development Budget:** $0 — This is a hackathon project with no allocated development budget
- **Infrastructure Costs:** $0 for MVP (Agentverse free tier, no paid APIs, no cloud hosting)
- **Post-MVP Budget TBD:** Real-time blockchain data APIs ($50-200/month for Alchemy/QuickNode), cloud hosting ($20-100/month for backend services), domain/SSL ($15/year)
- **Implications:** Technology choices must prioritize free/open-source options; no paid data sources or premium APIs for MVP; must validate product-market fit before committing to recurring costs

**Timeline:**
- **Total Development Time:** 10 days from project start to submission deadline
- **Hard Deadline:** ASI Alliance Hackathon submission date (estimated early November 2025)
- **Time Allocation:**
  - Days 1-4: Core agent development (Guardian, CorrelationAgent, SectorAgent) + basic inter-agent communication
  - Days 5-6: MeTTa integration + testing multi-agent flows + demo scenario refinement
  - Day 7: Deployment to Agentverse + Chat Protocol integration + end-to-end testing
  - Day 8: Demo video production (script, record, edit)
  - Day 9: Documentation (README, architecture docs, demo instructions)
  - Day 10: Buffer for unexpected issues, final polish, submission preparation
- **Implications:** Features that require >1 day of work are automatically out of scope; architectural decisions must favor speed over perfection; testing must be time-boxed; no time for multiple design iterations

**Resources:**
- **Team Size:** Solo developer (1 person)
- **Available Hours:** ~80-100 hours total across 10 days (8-10 hours per day)
- **Skills Required:** Python development, agent framework learning (uAgents new), MeTTa integration (new), DeFi domain knowledge (existing), video production (basic)
- **Learning Curve:** 20-30% of time allocated to learning uAgents and MeTTa (first time using both frameworks)
- **Implications:** No parallel workstreams; single point of failure; context switching penalty; must choose technologies with good documentation; cannot outsource or delegate any component; design decisions must account for solo execution reality

**Technical:**
- **Platform Lock-in:** Must use ASI Alliance tech stack (uAgents, MeTTa, Agentverse, Chat Protocol) to qualify for hackathon — no alternative architectures considered
- **Agent Framework Maturity:** uAgents framework may have limitations or bugs that constrain architecture choices; must work within framework capabilities
- **MeTTa Knowledge Graph Size:** Limited to what can be manually curated in 1-2 days — ~20-30 tokens, 3 crash scenarios, basic sector taxonomy. Cannot build comprehensive knowledge graph in 10 days.
- **Data Availability:** Historical price data must be freely available and pre-downloadable (no premium data sources)
- **Testing Environment:** Limited to local testing and Agentverse testnet — no production-grade testing infrastructure
- **Documentation Dependency:** Success depends on quality of uAgents and MeTTa documentation — gaps could block progress
- **Implications:** Architecture must be framework-native (can't fight uAgents patterns); scope must fit within MeTTa's capabilities; workarounds required if documentation is incomplete; plan buffer time for framework learning and debugging

### Key Assumptions

**Technical Assumptions:**
- uAgents framework is stable enough for production deployment (not alpha-quality)
- MeTTa Python bindings (hyperon) work reliably for MVP use cases (historical data queries, pattern matching)
- Agentverse free tier has sufficient capacity for 3 agents + demo traffic
- Inter-agent communication latency via uAgents is acceptable (<5 seconds per message)
- Chat Protocol integration is well-documented and doesn't require deep Fetch.ai expertise
- Pre-downloaded historical price data from CoinGecko is sufficient for correlation calculations
- Python correlation calculations (Pandas/NumPy) are fast enough to meet <60 second end-to-end requirement

**Market/User Assumptions:**
- DeFi investors with $50K+ portfolios exist in meaningful numbers and experience risk blindness problem
- Users value intelligence/judgment over raw data (willingness to use conversational agent vs. dashboard)
- Hackathon judges prioritize alignment with ASI Alliance vision (multi-agent collaboration) over product polish
- Portfolio risk analysis is valuable enough to attract post-hackathon users even with limited token coverage
- Conversational interface is acceptable for financial analysis (users won't demand charts/graphs immediately)
- Demo-only wallets will be accepted by judges and early users as proof-of-concept (not rejected as "not real")

**Domain Assumptions:**
- ETH correlation is the primary structural risk in DeFi portfolios (more important than BTC or stablecoin correlation)
- DeFi governance token sector concentration is common and dangerous enough to be primary sector focus
- Historical crash patterns (2022 bear, 2021 correction, 2020 COVID) are representative of future crash dynamics
- 95%+ correlation means "3x leverage" is an accurate and useful mental model
- Sector concentration >60% in single category represents dangerous concentration threshold
- Two-dimensional analysis (correlation + sector) captures majority of structural portfolio risk

**Product Assumptions:**
- Multi-agent architecture creates meaningful differentiation vs. monolithic analysis
- Historical "time machine" approach is more compelling than forward-looking risk scores
- Synthesis of correlation + sector reveals insights not obvious from individual analyses
- Three agents is sufficient to demonstrate multi-agent collaboration (don't need 4-5 agents)
- Actionable recommendations can be generated without knowing user's risk tolerance, time horizon, or investment goals
- Users will trust Guardian's analysis despite it being a hackathon project from unknown developer

**Post-Hackathon Assumptions:**
- Winning/placing in hackathon will generate organic user interest (not requiring marketing spend)
- Beta users will tolerate hardcoded wallet limitation while real-time fetching is built
- Architecture designed for hackathon demo can be refactored for production without full rewrite
- Real-time blockchain data APIs are cost-effective enough to support freemium business model
- Market for DeFi risk intelligence is large enough to support venture funding or sustainable business

---

## Risks & Open Questions

### Key Risks

- **uAgents/MeTTa Learning Curve Risk (HIGH):** First time using both uAgents framework and MeTTa knowledge representation. If documentation is incomplete or frameworks are buggy, could consume 40-50% of available time troubleshooting instead of building features. **Mitigation:** Allocate Day 1 to framework exploration and "hello world" agents before committing to architecture. Have fallback plan to simplify MeTTa integration if hyperon Python bindings prove problematic (store historical data in JSON, use simple dictionary lookups instead of sophisticated queries).

- **Timeline Compression Risk (HIGH):** 10-day timeline leaves zero margin for error. Any single blocker (deployment issues, integration bugs, personal emergency) could cascade into incomplete submission. **Mitigation:** Day 10 buffer is sacred — protect it by being ruthless about scope on Days 1-9. Have "minimum viable demo" fallback: 2 agents instead of 3, 1 crash scenario instead of 3, shorter demo video. Ship something complete rather than something ambitious but broken.

- **Demo Failure Risk (MEDIUM):** Live demo could fail due to Agentverse downtime, network issues, or inter-agent communication timeout. Judges might not see the working system. **Mitigation:** Record video demo as backup — judges can watch even if live system is down. Include screenshots in README showing successful agent interactions. Have pre-recorded demo conversation ready to present if live demo fails.

- **Value Proposition Risk (MEDIUM):** Users might view hardcoded demo wallets as "not real" and dismiss the project as vaporware rather than proof-of-concept. Post-hackathon interest might be zero if users demand real-time functionality immediately. **Mitigation:** Be explicit in demo and documentation that this is "Phase 1: proof of concept" with "Phase 2: real-time integration" planned. Choose demo wallet addresses that are real, verifiable addresses (anyone can check on Etherscan) so users see Guardian is analyzing actual portfolios, just pre-selected ones.

- **Judging Criteria Misalignment Risk (MEDIUM):** Might overemphasize multi-agent architecture and underdeliver on user experience, or vice versa. Hackathon judges might prioritize different aspects than assumed (polish over vision, features over tech stack usage). **Mitigation:** Review hackathon judging criteria weekly and adjust focus if rubric becomes clearer. Ensure ALL criteria are met at minimum threshold: some functionality (✓), ASI tech usage (✓), innovation (✓), real-world impact story (✓), acceptable UX (✓). Better to score 7/10 across all criteria than 10/10 on tech and 3/10 on UX.

- **Correlation/Sector Analysis Accuracy Risk (MEDIUM):** The risk calculations might be oversimplified or inaccurate. Claiming "3x leverage" from 95% correlation might be mathematically imprecise. Financial experts might dismiss analysis as naive. **Mitigation:** Include disclaimers that Guardian provides directional insights, not precise quantitative risk metrics. Reference methodology in documentation (Pearson correlation over 90-day window, sector classifications based on token documentation). Emphasize comparative insights ("your portfolio vs. typical portfolio") rather than absolute predictions.

- **MeTTa Integration Shallow Risk (LOW-MEDIUM):** Might implement MeTTa integration superficially (basic key-value lookups) rather than demonstrating sophisticated knowledge reasoning. Judges familiar with MeTTa might view usage as checkbox-checking rather than meaningful. **Mitigation:** Study MeTTa examples from SingularityNET documentation. Implement at least one non-trivial query pattern (e.g., "find all crash scenarios where correlation >90% AND sector concentration >60% AND ETH drawdown >15%"). Show MeTTa reasoning in demo: "I'm querying the knowledge graph for similar portfolio structures during historical crashes..."

- **Solo Developer Burnout Risk (LOW-MEDIUM):** 10 days of 8-10 hour development sprints could lead to burnout, degraded decision-making, or scope creep from fatigue. **Mitigation:** Protect sleep and breaks — tired developer ships bugs. Use Day 10 buffer for recovery if needed. Have accountability partner for daily check-ins to catch scope creep early.

- **Chat-Only Interface Limitation Risk (LOW):** Users might expect visualizations (charts showing correlation over time, sector pie charts) and be disappointed by text-only conversational output. **Mitigation:** Set expectations clearly in demo: "Guardian is a conversational intelligence agent, not a dashboard — it tells you what matters, not shows you everything." Include ASCII-style tables in chat responses if needed for clarity (e.g., sector breakdown table). Acknowledge in documentation that Phase 2 adds visual dashboard.

- **Token Coverage Inadequacy Risk (LOW):** Demo portfolios might include tokens outside the top 20-30 covered by MeTTa knowledge graph, requiring "insufficient data" responses that make Guardian look incomplete. **Mitigation:** Carefully select demo wallet addresses with portfolios composed entirely of covered tokens. If showing "insufficient data" response, frame it as feature ("Guardian is honest about knowledge limitations") rather than bug.

### Open Questions

**MeTTa Knowledge Graph Design:**
- What's the optimal schema for storing historical crash data? Should it be flat (token → crash → performance) or relational (crash → sector → token → performance)?
- How should opportunity cost data be structured? (missed gains during specific time periods vs. general "winners" per sector)
- Can MeTTa handle temporal queries efficiently? ("Show me performance during Q2 2022" vs. just "Show me 2022 bear market data")
- Should correlation patterns be stored in MeTTa or calculated on-the-fly in Python?

**Agent Communication Patterns:**
- Should Guardian call CorrelationAgent and SectorAgent sequentially or in parallel? Sequential is simpler but slower; parallel is faster but adds complexity.
- What's the user experience during agent communication wait time? Should Guardian send "thinking..." messages? Show which agent is currently being consulted?
- How should agents handle timeout scenarios? (CorrelationAgent takes >30 seconds to respond)
- Should individual agent responses be streamed to user in real-time, or only show final synthesis?

**Demo Wallet Selection:**
- Which real wallet addresses best demonstrate the risk analysis? Need portfolios with clear correlation + sector concentration without being cherry-picked to extreme scenarios.
- Should demo include one "well-diversified portfolio" to show Guardian doesn't always find problems? Or only show high-risk portfolios to maximize impact?
- How many demo wallets needed? 2 (one risky, one moderate) or 3 (risky, moderate, well-diversified)?
- Should demo wallets be anonymous or attributed to known DeFi personas (with permission)?

**Opportunity Cost Calculation:**
- How to select the "missed opportunities" to show? Should match risk profile (show what conservative investor should have held) or just show biggest winners (SOL, regardless of risk profile)?
- What time period for opportunity cost comparison? (2023 bull run, last 12 months, since 2022 bottom?)
- Should opportunity cost be mandatory in every analysis or optional based on relevance?
- How to frame opportunity cost without making users feel bad? (educational tone vs. critical tone)

**Guardian Personality & Voice:**
- Should Guardian have consistent personality (worried advisor, strict teacher, supportive friend, neutral analyst)?
- How direct should warnings be? ("Your portfolio will likely crash" vs. "Your portfolio has elevated risk" vs. "Consider these risk factors")
- Should tone vary based on risk level? (urgent for high-risk, calm for moderate-risk)
- How much confidence should Guardian project? (definitive statements vs. probabilistic language)

**Risk Threshold Definitions:**
- What correlation threshold defines "high risk"? (>90%, >85%, >80%?)
- What sector concentration threshold is dangerous? (>60%, >50%?, varies by sector?)
- Should thresholds be hardcoded or learned from historical data?
- How to handle edge cases like "99% stablecoin portfolio" (high concentration but low risk) or "50% BTC, 50% ETH" (low diversity but not necessarily high risk)?

**Scalability & Production Readiness:**
- What's the migration path from hardcoded demos to real-time fetching? Can reuse agent architecture or need significant refactor?
- How to handle tokens with insufficient price history for correlation calculation?
- Should Guardian maintain state across multiple user questions in single session, or treat each query independently?
- What's the cost structure for production deployment? (Agentverse paid tier pricing, API costs, infrastructure costs)

**User Experience Edge Cases:**
- What happens if user inputs empty wallet, wallet with 1 token, or wallet with 100 tokens?
- How should Guardian handle user questions outside risk analysis scope? ("What's the price of ETH?" or "Should I buy SOL?")
- Should Guardian offer follow-up questions/clarifications, or wait for user to ask?
- How to handle users who disagree with analysis? ("I don't think my portfolio is risky")

### Areas Needing Further Research

**DeFi Correlation Dynamics:**
- Are there correlation patterns beyond ETH? (BTC correlation for Bitcoin-ecosystem tokens, stablecoin correlation for yield products)
- How does correlation behave during different market phases? (bull market vs. bear market vs. sideways)
- Do layer-2 tokens correlate more strongly with their base layer (e.g., Arbitrum → Ethereum) than with DeFi sector peers?
- Research source: Academic papers on crypto correlation, on-chain data analysis from Nansen/Glassnode

**Sector Taxonomy Validation:**
- Is "DeFi governance token" a meaningful risk category, or should it be further subdivided? (DEX governance vs. lending governance vs. yield aggregator governance)
- Are there emerging sectors not captured in current taxonomy? (liquid staking derivatives, real-world assets, decentralized social)
- Do some tokens belong to multiple sectors? (e.g., UNI is both DEX and governance)
- Research source: Token categorization from CoinGecko, Messari, or DeFi Llama; interview DeFi investors about mental models

**Historical Crash Scenario Selection:**
- Are 2022 bear, 2021 correction, and 2020 COVID crash the most representative scenarios? Should include 2018 ICO crash, 2019 DeFi summer, or other periods?
- What granularity of crash data is useful? (quarterly aggregates vs. specific crash dates like Terra/Luna collapse)
- How to handle crashes specific to protocols (UST depeg) vs. market-wide crashes (2022 bear)?
- Research source: Historical price data analysis, DeFi researcher reports, post-mortem analyses of major crashes

**Competitive Landscape:**
- What other DeFi portfolio risk tools exist? (academic projects, unreleased startups, enterprise tools)
- How do traditional finance portfolio analysis tools (Morningstar, Bloomberg Terminal) approach correlation and concentration?
- Are there multi-agent DeFi applications already built on ASI Alliance stack that Guardian should learn from?
- Research source: Product Hunt, DeFi tool directories, ASI Alliance community showcases, Twitter/CT research

**Hackathon Judging Criteria:**
- Has the specific rubric been published? What are exact weightings for functionality vs. tech usage vs. innovation?
- Who are the judges? (Technical evaluators from Fetch.ai/SingularityNET vs. business/product evaluators)
- Are there past winning projects to study for patterns?
- Research source: Hackathon website, organizer communications, previous ASI Alliance hackathon archives

---

## Appendices

### A. Research Summary

**Brainstorming Session Results (October 17, 2025)**

A comprehensive brainstorming session was conducted to scope and refine the Guardian concept for the ASI Alliance Hackathon. The session employed multiple ideation techniques over 2 hours and generated the foundational insights that shaped this project brief.

**Techniques Used & Key Findings:**

**1. Role Playing (Judge's Perspective) - 45 minutes**
- **Insight:** Hackathon judges from Fetch.ai and SingularityNET prioritize seeing their technologies used in concert, not just individually. Multi-agent collaboration is the defining requirement.
- **Finding:** 3 agents with real communication beats 2 sophisticated agents. Judges want to see "agents talking to each other" in real-time.
- **Decision Impact:** Committed to 3-agent architecture (Guardian, CorrelationAgent, SectorAgent) as non-negotiable core.

**2. First Principles Thinking (Core Problem Analysis) - 30 minutes**
- **Insight:** DeFi investors don't need more data—they need better judgment applied to existing data. The fundamental pain is "risk blindness": believing you're diversified when you're actually concentrated.
- **Finding:** Two-dimensional risk analysis (correlation + sector) reveals compounding effects that neither dimension shows alone. This is the "lean forward moment."
- **Decision Impact:** Positioned Guardian as judgment engine, not dashboard. Focus on synthesis over raw analysis.

**3. Resource Constraints (10-Day Reality Check) - 25 minutes**
- **Insight:** In a 5-day hypothetical, would choose 3 basic agents over 2 sophisticated agents. Alignment with ASI Alliance vision matters more than perfection.
- **Finding:** Blockchain API integration is biggest time sink with external dependencies. Hardcoded demo wallets give full control and ensure reliable demo.
- **Decision Impact:** Scoped out real-time blockchain fetching for MVP. Demo-only approach with pre-selected wallets.

**4. Assumption Reversal (Differentiation Strategy) - 20 minutes**
- **Insight:** Portfolio analysis doesn't have to be snapshot-based. Historical context makes abstract risk concrete and urgent.
- **Finding:** "Time-machine approach"—showing what would have happened during past crashes—creates emotional impact and demonstrates sophisticated MeTTa usage.
- **Decision Impact:** Historical crash simulations became signature differentiator. Every risk metric includes historical context.

**Quantitative Outcomes:**
- 15+ core concepts generated and evaluated
- Narrowed to 1 focused architecture (3 agents, 2 dimensions, time-machine approach)
- Identified 4 key themes: multi-agent collaboration, risk intelligence over data display, historical context, realistic scoping
- Validated 10-day timeline feasibility with day-by-day allocation

**Validation:**
The brainstorming session validated that Guardian addresses a real problem (risk blindness), has a defensible approach (multi-agent synthesis), and is achievable within constraints (10-day solo build). The session's outputs directly informed the MVP scope, technical architecture, and product positioning in this brief.

**Full Documentation:** `docs/brainstorming-session-results.md`

---

### B. Stakeholder Input

**Primary Stakeholder:** Solo developer / project creator

**Stakeholder Context:**
- Experienced in DeFi domain and portfolio analysis concepts
- First-time user of uAgents framework and MeTTa knowledge representation
- Motivated by hackathon success and potential post-hackathon product viability
- Committed to 10-day timeline with 8-10 hours per day availability

**Key Stakeholder Priorities:**
1. Win or place in ASI Alliance Hackathon top tier
2. Build foundation for post-hackathon product development (extensible architecture)
3. Validate product-market fit through demo feedback
4. Learn ASI Alliance tech stack (uAgents, MeTTa, Agentverse) for future projects

**Stakeholder Constraints:**
- Zero budget for development or infrastructure
- Solo execution (no team, no ability to delegate)
- Limited time for learning curve (must ship in 10 days)
- First hackathon submission in this ecosystem

**Alignment Confirmation:**
This project brief reflects stakeholder priorities by:
- Optimizing for hackathon judging criteria (multi-agent + full ASI stack usage)
- Maintaining realistic scope for solo 10-day execution
- Designing extensible architecture for post-hackathon development
- Including product validation metrics (beta interest, community engagement)

---

### C. References

**ASI Alliance Resources:**

**Fetch.ai - uAgents Framework:**
- **How to create an Agent with uAgents Framework:** https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation
- **Communication between two uAgents:** https://innovationlab.fetch.ai/resources/docs/agent-communication/uagent-uagent-communication
- **How to create ASI:One compatible uAgents:** https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/asi-compatible-uagents
- **Innovation Lab GitHub Repo (Examples & Templates):** https://github.com/fetchai/innovation-lab-examples
- **Past Hackathon Projects (Reference Implementations):** https://innovationlab.fetch.ai/projects
- **How to write a good README for your Agents:** https://innovationlab.fetch.ai/resources/docs/agentverse/searching#importance-of-good-readme
- **Agentverse Platform:** https://agentverse.ai/

**SingularityNET - MeTTa:**
- **Understanding MeTTa (Main Concepts):** https://metta-lang.dev/docs/learn/tutorials/eval_intro/main_concepts.html
- **Running MeTTa in Python (Basics):** https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html
- **Nested Queries and Recursive Graph Traversal:** https://metta-lang.dev/docs/learn/tutorials/ground_up/nested_queries.html
- **Setup MeTTa on Windows OS (Video Tutorial):** https://youtu.be/Hp28F9gL2Cc?si=g9WN5X1I0jeP_4RH

**Fetch.ai + MeTTa Integration:**
- **Integration Example Repository:** https://github.com/fetchai/innovation-lab-examples/tree/main/web3/singularity-net-metta

**DeFi & Portfolio Analysis:**
- **CoinGecko API:** https://www.coingecko.com/en/api (Historical price data source)
- **DeFi Llama:** https://defillama.com/ (Protocol and sector classification reference)
- **Messari Research:** https://messari.io/research (Crypto sector taxonomy and market analysis)
- **Nansen Portfolio Tracker:** https://www.nansen.ai/ (Competitive reference for portfolio tracking)
- **Zerion:** https://zerion.io/ (Competitive reference for DeFi portfolio management)

**Relevant Academic & Industry Research:**
- "Correlation Dynamics in Cryptocurrency Markets" (Various authors, 2020-2023)
- "Understanding DeFi Risk: A Multidimensional Framework" (Research papers on crypto risk)
- "Portfolio Construction in Crypto Markets" (Traditional portfolio theory applied to crypto)
- Historical crash analyses: 2022 bear market post-mortems, Terra/Luna collapse analysis, 2020 COVID crash DeFi impact

**Hackathon Information:**
- **ASI Alliance Hackathon Page:** [URL to be added when available]
- **Judging Criteria:** Functionality (25%), ASI Tech Usage (20%), Innovation (20%), Real-World Impact (20%), UX (15%)
- **Submission Guidelines:** [To be researched and added]

**Project Documentation:**
- **Brainstorming Session Results:** `docs/brainstorming-session-results.md`
- **Project Brief (this document):** `docs/brief.md`
- **Architecture Documentation:** `docs/architecture.md` (to be created during development)
- **Demo Instructions:** `docs/demo.md` (to be created during development)

**Development Tools & Utilities:**
- **Python:** https://www.python.org/ (Primary development language, 3.10+)
- **Pandas:** https://pandas.pydata.org/ (Portfolio and correlation analysis)
- **NumPy:** https://numpy.org/ (Numerical computation for correlation calculations)
- **Git/GitHub:** Version control and code hosting

**Community Resources:**
- **Fetch.ai Discord:** Community support for uAgents development questions
- **SingularityNET Community:** MeTTa usage questions and examples
- **Crypto Twitter (CT):** DeFi investor community for user research and validation

---

## Next Steps

### Immediate Actions

**1. Environment Setup & Framework Familiarization (Day 1 Morning - 4 hours)**
- Install Python 3.10+ and create virtual environment
- Install uAgents framework following Innovation Lab guide
- Install MeTTa/Hyperon Python bindings
- Run "Hello World" agent from Innovation Lab examples
- Test basic inter-agent communication example
- Create GitHub repository and initialize project structure

**2. Study Reference Implementations (Day 1 Afternoon - 4 hours)**
- Review past hackathon projects from Innovation Lab
- Study ASI:One compatible agent examples thoroughly
- Read MeTTa Python basics and nested query tutorials
- Examine Fetch.ai + MeTTa integration example
- Document key patterns and code snippets for reuse
- Create technical notes on framework capabilities and limitations

**3. Build Core Agent Structure (Days 2-3 - 16 hours)**
- Implement Guardian orchestrator agent with Chat Protocol
- Implement CorrelationAgent with basic ETH correlation calculation
- Implement SectorAgent with token-to-sector mapping logic
- Test each agent independently on Agentverse testnet
- Verify all 3 agents can be queried via unique addresses

**4. Implement Inter-Agent Communication (Day 4 - 8 hours)**
- Add message-passing from Guardian to CorrelationAgent
- Add message-passing from Guardian to SectorAgent
- Test end-to-end flow: user query → agent calls → synthesis response
- Debug timeout and error handling scenarios
- Measure and optimize communication latency

**5. Integrate MeTTa Historical Intelligence (Days 5-6 - 16 hours)**
- Define MeTTa schema for crash scenarios (2022 bear, 2021 correction, 2020 COVID)
- Populate knowledge graph with historical correlation performance data
- Populate knowledge graph with sector crash performance + opportunity cost
- Add MeTTa queries to CorrelationAgent and SectorAgent
- Test that historical context appears in agent responses
- Validate accuracy of historical simulations against actual data

**6. Create Demo Wallet Scenarios (Day 6 Evening - 2 hours)**
- Identify 2-3 real wallet addresses with known risk profiles
- Hardcode portfolio compositions (token holdings and amounts)
- Pre-calculate expected correlation and sector concentration
- Document demo wallet addresses and expected analysis outcomes
- Test complete analysis flow for each demo wallet

**7. Deploy to Agentverse Production (Day 7 Morning - 3 hours)**
- Deploy all 3 agents to Agentverse production environment
- Verify agents are accessible via ASI:One interface
- Test Chat Protocol integration with sample queries
- Document agent addresses and interaction instructions
- Run smoke tests to ensure production deployment works

**8. End-to-End Testing & Refinement (Day 7 Afternoon - 5 hours)**
- Execute complete user flow 10+ times with different queries
- Test edge cases (unknown tokens, empty responses, timeouts)
- Refine agent response narratives for clarity
- Optimize synthesis logic to highlight compounding risks
- Fix any bugs discovered during testing

**9. Create Demo Video (Day 8 - 8 hours)**
- Write demo script showing narrative arc (intro → reveals → synthesis → recommendations)
- Record screen capture of ASI:One interaction with Guardian
- Show code snippets of inter-agent communication in video
- Record voiceover explaining what's happening
- Edit video to 3-5 minutes with clear pacing
- Add titles/annotations to highlight key moments

**10. Write Documentation (Day 9 - 8 hours)**
- Create comprehensive README following Innovation Lab best practices
- Write ARCHITECTURE.md explaining multi-agent design
- Create DEMO.md with step-by-step interaction instructions
- Document agent addresses, sample queries, and expected responses
- Include architecture diagram (hand-drawn or simple tool)
- Add "How to Run" section for judges to test locally

**11. Final Polish & Submission Prep (Day 10 - 8 hours)**
- Review all documentation for completeness and clarity
- Test submission package (does everything work without creator assistance?)
- Write submission form responses
- Upload demo video to YouTube/Vimeo
- Create project thumbnail/banner image
- Submit to hackathon platform
- Buffer time for unexpected last-minute issues

**12. Post-Submission User Validation (Weeks 1-2 After Hackathon)**
- Share demo video on Twitter/CT, Fetch.ai Discord, SingularityNET community
- Collect feedback on value proposition and user experience
- Track beta interest requests and engagement metrics
- Conduct 5-10 informal user interviews with DeFi investors
- Document feature requests and pain points for Phase 2 planning

---

### PM Handoff

This Project Brief provides the full context for **Guardian - DeFi Portfolio Intelligence Agent**.

**For Product/Project Manager Review:**

Guardian is now ready to move from strategic planning to execution. This brief documents:
- ✅ Clear problem statement (DeFi risk blindness) validated through brainstorming
- ✅ Differentiated solution (multi-agent risk synthesis with time-machine approach)
- ✅ Realistic MVP scope for 10-day solo build
- ✅ Technical architecture aligned with ASI Alliance tech stack requirements
- ✅ Success metrics tied to hackathon judging criteria and product validation
- ✅ Risk mitigation strategies for high-priority challenges
- ✅ Day-by-day execution plan with concrete deliverables

**Recommended Next Steps:**
1. **Review and approve** this brief to confirm strategic direction and scope
2. **Proceed to execution** following the 12-step immediate action plan
3. **Daily check-ins** to catch scope creep and monitor timeline adherence
4. **Adjust priorities** if framework learning curve exceeds estimates (Days 1-2)

**Key Decision Points During Execution:**
- **Day 2:** After framework familiarization, confirm 3-agent architecture is feasible or simplify to 2 agents
- **Day 4:** After inter-agent communication testing, assess if integration complexity requires scope reduction
- **Day 6:** After MeTTa integration, determine if historical context is working as designed or needs simplification
- **Day 7:** After deployment, decide if demo quality is sufficient or requires Day 10 buffer reallocation

**Success Indicators:**
- All 3 agents deployed and communicating by end of Day 7
- Demo video completed by end of Day 8
- Documentation comprehensive enough for judge self-service by end of Day 9
- At least one "lean forward moment" in demo where synthesis reveals non-obvious insight

**Risk Watch List:**
- uAgents/MeTTa learning curve consuming >30% of Days 1-2
- Inter-agent communication reliability <90% by Day 4
- MeTTa integration proving superficial rather than meaningful by Day 6
- Demo video requiring >8 hours (cutting into Day 9 buffer)

This project is positioned to demonstrate meaningful multi-agent DeFi intelligence while maintaining realistic execution constraints. The brief balances ambitious vision (predictive intelligence, multi-chain, enterprise) with pragmatic MVP scope (3 agents, hardcoded demos, 10-day delivery).

**Ready for execution. Awaiting approval to proceed.**

---

*Generated with BMAD™ Core - Business Analyst Mary*
*Date: October 18, 2025*
