# User Interface Design Goals

## Overall UX Vision

Guardian is designed as a **conversational intelligence agent**, not a traditional dashboard or visualization tool. The user experience centers on natural language interaction where users ask questions in plain English and receive narrative responses that synthesize complex risk analysis into clear insights. The UX philosophy is "show me what matters, not everything"—Guardian proactively reveals risks users didn't know to ask about rather than overwhelming with raw data.

The interaction feels like consulting a knowledgeable financial advisor who has deeply analyzed your portfolio: thoughtful, educational, and action-oriented. Users should experience progressive revelation—starting with surface understanding, then correlation risk, then sector risk, then the synthesis that shows how these dimensions compound. Each revelation builds toward the "lean forward moment" where the user realizes their portfolio structure is riskier than they thought.

**Key UX Principles:**
- **Intelligence over information:** Judgment and interpretation, not data dumps
- **Visceral over abstract:** Historical crash simulations make risk concrete
- **Transparent reasoning:** Users see which agents contributed what insights
- **Conversational flow:** Natural back-and-forth, not form filling
- **Actionable outcomes:** Every analysis ends with clear next steps

## Key Interaction Paradigms

**1. Natural Language Query Input**
Users interact via text-based conversational interface through ASI:One. Primary entry point is wallet address submission: "Analyze 0xabc123..." or "How risky is my portfolio at 0xabc123". System also supports follow-up questions: "Why is governance token concentration dangerous?" or "What should I do about this?"

**2. Progressive Risk Disclosure**
Information is revealed in layers rather than all at once:
- Layer 1: Surface acknowledgment ("Analyzing your portfolio...")
- Layer 2: Correlation risk reveal with historical context
- Layer 3: Sector concentration reveal with opportunity cost
- Layer 4: Synthesis showing compounding effects
- Layer 5: Actionable recommendations

This structure creates narrative tension and makes the synthesis feel like an earned insight rather than just another data point.

**3. Multi-Agent Transparency**
Individual agent contributions are visible to users, not hidden in backend processing. When Guardian consults CorrelationAgent or SectorAgent, users see the specific responses from each agent. This demonstrates the multi-agent collaboration explicitly—critical for hackathon judging and for building user trust in the analysis.

**4. Contextual Education**
Guardian doesn't assume users understand correlation coefficients or sector dynamics. Responses include brief educational context: "95% correlation means your portfolio moves almost identically to ETH—like 3x leveraged exposure" before diving into implications.

## Core Screens and Views

*Note: Guardian is chat-based via ASI:One, so "screens" are conversation stages rather than traditional UI screens.*

**1. Initial Query/Wallet Input Stage**
User provides wallet address in natural language. System confirms receipt and initiates analysis.

**2. Analysis In-Progress Stage**
Guardian shows which agents are being consulted and what they're analyzing. Example: "Consulting CorrelationAgent to analyze your portfolio structure..." This makes wait time feel purposeful and shows multi-agent collaboration.

**3. Correlation Risk Reveal Stage**
CorrelationAgent's response is presented with correlation coefficient, interpretation, and historical crash performance. Includes clear explanation of what the numbers mean.

**4. Sector Concentration Reveal Stage**
SectorAgent's response shows sector breakdown, concentration percentages, sector-specific crash performance, and opportunity cost (what was missed by over-concentrating).

**5. Synthesis & Compounding Risk Stage**
Guardian's synthesis explains how correlation + sector risks multiply. This is the "lean forward moment"—the insight neither individual agent revealed.

**6. Recommendations Stage**
2-3 specific, actionable recommendations based on identified risks. Includes rationale for each recommendation.

**7. Follow-Up Q&A Stage**
User can ask clarifying questions, drill into specific risks, or request alternative strategies. Guardian maintains context from previous analysis.

## Accessibility: **None** (MVP), WCAG AA (Post-MVP)

**MVP Stance:** Guardian's MVP relies entirely on ASI:One's accessibility features. As a text-based conversational interface, ASI:One should be inherently more accessible than visual dashboards (screen reader friendly, keyboard navigable). However, no Guardian-specific accessibility testing or enhancements are in scope for the 10-day hackathon build.

**Assumption:** ASI:One platform provides baseline accessibility compliance. Guardian doesn't introduce additional accessibility barriers since responses are plain text narratives.

**Post-MVP Goal:** When building standalone web dashboard (Phase 2), target WCAG AA compliance with proper semantic HTML, ARIA labels, keyboard navigation, and sufficient color contrast for any visualizations added.

## Branding

**MVP Approach: Minimal/Functional Branding**

Guardian is a hackathon proof-of-concept, not a consumer brand. Branding elements are functional and trust-building rather than marketing-focused:

- **Name:** "Guardian" conveys protection and vigilance—appropriate for risk analysis
- **Tagline:** "DeFi Portfolio Intelligence Agent" (descriptive, communicates purpose immediately)
- **Agent Persona:** Investigative, analytical, direct but supportive. Like a concerned financial advisor who tells you hard truths.
- **Visual Identity:** None required for MVP (ASI:One handles all UI rendering). If needed, simple text-based identifier: "🛡️ Guardian" with shield emoji.
- **Tone of Voice:** Professional but not alarmist. Educational without being condescending. Clear warnings about risk without creating panic.

## Target Device and Platforms: **Web Responsive** (ASI:One Interface)

**Primary Platform:** Web browser access via ASI:One conversational interface. Users access Guardian through ASI:One's web platform on desktop or mobile browsers.

**Device Support:**
- **Desktop browsers:** Chrome, Firefox, Safari, Edge (whatever ASI:One supports)
- **Mobile browsers:** Responsive web interface, no native mobile app
- **Tablets:** Supported via responsive web (ASI:One's responsibility)

**No Platform-Specific Optimization:** Guardian doesn't control the UI rendering—ASI:One does. As a conversational agent, Guardian's output is plain text narrative that adapts to any screen size naturally.

---
