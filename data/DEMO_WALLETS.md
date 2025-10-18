# Demo Wallet Documentation

This document describes the three demo portfolios used for testing Guardian's risk analysis capabilities. Each wallet represents a different risk profile commonly seen among DeFi investors.

## Overview

Guardian uses these pre-configured demo wallets to demonstrate its correlation and sector concentration analysis capabilities. Each wallet has been carefully designed to represent realistic DeFi investment patterns with varying risk levels.

## Demo Wallet Profiles

### Wallet 1: High Risk DeFi Whale
**Address:** `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58`
**Total Value:** $135,198.00
**Risk Profile:** High Risk
**Holdings:** 9 tokens

#### Composition
- **UNI (23.7%):** $32,100 - Governance token
- **COMP (17.6%):** $23,760 - Governance token
- **AAVE (17.4%):** $23,575 - Lending/Governance token
- **MKR (14.0%):** $18,966 - Governance token
- **OP (10.3%):** $13,940 - Layer-2 token
- **MATIC (6.9%):** $9,360 - Layer-2 token
- **SNX (5.1%):** $6,880 - DeFi protocol
- **CRV (3.4%):** $4,560 - DEX token
- **BAL (1.5%):** $2,057 - DEX token

#### Risk Characteristics
- **Expected ETH Correlation:** >90% - Almost all tokens are ETH-based DeFi protocols
- **Sector Concentration:** >65% in governance tokens (UNI, COMP, AAVE, MKR combined = 72.8%)
- **Compounding Risk:** Heavy governance sector concentration + high ETH correlation creates compounding downside risk
- **Pattern:** Typical DeFi whale who accumulated during 2020-2021 DeFi summer and hasn't diversified

#### Expected Guardian Analysis
- **Correlation Warning:** High correlation to ETH detected
- **Sector Warning:** Critical concentration in governance tokens
- **Recommendation:** Diversify into stablecoins, non-ETH Layer-1s (SOL, AVAX), or BTC to reduce correlation
- **Historical Context:** Would have suffered significant losses during May 2022 Terra/Luna crash and November 2022 FTX collapse

---

### Wallet 2: Moderate Risk Balanced Portfolio
**Address:** `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`
**Total Value:** $89,855.00
**Risk Profile:** Moderate Risk
**Holdings:** 10 tokens

#### Composition
- **ETH (25.1%):** $22,525 - Core Layer-1 asset
- **LINK (12.7%):** $11,400 - Oracle infrastructure
- **UNI (10.7%):** $9,630 - DEX/Governance
- **AAVE (10.5%):** $9,430 - Lending protocol
- **ARB (10.0%):** $9,000 - Layer-2 token
- **DAI (8.9%):** $8,000 - Stablecoin
- **OP (7.3%):** $6,560 - Layer-2 token
- **USDC (7.2%):** $6,500 - Stablecoin
- **SUSHI (4.0%):** $3,570 - DEX token
- **GRT (3.6%):** $3,240 - Infrastructure

#### Risk Characteristics
- **Expected ETH Correlation:** 80-85% - Mix of ETH-based assets with some diversification via stablecoins
- **Sector Concentration:** 40-50% - No single sector dominates; split between DeFi governance (20%), Layer-2 (17%), stablecoins (16%), infrastructure (16%)
- **Moderate Risk:** Balanced approach with some downside protection from stablecoins
- **Pattern:** Experienced DeFi investor who understands risk management basics but remains heavily exposed to ETH ecosystem

#### Expected Guardian Analysis
- **Correlation Notice:** Moderate correlation to ETH detected
- **Sector Notice:** Reasonable diversification across sectors
- **Recommendation:** Consider adding non-ETH Layer-1s or BTC to further reduce correlation; increase stablecoin allocation during high volatility periods
- **Historical Context:** Stablecoin holdings would have provided cushion during 2022 bear market

---

### Wallet 3: Well-Diversified Conservative
**Address:** `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8`
**Total Value:** $149,490.50
**Risk Profile:** Low Risk (Well-Diversified)
**Holdings:** 12 tokens

