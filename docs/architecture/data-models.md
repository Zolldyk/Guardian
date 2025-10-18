# Data Models

This section defines the core data models and entities used throughout Guardian's multi-agent system. These models serve as **contracts** between agents and data sources, ensuring consistent data structures across the entire system.

**Design Philosophy:** Since Guardian uses Python (not TypeScript), we use **Pydantic models** for data validation and serialization. Pydantic integrates natively with uAgents for message-passing and provides runtime type checking, making it ideal for agent communication contracts.

## Portfolio

**Purpose:** Represents a user's cryptocurrency portfolio containing multiple token holdings with their current values.

**Key Attributes:**
- `wallet_address`: str - Ethereum wallet address (0x format, used as unique identifier)
- `tokens`: List[TokenHolding] - List of token holdings in the portfolio
- `total_value_usd`: float - Total portfolio value in USD (sum of all token values)
- `analysis_timestamp`: datetime - When this portfolio snapshot was created

**Relationships:**
- Has many `TokenHolding` records (composition)
- Referenced by `AnalysisRequest` messages sent to agents

### Python Data Model (Pydantic)

```python
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TokenHolding(BaseModel):
    """Represents a single token holding within a portfolio."""
    symbol: str = Field(..., description="Token symbol (e.g., 'ETH', 'UNI', 'AAVE')")
    amount: float = Field(..., gt=0, description="Amount of tokens held")
    price_usd: float = Field(..., gt=0, description="Current price per token in USD")
    value_usd: float = Field(..., gt=0, description="Total value (amount * price_usd)")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "UNI",
                "amount": 1250.0,
                "price_usd": 6.42,
                "value_usd": 8025.0
            }
        }

class Portfolio(BaseModel):
    """Complete portfolio data structure passed between agents."""
    wallet_address: str = Field(..., regex=r'^0x[a-fA-F0-9]{40}$', description="Ethereum wallet address")
    tokens: List[TokenHolding] = Field(..., min_items=1, description="List of token holdings")
    total_value_usd: float = Field(..., gt=0, description="Total portfolio value in USD")
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Snapshot timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
                "tokens": [
                    {"symbol": "UNI", "amount": 1250.0, "price_usd": 6.42, "value_usd": 8025.0},
                    {"symbol": "AAVE", "amount": 85.0, "price_usd": 94.30, "value_usd": 8015.5}
                ],
                "total_value_usd": 16040.5,
                "analysis_timestamp": "2025-10-18T14:32:00Z"
            }
        }
```

---

## CorrelationAnalysis

**Purpose:** Results from CorrelationAgent analyzing portfolio's correlation to ETH, including historical crash context.

**Key Attributes:**
- `correlation_coefficient`: float - Pearson correlation coefficient (0.0 to 1.0)
- `correlation_percentage`: int - Correlation as percentage (0-100) for user-facing display
- `interpretation`: str - Human-readable interpretation ("High", "Moderate", "Low")
- `historical_context`: List[CrashPerformance] - Performance in historical crashes
- `calculation_period_days`: int - Historical window used for calculation (typically 90)

**Relationships:**
- Contains multiple `CrashPerformance` records
- Produced by CorrelationAgent, consumed by Guardian for synthesis

### Python Data Model (Pydantic)

```python
class CrashPerformance(BaseModel):
    """Historical crash performance for a given correlation bracket."""
    crash_name: str = Field(..., description="Crash scenario name (e.g., '2022 Bear Market')")
    crash_period: str = Field(..., description="Date range of crash (e.g., 'Nov 2021 - Jun 2022')")
    eth_drawdown_pct: float = Field(..., description="ETH drawdown percentage during crash")
    portfolio_loss_pct: float = Field(..., description="Avg portfolio loss for this correlation bracket")
    market_avg_loss_pct: float = Field(..., description="Market average loss for comparison")

class CorrelationAnalysis(BaseModel):
    """Correlation analysis results from CorrelationAgent."""
    correlation_coefficient: float = Field(..., ge=0.0, le=1.0, description="Pearson correlation (0-1)")
    correlation_percentage: int = Field(..., ge=0, le=100, description="Correlation as percentage")
    interpretation: str = Field(..., description="High (>85%), Moderate (70-85%), Low (<70%)")
    historical_context: List[CrashPerformance] = Field(default_factory=list, description="Historical crash data")
    calculation_period_days: int = Field(default=90, description="Historical window in days")
    narrative: str = Field(..., description="Plain English explanation of correlation risk")

    class Config:
        json_schema_extra = {
            "example": {
                "correlation_coefficient": 0.95,
                "correlation_percentage": 95,
                "interpretation": "High",
                "historical_context": [
                    {
                        "crash_name": "2022 Bear Market",
                        "crash_period": "Nov 2021 - Jun 2022",
                        "eth_drawdown_pct": -75.0,
                        "portfolio_loss_pct": -73.0,
                        "market_avg_loss_pct": -55.0
                    }
                ],
                "calculation_period_days": 90,
                "narrative": "Your portfolio is 95% correlated to ETH. Portfolios with >90% correlation lost an average of 73% in the 2022 crash versus 55% market average."
            }
        }
```

