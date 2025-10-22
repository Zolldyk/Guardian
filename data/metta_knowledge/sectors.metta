;; MeTTa Knowledge Graph: Sector Taxonomy and Token-to-Sector Mappings
;; Schema documentation in README.md
;;
;; Note: This is a schema representation file demonstrating MeTTa/SingularityNET
;; knowledge graph design. Actual queries use JSON representation due to
;; Hyperon library compatibility constraints.

;; ============================================================================
;; SECTOR DEFINITIONS
;; ============================================================================

(Sector "DeFi Governance" "Decentralized governance protocols with voting mechanisms")
(Sector "Layer-2" "Ethereum scaling solutions and layer-2 protocols")
(Sector "Yield Protocols" "Yield farming and liquid staking protocols")
(Sector "DEX" "Decentralized exchanges and AMM protocols")
(Sector "Stablecoins" "USD-pegged stablecoins for capital preservation")
(Sector "Layer-1 Alts" "Alternative layer-1 blockchains and infrastructure")

;; ============================================================================
;; TOKEN-TO-SECTOR MAPPINGS
;; ============================================================================

;; DeFi Governance tokens
(Token "AAVE" "DeFi Governance")
(TokenTags "AAVE" "Lending" "Governance")

(Token "COMP" "DeFi Governance")
(TokenTags "COMP" "Lending" "Governance")

(Token "MKR" "DeFi Governance")
(TokenTags "MKR" "Lending" "Stablecoin" "Governance")

(Token "SNX" "DeFi Governance")
(TokenTags "SNX" "Derivatives" "Governance")

(Token "UNI" "DeFi Governance")
(TokenTags "UNI" "DEX" "Governance")

(Token "YFI" "DeFi Governance")
(TokenTags "YFI" "Yield" "Aggregator" "Governance")

;; Layer-2 tokens
(Token "ARB" "Layer-2")
(TokenTags "ARB" "Scaling" "Rollup")

(Token "IMX" "Layer-2")
(TokenTags "IMX" "Scaling" "NFT" "Gaming")

(Token "MATIC" "Layer-2")
(TokenTags "MATIC" "Scaling" "Polygon")

(Token "OP" "Layer-2")
(TokenTags "OP" "Scaling" "Rollup")

;; Yield Protocols
(Token "CRV" "Yield Protocols")
(TokenTags "CRV" "DEX" "Stablecoin" "Yield")

(Token "CVX" "Yield Protocols")
(TokenTags "CVX" "Yield" "Curve Booster")

(Token "FXS" "Yield Protocols")
(TokenTags "FXS" "Stablecoin" "Governance" "Yield")

(Token "LDO" "Yield Protocols")
(TokenTags "LDO" "Liquid Staking" "Governance")

(Token "RPL" "Yield Protocols")
(TokenTags "RPL" "Liquid Staking" "Governance")

;; DEX tokens
(Token "1INCH" "DEX")
(TokenTags "1INCH" "DEX" "Aggregator")

(Token "BAL" "DEX")
(TokenTags "BAL" "DEX" "AMM" "Liquidity")

(Token "SUSHI" "DEX")
(TokenTags "SUSHI" "DEX" "AMM")

;; Stablecoins
(Token "DAI" "Stablecoins")
(TokenTags "DAI" "Stablecoin" "Decentralized")

(Token "USDC" "Stablecoins")
(TokenTags "USDC" "Stablecoin" "USD-pegged")

(Token "USDT" "Stablecoins")
(TokenTags "USDT" "Stablecoin" "USD-pegged")

;; Layer-1 Alts
(Token "ATOM" "Layer-1 Alts")
(TokenTags "ATOM" "Blockchain" "Interoperability")

(Token "AVAX" "Layer-1 Alts")
(TokenTags "AVAX" "Blockchain" "Smart Contracts")

(Token "BTC" "Layer-1 Alts")
(TokenTags "BTC" "Bitcoin" "Store of Value")

(Token "DOT" "Layer-1 Alts")
(TokenTags "DOT" "Blockchain" "Interoperability")

(Token "ETH" "Layer-1 Alts")
(TokenTags "ETH" "Ethereum" "Smart Contracts")

(Token "GRT" "Layer-1 Alts")
(TokenTags "GRT" "Infrastructure" "Indexing")

(Token "LINK" "Layer-1 Alts")
(TokenTags "LINK" "Oracle" "Infrastructure")

(Token "SOL" "Layer-1 Alts")
(TokenTags "SOL" "Blockchain" "Smart Contracts")

(Token "WBTC" "Layer-1 Alts")
(TokenTags "WBTC" "Wrapped Asset" "Bitcoin")

;; ============================================================================
;; SAMPLE QUERIES (for documentation)
;; ============================================================================

;; Query 1: Find all tokens in a specific sector
;; (match (Token ?symbol "DeFi Governance") ?symbol)
;; Expected: "AAVE", "COMP", "MKR", "SNX", "UNI", "YFI"

;; Query 2: Get sector for specific token
;; (match (Token "AAVE" ?sector) ?sector)
;; Expected: "DeFi Governance"

;; Query 3: Find tokens with specific tag
;; (match (and (Token ?symbol ?sector)
;;             (TokenTags ?symbol ?tag1 ?tag2)
;;             (== ?tag1 "Governance"))
;;   (?symbol ?sector))

;; Query 4: Count tokens per sector
;; (match (Token ?symbol "Layer-2") ?symbol)
;; Expected: "ARB", "IMX", "MATIC", "OP" (count: 4)

;; Query 5: Find all sectors
;; (match (Sector ?name ?description) ?name)
;; Expected: "DeFi Governance", "Layer-2", "Yield Protocols", "DEX", "Stablecoins", "Layer-1 Alts"
