# Development Workflow

## Local Development Setup

**Prerequisites:**
```bash
# Python 3.10 or higher
python --version

# Verify pip
pip --version
```

**Initial Setup:**
```bash
# Clone repository
git clone https://github.com/your-username/guardian.git
cd guardian

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with agent addresses (obtained after first deployment to Agentverse)
# GUARDIAN_ADDRESS=agent1qy...
# CORRELATION_AGENT_ADDRESS=agent1qw...
# SECTOR_AGENT_ADDRESS=agent1qx...
```

**Development Commands:**
```bash
# Run unit tests
pytest tests/test_agents.py -v

# Run integration tests (requires deployed agents)
pytest tests/test_integration.py -v

# Run all tests with coverage
pytest --cov=agents --cov-report=html

# Lint code
ruff check agents/

# Type check
mypy agents/

# Run local agent for development (Guardian example)
python agents/guardian.py
```

## Environment Configuration

**Required Environment Variables:**

```bash
# .env file structure
# Agent Addresses (assigned by Agentverse on deployment)
GUARDIAN_ADDRESS=agent1qy4mj8k2nqz...
CORRELATION_AGENT_ADDRESS=agent1qw9xth4kl2p...
SECTOR_AGENT_ADDRESS=agent1qx7bvc3mn8s...

# Agent Seeds (for deterministic address generation)
GUARDIAN_SEED=<secret_seed_guardian>
CORRELATION_AGENT_SEED=<secret_seed_correlation>
SECTOR_AGENT_SEED=<secret_seed_sector>

# MeTTa Configuration
METTA_ENABLED=true
METTA_KNOWLEDGE_PATH=./data/metta_knowledge/

# Logging
LOG_LEVEL=INFO
```

---