---

## SectorAnalysis

**Purpose:** Results from SectorAgent analyzing portfolio sector concentration and historical sector performance.

**Key Attributes:**
- `sector_breakdown`: Dict[str, SectorHolding] - Portfolio value percentage by sector
- `concentrated_sectors`: List[str] - Sectors exceeding 60% concentration threshold
- `diversification_score`: str - Overall diversification quality ("Well-Diversified", "Moderate Concentration", "High Concentration")
- `sector_risks`: List[SectorRisk] - Sector-specific historical performance and opportunity cost

**Relationships:**
- Contains multiple `SectorHolding` and `SectorRisk` records
- Produced by SectorAgent, consumed by Guardian for synthesis

### Python Data Model (Pydantic)

```python
class SectorHolding(BaseModel):
    """Portfolio allocation to a specific sector."""
    sector_name: str = Field(..., description="Sector name (e.g., 'DeFi Governance', 'Layer-2')")
    value_usd: float = Field(..., ge=0, description="Total USD value in this sector")
    percentage: float = Field(..., ge=0, le=100, description="Percentage of portfolio in this sector")
    token_symbols: List[str] = Field(default_factory=list, description="Tokens in this sector")

class SectorRisk(BaseModel):
    """Historical risk and opportunity cost for a sector."""
    sector_name: str
    crash_performance: CrashPerformance  # Reuse CrashPerformance model
    opportunity_cost: str = Field(..., description="What was missed by over-concentrating")

class SectorAnalysis(BaseModel):
    """Sector concentration analysis results from SectorAgent."""
    sector_breakdown: dict[str, SectorHolding] = Field(..., description="Portfolio by sector")
    concentrated_sectors: List[str] = Field(default_factory=list, description="Sectors >60% of portfolio")
    diversification_score: str = Field(..., description="Well-Diversified | Moderate | High Concentration")
    sector_risks: List[SectorRisk] = Field(default_factory=list, description="Sector-specific risks")
    narrative: str = Field(..., description="Plain English explanation of sector concentration")

    class Config:
        json_schema_extra = {
            "example": {
                "sector_breakdown": {
                    "DeFi Governance": {
                        "sector_name": "DeFi Governance",
                        "value_usd": 10912.0,
                        "percentage": 68.0,
                        "token_symbols": ["UNI", "AAVE", "COMP"]
                    },
                    "Layer-2": {
                        "sector_name": "Layer-2",
                        "value_usd": 5136.0,
                        "percentage": 32.0,
                        "token_symbols": ["MATIC", "OP"]
                    }
                },
                "concentrated_sectors": ["DeFi Governance"],
                "diversification_score": "High Concentration",
                "narrative": "68% of your portfolio is concentrated in DeFi Governance tokens. This sector lost 75% in the 2022 crash."
            }
        }
```

---

## GuardianSynthesis

**Purpose:** Guardian orchestrator's synthesized analysis combining correlation and sector insights to reveal compounding risks.

**Key Attributes:**
- `correlation_analysis`: CorrelationAnalysis - Results from CorrelationAgent
- `sector_analysis`: SectorAnalysis - Results from SectorAgent
- `compounding_risk_detected`: bool - Whether dual-risk pattern exists
- `risk_multiplier_effect`: str - Explanation of how risks amplify each other
- `recommendations`: List[Recommendation] - Actionable steps to reduce risk
- `overall_risk_level`: str - "Low", "Moderate", "High", "Critical"

**Relationships:**
- Aggregates `CorrelationAnalysis` and `SectorAnalysis`
- Contains multiple `Recommendation` records
- Returned to user via ASI:One Chat Protocol

