# Guardian Sample Responses

This directory contains complete Guardian analysis responses for all three demo wallets. These sample responses serve multiple purposes:

1. **Verification:** Compare your ASI:One test results against expected outputs
2. **Response Structure Reference:** Understand the format and content of Guardian's multi-agent analysis
3. **Transparency Demonstration:** See complete agent responses with addresses, timing, and synthesis logic

---

## File Structure

| File | Wallet Address | Risk Profile | Purpose |
|------|---------------|--------------|---------|
| `wallet-1-high-risk-transparency.md` | `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58` | High Risk | Demonstrates compounding risk detection (95% correlation + 68% sector concentration) |
| `wallet-2-moderate-risk.md` | `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0` | Moderate Risk | Shows balanced portfolio analysis with incremental recommendations |
| `wallet-3-diversified.md` | `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8` | Well-Diversified | Validates Guardian recognizes excellent portfolio structure |
| `multi-turn-conversation-example.md` | (Various) | N/A | Demonstrates Guardian's conversational follow-up capabilities |
| `README.md` | N/A | N/A | This file—explains sample response structure |

---

## Response Format

All sample responses follow this structure:

### 1. Request Details (Metadata)

```markdown
**Wallet Address:** 0x...
**Demo Profile:** High Risk / Moderate Risk / Well-Diversified
**Portfolio Value:** $XXX,XXX USD
**Key Holdings:** Token allocations
**Analysis Timestamp:** ISO 8601 timestamp
**Agent Versions:** Guardian v1.0.0, CorrelationAgent v1.0.0, SectorAgent v1.0.0
```

**Purpose:** Provides context for judges. Timestamps prove responses are from actual agent runs, not manually crafted examples.

### 2. Full Guardian Response

The complete multi-agent response as it would appear in ASI:One, including:

#### Section 1: CorrelationAgent Analysis

```
CorrelationAgent Analysis (agent1q...):

Your portfolio is XX% correlated to ETH. [Narrative explanation]

Historical Context:
- 2022 Bear Market: [Loss percentages and context]
- 2021 May Flash Crash: [Loss percentages and context]

(Processing: XXXXms)
```

**Key Elements:**
- **Header:** identifies CorrelationAgent section
- **Agent address:** Truncated address in header (`agent1q...`)
- **Correlation percentage:** Quantitative risk metric
- **Historical context:** Crash scenarios from MeTTa knowledge graph
- **Processing time:** Demonstrates parallel processing efficiency

#### Section 2: SectorAgent Analysis

```
🏛️ SectorAgent Analysis (agent1q...):

XX% of your portfolio is concentrated in [Sector Name]. [Narrative explanation]

Sector Breakdown:
- Sector 1: XX% ($XX,XXX) - [Tokens]
- Sector 2: XX% ($XX,XXX) - [Tokens]
...

Historical Sector Risks:
- 2022 Bear Market: [Sector-specific performance]

(Processing: XXXXms)
```

**Key Elements:**
- **Header:** identifies SectorAgent section
- **Agent address:** Truncated address in header
- **Sector concentration percentage:** Quantitative risk metric
- **Sector breakdown:** Complete allocation with token examples
- **Historical sector risks:** Sector-specific crash performance
- **Processing time:** Shows SectorAgent timing

#### Section 3: Guardian Synthesis

```
Guardian Synthesis:

Risk Level: Critical / Moderate / Low
Compounding Risk Detected: Yes / No

[Synthesis narrative referencing both CorrelationAgent and SectorAgent by name]

Risk Multiplier: X.Xx

Recommendations:
1. [Prioritized recommendation with rationale and expected impact]
2. [Second recommendation]
3. [Third recommendation]

---

Agents Consulted:
- CorrelationAgent (agent1q...[full address]) - XXXXms
- SectorAgent (agent1q...[full address]) - XXXXms

Total Analysis Time: X.X seconds
```

**Key Elements:**
- **Header:** identifies Guardian synthesis section
- **Risk level:** Critical / Moderate / Low classification
- **Compounding risk detection:** Yes/No flag for dual-risk pattern
- **Synthesis narrative:** References both agents by name ("As CorrelationAgent showed...", "SectorAgent revealed...")
- **Risk multiplier:** Quantifies compounding effect (e.g., 3.2x leverage)
- **Recommendations:** 2-3 prioritized suggestions with rationale and expected impact
- **Agents consulted:** Full agent addresses for verification
- **Total analysis time:** End-to-end processing time

### 3. Key Characteristics (Educational)

Explains why this portfolio has this risk level, highlighting:
- Correlation analysis
- Sector concentration analysis
- Compounding risk logic (if applicable)
- Recommendation prioritization

### 4. Comparison Tables (Validation)

Provides side-by-side comparison of all three demo wallets for easy verification:

| Metric | Wallet 1 (High) | Wallet 2 (Moderate) | Wallet 3 (Low) |
|--------|----------------|---------------------|----------------|
| ETH Correlation | 95% | 83% | 67% |
| Max Sector Concentration | 68% | 25.1% | 20.3% |
| Compounding Risk | Yes (3.2x) | No (1.1x) | No (0.85x) |
| ... | ... | ... | ... |

### 5. Judge Experience Notes

