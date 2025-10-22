;; MeTTa Knowledge Graph: Historical Crypto Market Crashes
;; Schema documentation in README.md
;;
;; Note: This is a schema representation file demonstrating MeTTa/SingularityNET
;; knowledge graph design. Actual queries use JSON representation due to
;; Hyperon library compatibility constraints.

;; ============================================================================
;; CRASH ENTITIES
;; ============================================================================

;; 2022 Bear Market
(Crash crash_2022_bear "2022 Bear Market" "Nov 2021 - Jun 2022")
(EthDrawdown crash_2022_bear -75.0)
(MarketAvgLoss crash_2022_bear -55.0)
(RecoveryPeriod crash_2022_bear "Jun 2022 - Dec 2023")

;; Correlation bracket losses for 2022 crash
(CorrelationBracketLoss crash_2022_bear ">90%" -73.0)
(CorrelationBracketLoss crash_2022_bear "80-90%" -68.0)
(CorrelationBracketLoss crash_2022_bear "70-80%" -62.0)
(CorrelationBracketLoss crash_2022_bear "<70%" -48.0)

;; Sector performance for 2022 crash
(SectorPerformance crash_2022_bear "DeFi Governance" -75.0)
(SectorPerformance crash_2022_bear "Layer-2" -60.0)
(SectorPerformance crash_2022_bear "Yield Protocols" -80.0)
(SectorPerformance crash_2022_bear "DEX" -68.0)
(SectorPerformance crash_2022_bear "Stablecoins" -5.0)
(SectorPerformance crash_2022_bear "Layer-1 Alts" -65.0)

;; Recovery winners for 2022 crash
(RecoveryWinner crash_2022_bear "SOL")
(RecoveryWinner crash_2022_bear "MATIC")
(RecoveryWinner crash_2022_bear "OP")

;; Opportunity cost data for 2022 crash
(OpportunityCost crash_2022_bear "Layer-2" "OP" 420.0 "Optimism airdrop and L2 narrative dominance")
(OpportunityCost crash_2022_bear "Layer-1 Alts" "SOL" 500.0 "FTX recovery and ecosystem growth")
(OpportunityCost crash_2022_bear "Stablecoins" "USDC" 2.0 "Capital preservation during crash, avoided 75% drawdown")

;; ============================================================================

;; 2021 Correction
(Crash crash_2021_correction "2021 Correction" "May 2021 - Jul 2021")
(EthDrawdown crash_2021_correction -55.0)
(MarketAvgLoss crash_2021_correction -45.0)
(RecoveryPeriod crash_2021_correction "Jul 2021 - Nov 2021")

;; Correlation bracket losses for 2021 correction
(CorrelationBracketLoss crash_2021_correction ">90%" -52.0)
(CorrelationBracketLoss crash_2021_correction "80-90%" -48.0)
(CorrelationBracketLoss crash_2021_correction "70-80%" -43.0)
(CorrelationBracketLoss crash_2021_correction "<70%" -35.0)

;; Sector performance for 2021 correction
(SectorPerformance crash_2021_correction "DeFi Governance" -58.0)
(SectorPerformance crash_2021_correction "Layer-2" -52.0)
(SectorPerformance crash_2021_correction "Yield Protocols" -62.0)
(SectorPerformance crash_2021_correction "DEX" -55.0)
(SectorPerformance crash_2021_correction "Stablecoins" -3.0)
(SectorPerformance crash_2021_correction "Layer-1 Alts" -50.0)

;; Recovery winners for 2021 correction
(RecoveryWinner crash_2021_correction "BNB")
(RecoveryWinner crash_2021_correction "ADA")
(RecoveryWinner crash_2021_correction "DOT")

;; Opportunity cost data for 2021 correction
(OpportunityCost crash_2021_correction "Layer-1 Alts" "DOT" 180.0 "Parachain auctions and ecosystem expansion")
(OpportunityCost crash_2021_correction "Layer-2" "MATIC" 220.0 "Polygon scaling adoption and NFT boom")
(OpportunityCost crash_2021_correction "Stablecoins" "USDC" 1.5 "Avoided 55% correction, maintained purchasing power")

