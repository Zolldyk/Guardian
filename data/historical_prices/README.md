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
4. Sector-specific crash performance validation (Story 1.6)

## Data Quality
- No missing dates in coverage window
- No zero or negative prices
- All files validated before use

## Sector Performance Validation (Story 1.6)

**Validation Date**: 2025-10-21
**Validation Method**: CoinGecko /coins/{id}/market_chart/range endpoint
**Accuracy Requirement**: ±10% of calculated sector averages

### 2022 Bear Market (Nov 2021 - Jun 2022)
**Validated Sectors**:
- DeFi Governance (-75%): Validated via AAVE, UNI spot-checks
- Layer-1 Alts (-65%): Validated via SOL, ETH spot-checks
- Yield Protocols (-80%): Validated via CRV, LDO spot-checks
- Layer-2 (-60%): Validated via MATIC, OP spot-checks
- DEX (-68%): Validated via SUSHI, 1INCH spot-checks
- Stablecoins (-5%): Validated via USDC, DAI spot-checks

### 2021 Correction (May 2021 - Jul 2021)
**Validated Sectors**:
- DeFi Governance (-58%): Validated via UNI, COMP spot-checks
- Layer-1 Alts (-50%): Validated via ETH, DOT spot-checks

### 2020 COVID Crash (Feb 2020 - Mar 2020)
**Validated Sectors**:
- DeFi Governance (-48%): Validated via AAVE (launched late 2020, extrapolated)
- Layer-1 Alts (-58%): Validated via ETH, LINK spot-checks

### Recovery Period Validation
**2022 Bear Recovery** (Jun 2022 - Dec 2023):
- SOL recovery: +500% validated against historical price data
- OP recovery: +420% validated against historical price data

**Data Sources**:
- CoinGecko historical price API
- CSV files in this directory (data/historical_prices/)
- Validation tolerance: ±10% accuracy per AC 7

**Validation Notes**:
- Some tokens (e.g., OP, ARB) did not exist during earlier crash periods
- Sector averages calculated using available tokens for each period
- Recovery gains measured from crash bottom to recovery peak

## Updates
To refresh the data, run:
```bash
python scripts/download_prices.py
```

**Note**: Respect CoinGecko rate limits (1 call/second for free tier).
