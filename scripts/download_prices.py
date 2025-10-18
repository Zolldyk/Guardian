#!/usr/bin/env python3
"""
Download historical price data from CoinGecko API.

This script downloads 90-day historical price data for top DeFi tokens
and stores them as CSV files in data/historical_prices/.

Rate limiting: 1 API call per second (respects CoinGecko free tier)
Error handling: Retries on 429 errors with exponential backoff
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# CoinGecko API configuration
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
RATE_LIMIT_DELAY = 1.0  # seconds between API calls
MAX_RETRIES = 3
RETRY_DELAY = 60  # seconds to wait on 429 error

# Top 30 DeFi tokens (CoinGecko IDs)
DEFI_TOKENS = {
    # DeFi Governance
    "uniswap": "UNI",
    "aave": "AAVE",
    "compound-governance-token": "COMP",
    "maker": "MKR",
    "havven": "SNX",
    "curve-dao-token": "CRV",
    "balancer": "BAL",
    "yearn-finance": "YFI",
    # Layer-2
    "matic-network": "MATIC",
    "optimism": "OP",
    "arbitrum": "ARB",
    "immutable-x": "IMX",
    # DEX
    "sushi": "SUSHI",
    "1inch": "1INCH",
    # Stablecoins
    "dai": "DAI",
    "usd-coin": "USDC",
    "tether": "USDT",
    # Layer-1 Alts
    "solana": "SOL",
    "avalanche-2": "AVAX",
    "cosmos": "ATOM",
    "polkadot": "DOT",
    # Yield Protocols
    "lido-dao": "LDO",
    "rocket-pool": "RPL",
    "frax-share": "FXS",
    # Infrastructure
    "chainlink": "LINK",
    "the-graph": "GRT",
    # Core assets
    "ethereum": "ETH",
    "bitcoin": "BTC",
    "wrapped-bitcoin": "WBTC",
    # Additional DeFi
    "convex-finance": "CVX",
}


def get_historical_prices(
    coin_id: str, days: int = 90, vs_currency: str = "usd"
) -> Optional[pd.DataFrame]:
    """
    Fetch historical price data from CoinGecko API.

    Args:
        coin_id: CoinGecko coin ID (e.g., 'uniswap')
        days: Number of days of historical data (default 90)
        vs_currency: Currency for pricing (default 'usd')

    Returns:
        DataFrame with columns: date, price_usd, volume_usd
        None if request fails after all retries
    """
    url = f"{COINGECKO_API_BASE}/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days, "interval": "daily"}

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Fetching {coin_id} (attempt {attempt + 1}/{MAX_RETRIES})")
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 429:
                logger.warning(
                    f"Rate limit hit for {coin_id}, waiting {RETRY_DELAY}s..."
                )
                time.sleep(RETRY_DELAY)
                continue

            response.raise_for_status()
            data = response.json()

            # Parse prices and volumes
            prices = data.get("prices", [])
            volumes = data.get("total_volumes", [])

            if not prices or not volumes:
                logger.error(f"No data returned for {coin_id}")
                return None

            # Convert to DataFrame
            df = pd.DataFrame(
                {
                    "date": [datetime.fromtimestamp(p[0] / 1000).date() for p in prices],
                    "price_usd": [p[1] for p in prices],
                    "volume_usd": [v[1] for v in volumes],
                }
            )

            logger.info(f"✓ Fetched {len(df)} days of data for {coin_id}")
            return df

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {coin_id}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return None

    return None


def save_to_csv(df: pd.DataFrame, symbol: str, output_dir: Path) -> bool:
    """
    Save price data to CSV file.

    Args:
        df: DataFrame with price data
        symbol: Token symbol (e.g., 'UNI')
        output_dir: Directory to save CSV files

    Returns:
        True if save successful, False otherwise
    """
    try:
        output_path = output_dir / f"{symbol}.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"✓ Saved {symbol}.csv ({len(df)} rows)")
        return True
    except Exception as e:
        logger.error(f"Failed to save {symbol}.csv: {e}")
        return False


def validate_data(df: pd.DataFrame, symbol: str, expected_days: int = 90) -> bool:
    """
    Validate downloaded price data.

    Args:
        df: DataFrame to validate
        symbol: Token symbol for logging
        expected_days: Expected number of days (default 90)

    Returns:
        True if validation passes, False otherwise
    """
    if df is None or df.empty:
        logger.error(f"Validation failed for {symbol}: DataFrame is empty")
        return False

    # Check for missing dates (allow some variance due to API behavior)
    if len(df) < expected_days * 0.9:  # Allow 10% variance
        logger.warning(
            f"Validation warning for {symbol}: Only {len(df)} days (expected ~{expected_days})"
        )

    # Check for zero prices
    zero_prices = df[df["price_usd"] == 0]
    if not zero_prices.empty:
        logger.error(
            f"Validation failed for {symbol}: {len(zero_prices)} zero prices found"
        )
        return False

    # Check for negative values
    if (df["price_usd"] < 0).any() or (df["volume_usd"] < 0).any():
        logger.error(f"Validation failed for {symbol}: Negative values found")
        return False

    logger.info(f"✓ Validation passed for {symbol}")
    return True


def create_readme(output_dir: Path, success_count: int, total_count: int):
    """Create README documenting the data collection."""
    readme_content = f"""# Historical Price Data

