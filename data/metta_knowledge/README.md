# MeTTa Knowledge Graph Schema

## Overview

This directory contains MeTTa knowledge graph schema files demonstrating SingularityNET's MeTTa semantic knowledge representation for Guardian's historical crash analysis.

**Implementation Note:** Due to Hyperon library compatibility constraints with Python 3.13 and Agentverse deployment requirements, this implementation uses a **JSON representation** of the MeTTa knowledge graph. The `.metta` files serve as schema documentation, while the actual queries use pre-computed results from `data/historical-crashes.json`.

## Schema Design

### Entities

1. **Crash** - Historical market crash event
   - Attributes: scenario_id, name, period
   - Example: `(Crash crash_2022_bear "2022 Bear Market" "Nov 2021 - Jun 2022")`

2. **Sector** - Cryptocurrency sector classification
   - Attributes: sector_name, description
   - Example: `(Sector "DeFi Governance" "Decentralized governance protocols")`

3. **Token** - Individual cryptocurrency token
   - Attributes: token_symbol, sector
   - Example: `(Token "UNI" "DeFi Governance")`

4. **CorrelationBracket** - Portfolio correlation range
   - Attributes: bracket_id, range_description
   - Example: `(CorrelationBracket "high" ">90%")`

### Relationships

1. **EthDrawdown** - ETH decline percentage during crash
   - Syntax: `(EthDrawdown crash_id percentage)`
   - Example: `(EthDrawdown crash_2022_bear -75.0)`

2. **CorrelationBracketLoss** - Average portfolio loss by correlation bracket
   - Syntax: `(CorrelationBracketLoss crash_id bracket percentage)`
   - Example: `(CorrelationBracketLoss crash_2022_bear ">90%" -73.0)`

3. **SectorPerformance** - Sector performance during crash
   - Syntax: `(SectorPerformance crash_id sector percentage)`
   - Example: `(SectorPerformance crash_2022_bear "DeFi Governance" -75.0)`

4. **RecoveryWinner** - Tokens that performed well during recovery
   - Syntax: `(RecoveryWinner crash_id token_symbol)`
   - Example: `(RecoveryWinner crash_2022_bear "SOL")`

5. **RecoveryPeriod** - Recovery timeframe for crash
   - Syntax: `(RecoveryPeriod crash_id period)`
   - Example: `(RecoveryPeriod crash_2022_bear "Jun 2022 - Dec 2023")`

## Entity-Relationship Diagram (ASCII)

```
┌─────────────┐         ┌──────────────────────┐
│   Crash     │◄────────┤  EthDrawdown         │
│             │         │  (percentage)        │
└──────┬──────┘         └──────────────────────┘
       │
       │ 1:N            ┌──────────────────────┐
       ├────────────────┤ CorrelationBracket   │
       │                │ Loss                 │
       │                │ (bracket, %)         │
       │                └──────────────────────┘
       │
       │ 1:N            ┌──────────────────────┐
       ├────────────────┤ SectorPerformance    │
       │                │ (sector, %)          │
       │                └──────────────────────┘
       │
       │ 1:N            ┌──────────────────────┐
       ├────────────────┤ RecoveryWinner       │
       │                │ (token_symbol)       │
       │                └──────────────────────┘
       │
       │ 1:1            ┌──────────────────────┐
       └────────────────┤ RecoveryPeriod       │
                        │ (period)             │
                        └──────────────────────┘

┌─────────────┐         ┌──────────────────────┐
│   Sector    │◄────────┤  Token               │
│             │  belongs│  (sector)            │
└─────────────┘    to   └──────────────────────┘
```

## Sample MeTTa Queries

### Query 1: Find crashes where high correlation (>90%) portfolios lost more than 70%

```metta
;; Query: Crashes with >90% correlation bracket losing >70%
(match (and (Crash ?id ?name ?period)
            (CorrelationBracketLoss ?id ">90%" ?loss)
            (< ?loss -70.0))
  (?id ?name ?loss))

;; Expected Result:
;; (crash_2022_bear "2022 Bear Market" -73.0)
```

### Query 2: Get DeFi Governance sector performance across all crashes

```metta
;; Query: DeFi Governance sector performance
(match (and (Crash ?id ?name ?period)
            (SectorPerformance ?id "DeFi Governance" ?loss))
  (?id ?name ?loss))

;; Expected Results:
;; (crash_2022_bear "2022 Bear Market" -75.0)
;; (crash_2021_correction "2021 Correction" -58.0)
;; (crash_2020_covid "2020 COVID Crash" -48.0)
```

