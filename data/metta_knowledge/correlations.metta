;; MeTTa Knowledge Graph: Correlation Bracket Definitions
;; Schema documentation in README.md
;;
;; Note: This is a schema representation file demonstrating MeTTa/SingularityNET
;; knowledge graph design. Actual queries use JSON representation due to
;; Hyperon library compatibility constraints.

;; ============================================================================
;; CORRELATION BRACKET DEFINITIONS
;; ============================================================================

;; High correlation bracket (>90%)
(CorrelationBracket "high" ">90%")
(BracketRange "high" 0.90 1.00)
(BracketDescription "high" "Portfolio moves almost identically with ETH - very high systematic risk")
(RiskLevel "high" "severe")

;; Medium-high correlation bracket (80-90%)
(CorrelationBracket "medium_high" "80-90%")
(BracketRange "medium_high" 0.80 0.90)
(BracketDescription "medium_high" "Portfolio strongly correlated with ETH - high systematic risk")
(RiskLevel "medium_high" "high")

;; Medium correlation bracket (70-80%)
(CorrelationBracket "medium" "70-80%")
(BracketRange "medium" 0.70 0.80)
(BracketDescription "medium" "Portfolio moderately correlated with ETH - moderate systematic risk")
(RiskLevel "medium" "moderate")

;; Low correlation bracket (<70%)
(CorrelationBracket "low" "<70%")
(BracketRange "low" 0.00 0.70)
(BracketDescription "low" "Portfolio has lower correlation with ETH - better diversification")
(RiskLevel "low" "low")

;; ============================================================================
;; CORRELATION INTERPRETATION RULES
;; ============================================================================

;; Risk interpretation by bracket
(InterpretationRule "high"
  "Extremely high correlation (>90%) means portfolio will likely follow ETH's movements almost exactly. During crashes, expect similar drawdowns.")

(InterpretationRule "medium_high"
  "High correlation (80-90%) means portfolio will closely track ETH. Most altcoins fall in this range during market stress.")

(InterpretationRule "medium"
  "Moderate correlation (70-80%) provides some diversification benefit but still significant ETH exposure.")

(InterpretationRule "low"
  "Lower correlation (<70%) indicates better diversification. May include stablecoins or uncorrelated assets.")

;; ============================================================================
;; HISTORICAL PERFORMANCE PATTERNS
;; ============================================================================

;; Historical average losses by bracket (across all crashes)
(AverageLoss "high" -62.3)    ;; Average of -73.0, -52.0, -62.0
(AverageLoss "medium_high" -58.0)  ;; Average of -68.0, -48.0, -58.0
(AverageLoss "medium" -52.7)   ;; Average of -62.0, -43.0, -53.0
(AverageLoss "low" -41.7)      ;; Average of -48.0, -35.0, -42.0

;; Diversification benefit (compared to high correlation)
(DiversificationBenefit "medium_high" 4.3)  ;; 62.3 - 58.0
(DiversificationBenefit "medium" 9.6)       ;; 62.3 - 52.7
(DiversificationBenefit "low" 20.6)         ;; 62.3 - 41.7

;; ============================================================================
;; PORTFOLIO CLASSIFICATION RULES
;; ============================================================================

;; Classification based on correlation coefficient
(ClassificationRule
  "If correlation > 0.90 then bracket = 'high' AND risk = 'severe'")

(ClassificationRule
  "If 0.80 <= correlation <= 0.90 then bracket = 'medium_high' AND risk = 'high'")

(ClassificationRule
  "If 0.70 <= correlation < 0.80 then bracket = 'medium' AND risk = 'moderate'")

(ClassificationRule
  "If correlation < 0.70 then bracket = 'low' AND risk = 'low'")

;; ============================================================================
;; SAMPLE QUERIES (for documentation)
;; ============================================================================

;; Query 1: Get bracket definition for specific range
;; (match (CorrelationBracket "high" ?range) ?range)
;; Expected: ">90%"

;; Query 2: Get risk level for bracket
;; (match (RiskLevel "high" ?level) ?level)
;; Expected: "severe"

;; Query 3: Get interpretation for bracket
;; (match (InterpretationRule "medium_high" ?interpretation) ?interpretation)
;; Expected: "High correlation (80-90%) means portfolio will closely track ETH..."

;; Query 4: Find brackets with severe/high risk
;; (match (and (CorrelationBracket ?id ?range)
;;             (RiskLevel ?id ?risk)
;;             (or (== ?risk "severe") (== ?risk "high")))
;;   (?id ?range ?risk))
;; Expected: ("high" ">90%" "severe"), ("medium_high" "80-90%" "high")

;; Query 5: Get average historical loss for bracket
;; (match (AverageLoss "high" ?avg_loss) ?avg_loss)
;; Expected: -62.3

;; Query 6: Get diversification benefit compared to high correlation
;; (match (DiversificationBenefit "low" ?benefit) ?benefit)
;; Expected: 20.6 (percentage points of loss avoided vs high correlation)