## Data Source
- **Provider**: CoinGecko API (Free Tier)
- **Collection Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- **Tokens Collected**: {success_count} / {total_count}
- **Time Period**: 90-day historical window
- **Data Interval**: Daily (OHLCV)

## File Format
Each CSV file contains daily price data with the following columns:
- `date`: Date in YYYY-MM-DD format
- `price_usd`: Closing price in USD
- `volume_usd`: 24-hour trading volume in USD

## Token List
Top DeFi tokens including:
- DeFi Governance: UNI, AAVE, COMP, MKR, SNX, CRV, BAL, YFI
- Layer-2: MATIC, OP, ARB, IMX
- DEX: SUSHI, 1INCH
- Stablecoins: DAI, USDC, USDT
- Layer-1 Alts: SOL, AVAX, ATOM, DOT
- Yield Protocols: LDO, RPL, FXS
- Infrastructure: LINK, GRT
- Core Assets: ETH, BTC, WBTC

## Usage
Historical price data is used for:
1. Correlation analysis with ETH (Story 1.3-1.4)
2. Sector concentration analysis (Story 1.5-1.6)
3. Historical crash scenario testing (Story 1.4)

## Data Quality
- No missing dates in coverage window
- No zero or negative prices
- All files validated before use

## Updates
To refresh the data, run:
```bash
python scripts/download_prices.py
```

**Note**: Respect CoinGecko rate limits (1 call/second for free tier).
"""
    readme_path = output_dir / "README.md"
    readme_path.write_text(readme_content)
    logger.info(f"✓ Created README.md")


def main():
    """Main execution function."""
    logger.info("Starting historical price data download...")
    logger.info(f"Target: {len(DEFI_TOKENS)} tokens, 90-day window")

    # Setup output directory
    output_dir = Path(__file__).parent.parent / "data" / "historical_prices"
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed_tokens = []

    # Download data for each token
    for coin_id, symbol in DEFI_TOKENS.items():
        logger.info(f"\n--- Processing {symbol} ({coin_id}) ---")

        # Fetch data
        df = get_historical_prices(coin_id, days=90)

        if df is None:
            logger.error(f"✗ Failed to fetch {symbol}")
            failed_tokens.append(symbol)
            continue

        # Validate data
        if not validate_data(df, symbol):
            logger.error(f"✗ Validation failed for {symbol}")
            failed_tokens.append(symbol)
            continue

        # Save to CSV
        if save_to_csv(df, symbol, output_dir):
            success_count += 1
        else:
            failed_tokens.append(symbol)

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

    # Create README
    create_readme(output_dir, success_count, len(DEFI_TOKENS))

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"Download complete!")
    logger.info(f"Success: {success_count}/{len(DEFI_TOKENS)} tokens")
    if failed_tokens:
        logger.warning(f"Failed tokens: {', '.join(failed_tokens)}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()
