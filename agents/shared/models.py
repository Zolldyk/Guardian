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
