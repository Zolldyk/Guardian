# Tech Stack

This section defines the **complete and authoritative technology stack** for Guardian. All development must use these exact technologies and versions. This is the single source of truth for technology selection—no substitutions without updating this document.

## Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|-----------|---------|---------|-----------|
| **Backend Language** | Python | 3.10+ (3.14.0 latest) | Agent implementation, data analysis, all backend logic | uAgents framework requires Python 3.10+; ecosystem has mature libraries (Pandas, NumPy) for portfolio analysis; Python 3.14.0 is latest stable; solo developer proficiency |
| **Agent Framework** | uAgents | 0.22.10 | Core framework for agent implementation and inter-agent communication | Mandatory for ASI Alliance Hackathon; provides native multi-agent architecture, message-passing protocol, and Agentverse deployment integration |
| **Agent Platform** | Agentverse | N/A (Platform) | Agent hosting, discovery, and runtime environment | Fetch.ai's managed platform for agent deployment; zero infrastructure management; hackathon requirement |
| **Conversational Interface** | ASI:One Chat Protocol | Latest | User-facing natural language interface | Hackathon requirement; enables conversational AI interaction; handles UI rendering (no custom frontend needed) |
| **Knowledge Graph** | MeTTa (Hyperon) | 0.2.6 | Semantic storage for historical crash data and sector relationships | SingularityNET technology (hackathon requirement); enables rich semantic queries; separates domain knowledge from code |
| **Knowledge Graph Bindings** | Hyperon Python | 0.2.8 | Python interface to MeTTa knowledge graph | Required to query MeTTa from Python agents; official SingularityNET bindings |
| **Data Analysis** | Pandas | 2.3.3 | Portfolio data manipulation, time-series analysis | Industry standard for financial data analysis; handles historical price data and portfolio calculations efficiently |
| **Numerical Computing** | NumPy | 2.3.4 | Correlation calculations, statistical operations | Foundation for Pandas; optimized numerical operations for portfolio correlation coefficient calculations |
| **Data Storage** | JSON Files | N/A (Standard) | Demo wallets, sector mappings, crash scenarios | Zero infrastructure setup; deterministic demo behavior; version-controlled alongside code; suitable for read-only hackathon data |
| **Database** | None (MVP) | N/A | N/A | No database server for hackathon; embedded JSON files sufficient for demo scenarios; post-MVP: PostgreSQL for user data persistence |
| **Cache** | None (MVP) | N/A | N/A | Agent responses fast enough (<5s) without caching; Agentverse may provide platform-level caching; post-MVP: Redis for historical data |
| **File Storage** | Local File System | N/A | MeTTa knowledge files, JSON data files deployed with agents | Data embedded in agent deployment; no separate object storage needed for hackathon scope |
| **Authentication** | None (MVP) | N/A | N/A | Demo wallets are public addresses; no user accounts or login; ASI:One may handle user sessions; post-MVP: Agentverse identity or OAuth |
| **Testing Framework** | pytest | 8.4.2 | Unit tests, integration tests, all Python testing | Python standard for testing; rich assertion library; fixture support for agent testing; compatible with CI/CD |
| **Testing - Mocking** | unittest.mock | 3.14+ (stdlib) | Mocking uAgents messages and MeTTa queries in unit tests | Python standard library (available since 3.3); no additional dependency; mock 5.2.0 available as backport; sufficient for isolating agent logic during unit testing |
| **Testing - Browser Automation** | Playwright MCP | Latest | Live browser testing, E2E UI validation, visual regression testing | Model Context Protocol integration for browser automation; enables Claude Code to perform live browser testing; supports Chromium/Firefox/WebKit; useful for validating ASI:One interface interactions and web-based workflows |
| **Linting** | ruff | Latest | Code quality, style enforcement, fast Python linting | Modern, fast replacement for flake8/black; single tool for linting + formatting; speeds up pre-commit checks |
| **Type Checking** | mypy | 1.18.2 | Static type analysis for Python code | Catches type errors before runtime; important for agent message contracts; improves IDE experience |
| **Dependency Management** | pip + requirements.txt | 25.2 | Python package installation and version pinning | Simple, universally supported; sufficient for monorepo with single Python environment; no need for Poetry/pipenv complexity |
| **Version Control** | Git | 2.51.1 | Source code version control | Industry standard; required for GitHub hosting |
| **Code Hosting** | GitHub | N/A | Repository hosting, judge code review access | Hackathon submission platform; enables judge review; free for public repos |
| **CI/CD** | GitHub Actions | N/A | Automated testing on commit (linting, type checking, unit tests, integration tests) | Free for public repos; integrated with GitHub; YAML-based workflow (.github/workflows/ci.yml); runs on push/PR to main/develop branches; deployment to Agentverse remains manual for hackathon control |
| **Logging** | Python logging | 3.14+ (stdlib) | Agent debugging, inter-agent message tracing | Python standard library; structured logging for agent behavior; critical for debugging message-passing |
| **Monitoring** | Agentverse Dashboard | N/A (Platform) | Agent health monitoring, uptime tracking, message volume | Built into Agentverse platform; sufficient for hackathon; post-MVP: add Sentry for error tracking |
| **Environment Management** | python-dotenv | 1.1.1 | Loading environment variables from .env files | Manages agent addresses, API keys, configuration across dev/production; prevents hardcoded secrets |
| **Documentation** | Markdown | N/A | All project documentation (README, architecture, demo guide) | Universal format; renders on GitHub; hackathon judges expect Markdown docs |
| **Deployment Automation** | Shell Scripts | Bash 5.3 | Agent deployment to Agentverse via CLI | Simple automation for deploying all 3 agents; sufficient for hackathon; post-MVP: migrate to proper IaC |
| **Frontend Language** | N/A | N/A | N/A | No custom frontend—ASI:One provides conversational interface; all user interaction is text-based through Chat Protocol |
| **Frontend Framework** | N/A | N/A | N/A | ASI:One handles UI rendering; Guardian only produces narrative text responses |
| **UI Component Library** | N/A | N/A | N/A | No custom UI components |
| **State Management** | N/A | N/A | N/A | Agents are stateless for MVP; no client-side state management needed |
| **API Style** | uAgents Protocol | N/A | Agent-to-agent communication via message-passing | Not REST/GraphQL/gRPC—agents use native uAgents message protocol with defined message models |
| **Build Tool** | None | N/A | N/A | Python doesn't require compilation; deployment = copying .py files to Agentverse |
| **Bundler** | None | N/A | N/A | No JavaScript bundling; Python modules loaded dynamically |
| **IaC Tool** | None (MVP) | N/A | N/A | Agentverse is fully managed platform; no infrastructure to define; post-MVP: Terraform if migrating to hybrid cloud |
| **CSS Framework** | N/A | N/A | N/A | No custom styling—ASI:One renders conversation interface |

---
