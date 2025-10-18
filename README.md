# Guardian

**AI-powered crypto portfolio risk analysis using multi-agent systems**

Guardian is a sophisticated portfolio risk assessment tool built on the Fetch.ai uAgents framework, designed for the ASI Alliance Hackathon. It analyzes cryptocurrency portfolios for systemic risks by detecting high asset correlations and sector concentration issues that could lead to cascading losses during market downturns.

## Overview

Guardian uses a multi-agent architecture to provide comprehensive portfolio risk analysis:

- **Guardian Agent**: Main orchestrator that coordinates risk analysis
- **Correlation Agent**: Analyzes asset correlations using historical crash data
- **Sector Agent**: Evaluates sector concentration risks

The system leverages MeTTa knowledge graphs (SingularityNET Hyperon) to store historical market crash scenarios and semantic relationships between crypto sectors.

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

The seed phrase generates a deterministic address, enabling other agents to discover and communicate with it.

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
   - Option B: Use CLI deployment (future: `scripts/deploy_agents.sh`)

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

### Project Documentation

- `docs/prd/` - Product requirements (sharded)
- `docs/architecture/` - Architecture documentation (sharded)
- `docs/stories/` - Development stories

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

## Contributing

This project follows strict coding standards:

- **Agent Files**: snake_case (e.g., `correlation_agent.py`)
- **Message Models**: PascalCase (e.g., `AnalysisRequest`)
- **Message Handlers**: `handle_` prefix (e.g., `handle_analysis_request`)
- **Environment Variables**: SCREAMING_SNAKE_CASE

See `docs/architecture/coding-standards.md` for complete guidelines.

## License

This project is developed for the ASI Alliance Hackathon.

## Support

For issues or questions:
- GitHub Issues: https://github.com/Zolldyk/Guardian/issues
- Fetch.ai Discord: https://discord.gg/fetchai