#### Composition
- **BTC (20.3%):** $30,375 - Uncorrelated to ETH Layer-1
- **SOL (17.2%):** $25,650 - Non-ETH Layer-1
- **AVAX (11.4%):** $17,040 - Non-ETH Layer-1
- **ETH (10.6%):** $15,900 - Core ETH exposure
- **USDC (10.0%):** $15,000 - Stablecoin
- **DAI (8.0%):** $12,000 - Stablecoin
- **LINK (5.7%):** $8,550 - Infrastructure
- **ATOM (4.1%):** $6,120 - Non-ETH Layer-1
- **DOT (3.5%):** $5,220 - Non-ETH Layer-1
- **UNI (3.4%):** $5,136 - DeFi governance
- **AAVE (2.8%):** $4,243.50 - Lending protocol
- **LDO (2.8%):** $4,256 - Yield protocol

#### Risk Characteristics
- **Expected ETH Correlation:** <70% - Significant allocation to BTC, SOL, AVAX, and other non-ETH chains
- **Sector Diversification:** No single sector >30%; spread across Layer-1s (62.9%), stablecoins (18%), infrastructure (5.7%), DeFi (9.1%)
- **Low Risk:** Conservative portfolio with multiple uncorrelated assets and stable value stores
- **Pattern:** Sophisticated investor prioritizing capital preservation while maintaining crypto exposure

#### Expected Guardian Analysis
- **Correlation Pass:** Healthy diversification detected
- **Sector Pass:** Excellent sector balance with no concentration risk
- **Recommendation:** Portfolio structure is sound; maintain rebalancing discipline during market movements
- **Historical Context:** Would have significantly outperformed ETH-only portfolios during 2022 bear market due to BTC and stablecoin allocations

---

## Selection Rationale

### Why These Portfolios?

1. **Wallet 1 (High Risk)** demonstrates Guardian's ability to identify compounding risks (correlation + sector concentration)
2. **Wallet 2 (Moderate Risk)** shows mid-range risk profiles that benefit from optimization suggestions
3. **Wallet 3 (Diversified)** validates that Guardian correctly identifies well-structured portfolios

### Real vs. Synthetic Addresses

All addresses are **properly formatted Ethereum addresses** (42 characters, 0x prefix, hexadecimal). While these are valid addresses, the token holdings are synthetic and designed for demonstration purposes. The addresses can be verified on Etherscan as valid format.

### Token Selection

Tokens were chosen based on:
- **Liquidity:** Top DeFi tokens with reliable historical price data
- **Sector Representation:** Governance, DEX, Layer-2, lending, infrastructure, stablecoins
- **Correlation Profiles:** Mix of ETH-correlated and uncorrelated assets (BTC, SOL)
- **Realistic Allocations:** Proportions match common DeFi investor patterns

## Verification Instructions

### Validate Address Format
```bash
# All addresses should be 42 characters (0x + 40 hex digits)
grep "wallet_address" data/demo-wallets.json
```

### Load and Validate Portfolios
```python
from agents.shared.portfolio_utils import list_demo_wallets, load_demo_wallet

# List all demo wallets
addresses = list_demo_wallets()
print(f"Found {len(addresses)} demo wallets")

# Load and validate each wallet
for addr in addresses:
    portfolio = load_demo_wallet(addr)
    print(f"{portfolio.wallet_address}: {len(portfolio.tokens)} tokens, ${portfolio.total_value_usd:,.2f}")
```

### Expected Analysis Outcomes

| Wallet | ETH Correlation | Sector Concentration | Guardian Alert Level |
|--------|----------------|---------------------|---------------------|
| Wallet 1 (High Risk) | >90% | >65% (Governance) | 🔴 High Risk |
| Wallet 2 (Moderate) | 80-85% | 40-50% (Mixed) | 🟡 Moderate Risk |
| Wallet 3 (Diversified) | <70% | <30% (All sectors) | 🟢 Low Risk |

## Usage in Development

These demo wallets are used in:
- **Story 1.2:** Portfolio data structure validation (this story)
- **Story 1.3-1.4:** Correlation analysis testing
- **Story 1.5-1.6:** Sector concentration testing
- **Story 2.4-2.5:** Full Guardian orchestrator integration tests
- **Story 3.3:** Demo response generation for hackathon judges

## Data Source

- **Portfolio Data:** `data/demo-wallets.json`
- **Historical Prices:** `data/historical_prices/{TOKEN}.csv`
- **Validation:** All portfolios validated using `agents/shared/models.py` Pydantic schemas

---

**Last Updated:** 2025-10-18
**Story:** 1.2 - Portfolio Data Structure and Demo Wallet Configuration
**Author:** James (Dev Agent)