### Python Data Model (Pydantic)

```python
class Recommendation(BaseModel):
    """Actionable recommendation to improve portfolio structure."""
    priority: int = Field(..., ge=1, le=3, description="Priority order (1 = highest)")
    action: str = Field(..., description="Specific action to take")
    rationale: str = Field(..., description="Why this reduces risk")
    expected_impact: str = Field(..., description="What improvement to expect")

class GuardianSynthesis(BaseModel):
    """Complete synthesized analysis from Guardian orchestrator."""
    correlation_analysis: CorrelationAnalysis
    sector_analysis: SectorAnalysis
    compounding_risk_detected: bool = Field(..., description="True if correlation >85% AND sector concentration >60%")
    risk_multiplier_effect: str = Field(..., description="How correlation + sector risks compound")
    recommendations: List[Recommendation] = Field(..., min_items=1, max_items=3)
    overall_risk_level: str = Field(..., description="Low | Moderate | High | Critical")
    synthesis_narrative: str = Field(..., description="Cohesive explanation of compounding risks")

    class Config:
        json_schema_extra = {
            "example": {
                "compounding_risk_detected": True,
                "risk_multiplier_effect": "Your 95% ETH correlation acts like 3x leverage, and 68% governance concentration means when governance tokens crash (which they did 75% in 2022), your entire portfolio amplifies the loss. Combined structure would have lost 75%, not just 60%.",
                "recommendations": [
                    {
                        "priority": 1,
                        "action": "Reduce DeFi Governance token concentration from 68% to below 40%",
                        "rationale": "Sector concentration is the larger risk multiplier",
                        "expected_impact": "Reduces compounding effect, limits single-sector crash exposure"
                    }
                ],
                "overall_risk_level": "Critical"
            }
        }
```

---

## Historical Crash Scenario (Knowledge Graph Entity)

**Purpose:** Historical market crash data stored in MeTTa knowledge graph, queried by CorrelationAgent and SectorAgent.

**Key Attributes:**
- `scenario_id`: str - Unique identifier (e.g., "crash_2022_bear")
- `name`: str - Human-readable name ("2022 Bear Market")
- `period`: str - Date range ("Nov 2021 - Jun 2022")
- `eth_drawdown_pct`: float - ETH peak-to-trough decline
- `correlation_brackets`: Dict[str, float] - Avg loss by correlation bracket (">90%": -73.0)
- `sector_performance`: Dict[str, float] - Avg loss by sector
- `recovery_winners`: List[str] - Assets that gained during recovery

**Note:** This is a conceptual model representing MeTTa knowledge graph structure. Actual MeTTa queries will return data matching this shape.

### Conceptual Schema (for MeTTa queries)

```python
class HistoricalCrashScenario(BaseModel):
    """Conceptual model for crash scenarios in MeTTa knowledge graph."""
    scenario_id: str = Field(..., description="Unique crash identifier")
    name: str = Field(..., description="Human-readable crash name")
    period: str = Field(..., description="Date range of crash")
    eth_drawdown_pct: float = Field(..., description="ETH decline percentage")
    correlation_brackets: dict[str, float] = Field(..., description="Avg loss by correlation bracket")
    sector_performance: dict[str, float] = Field(..., description="Avg loss by sector")
    recovery_winners: List[str] = Field(default_factory=list, description="Best performers in recovery")
```

---

## Sector Mapping (Static Configuration)

**Purpose:** Maps cryptocurrency tokens to sector classifications. Used by SectorAgent to categorize portfolio holdings.

**Key Attributes:**
- `token_symbol`: str - Token symbol (e.g., "UNI")
- `sector`: str - Sector classification ("DeFi Governance", "Layer-2", etc.)
- `sector_tags`: List[str] - Additional categorization tags

**Storage:** `data/sector_mappings.json` file deployed with agents.

### JSON Structure Example

```json
{
  "UNI": {
    "token_symbol": "UNI",
    "sector": "DeFi Governance",
    "sector_tags": ["DEX", "Governance"]
  },
  "AAVE": {
    "token_symbol": "AAVE",
    "sector": "DeFi Governance",
    "sector_tags": ["Lending", "Governance"]
  },
  "MATIC": {
    "token_symbol": "MATIC",
    "sector": "Layer-2",
    "sector_tags": ["Scaling", "Infrastructure"]
  }
}
```

---