;; ============================================================================

;; 2020 COVID Crash
(Crash crash_2020_covid "2020 COVID Crash" "Feb 2020 - Mar 2020")
(EthDrawdown crash_2020_covid -65.0)
(MarketAvgLoss crash_2020_covid -50.0)
(RecoveryPeriod crash_2020_covid "Mar 2020 - Dec 2020")

;; Correlation bracket losses for 2020 COVID crash
(CorrelationBracketLoss crash_2020_covid ">90%" -62.0)
(CorrelationBracketLoss crash_2020_covid "80-90%" -58.0)
(CorrelationBracketLoss crash_2020_covid "70-80%" -53.0)
(CorrelationBracketLoss crash_2020_covid "<70%" -42.0)

;; Sector performance for 2020 COVID crash
(SectorPerformance crash_2020_covid "DeFi Governance" -48.0)
(SectorPerformance crash_2020_covid "Layer-2" -55.0)
(SectorPerformance crash_2020_covid "Yield Protocols" -52.0)
(SectorPerformance crash_2020_covid "DEX" -50.0)
(SectorPerformance crash_2020_covid "Stablecoins" -2.0)
(SectorPerformance crash_2020_covid "Layer-1 Alts" -58.0)

;; Recovery winners for 2020 COVID crash
(RecoveryWinner crash_2020_covid "LINK")
(RecoveryWinner crash_2020_covid "UNI")
(RecoveryWinner crash_2020_covid "AAVE")

;; Opportunity cost data for 2020 COVID crash
(OpportunityCost crash_2020_covid "DeFi Governance" "UNI" 650.0 "DeFi summer explosion and Uniswap V2 dominance")
(OpportunityCost crash_2020_covid "Layer-1 Alts" "LINK" 550.0 "Oracle demand surge during DeFi summer")
(OpportunityCost crash_2020_covid "Stablecoins" "USDC" 1.0 "Preserved capital through 65% market crash")

;; ============================================================================
;; SAMPLE QUERIES (for documentation)
;; ============================================================================

;; Query 1: Find crashes where >90% correlation portfolios lost more than 70%
;; (match (and (Crash ?id ?name ?period)
;;             (CorrelationBracketLoss ?id ">90%" ?loss)
;;             (< ?loss -70.0))
;;   (?id ?name ?loss))
;; Expected: (crash_2022_bear "2022 Bear Market" -73.0)

;; Query 2: Get DeFi Governance sector performance across all crashes
;; (match (and (Crash ?id ?name ?period)
;;             (SectorPerformance ?id "DeFi Governance" ?loss))
;;   (?id ?name ?loss))
;; Expected:
;;   (crash_2022_bear "2022 Bear Market" -75.0)
;;   (crash_2021_correction "2021 Correction" -58.0)
;;   (crash_2020_covid "2020 COVID Crash" -48.0)

;; Query 3: Find recovery winners for specific crash
;; (match (RecoveryWinner crash_2022_bear ?token) ?token)
;; Expected: "SOL", "MATIC", "OP"

;; Query 4: Complex - High correlation AND severe DeFi concentration
;; (match (and (Crash ?id ?name ?period)
;;             (CorrelationBracketLoss ?id ">90%" ?corr_loss)
;;             (SectorPerformance ?id "DeFi Governance" ?sector_loss)
;;             (< ?corr_loss -70.0)
;;             (< ?sector_loss -70.0))
;;   (?id ?name ?corr_loss ?sector_loss))
;; Expected: (crash_2022_bear "2022 Bear Market" -73.0 -75.0)

;; Query 5: Get all data for specific crash
;; (match (and (Crash crash_2020_covid ?name ?period)
;;             (EthDrawdown crash_2020_covid ?eth_loss))
;;   (?name ?period ?eth_loss))
;; Expected: ("2020 COVID Crash" "Feb 2020 - Mar 2020" -65.0)
