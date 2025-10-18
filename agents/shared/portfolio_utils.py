"""
Portfolio parsing and loading utilities.

This module provides functions for parsing portfolio JSON data, loading demo wallets,
and validating portfolio structures. All portfolio data is validated using Pydantic models.
"""

import json
import logging
from pathlib import Path
from typing import Dict

from pydantic import ValidationError

from agents.shared.models import Portfolio

logger = logging.getLogger(__name__)

# Path to demo wallets JSON file
DEMO_WALLETS_PATH = Path(__file__).parent.parent.parent / "data" / "demo-wallets.json"


class InvalidPortfolioError(Exception):
    """Raised when portfolio data fails validation."""

    pass


def parse_portfolio(json_data: Dict) -> Portfolio:
    """
    Parse portfolio JSON data into a Portfolio model.

    This function validates the JSON structure and converts it to a Portfolio
    Pydantic model, ensuring all fields meet validation requirements.

    Args:
        json_data: Dictionary containing portfolio data with keys:
                  - wallet_address: Ethereum address (0x...)
                  - tokens: List of token holdings
                  - total_value_usd: Total portfolio value
                  - analysis_timestamp (optional): Timestamp of analysis

    Returns:
        Portfolio: Validated Portfolio object

    Raises:
        InvalidPortfolioError: If validation fails (invalid address, negative values, etc.)

    Example:
        >>> data = {
        ...     "wallet_address": "0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58",
        ...     "tokens": [
        ...         {"symbol": "UNI", "amount": 1250.0, "price_usd": 6.42, "value_usd": 8025.0}
        ...     ],
        ...     "total_value_usd": 8025.0
        ... }
        >>> portfolio = parse_portfolio(data)
        >>> print(portfolio.wallet_address)
        0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58
    """
    try:
        portfolio = Portfolio(**json_data)
        logger.info(
            f"Loaded portfolio {portfolio.wallet_address} with {len(portfolio.tokens)} holdings"
        )
        return portfolio
    except ValidationError as e:
        error_msg = f"Portfolio validation failed: {str(e)}"
        logger.error(error_msg)
        raise InvalidPortfolioError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error parsing portfolio: {str(e)}"
        logger.error(error_msg)
        raise InvalidPortfolioError(error_msg) from e


def load_demo_wallet(wallet_address: str) -> Portfolio:
    """
    Load a demo wallet from the demo-wallets.json file.

    This function reads the demo wallets configuration file and returns
    the portfolio matching the specified wallet address.

    Args:
        wallet_address: Ethereum wallet address to load

    Returns:
        Portfolio: Validated Portfolio object for the demo wallet

    Raises:
        InvalidPortfolioError: If wallet not found or validation fails
        FileNotFoundError: If demo-wallets.json file doesn't exist

    Example:
        >>> portfolio = load_demo_wallet("0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58")
        >>> print(f"Loaded wallet with {len(portfolio.tokens)} tokens")
    """
    try:
        if not DEMO_WALLETS_PATH.exists():
            error_msg = f"Demo wallets file not found: {DEMO_WALLETS_PATH}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        with open(DEMO_WALLETS_PATH, "r") as f:
            demo_data = json.load(f)

        # Find wallet by address
        wallet_data = None
        for wallet in demo_data.get("wallets", []):
            if wallet.get("wallet_address") == wallet_address:
                wallet_data = wallet
                break

        if wallet_data is None:
            error_msg = f"Wallet {wallet_address} not found in demo wallets"
            logger.error(error_msg)
            raise InvalidPortfolioError(error_msg)

        # Parse and return portfolio
        return parse_portfolio(wallet_data)

    except FileNotFoundError:
        raise
    except InvalidPortfolioError:
        raise
    except Exception as e:
        error_msg = f"Failed to load demo wallet {wallet_address}: {str(e)}"
        logger.error(error_msg)
        raise InvalidPortfolioError(error_msg) from e


def list_demo_wallets() -> list[str]:
    """
    List all available demo wallet addresses.

    Returns:
        List of wallet addresses available in demo-wallets.json

    Raises:
        FileNotFoundError: If demo-wallets.json file doesn't exist

    Example:
        >>> addresses = list_demo_wallets()
        >>> print(f"Found {len(addresses)} demo wallets")
    """
    try:
        if not DEMO_WALLETS_PATH.exists():
            error_msg = f"Demo wallets file not found: {DEMO_WALLETS_PATH}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        with open(DEMO_WALLETS_PATH, "r") as f:
            demo_data = json.load(f)

        addresses = [
            wallet.get("wallet_address")
            for wallet in demo_data.get("wallets", [])
            if wallet.get("wallet_address")
        ]

        logger.info(f"Found {len(addresses)} demo wallets")
        return addresses

    except Exception as e:
        error_msg = f"Failed to list demo wallets: {str(e)}"
        logger.error(error_msg)
        raise InvalidPortfolioError(error_msg) from e
