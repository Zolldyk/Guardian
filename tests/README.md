# Guardian Integration Test Suite

**Story 1.7: Specialized Agent Integration Testing**

This directory contains comprehensive integration tests for the Guardian multi-agent portfolio risk analysis system. The test suite validates end-to-end functionality of CorrelationAgent and SectorAgent with realistic demo portfolios.

## Table of Contents

- [Overview](#overview)
- [Running Tests](#running-tests)
- [Test Organization](#test-organization)
- [Demo Wallet Test Results](#demo-wallet-test-results)
- [Agent Response Samples](#agent-response-samples)
- [Test Coverage](#test-coverage)
- [Hosted Agent Testing](#hosted-agent-testing)
- [Troubleshooting](#troubleshooting)

---

## Overview

The integration test suite validates:

- **CorrelationAgent**: ETH correlation analysis with 3 risk profiles (high/moderate/low)
- **SectorAgent**: Sector concentration analysis with diversification scoring
- **Error Handling**: Empty portfolios, single tokens, unknown tokens
- **Response Times**: All agents respond in <5 seconds
- **Message Protocols**: AnalysisRequest/Response serialization
- **README Completeness**: Agent documentation meets requirements
- **Chat Protocol**: Natural language query handling (hosted agents only)
- **ASI:One Discoverability**: Agent visibility in ASI:One interface (manual verification)

---

## Running Tests

### Run All Integration Tests

```bash
# From project root
pytest tests/test_integration.py -v
```

### Run Specific Test Classes

```bash
# CorrelationAgent tests only
pytest tests/test_integration.py::TestCorrelationAgentDemoWallets -v

# SectorAgent tests only
pytest tests/test_integration.py::TestSectorAgentDemoWallets -v

# Error handling tests
pytest tests/test_integration.py::TestErrorHandling -v

# README validation tests
pytest tests/test_integration.py::TestAgentREADMEValidation -v

# Comprehensive risk profile test
pytest tests/test_integration.py::TestComprehensiveRiskProfiles -v
```

### Run Tests with Detailed Logging

```bash
# Logs saved to tests/integration_test.log
pytest tests/test_integration.py -v --log-cli-level=DEBUG
```

### Run Tests with Coverage Report

```bash
pytest tests/test_integration.py --cov=agents --cov-report=html
# Open htmlcov/index.html to view coverage report
```

### Skip Hosted Agent Tests

By default, hosted agent tests are skipped (require Agentverse deployment).

```bash
# Run only local agent tests (default)
pytest tests/test_integration.py -v -m "not hosted"
```

### Run Hosted Agent Tests (After Deployment)

```bash
# Requires CORRELATION_AGENT_ADDRESS_HOSTED and SECTOR_AGENT_ADDRESS_HOSTED in .env
pytest tests/test_integration.py -v -m hosted
```

---

## Test Organization

### Test Classes

| Test Class | Purpose | Acceptance Criteria |
|------------|---------|---------------------|
| `TestCorrelationAgentDemoWallets` | Test CorrelationAgent with all 3 demo wallets | AC 2, 4, 6, 7, 8, 11 |
| `TestSectorAgentDemoWallets` | Test SectorAgent with all 3 demo wallets | AC 3, 4, 6, 7, 8, 11 |
| `TestErrorHandling` | Test error handling for edge cases | AC 5 |
| `TestChatProtocolIntegration` | Test Chat Protocol with natural language queries | AC 12, 13, 14 |
| `TestLocalVsHostedConsistency` | Compare local and hosted agent outputs | AC 16 |
| `TestAgentREADMEValidation` | Validate agent README completeness | AC 17 |
| `TestComprehensiveRiskProfiles` | Validate all 3 demo wallets return expected risk profiles | AC 7, 8 |

### Test Files

- **test_integration.py**: Main integration test suite (extended in Story 1.7)
- **test_agents.py**: Unit tests for individual agent functions
- **test_portfolio_utils.py**: Portfolio parsing and validation tests
- **integration_test.log**: Detailed test execution logs
- **sample_responses/**: Sample agent responses for demo wallets

---

## Demo Wallet Test Results

The integration tests use 3 pre-configured demo wallets from `data/demo-wallets.json`:

### Demo Wallet 1: High Risk DeFi Whale

**Expected Risk Profile**: HIGH

**Portfolio Composition**:
- Address: `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58`
- Total Value: $135,198
- Tokens: 9 DeFi governance tokens (UNI, AAVE, COMP, MKR, MATIC, OP, SNX, CRV, BAL)

**CorrelationAgent Results**:
- **Correlation**: Expected >85% (High correlation to ETH)
- **Interpretation**: "High" - Portfolio closely follows ETH movements
- **Historical Context**: Crash scenarios from 2020-2022 included
- **Response Time**: <5 seconds ✅

**SectorAgent Results**:
- **Diversification Score**: "High Concentration"
- **Concentrated Sectors**: ["DeFi Governance"] (>60% of portfolio)
- **Risk Level**: High sector concentration detected
- **Response Time**: <5 seconds ✅

---

### Demo Wallet 2: Moderate Risk Balanced Portfolio

**Expected Risk Profile**: MODERATE

**Portfolio Composition**:
- Address: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`
- Total Value: $89,855
- Tokens: 10 mixed tokens (ETH, DeFi, stablecoins)

**CorrelationAgent Results**:
- **Correlation**: Expected 70-85% (Moderate correlation)
- **Interpretation**: "Moderate" - Some diversification but still correlated
- **Response Time**: <5 seconds ✅

**SectorAgent Results**:
- **Diversification Score**: "Moderate Concentration"
- **Concentrated Sectors**: Some concentration (40-60%)
- **Response Time**: <5 seconds ✅

---

### Demo Wallet 3: Well-Diversified Conservative

**Expected Risk Profile**: LOW (Well-Diversified)

**Portfolio Composition**:
- Address: `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8`
- Total Value: $149,490.50
- Tokens: 12 diversified tokens (BTC, ETH, SOL, AVAX, stablecoins, DeFi, L1 alts)

**CorrelationAgent Results**:
- **Correlation**: Expected <70% (Low correlation)
- **Interpretation**: "Low" - Good diversification
- **Response Time**: <5 seconds ✅

**SectorAgent Results**:
- **Diversification Score**: "Well-Diversified"
- **Concentrated Sectors**: [] (No sector exceeds 60%)
- **Response Time**: <5 seconds ✅

---

## Agent Response Samples

Sample agent responses are logged during test execution and saved to `tests/integration_test.log`.

### Sample CorrelationAgent Response (High Risk Wallet)

```
=== Demo Wallet 1 (High Risk) Correlation Analysis ===
Correlation: 87%
Interpretation: High
Narrative: Your portfolio is 87% positively correlated to ETH over the past 90 days.
This is High correlation. When ETH crashes, your portfolio will likely crash equally hard.

Historical crash performance:
- 2022 Bear Market: -68% portfolio loss (ETH: -75%)
- 2021 Correction: -48% portfolio loss (ETH: -55%)
- 2020 COVID Crash: -58% portfolio loss (ETH: -65%)

Response time: 3247ms
```

### Sample SectorAgent Response (High Risk Wallet)

```
=== Demo Wallet 1 (High Risk) Sector Analysis ===
Diversification Score: High Concentration
Concentrated Sectors: ['DeFi Governance']
Sector Breakdown: {
  'DeFi Governance': {'percentage': 68.5, 'value_usd': 92635.0},
  'Layer-2': {'percentage': 17.2, 'value_usd': 23260.0},
  'DeFi Exchange': {'percentage': 14.3, 'value_usd': 19303.0}
}
Narrative: 68% of your portfolio is concentrated in DeFi Governance tokens,
creating significant sector risk.

Response time: 2891ms
```

---

## Test Coverage

### Acceptance Criteria Coverage

| AC | Requirement | Status | Test Class |
|----|-------------|--------|------------|
| 1 | Integration test suite created | ✅ | `test_integration.py` extended |
| 2 | CorrelationAgent tested with 3 demo wallets | ✅ | `TestCorrelationAgentDemoWallets` |
| 3 | SectorAgent tested with 3 demo wallets | ✅ | `TestSectorAgentDemoWallets` |
| 4 | Response times <5 seconds | ✅ | All demo wallet tests |
| 5 | Error handling tested | ✅ | `TestErrorHandling` |
| 6 | Hosted agents accessible | ⏭️ | `test_*_hosted_accessible` (skipped - requires deployment) |
| 7 | All 3 wallets return expected risk profiles | ✅ | `TestComprehensiveRiskProfiles` |
| 8 | Agent responses logged for review | ✅ | All tests log to `integration_test.log` |
| 9 | 100% integration tests pass | ✅ | Run `pytest tests/test_integration.py` |
| 10 | Test results documented | ✅ | This README |
| 11 | Hosted versions deployed and accessible | ⏭️ | Requires manual Agentverse deployment |
| 12 | Chat Protocol integration works | ⏭️ | `TestChatProtocolIntegration` (skipped) |
| 13 | AI parameter extraction validated | ⏭️ | `TestChatProtocolIntegration` (skipped) |
| 14 | Session management validated | ⏭️ | `TestChatProtocolIntegration` (skipped) |
| 15 | Agents discoverable in ASI:One | ⏭️ | Manual verification required |
| 16 | Local vs hosted consistency | ⏭️ | `TestLocalVsHostedConsistency` (skipped) |
| 17 | Agent READMEs validated | ✅ | `TestAgentREADMEValidation` |

**Legend**: ✅ Passing | ⏭️ Skipped (requires hosted deployment) | ❌ Failing

### Current Test Results

```bash
# Run tests to see current status
pytest tests/test_integration.py -v
```

**Expected Results**:
- All local integration tests: **PASS** ✅
- Hosted agent tests: **SKIPPED** (requires deployment)
- README validation tests: **PASS** ✅
- Error handling tests: **PASS** ✅

---

## Hosted Agent Testing

### Prerequisites for Hosted Tests

1. **Deploy Agents to Agentverse**:
   ```bash
   # Deploy correlation_agent_hosted.py and sector_agent_hosted.py
   # Follow deployment guide in docs/architecture/agentverse-deployment-guide.md
   ```

2. **Configure Environment Variables**:
   ```bash
   # Add to .env file
   CORRELATION_AGENT_ADDRESS_HOSTED=agent1qw...
   SECTOR_AGENT_ADDRESS_HOSTED=agent1qx...
   ```

3. **Run Hosted Tests**:
   ```bash
   pytest tests/test_integration.py -v -m hosted
   ```

### Manual Verification Steps

#### Chat Protocol Testing (AC 12-14)

1. Open ASI:One interface
2. Search for "correlation agent" or "sector agent"
3. Send natural language query: "Analyze wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
4. Verify agent responds with analysis
5. Send follow-up query to test session management

#### ASI:One Discoverability (AC 15)

1. Search ASI:One for "correlation" or "ETH correlation"
2. Verify CorrelationAgent appears in results
3. Verify agent README is visible in overview
4. Verify `publish_manifest=True` in agent code
5. Repeat for SectorAgent with "sector concentration"

#### Local vs Hosted Consistency (AC 16)

1. Send identical `AnalysisRequest` to both local and hosted CorrelationAgent
2. Compare `correlation_percentage` (should match within ±2%)
3. Compare `historical_context` crash scenarios (should be identical)
4. Repeat for SectorAgent
5. Log any discrepancies for investigation

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

```
ModuleNotFoundError: No module named 'agents'
```

**Solution**: Run tests from project root:
```bash
cd /Users/pc/Guardian
pytest tests/test_integration.py -v
```

#### 2. Demo Wallets Not Found

```
FileNotFoundError: data/demo-wallets.json not found
```

**Solution**: Verify `data/demo-wallets.json` exists:
```bash
ls -la data/demo-wallets.json
```

#### 3. Test Timeout (>30 seconds)

```
FAILED tests/test_integration.py::test_correlation_agent_demo_wallet_1 - TimeoutError
```

**Solution**: Check historical price data availability. Agents may be fetching data from GitHub. Increase timeout in `pytest.ini` if needed.

#### 4. Correlation Calculation Fails

```
ErrorMessage: Insufficient historical data
```

**Solution**: Verify historical price data exists for all tokens in demo wallet. Check `data/historical_prices/` directory.

#### 5. Hosted Agent Tests Fail

```
AssertionError: CORRELATION_AGENT_ADDRESS_HOSTED not configured
```

**Solution**: These tests are meant to be skipped unless hosted agents are deployed. Deploy agents to Agentverse and add addresses to `.env` file.

---

## Test Execution Tips

### Fast Test Run (Skip Slow Tests)

```bash
pytest tests/test_integration.py -v -m "not slow"
```

### Run Single Test

```bash
pytest tests/test_integration.py::TestCorrelationAgentDemoWallets::test_correlation_agent_demo_wallet_1_high_risk -v
```

### Debug Mode with Print Statements

```bash
pytest tests/test_integration.py -v -s --log-cli-level=DEBUG
```

### Generate HTML Test Report

```bash
pytest tests/test_integration.py --html=tests/report.html --self-contained-html
```

---

## Next Steps

### After Completing Story 1.7

1. **Deploy Agents to Agentverse** (Epic 2):
   - Deploy `correlation_agent_hosted.py`
   - Deploy `sector_agent_hosted.py`
   - Configure `.env` with hosted addresses

2. **Run Hosted Tests**:
   ```bash
   pytest tests/test_integration.py -v -m hosted
   ```

3. **Manual Verification**:
   - Test Chat Protocol in ASI:One
   - Verify agent discoverability
   - Validate local vs hosted consistency

4. **Proceed to Epic 2: Guardian Orchestrator**:
   - Build Guardian agent to coordinate CorrelationAgent + SectorAgent
   - Add end-to-end integration tests for full workflow

---

## Additional Resources

- **Architecture Documentation**: `docs/architecture/`
- **Coding Standards**: `docs/architecture/coding-standards.md`
- **Testing Strategy**: `docs/architecture/testing-strategy.md`
- **Agent READMEs**:
  - `agents/correlation_agent_README.md`
  - `agents/sector_agent_README.md`

---

**Last Updated**: 2025-10-22 (Story 1.7 Completion)

**Test Suite Status**: ✅ All local integration tests passing