Highlights what judges should verify when comparing their ASI:One results to these samples.

### 6. Portfolio Holdings Reference

Complete token-by-token breakdown for verification:

| Token | Amount | Value | % of Portfolio | Sector |
|-------|--------|-------|----------------|--------|
| UNI | 5000 | $32,100 | 23.7% | DeFi Governance |
| ... | ... | ... | ... | ... |

---

## How to Use These Samples

**Step 1: Test Guardian via ASI:One**

Follow `DEMO.md` instructions to test each demo wallet:
- Wallet 1: `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58` (High Risk)
- Wallet 2: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0` (Moderate Risk)
- Wallet 3: `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8` (Well-Diversified)

**Step 2: Compare Results**

For each wallet, compare your ASI:One response against the corresponding sample file:

| Your ASI:One Response | Sample Response File |
|----------------------|---------------------|
| Wallet 1 analysis | `wallet-1-high-risk-transparency.md` |
| Wallet 2 analysis | `wallet-2-moderate-risk.md` |
| Wallet 3 analysis | `wallet-3-diversified.md` |

**Step 3: Verify Key Metrics**

Use the "Validation Checklist" in each sample response to confirm:
- [ ] Correlation percentage matches (±3% acceptable variance)
- [ ] Sector concentration matches (±5% acceptable variance)
- [ ] Risk level classification matches (Critical/Moderate/Low)
- [ ] Compounding risk detection matches (Yes/No)
- [ ] Three distinct sections visible (CorrelationAgent, SectorAgent, Guardian)
- [ ] Agent addresses shown
- [ ] Processing times shown
- [ ] Total analysis time ~3-6 seconds

**Step 4: Assess Multi-Agent Architecture**

Verify Guardian demonstrates true multi-agent collaboration:
- ✅ Three separate agent addresses visible
- ✅ Each agent provides independent analysis (not duplicated)
- ✅ Guardian synthesis references both agents by name
- ✅ Compounding risk detected only when BOTH high correlation AND high sector concentration present

### For Developers

**Reference Implementation:**

These sample responses show the expected output format for:
- Message formatting (emoji headers, section separators)
- Narrative tone (technical but accessible)
- Recommendation structure (prioritized with rationale and expected impact)
- Historical context integration (crash scenarios from MeTTa)
- Agent transparency (addresses, timing, attribution)

**Testing Validation:**

Use these samples as golden outputs for integration tests:

```python
def test_wallet_1_high_risk_analysis():
    """Verify Guardian correctly identifies compounding risk for Wallet 1"""
    response = guardian.analyze_wallet("0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58")

    # Verify correlation
    assert response.correlation_percentage > 90.0  # High correlation

    # Verify sector concentration
    assert response.max_sector_concentration > 60.0  # High concentration

    # Verify compounding risk detected
    assert response.compounding_risk_detected is True
    assert response.risk_level == "Critical"

    # Verify risk multiplier
    assert response.risk_multiplier > 2.0  # Leverage effect
```

---

## Response Variations

### Expected Variations

Some response elements may vary between test runs:

**Acceptable Variations:**
- **Processing times:** ±500ms variance (network latency, load)
- **Correlation percentages:** ±2-3% (price data timing)
- **Sector concentration percentages:** ±3-5% (price fluctuations)
- **Total analysis time:** ±1 second (platform load)

**Consistent Elements:**
- **Risk level classification:** Should always match (Critical/Moderate/Low)
- **Compounding risk detection:** Should always match (Yes/No)
- **Number of sections:** Always 3 (CorrelationAgent, SectorAgent, Guardian)
- **Agent addresses:** Same agents should respond
- **Recommendation count:** 2-3 recommendations

---

## Timestamp Information

All sample responses include analysis timestamps in ISO 8601 format:

```markdown
**Analysis Timestamp:** 2025-10-23T22:00:00Z
```

**Purpose:**
- Proves responses are from actual agent runs (not manually fabricated examples)
- Enables judges to verify agent versions used
- Documents when sample responses were generated

**Note:** Your ASI:One test results will have different timestamps (current time). This is expected and normal.

---

## Agent Version Information

All sample responses document agent versions:

```markdown
**Agent Versions:**
- Guardian: v1.0.0
- CorrelationAgent: v1.0.0
- SectorAgent: v1.0.0
```

**Purpose:**
- Enables reproducibility (same agent versions should produce same results)
- Documents which agent implementation generated responses
- Useful for post-hackathon debugging if discrepancies found

**Note:** Judges can verify agent versions by querying agents on Agentverse using addresses from responses.

---

## Cross-References

**Related Documentation:**
- `README.md` (root) - Project overview with demo wallet descriptions
- `docs/DEMO.md` - Step-by-step testing instructions for judges
- `docs/ARCHITECTURE.md` - Technical architecture explaining multi-agent design
- `data/DEMO_WALLETS.md` - Complete demo wallet specifications

**Testing Flow:**
1. Read `README.md` for project overview and demo wallet addresses
2. Follow `DEMO.md` for step-by-step ASI:One testing
3. Compare ASI:One results to `docs/sample-responses/wallet-X-*.md`
4. Reference `ARCHITECTURE.md` for technical deep-dive

---