### Query 3: Find recovery winners for 2022 bear market

```metta
;; Query: Recovery winners after 2022 crash
(match (and (Crash crash_2022_bear ?name ?period)
            (RecoveryWinner crash_2022_bear ?token))
  ?token)

;; Expected Results:
;; "SOL"
;; "MATIC"
;; "OP"
```

### Query 4: Complex query - Crashes with high correlation AND severe sector concentration

```metta
;; Query: Crashes where >90% correlation AND DeFi Governance lost >70%
(match (and (Crash ?id ?name ?period)
            (CorrelationBracketLoss ?id ">90%" ?corr_loss)
            (SectorPerformance ?id "DeFi Governance" ?sector_loss)
            (< ?corr_loss -70.0)
            (< ?sector_loss -70.0))
  (?id ?name ?corr_loss ?sector_loss))

;; Expected Result:
;; (crash_2022_bear "2022 Bear Market" -73.0 -75.0)
```

### Query 5: Get all data for specific crash scenario

```metta
;; Query: Complete crash scenario data
(match (and (Crash crash_2020_covid ?name ?period)
            (EthDrawdown crash_2020_covid ?eth_loss))
  (?name ?period ?eth_loss))

;; Expected Result:
;; ("2020 COVID Crash" "Feb 2020 - Mar 2020" -65.0)
```

## Historical Crash Scenarios

The knowledge graph includes 3 historical crash scenarios:

### 1. 2022 Bear Market (crash_2022_bear)
- **Period:** Nov 2021 - Jun 2022
- **ETH Drawdown:** -75.0%
- **Correlation Brackets:**
  - >90%: -73.0%
  - 80-90%: -68.0%
  - 70-80%: -62.0%
  - <70%: -48.0%
- **Sector Performance:**
  - DeFi Governance: -75.0%
  - Layer-2: -60.0%
  - Yield Protocols: -80.0%
  - DEX: -68.0%
  - Stablecoins: -5.0%
  - Layer-1 Alts: -65.0%
- **Recovery Winners:** SOL, MATIC, OP
- **Recovery Period:** Jun 2022 - Dec 2023

### 2. 2021 Correction (crash_2021_correction)
- **Period:** May 2021 - Jul 2021
- **ETH Drawdown:** -55.0%
- **Correlation Brackets:**
  - >90%: -52.0%
  - 80-90%: -48.0%
  - 70-80%: -43.0%
  - <70%: -35.0%
- **Sector Performance:**
  - DeFi Governance: -58.0%
  - Layer-2: -52.0%
  - Yield Protocols: -62.0%
  - DEX: -55.0%
  - Stablecoins: -3.0%
  - Layer-1 Alts: -50.0%
- **Recovery Winners:** BNB, ADA, DOT
- **Recovery Period:** Jul 2021 - Nov 2021

### 3. 2020 COVID Crash (crash_2020_covid)
- **Period:** Feb 2020 - Mar 2020
- **ETH Drawdown:** -65.0%
- **Correlation Brackets:**
  - >90%: -62.0%
  - 80-90%: -58.0%
  - 70-80%: -53.0%
  - <70%: -42.0%
- **Sector Performance:**
  - DeFi Governance: -48.0%
  - Layer-2: -55.0%
  - Yield Protocols: -52.0%
  - DEX: -50.0%
  - Stablecoins: -2.0%
  - Layer-1 Alts: -58.0%
- **Recovery Winners:** LINK, UNI, AAVE
- **Recovery Period:** Mar 2020 - Dec 2020

## Data Consistency

All MeTTa knowledge graph data is synchronized with `data/historical-crashes.json` to ensure consistency across the system. Unit tests validate that MeTTa query results (via JSON representation) match the source data exactly.

## Files

- `crashes.metta` - Crash scenario entities and relationships
- `sectors.metta` - Sector taxonomy and token-to-sector mappings
- `correlations.metta` - Correlation bracket definitions
- `README.md` - This schema documentation

## Implementation Details

**Query Interface:** `agents/shared/metta_interface.py` provides `query_historical_performance()` function that implements the query patterns above using JSON data lookups.

**Fallback Strategy:** Since Hyperon library is not compatible with Python 3.13 or Agentverse, all queries use pre-computed results from `data/historical-crashes.json`. This maintains semantic correctness while ensuring deployment compatibility.

**Logging:** All queries log at INFO level to indicate MeTTa knowledge graph usage (JSON representation).
