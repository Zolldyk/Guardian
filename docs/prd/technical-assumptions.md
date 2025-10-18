# Technical Assumptions

## Repository Structure: **Monorepo**

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

## Service Architecture: **Distributed Multi-Agent System (Message-Passing)**

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

## Testing Requirements: **Unit + Integration (Time-Boxed)**

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

## Additional Technical Assumptions and Requests

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
