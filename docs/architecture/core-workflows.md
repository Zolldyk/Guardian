# Core Workflows

## End-to-End Portfolio Analysis Workflow

This sequence diagram shows the complete flow from user query to synthesized analysis:

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant ASI_One as ASI:One
    participant Guardian
    participant CorrAgent as CorrelationAgent
    participant SectorAgent
    participant MeTTa

    User->>ASI_One: "Analyze wallet 0x742d35Cc..."
    ASI_One->>Guardian: ChatMessage

    Note over Guardian: Extract wallet address<br/>Load demo portfolio

    par Parallel Analysis
        Guardian->>CorrAgent: AnalysisRequest
        Guardian->>SectorAgent: AnalysisRequest
    end

    Note over CorrAgent: Calculate 90-day correlation<br/>to ETH using Pandas/NumPy

    CorrAgent->>MeTTa: Query crash performance<br/>for correlation >90%
    MeTTa-->>CorrAgent: Historical data

    Note over CorrAgent: Generate narrative with<br/>historical context

    CorrAgent->>Guardian: CorrelationAnalysisResponse

    Note over SectorAgent: Map tokens to sectors<br/>Calculate concentration %

    SectorAgent->>MeTTa: Query sector performance<br/>for DeFi Governance
    MeTTa-->>SectorAgent: Sector crash data

    Note over SectorAgent: Generate sector narrative<br/>with opportunity cost

    SectorAgent->>Guardian: SectorAnalysisResponse

    Note over Guardian: Detect compounding risk:<br/>95% correlation + 68% sector concentration<br/>Generate risk multiplier explanation<br/>Create 2-3 recommendations

    Guardian->>ASI_One: ChatResponse (narrative)
    ASI_One->>User: Display analysis
```

**Key Decision Points:**
1. **Step 3:** If wallet address not found in demo_wallets.json, return error
2. **Steps 4-5:** Agents called in parallel to minimize latency
3. **Step 9:** If MeTTa unavailable, fall back to historical_crashes.json
4. **Step 15:** If MeTTa unavailable, fall back to JSON sector data
5. **Step 17:** Synthesis detects compounding risk if BOTH correlation >85% AND any sector >60%

---
