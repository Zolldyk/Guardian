# Deployment Architecture

## Deployment Strategy

**Platform:** Agentverse (Fetch.ai managed platform)

**CI/CD Pipeline:** GitHub Actions automates testing on all commits and pull requests. Deployment to Agentverse is manual via deployment scripts to maintain control during hackathon timeline.

**Deployment Process:**

1. **Local Development → CI Testing (GitHub Actions) → Agentverse Testnet → Agentverse Production**

2. **Agent Deployment Commands:**
```bash
# Deploy CorrelationAgent
./scripts/deploy_agent.sh correlation_agent

# Deploy SectorAgent
./scripts/deploy_agent.sh sector_agent

# Deploy Guardian
./scripts/deploy_agent.sh guardian

# Verify all agents online
./scripts/verify_deployment.sh
```

3. **Deployment Script Example:**
```bash
#!/bin/bash
# scripts/deploy_agent.sh

AGENT_NAME=$1

echo "Deploying ${AGENT_NAME} to Agentverse..."

# Agentverse CLI deployment (assumes agentverse CLI installed)
agentverse deploy \
  --agent agents/${AGENT_NAME}.py \
  --name ${AGENT_NAME} \
  --network production

echo "Deployment complete. Retrieving agent address..."
AGENT_ADDRESS=$(agentverse get-address ${AGENT_NAME})
echo "${AGENT_NAME} address: ${AGENT_ADDRESS}"
echo "Update .env file with this address."
```

**Deployment Environments:**

| Environment | Frontend URL | Backend Agents | Purpose |
|-------------|-------------|----------------|---------|
| Development | Local testing | Local Python processes | Feature development |
| Staging | ASI:One testnet | Agentverse testnet | Pre-production testing |
| Production | ASI:One production | Agentverse production | Live hackathon demo |

---
