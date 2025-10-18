"""
Pydantic data models for portfolio analysis.

This module defines the core data structures used across all agents for portfolio
representation and validation. Always import models from this module to ensure
consistency across the system.
"""

import logging
from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, ConfigDict, Field, model_validator
from uagents import Model

logger = logging.getLogger(__name__)


class TokenHolding(BaseModel):
    """Represents a single token holding within a portfolio."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symbol": "UNI",
                "amount": 1250.0,
                "price_usd": 6.42,
                "value_usd": 8025.0,
            }
        }
    )

    symbol: str = Field(..., description="Token symbol (e.g., 'ETH', 'UNI', 'AAVE')")
    amount: float = Field(..., gt=0, description="Amount of tokens held")
    price_usd: float = Field(..., gt=0, description="Current price per token in USD")
    value_usd: float = Field(..., gt=0, description="Total value (amount * price_usd)")


class Portfolio(BaseModel):
    """Complete portfolio data structure passed between agents."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
                "tokens": [
                    {
                        "symbol": "UNI",
                        "amount": 1250.0,
                        "price_usd": 6.42,
                        "value_usd": 8025.0,
                    },
                    {
                        "symbol": "AAVE",
                        "amount": 85.0,
                        "price_usd": 94.30,
                        "value_usd": 8015.5,
                    },
                ],
                "total_value_usd": 16040.5,
                "analysis_timestamp": "2025-10-18T14:32:00Z",
            }
        }
    )

    wallet_address: str = Field(
        ...,
        pattern=r"^0x[a-fA-F0-9]{40}$",
        description="Ethereum wallet address",
    )
    tokens: List[TokenHolding] = Field(
        ..., min_length=1, description="List of token holdings"
    )
    total_value_usd: float = Field(..., gt=0, description="Total portfolio value in USD")
    analysis_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Snapshot timestamp"
    )

    @model_validator(mode="after")
    def validate_total_value(self) -> "Portfolio":
        """Verify total_value_usd matches sum of token values."""
        calculated_total = sum(token.value_usd for token in self.tokens)
        # Allow small floating point differences (0.01 USD tolerance)
        if abs(self.total_value_usd - calculated_total) > 0.01:
            raise ValueError(
                f"total_value_usd ({self.total_value_usd}) does not match sum of token values ({calculated_total})"
            )
        return self


class CrashPerformance(BaseModel):
    """Historical crash performance for a given correlation bracket."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "crash_name": "2022 Bear Market",
                "crash_period": "Nov 2021 - Jun 2022",
                "eth_drawdown_pct": -75.3,
                "portfolio_loss_pct": -68.2,
                "market_avg_loss_pct": -62.5,
            }
        }
    )

    crash_name: str = Field(..., description="Crash scenario name (e.g., '2022 Bear Market')")
    crash_period: str = Field(..., description="Date range of crash (e.g., 'Nov 2021 - Jun 2022')")
    eth_drawdown_pct: float = Field(..., description="ETH drawdown percentage during crash")
    portfolio_loss_pct: float = Field(..., description="Avg portfolio loss for this correlation bracket")
    market_avg_loss_pct: float = Field(..., description="Market average loss for comparison")


class CorrelationAnalysis(BaseModel):
    """Correlation analysis results from CorrelationAgent."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "correlation_coefficient": 0.95,
                "correlation_percentage": 95,
                "interpretation": "High",
                "historical_context": [],
                "calculation_period_days": 90,
                "narrative": "Your portfolio is 95% correlated to ETH over the past 90 days.",
            }
        }
    )

    correlation_coefficient: float = Field(..., ge=-1.0, le=1.0, description="Pearson correlation (-1 to +1)")
    correlation_percentage: int = Field(..., ge=0, le=100, description="Correlation as percentage (absolute value)")
    interpretation: str = Field(..., description="High (>85%), Moderate (70-85%), Low (<70%)")
    historical_context: List[CrashPerformance] = Field(default_factory=list, description="Historical crash data")
    calculation_period_days: int = Field(default=90, description="Historical window in days")
    narrative: str = Field(..., description="Plain English explanation of correlation risk")


# uAgents Message Models for inter-agent communication
# These models inherit from uagents.Model and define message-passing contracts
# Note: These use dict types for Pydantic v2 models to maintain compatibility with uAgents (Pydantic v1)

class AnalysisRequest(Model):
    """
    Request message sent from Guardian to CorrelationAgent requesting portfolio analysis.
    Portfolio is sent as dict and converted to Portfolio model in handler.
    """
    request_id: str
    wallet_address: str
    portfolio_data: dict  # Portfolio serialized as dict
    requested_by: str


class CorrelationAnalysisResponse(Model):
    """
    Response message from CorrelationAgent containing correlation analysis results.
    Analysis is sent as dict and converted from CorrelationAnalysis model.
    """
    request_id: str
    wallet_address: str
    analysis_data: dict  # CorrelationAnalysis serialized as dict
    agent_address: str
    processing_time_ms: int


class ErrorMessage(Model):
    """
    Universal error message for communicating failures between agents.
    """
    request_id: str
    error_type: str  # "timeout" | "invalid_data" | "insufficient_data" | "agent_unavailable"
    error_message: str
    agent_address: str
    retry_recommended: bool
