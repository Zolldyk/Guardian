# Source Tree

This document provides the complete directory structure and file organization for the Guardian project.

## Project Structure Overview

Guardian follows a **monorepo structure** with clear separation of concerns across different layers:

```
guardian/
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── guardian.py              # Main orchestrator agent (Epic 2)
│   ├── correlation_agent.py     # Correlation analysis specialist (Story 1.3-1.4)
│   ├── sector_agent.py          # Sector concentration specialist (Story 1.5-1.6)
│   ├── hello_world_agent.py     # Learning agent from Story 1.1
│   ├── test_client_agent.py     # Test agent for inter-agent communication
│   └── shared/                  # Shared utilities across agents
│       ├── __init__.py
│       ├── config.py            # Centralized environment configuration (Story 1.1)
│       ├── models.py            # Pydantic data models (Story 1.2)
│       ├── portfolio_utils.py   # Portfolio parsing functions (Story 1.2)
│       └── metta_interface.py   # MeTTa query abstraction layer (Story 2.1)
├── data/                        # Data files embedded with agents
│   ├── demo-wallets.json        # Pre-configured demo portfolios (Story 1.2, 3.3)
│   ├── historical-crashes.json  # Market crash scenario data (Story 1.4, 1.6)
│   ├── sector-mappings.json     # Token-to-sector classifications (Story 1.5)
│   ├── historical_prices/       # Historical price CSVs by token (Story 1.2)
│   │   ├── README.md            # Data collection metadata
│   │   ├── ETH.csv
│   │   ├── UNI.csv
│   │   ├── AAVE.csv
│   │   └── ...                  # 30+ token CSVs
│   ├── DEMO_WALLETS.md          # Demo wallet documentation (Story 1.2)
│   └── metta_knowledge/         # MeTTa knowledge graph files (.metta) (Story 2.1)
│       ├── crashes.metta
│       ├── sectors.metta
│       └── correlations.metta
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_hello_world.py      # Hello world agent tests (Story 1.1)
│   ├── test_portfolio_utils.py  # Portfolio parsing tests (Story 1.2)
│   ├── test_agents.py           # Unit tests for agent logic (Story 1.3+)
│   ├── test_integration.py      # Inter-agent communication tests (Story 1.7+)
│   └── test_metta_queries.py    # MeTTa query accuracy validation (Story 2.1)
├── docs/                        # Documentation
│   ├── README.md                # Main project documentation
│   ├── prd/                     # Product requirements (sharded)
│   │   ├── epic-list.md         # High-level epic summaries
│   │   └── epic-details.md      # Detailed epic and story specifications
│   ├── architecture/            # Architecture documentation (sharded)
│   │   ├── index.md             # Architecture navigation
│   │   ├── introduction.md
│   │   ├── high-level-architecture.md
│   │   ├── source-tree.md       # This file
│   │   ├── data-models.md       # Pydantic model definitions
│   │   ├── api-specification.md
│   │   ├── components.md
│   │   ├── core-workflows.md
│   │   ├── development-workflow.md
│   │   ├── coding-standards.md
│   │   ├── testing-strategy.md
│   │   ├── tech-stack.md
│   │   ├── deployment-architecture.md
│   │   └── conclusion.md
│   ├── stories/                 # Story documentation
│   │   ├── 1.1.story.md         # Project setup (Done)
│   │   ├── 1.2.story.md         # Portfolio data structure (Current)
│   │   └── ...                  # Future stories
│   ├── qa/                      # Quality assurance artifacts
│   │   ├── gates/               # Story completion gates
│   │   └── assessments/         # QA review assessments
│   ├── DEMO.md                  # Demo instructions for judges (Story 3.4)
│   └── sample-responses/        # Expected agent responses for demo wallets (Story 3.3)
│       ├── wallet-1-high-risk.json
│       ├── wallet-2-moderate-risk.json
│       └── wallet-3-diversified.json
├── scripts/                     # Deployment and utility scripts
│   ├── deploy_agents.sh         # Agent deployment automation (Story 3.2)
│   └── download_prices.py       # CoinGecko data collection script (Story 1.2)
├── .github/                     # GitHub configuration
│   └── workflows/
│       └── ci.yml               # CI/CD workflow (Story 1.1)
├── .bmad-core/                  # BMAD framework files (not part of Guardian)
│   ├── core-config.yaml         # Project configuration
│   ├── tasks/                   # Agent workflow tasks
│   ├── checklists/              # Process checklists
│   ├── templates/               # Document templates
│   └── agents/                  # BMAD agent definitions
├── .env.example                 # Environment variable template (Story 1.1)
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies (pinned versions)
├── README.md                    # Root readme (duplicates docs/README.md)
└── CLAUDE.md                    # AI agent development guidelines
```

## Directory Purposes

### `/agents/`
Contains all uAgents agent implementations. Each agent is an autonomous entity that communicates via asynchronous message-passing.

**Key Files:**
- `guardian.py` - Main orchestrator that coordinates specialized agents (Epic 2)
- `correlation_agent.py` - Analyzes portfolio correlation to ETH (Story 1.3-1.4)
- `sector_agent.py` - Analyzes sector concentration risk (Story 1.5-1.6)

**Shared Utilities (`/agents/shared/`):**
- `config.py` - Centralized environment variable loading
- `models.py` - Pydantic data models (Portfolio, TokenHolding, etc.)
- `portfolio_utils.py` - Portfolio parsing and validation functions
- `metta_interface.py` - MeTTa knowledge graph query abstraction

