# Testing Strategy

## Testing Pyramid

Guardian follows a pragmatic testing approach optimized for the 10-day hackathon timeline:

```
        E2E Tests (10%)
       /              \
    Integration (60%)
   /                    \
  Unit Tests (30%)
```

**Time Allocation:**
- **Unit Tests:** 30% of testing effort - Core logic isolation
- **Integration Tests:** 60% of testing effort - Inter-agent communication reliability
- **E2E Tests:** 10% of testing effort - Manual testing via ASI:One

## Unit Tests

**Scope:** Test individual agent logic in isolation with mocked dependencies.

**Location:** `tests/test_agents.py`

**Example Test Cases:**

```python
# tests/test_agents.py
import pytest
from unittest.mock import Mock, patch
from agents.correlation_agent import calculate_portfolio_returns
from agents.sector_agent import classify_tokens
from agents.guardian import synthesize_analysis, detect_compounding_risk

def test_correlation_calculation():
    """Test Pearson correlation coefficient calculation."""
    portfolio_returns = [0.05, -0.03, 0.02, 0.01]
    eth_returns = [0.06, -0.02, 0.03, 0.01]

    correlation = calculate_correlation(portfolio_returns, eth_returns)

    assert 0.8 <= correlation <= 1.0  # High correlation expected

def test_sector_classification():
    """Test token-to-sector mapping."""
    tokens = ["UNI", "AAVE", "MATIC"]

    sector_map = classify_tokens(tokens)

    assert sector_map["UNI"] == "DeFi Governance"
    assert sector_map["MATIC"] == "Layer-2"

def test_compounding_risk_detection():
    """Test synthesis logic detects compounding risk."""
    correlation_analysis = Mock(correlation_percentage=95)
    sector_analysis = Mock(concentrated_sectors=["DeFi Governance"])

    compounding_detected = detect_compounding_risk(correlation_analysis, sector_analysis)

    assert compounding_detected == True

@patch('agents.shared.metta_interface.query_metta')
def test_metta_fallback(mock_query):
    """Test JSON fallback when MeTTa unavailable."""
    mock_query.side_effect = ConnectionError("MeTTa unavailable")

    crash_data = get_historical_crash_data("2022-bear")

    assert crash_data["name"] == "2022 Bear Market"  # From JSON fallback
```

**Coverage Target:** 70% code coverage on critical business logic

---

## Integration Tests

**Scope:** Test inter-agent communication, message serialization, and end-to-end workflows.

**Location:** `tests/test_integration.py`

**Example Test Cases:**

```python
# tests/test_integration.py
import pytest
from uagents import Agent
from agents.guardian import guardian
from agents.correlation_agent import correlation_agent
from agents.sector_agent import sector_agent

@pytest.mark.asyncio
async def test_guardian_to_correlation_agent():
    """Test Guardian → CorrelationAgent message flow."""
    portfolio = load_demo_portfolio("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")

    request = AnalysisRequest(
        request_id="test_req_1",
        wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        portfolio=portfolio,
        requested_by="guardian_test"
    )

    # Send request to CorrelationAgent
    response = await send_and_wait(correlation_agent.address, request, timeout=10.0)

    assert isinstance(response, CorrelationAnalysisResponse)
    assert response.request_id == "test_req_1"
    assert 0 <= response.analysis.correlation_percentage <= 100
    assert response.processing_time_ms < 5000

@pytest.mark.asyncio
async def test_full_analysis_demo_wallet_1():
    """Test complete flow for high-risk demo wallet."""
    chat_msg = ChatMessage(
        user_id="test_user",
        message_text="Analyze wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        session_id="test_session",
        timestamp=datetime.utcnow()
    )

    response = await send_and_wait(guardian.address, chat_msg, timeout=60.0)

    assert isinstance(response, ChatResponse)
    assert "95% correlated" in response.response_text  # Expected for demo wallet 1
    assert "68%" in response.response_text  # Expected sector concentration
    assert "compounding" in response.response_text.lower()
    assert len(response.metadata["recommendations"]) >= 2

@pytest.mark.asyncio
async def test_timeout_handling():
    """Test Guardian handles CorrelationAgent timeout gracefully."""
    # Simulate CorrelationAgent being unavailable
    with patch('agents.correlation_agent.correlation_agent', None):
        chat_msg = ChatMessage(...)

        response = await send_and_wait(guardian.address, chat_msg, timeout=15.0)

        # Guardian should proceed with SectorAgent results only
        assert "correlation analysis unavailable" in response.response_text.lower()
```

**Coverage Target:** 100% of demo scenarios pass integration tests

---

## E2E Tests (Browser Automation)

**Scope:** Test user-facing workflows through live browser automation, validating ASI:One interface interactions and complete end-to-end scenarios.

**Tool:** Playwright MCP (Model Context Protocol integration)

**Capabilities:**
- **Live Browser Testing:** Automate Chromium, Firefox, and WebKit browsers
- **Visual Validation:** Screenshot comparisons and visual regression testing
- **Interactive Testing:** Simulate user interactions with ASI:One chat interface
- **Network Monitoring:** Capture and validate agent communication patterns
- **Claude Code Integration:** Execute browser tests directly through Claude Code

**Example Use Cases:**

```python
# Example: Testing ASI:One chat interface interaction
# Note: Playwright MCP is accessed through Claude Code, not directly in code

# Test Case 1: Verify wallet analysis workflow
1. Navigate to ASI:One chat interface
2. Send message: "Analyze wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
3. Verify Guardian agent responds within 60 seconds
4. Validate response contains correlation percentage
5. Validate response contains sector concentration data
6. Capture screenshot of complete analysis

# Test Case 2: Verify recommendation rendering
1. Send analysis request for high-risk demo wallet
2. Wait for Guardian response
3. Verify recommendations section is present
4. Validate minimum 2 recommendations displayed
5. Check for "compounding risk" warning message

# Test Case 3: Network validation
1. Monitor network requests during analysis
2. Verify agent-to-agent message passing occurs
3. Validate response times < 5s for each specialist agent
4. Check for timeout handling if agent unavailable
```

**Testing Strategy:**
- **Manual execution via Claude Code:** Use Playwright MCP through Claude Code for ad-hoc E2E testing
- **Visual regression:** Compare screenshots across releases to detect UI changes
- **Cross-browser validation:** Test on Chromium, Firefox, and WebKit to ensure compatibility
- **Performance monitoring:** Track page load times and agent response times

**Coverage Target:** 100% of critical user workflows validated through live browser testing

---
