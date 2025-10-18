# Historical Price Data

## Data Source
- **Provider**: CoinGecko API (Free Tier)
- **Collection Date**: 2025-10-18 12:45:23 UTC
- **Tokens Collected**: 29 / 30
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