### `/data/`
Static data files deployed alongside agents. All files use kebab-case naming convention.

**Data Categories:**
- **Demo portfolios** - Pre-configured wallets with known risk profiles
- **Historical data** - Market crashes, price history, sector performance
- **Configuration** - Token-to-sector mappings, crash scenarios
- **Knowledge graphs** - MeTTa files for semantic queries

### `/tests/`
Comprehensive test suite following testing pyramid (30% unit, 60% integration, 10% E2E).

**Test Organization:**
- Unit tests - Test individual functions in isolation with mocked dependencies
- Integration tests - Test inter-agent communication and message-passing
- MeTTa tests - Validate knowledge graph query accuracy

### `/docs/`
All project documentation organized by type.

**Subdirectories:**
- `prd/` - Product requirements and epic definitions
- `architecture/` - Technical architecture documentation (sharded)
- `stories/` - Individual story specifications with Dev Notes
- `qa/` - Quality assurance artifacts (gates, assessments)

### `/scripts/`
Automation scripts for deployment and data collection.

**Planned Scripts:**
- `deploy_agents.sh` - Deploy all 3 agents to Agentverse
- `download_prices.py` - Download historical price data from CoinGecko

## File Naming Conventions

Following project coding standards (architecture/coding-standards.md):

| File Type | Convention | Examples |
|-----------|-----------|----------|
| Agent files | snake_case | `correlation_agent.py`, `sector_agent.py` |
| Python modules | snake_case | `portfolio_utils.py`, `metta_interface.py` |
| Data files | kebab-case | `demo-wallets.json`, `historical-crashes.json` |
| Documentation | kebab-case | `source-tree.md`, `tech-stack.md` |
| Test files | `test_*.py` | `test_portfolio_utils.py`, `test_integration.py` |

## Key File Relationships

### Portfolio Data Flow
```
data/demo-wallets.json
  ↓ (parsed by)
agents/shared/portfolio_utils.py
  ↓ (validates using)
agents/shared/models.py (Portfolio, TokenHolding)
  ↓ (consumed by)
agents/correlation_agent.py + agents/sector_agent.py
  ↓ (synthesized by)
agents/guardian.py
```

### Historical Data Integration
```
data/historical_prices/*.csv
  ↓ (loaded by)
agents/correlation_agent.py (calculates returns)

data/metta_knowledge/*.metta
  ↓ (queried via)
agents/shared/metta_interface.py
  ↓ (used by)
agents/correlation_agent.py + agents/sector_agent.py
```

### Testing Flow
```
tests/test_portfolio_utils.py
  ↓ (tests)
agents/shared/portfolio_utils.py

tests/test_integration.py
  ↓ (tests)
guardian → correlation_agent → sector_agent (message flow)
```

## Import Path Examples

When working with shared modules, use absolute imports from the project root:

```python
# Correct: Absolute imports from project root
from agents.shared.config import get_env_var
from agents.shared.models import Portfolio, TokenHolding
from agents.shared.portfolio_utils import parse_portfolio, load_demo_wallet

# Incorrect: Relative imports can break depending on execution context
from ..shared.config import get_env_var  # Avoid
```

## Development Environment Files

**Not committed to git:**
- `.env` - Local environment variables (contains secrets)
- `venv/` - Python virtual environment
- `__pycache__/` - Python bytecode cache
- `.pytest_cache/` - Pytest cache
- `.mypy_cache/` - MyPy type checking cache
- `.ruff_cache/` - Ruff linting cache
- `.coverage` - Coverage.py data file

**Committed to git:**
- `.env.example` - Template showing required environment variables
- `.gitignore` - Specifies files to exclude from version control

## Story-to-File Mapping

Quick reference for which stories create which files:

**Story 1.1 (Project Setup):**
- agents/__init__.py
- agents/shared/__init__.py
- agents/shared/config.py
- agents/hello_world_agent.py
- agents/test_client_agent.py
- tests/__init__.py
- tests/test_hello_world.py
- tests/test_integration.py (stub)
- requirements.txt
- .env.example
- .github/workflows/ci.yml
- README.md

**Story 1.2 (Portfolio Data Structure):**
- agents/shared/models.py
- agents/shared/portfolio_utils.py
- data/demo-wallets.json
- data/historical_prices/*.csv (30+ files)
- data/historical_prices/README.md
- data/DEMO_WALLETS.md
- tests/test_portfolio_utils.py

**Story 1.3-1.4 (CorrelationAgent):**
- agents/correlation_agent.py
- data/historical-crashes.json
- tests/test_agents.py (correlation tests)

**Story 1.5-1.6 (SectorAgent):**
- agents/sector_agent.py
- data/sector-mappings.json
- tests/test_agents.py (sector tests)

**Story 2.1 (MeTTa Integration):**
- agents/shared/metta_interface.py
- data/metta_knowledge/*.metta
- tests/test_metta_queries.py

**Story 2.2-2.5 (Guardian Orchestrator):**
- agents/guardian.py
- tests/test_integration.py (full Guardian tests)

**Story 3.2 (Deployment):**
- scripts/deploy_agents.sh

**Story 3.3-3.4 (Documentation):**
- docs/DEMO.md
- docs/sample-responses/*.json

---
