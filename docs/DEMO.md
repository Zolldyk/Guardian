# Guardian Demo Guide

**Step-by-Step Testing Instructions for Hackathon Judges**

This guide provides complete instructions for testing Guardian independently via ASI:One. No creator assistance required—everything you need is documented here.

**Estimated Testing Time:** 15-20 minutes

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Accessing ASI:One](#accessing-asione)
3. [Finding Guardian Agent](#finding-guardian-agent)
4. [Test Scenario 1: High-Risk Portfolio](#test-scenario-1-high-risk-portfolio)
5. [Test Scenario 2: Moderate-Risk Portfolio](#test-scenario-2-moderate-risk-portfolio)
6. [Test Scenario 3: Well-Diversified Portfolio](#test-scenario-3-well-diversified-portfolio)
7. [Interpreting Results](#interpreting-results)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before testing Guardian, ensure you have:

### 1. Agentverse Account (Optional for Verification)

While not required to test Guardian via ASI:One, an Agentverse account allows you to verify agent addresses and inspect agent metadata.

**Create Account:**
1. Navigate to [https://agentverse.ai/](https://agentverse.ai/)
2. Click "Sign Up" or "Login with Google"
3. Complete registration
4. Access "My Agents" dashboard

**Optional Verification Steps:**
- View deployed Guardian agents by searching for "Guardian", "CorrelationAgent", "SectorAgent"

### 2. ASI:One Access

ASI:One is Fetch.ai's conversational AI interface for interacting with agents via natural language.

**Access ASI:One:**
- Navigate to [https://asi.one](https://asi.one) (or Fetch.ai-provided demo link)
- No account creation required for basic testing
- Web browser recommended: Chrome, Firefox, Safari, Edge (latest versions)

### 3. Demo Wallet Addresses (Provided)

Guardian includes three pre-configured demo wallets. You'll need these addresses for testing:

| Wallet | Address | Risk Profile |
|--------|---------|--------------|
| **Wallet 1** | `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58` | High Risk |
| **Wallet 2** | `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0` | Moderate Risk |
| **Wallet 3** | `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8` | Well-Diversified |

**Tip:** Bookmark this page or copy addresses to a text file for easy reference.

---

## Accessing ASI:One

### Step-by-Step Navigation

**Step 1: Open ASI:One Interface**

1. Navigate to [https://asi.one](https://asi.one) in your web browser
2. Wait for the chat interface to load (2-3 seconds)
3. You should see a chat input box with placeholder text like "Ask me anything..."

**Step 2: Verify Interface Elements**

Confirm you see the following UI elements:

- **Chat Input Box:** Text field at bottom of screen
- **Send Button:** Arrow or "Send" button next to input box
- **Chat History:** Message display area above input box
- **Agent Search/Discovery:** May be accessible via search icon or dropdown

**Step 3: Test Basic Interaction**

Before querying Guardian, test that ASI:One is responsive:

1. Type: "Hello"
2. Press Enter or click Send
3. Wait for ASI:One to respond (2-5 seconds)
4. Confirm you receive a response (indicates ASI:One is working)

**If ASI:One doesn't respond:**
- Check internet connection
- Refresh browser page
- Try a different browser
- See [Troubleshooting](#troubleshooting) section

---

## Finding Guardian Agent

ASI:One uses natural language discovery—you don't need to know the exact agent address. The ASI:One LLM will route your query to Guardian based on keywords.

### Method 1: Direct Query (Recommended)

Simply send a portfolio analysis query. ASI:One will automatically route to Guardian:

1. In the chat input box, type:
   ```
   Analyze wallet 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58
   ```

2. Press Enter or click Send

3. ASI:One will:
   - Recognize this as a portfolio risk analysis query
   - Search for agents matching "portfolio risk", "wallet analysis", or "Guardian"
   - Route your query to Guardian agent
   - Display Guardian's response

4. Wait 4-10 seconds for Guardian's response

**Expected Response Time:** 3-6 seconds (includes CorrelationAgent + SectorAgent processing)

### Method 2: Explicit Agent Search (If Available)

Some ASI:One interfaces provide explicit agent search:

1. Look for "Search Agents" or "Find Agent" button/icon
2. Enter search term: "Guardian" or "portfolio risk"
3. Select "Guardian" from search results
4. Confirm you see Guardian's agent card with:
   - Agent name: "Guardian"
   - Description: "AI-powered crypto portfolio risk analysis..."
   - Address: `agent1q...` (full address visible)

5. Click "Chat" or "Open Conversation" to start interacting

### Method 3: URL Direct Link (If Provided)

If Guardian provides a direct ASI:One link:

1. Navigate to: `https://asi.one/agent/{GUARDIAN_ADDRESS}` (replace with actual address)
2. Chat interface opens directly with Guardian
3. No search required

**Note:** Check `README.md` for updated Guardian address if needed.

---

## Test Scenario 1: High-Risk Portfolio

**Objective:** Verify Guardian detects compounding risk (high ETH correlation + high sector concentration)

### Test Input

**Wallet Address:** `0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58`

**Query to Send (copy exactly):**
```
Analyze wallet 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58
```

**Alternative Query Phrasings (any should work):**
- "What are the risks in wallet 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58?"
- "Give me a risk assessment for 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58"
- "Assess portfolio 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58"

### Expected Response Structure

Guardian should return a response with **three distinct sections**:

#### Section 1: CorrelationAgent Analysis

```
🔗 CorrelationAgent Analysis (agent1q...):

Your portfolio is 95% correlated to ETH. Portfolios with >90% correlation
lost an average of 73% in the 2022 crash versus 55% market average.

Historical Context:
- 2022 Bear Market (2022-05 to 2022-12): Portfolios with similar correlation
  lost 73.0% (vs. 55.0% market average)
- 2021 May Flash Crash (2021-05-12 to 2021-05-23): Portfolios with similar
  correlation lost 56.0% (vs. 38.0% market average)

(Processing: ~1200ms)
```

**What to Verify:**
- ✅ Correlation percentage is **>90%** (should be ~95%)
- ✅ Historical crash references included (2022 Bear Market, 2021 May Crash)
- ✅ Agent address visible: `agent1q...` (truncated in header)
- ✅ Processing time shown: ~1000-2000ms

#### Section 2: SectorAgent Analysis

```
🏛️ SectorAgent Analysis (agent1q...):

68% of your portfolio is concentrated in DeFi Governance tokens. This
sector lost 75% in the 2022 crash.

Sector Breakdown:
- DeFi Governance: 68.0% ($68,000+) - UNI, AAVE, MKR
- Layer-1 Platforms: 15.0% ($15,000+) - ETH
- DeFi Lending: 12.0% ($12,000+) - COMP
- Stablecoins: 5.0% ($5,000+) - USDC

Historical Sector Risks:
- 2022 Bear Market: DeFi Governance sector lost 75.0% (vs. 55.0% market average)
  Opportunity Cost: Diversified portfolios gained 500.0% during 2023 recovery
  while DeFi Governance only recovered 250.0%

(Processing: ~2300ms)
```

**What to Verify:**
- ✅ Sector concentration is **>60%** (should be ~68% DeFi Governance)
- ✅ Sector breakdown shown with token examples (UNI, AAVE, MKR)
- ✅ Historical sector performance included
- ✅ Agent address visible: `agent1q...` (truncated in header)

#### Section 3: Guardian Synthesis

```
🔮 Guardian Synthesis:

Risk Level: Critical
Compounding Risk Detected: Yes

As CorrelationAgent showed, your 95% ETH correlation creates significant
exposure to Ethereum price movements. SectorAgent revealed that your 68%
DeFi Governance concentration amplifies this risk through sector-specific
vulnerabilities.

Combining these insights, Guardian identifies a compounding risk pattern:
this structure acts like 3.2x leverage to ETH movements. In 2022 Bear Market,
portfolios with this dual-risk structure lost 73% (not just 57% from
correlation alone).

📋 Recommendations:
1. Reduce DeFi Governance token concentration from 68% to below 40%
2. Add uncorrelated assets (Bitcoin, Alternative Layer-1s, or Stablecoins)
3. Prioritize sector diversification before correlation reduction

---

⚙️ Agents Consulted:
- CorrelationAgent (agent1q...) - ~1200ms
- SectorAgent (agent1q...) - ~2300ms

⏱️ Total Analysis Time: ~3.6 seconds
```

**What to Verify:**
- ✅ Risk Level: **Critical** or **High Risk**
- ✅ Compounding Risk Detected: **Yes**
- ✅ Synthesis references both agents by name ("As CorrelationAgent showed...", "SectorAgent revealed...")
- ✅ Risk multiplier mentioned (e.g., "3.2x leverage effect")
- ✅ 2-3 prioritized recommendations provided
- ✅ Total analysis time: **3-6 seconds**

### Validation Checklist

Use this checklist to confirm Guardian's response meets expectations:

- [ ] Response received within 10 seconds
- [ ] Three distinct sections visible (CorrelationAgent, SectorAgent, Guardian)
- [ ] ETH correlation reported as >90%
- [ ] Sector concentration reported as >60% (DeFi Governance)
- [ ] Compounding risk explicitly detected
- [ ] Historical crash references included (2022, 2021)
- [ ] Agent addresses shown (truncated in headers, full in summary)
- [ ] Processing times shown for each agent
- [ ] Recommendations prioritize sector diversification
- [ ] Total analysis time shown (~3.6 seconds)

**Compare to Sample Response:**
See `docs/sample-responses/wallet-1-high-risk-transparency.md` for complete expected output.

---

## Test Scenario 2: Moderate-Risk Portfolio

**Objective:** Verify Guardian correctly identifies moderate risk with partial diversification

### Test Input

**Wallet Address:** `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0`

**Query to Send (copy exactly):**
```
Analyze wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0
```

### Expected Response Characteristics

#### CorrelationAgent Analysis

**Expected Correlation:** 80-85% (Moderate Risk)

**Key Points to Verify:**
- ✅ Correlation percentage between **75-90%**
- ✅ Historical context shows moderate crash losses (not as severe as high-risk portfolio)
- ✅ Narrative indicates moderate exposure to ETH price movements

#### SectorAgent Analysis

**Expected Sector Concentration:** 40-50% (Balanced)

**Key Points to Verify:**
- ✅ No single sector exceeds 60%
- ✅ Sector breakdown shows diversification across 4+ sectors
- ✅ Stablecoin allocation mentioned (DAI + USDC ~16%)
- ✅ Multiple sectors represented: DeFi, Layer-2, Stablecoins, Infrastructure

#### Guardian Synthesis

**Expected Risk Level:** Moderate or Medium Risk

**Key Points to Verify:**
- ✅ Risk Level: **Moderate** (not Critical)
- ✅ Compounding Risk Detected: **No** or **Low** (because sector concentration <60%)
- ✅ Synthesis acknowledges reasonable diversification
- ✅ Recommendations focus on incremental improvements (not urgent restructuring)
- ✅ Stablecoin cushion mentioned as positive factor

### Sample Recommendations (Expected)

1. Consider adding non-ETH Layer-1s (BTC, SOL, AVAX) to further reduce correlation
2. Increase stablecoin allocation during high volatility periods
3. Monitor sector rebalancing—maintain no sector >40%

### Validation Checklist

- [ ] Response received within 10 seconds
- [ ] Risk level classified as Moderate (not Critical or Low)
- [ ] Correlation between 75-90%
- [ ] No sector exceeds 60%
- [ ] Stablecoin allocation acknowledged
- [ ] Recommendations are incremental (not urgent)
- [ ] Compounding risk NOT detected (because lacks dual-risk pattern)

**Compare to Sample Response:**
See `docs/sample-responses/wallet-2-moderate-risk.md` for complete expected output.

---

## Test Scenario 3: Well-Diversified Portfolio

**Objective:** Verify Guardian correctly identifies low-risk, well-structured portfolios

### Test Input

**Wallet Address:** `0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8`

**Query to Send (copy exactly):**
```
Analyze wallet 0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8
```

### Expected Response Characteristics

#### CorrelationAgent Analysis

**Expected Correlation:** <70% (Low Risk)

**Key Points to Verify:**
- ✅ Correlation percentage **below 70%**
- ✅ Narrative emphasizes healthy diversification
- ✅ Mentions cross-chain allocation (BTC, SOL, AVAX reduce ETH correlation)
- ✅ Historical context shows better crash performance than market average

#### SectorAgent Analysis

**Expected Sector Concentration:** No sector >30% (Excellent)

**Key Points to Verify:**
- ✅ All sectors below 30%
- ✅ Sector breakdown shows 5+ distinct sectors
- ✅ Layer-1 diversification across BTC, ETH, SOL, AVAX, ATOM, DOT
- ✅ Stablecoin allocation ~18% (significant downside protection)
- ✅ Narrative praises sector balance

#### Guardian Synthesis

**Expected Risk Level:** Low Risk or Well-Diversified

**Key Points to Verify:**
- ✅ Risk Level: **Low** or **Well-Diversified**
- ✅ Compounding Risk Detected: **No**
- ✅ Synthesis acknowledges excellent risk management
- ✅ Recommendations focus on maintaining discipline (not restructuring)
- ✅ May reference 2022 outperformance vs ETH-only portfolios

### Sample Recommendations (Expected)

1. Portfolio structure is sound—maintain rebalancing discipline during market movements
2. Continue cross-chain diversification strategy
3. Monitor sector drift—ensure no sector exceeds 30% during bull markets

### Validation Checklist

- [ ] Response received within 10 seconds
- [ ] Risk level classified as Low (not Moderate or Critical)
- [ ] Correlation below 70%
- [ ] No sector exceeds 30%
- [ ] Cross-chain diversification acknowledged (BTC, SOL, AVAX mentioned)
- [ ] Recommendations are maintenance-focused (not restructuring)
- [ ] Compounding risk NOT detected
- [ ] Historical outperformance mentioned

**Compare to Sample Response:**
See `docs/sample-responses/wallet-3-diversified.md` for complete expected output.

---

## Interpreting Results

### What to Look for in Guardian's Responses

#### 1. **Multi-Agent Collaboration**

**Evidence of multi-agent architecture:**

- ✅ **Three distinct sections:** CorrelationAgent, SectorAgent, Guardian
- ✅ **Visual separators:** Emoji headers (🔗, 🏛️, 🔮) or horizontal rules (`---`)
- ✅ **Agent addresses visible:** Truncated in section headers (`agent1q...`), full in summary
- ✅ **Independent analysis:** CorrelationAgent and SectorAgent provide different insights

**Why This Matters:** Proves Guardian is not a single-agent system. Each specialist contributes unique analysis.

#### 2. **Transparency Features**

**Evidence of transparent multi-agent collaboration:**

- ✅ **Verbatim agent responses:** CorrelationAgent and SectorAgent sections show raw specialist output (not summarized by Guardian)
- ✅ **Explicit attribution:** Guardian synthesis references agents by name ("As CorrelationAgent showed...", "SectorAgent revealed...")
- ✅ **Processing times shown:** Per-agent timing (~1200ms, ~2300ms) demonstrates parallel processing
- ✅ **Agent addresses verifiable:** Full addresses in summary enable Agentverse verification

**Why This Matters:** Builds trust by showing exactly how multi-agent collaboration works.

#### 3. **Compounding Risk Detection**

**Guardian's unique value-add (only in High-Risk scenario):**

- ✅ **Synthesis goes beyond individual metrics:** CorrelationAgent sees 95% correlation, SectorAgent sees 68% concentration, but **Guardian identifies compounding risk pattern**
- ✅ **Risk multiplier quantified:** "Acts like 3.2x leverage to ETH movements"
- ✅ **Historical validation:** "Portfolios with this dual-risk structure lost 73% (not just 57% from correlation alone)"

**Why This Matters:** Demonstrates that Guardian provides insights neither specialist agent could generate alone.

#### 4. **Recommendation Prioritization**

**Guardian's synthesis logic in action:**

**High-Risk Portfolio:**
- Recommendations prioritize **sector diversification first** (reduces both correlation and concentration)
- Rationale explained: "When both high correlation and high sector concentration are present, sector concentration amplifies correlation risk"

**Moderate/Low-Risk Portfolios:**
- Recommendations are incremental or maintenance-focused
- No urgent restructuring required

**Why This Matters:** Shows Guardian understands risk interactions, not just individual dimensions.

### Red Flags (Issues to Report)

If you see any of these, please note in your hackathon evaluation:

- ❌ **Single-section response:** Only Guardian synthesis (no CorrelationAgent/SectorAgent sections visible)
- ❌ **Missing agent addresses:** No addresses shown in headers or summary
- ❌ **No processing times:** Cannot verify parallel processing
- ❌ **Contradictory analysis:** CorrelationAgent says high risk, Guardian says low risk
- ❌ **Response timeout:** Guardian takes >15 seconds or doesn't respond
- ❌ **Generic recommendations:** No specific portfolio-tailored suggestions

---

## Troubleshooting

### Issue 1: ASI:One Doesn't Respond

**Symptoms:**
- You send a query, but no response appears
- Spinner/loading indicator doesn't appear
- Chat interface seems frozen

**Solutions:**

1. **Check Internet Connection:**
   - Verify browser can load other websites
   - Check network status indicator

2. **Refresh Browser Page:**
   - Press Ctrl+R (Windows) or Cmd+R (Mac)
   - Or click browser refresh button
   - ASI:One state should reload

3. **Clear Browser Cache:**
   - Chrome: Settings → Privacy → Clear Browsing Data
   - Firefox: Settings → Privacy → Clear Data
   - Select "Cached images and files"
   - Refresh page

4. **Try Different Browser:**
   - Test in Chrome, Firefox, Safari, or Edge
   - Some browsers may have better WebSocket support

5. **Disable Browser Extensions:**
   - Ad blockers or privacy extensions may block ASI:One
   - Temporarily disable extensions
   - Refresh page and retry

### Issue 2: Guardian Not Found

**Symptoms:**
- ASI:One responds, but says "Agent not found" or "No matching agent"
- Query routes to wrong agent (not Guardian)

**Solutions:**

1. **Use Direct Wallet Address Query:**
   - Instead of: "Find Guardian agent"
   - Use: "Analyze wallet 0x9aabD891ab1FaA750FAE5aba9b55623c7F69fD58"
   - ASI:One's LLM should route based on intent, not name

2. **Verify Agent is Deployed:**
   - Check `README.md` for latest agent status
   - Guardian may be temporarily offline for maintenance
   - Check Agentverse dashboard (if you have access) for agent status

3. **Try Alternative Phrasing:**
   - "What are the risks in portfolio 0x9aab..."
   - "Assess crypto wallet 0x9aab..."
   - "Portfolio analysis for 0x9aab..."

4. **Check Agent Address:**
   - If you have Guardian's agent address (`agent1q...`), try:
   - "Send message to agent1q... with wallet 0x9aab..."

### Issue 3: Response Missing CorrelationAgent or SectorAgent Section

**Symptoms:**
- Guardian response only shows synthesis (no specialist agent sections)
- Missing emoji headers (🔗, 🏛️)
- No agent addresses or processing times shown

**Possible Causes:**

1. **Timeout:** CorrelationAgent or SectorAgent didn't respond within 10 seconds
   - **Expected Behavior:** Guardian should show error message like "⚠️ CorrelationAgent did not respond within 10 seconds (timeout)"
   - **Action:** Retry query—timeout may be transient

2. **Specialist Agent Offline:** Agent deployment issue
   - **Action:** Check `README.md` for agent status updates
   - **Action:** Report issue in hackathon evaluation

3. **ASI:One Truncation:** Response too long, ASI:One truncated specialist sections
   - **Action:** Ask ASI:One to "Show full response" or "Show CorrelationAgent section"

### Issue 4: Analysis Takes Too Long (>15 seconds)

**Symptoms:**
- Guardian response takes longer than expected
- Spinner/loading indicator runs for >15 seconds

**Possible Causes:**

1. **MeTTa Query Delay:** Knowledge graph query is slow
   - **Expected:** Guardian should fall back to JSON within 10 seconds
   - **Action:** Wait up to 20 seconds before reporting issue

2. **Network Latency:** Slow connection between ASI:One and Agentverse
   - **Action:** Check internet connection speed
   - **Action:** Retry query

3. **High Platform Load:** Agentverse experiencing high traffic
   - **Expected:** Should still complete within 20 seconds
   - **Action:** Retry query after 1 minute

### Issue 5: Unexpected Risk Level

**Symptoms:**
- Demo Wallet 1 (High Risk) classified as Low Risk
- Demo Wallet 3 (Low Risk) classified as High Risk
- Risk level contradicts correlation/sector metrics

**This is a legitimate bug—please report in evaluation:**

1. **Document Discrepancy:**
   - Note expected risk level vs actual
   - Screenshot Guardian's response
   - Include correlation % and sector concentration % from response

2. **Verify Sample Response:**
   - Compare to `docs/sample-responses/wallet-X-...md`
   - Check if correlation/sector metrics match expectations

3. **Report in Hackathon Feedback:**
   - This indicates synthesis logic error
   - Include wallet address tested and observed behavior

### Issue 6: Invalid Wallet Address Error

**Symptoms:**
- Guardian responds: "Invalid wallet address format"
- Or: "Could not parse portfolio data"

**Solutions:**

1. **Verify Address Format:**
   - Must start with `0x`
   - Must be 42 characters total
   - Must be hexadecimal (0-9, a-f)
   - Copy addresses from `README.md` or this guide (don't retype manually)

2. **Check for Typos:**
   - Ensure no spaces before/after address
   - Ensure complete address (not truncated)

3. **Use Demo Wallet Addresses:**
   - Don't test with random wallet addresses—Guardian only supports demo wallets
   - Demo wallets: `0x9aab...`, `0x742d...`, `0xBE0e...` (see [Prerequisites](#prerequisites))

### Issue 7: Can't Verify Agent Addresses

**Symptoms:**
- Want to verify agent addresses on Agentverse, but can't find agents

**Solutions:**

1. **Search by Agent Name:**
   - Agentverse → Search → "Guardian"
   - Or: "CorrelationAgent", "SectorAgent"

2. **Search by Address:**
   - Copy full address from Guardian's response (summary section)
   - Agentverse → Search → Paste address

3. **Check README for Addresses:**
   - `README.md` lists deployed agent addresses
   - Use these for verification

4. **Not Critical for Testing:**
   - You can fully test Guardian via ASI:One without Agentverse verification
   - Agent address verification is optional

---

## Additional Testing Scenarios

### Bonus Test 1: Multi-Turn Conversation

Guardian supports conversational follow-up queries:

1. Send initial query: "Analyze wallet 0x9aab..."
2. Wait for Guardian's response
3. Send follow-up: "Why is DeFi Governance concentration risky?"
4. Guardian should provide detailed explanation referencing previous analysis

**Expected:** Guardian maintains conversation context and references previous portfolio analysis.

### Bonus Test 2: Compare All Three Wallets

Test Guardian's consistency across risk levels:

1. Analyze Wallet 1 (High Risk) - note correlation %
2. Analyze Wallet 2 (Moderate Risk) - note correlation %
3. Analyze Wallet 3 (Low Risk) - note correlation %

**Expected Pattern:**
- Wallet 1 correlation: >90%
- Wallet 2 correlation: 75-90%
- Wallet 3 correlation: <70%

**Validates:** Guardian consistently applies risk thresholds across portfolios.

---

## Summary Checklist

Use this final checklist to confirm successful Guardian testing:

- [ ] Accessed ASI:One successfully
- [ ] Found/queried Guardian agent
- [ ] Tested Demo Wallet 1 (High Risk) - compounding risk detected
- [ ] Tested Demo Wallet 2 (Moderate Risk) - balanced risk profile
- [ ] Tested Demo Wallet 3 (Low Risk) - excellent diversification
- [ ] Verified multi-agent collaboration (3 sections visible)
- [ ] Verified transparency (agent addresses, processing times shown)
- [ ] Compared results to sample responses in `docs/sample-responses/`
- [ ] Total testing time: ~15-20 minutes

**For complete technical architecture details, see `ARCHITECTURE.md`.**

---

## Support

If you encounter issues not covered in this guide:

1. **Check Sample Responses:** `docs/sample-responses/` contains full expected outputs
2. **Review README:** `README.md` has updated agent addresses and status
3. **Check Architecture Docs:** `ARCHITECTURE.md` explains technical design
4. **Report Issues:** Include in hackathon evaluation feedback

**Guardian is designed for independent judge testing—no creator assistance should be required.**

---

**Last Updated:** 2025-10-23
**Story:** 3.4 - Comprehensive Documentation for Judge Self-Service
**Author:** James (Dev Agent)