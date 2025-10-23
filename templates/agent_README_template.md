# [Agent Name]

## Description
[Clear, concise description of what this agent does - 2-3 sentences max. Focus on the primary value proposition.]

## What it does
This agent [specific functionality in plain language]. It can help you:
- **[Capability 1]** - [Brief explanation of first main capability]
- **[Capability 2]** - [Brief explanation of second main capability]
- **[Capability 3]** - [Brief explanation of third main capability]
- **[Capability 4]** - [Additional capabilities if applicable]

## Example Queries
Users can interact with this agent using natural language via ASI:One Chat:
- "[Example query 1 - be specific and realistic]"
- "[Example query 2 - show different use case]"
- "[Example query 3 - demonstrate variation in phrasing]"
- "[Example query 4 - show advanced usage]"
- "[Example query 5 - demonstrate edge case if relevant]"

**Tip:** You can ask in natural language - the agent will understand your intent!

## How it works
1. **[Step 1 Name]** - [Brief description of first processing step]
2. **[Step 2 Name]** - [Brief description of second processing step]
3. **[Step 3 Name]** - [Brief description of third processing step]
4. **[Step 4 Name]** - [Brief description of fourth processing step]
5. **[Step 5 Name]** - [Brief description of final step/output]

## [Optional: Key Metrics/Levels/Categories]
If your agent categorizes or scores results, explain the levels:
- **[Level 1 Name] ([Threshold])**: [What this means for the user]
- **[Level 2 Name] ([Threshold])**: [What this means for the user]
- **[Level 3 Name] ([Threshold])**: [What this means for the user]

## Technical Details
- **Agent Type:** [Analysis/Data/Service/Orchestration/etc.]
- **Response Time:** ~[X-Y] seconds (depending on [factors])
- **Data Sources:** [List primary data sources - APIs, databases, GitHub, etc.]
- **Supported Libraries:** [List key libraries used - requests, openai, langchain, etc.]
- **ASI1 LLM Integration:** ✅ Enabled via Chat Protocol
- **AI Parameter Extraction:** [OpenAI/Claude] Agent ([rate limit info])
- **Analysis Period/Window:** [Time period for historical analysis if applicable]
- **Minimum Data Requirements:** [What data is required, minimum thresholds]

## Message Protocol Support
This agent supports both:
1. **ASI1 Chat Protocol** - For natural language queries via ASI:One interface (recommended for users)
2. **Direct Agent Messages** - For structured `[RequestModelName]` messages from other agents (for agent-to-agent communication)

## Dependencies
List other agents or services this agent depends on:
- **[Agent/Service 1 Name]** - [What it provides to this agent]
- **[Agent/Service 2 Name]** - [What it provides to this agent]
- **[Optional: External API Name]** - [What it provides]

## Limitations
Be transparent about what the agent cannot do:
- [Limitation 1 - e.g., data availability constraints]
- [Limitation 2 - e.g., rate limits]
- [Limitation 3 - e.g., analysis window constraints]
- [Limitation 4 - e.g., specific edge cases not handled]
- [Important caveat - e.g., "Correlation does not imply causation"]

## Error Handling
Explain how the agent handles common errors:
- **[Error Type 1]**: [What happens and what user should do]
- **[Error Type 2]**: [What happens and what user should do]
- **[Error Type 3]**: [What happens and what user should do]
- **[Error Type 4]**: [What happens and what user should do]

## Example Output
```
[Show a realistic example of what the agent returns]
[Use actual formatting that users will see]
[Include all key sections of the response]
[Make it clear and easy to understand]

Example:
**[Agent Name] Results**

[Main narrative/summary]

**Details:**
- [Metric 1]: [Value]
- [Metric 2]: [Value]
- [Metric 3]: [Value]

**What this means:**
[Plain English interpretation of results]
[Actionable insights]
```

## Use Cases
Real-world scenarios where this agent is helpful:
1. **[Use Case 1 Title]** - [Description of who needs this and why]
2. **[Use Case 2 Title]** - [Description of who needs this and why]
3. **[Use Case 3 Title]** - [Description of who needs this and why]

## GitHub Repository
Source code and documentation: [Project Name]([GitHub URL])

## Version
- **Version:** [X.Y.Z]
- **Last Updated:** [YYYY-MM-DD]
- **Status:** ✅ [Production Ready/Beta/Alpha]
- **Compatibility:** Agentverse Hosted Platform

## Contact
For issues or questions:
- **GitHub Issues:** [GitHub Issues URL]
- **Agent Developer:** [Team/Individual Name]
- **Agent Address:** `{COPY_FROM_AGENTVERSE_LOGS_AFTER_DEPLOYMENT}`

## Tips for Best Results
- [Tip 1 for users to get better results]
- [Tip 2 for users to get better results]
- [Tip 3 for users to get better results]

---

**Ready to [action verb related to agent purpose]? Ask me [example opening question]!**

---

## For Developers

### Message Models

**Request Format (Direct Agent Communication):**
```python
class [RequestModelName](Model):
    request_id: str
    [field1]: [type] = Field(..., description="...")
    [field2]: [type] = Field(..., description="...")
    requested_by: str
```

**Response Format:**
```python
class [ResponseModelName](Model):
    request_id: str
    result_data: dict
    agent_address: str
    processing_time_ms: int
```

### Integration Example
```python
from uagents import Agent, Context

# Send request to this agent
await ctx.send(
    "[AGENT_ADDRESS]",
    [RequestModelName](
        request_id="unique_id",
        [field1]=[value1],
        [field2]=[value2],
        requested_by=ctx.agent.address
    )
)

# Handle response
@agent.on_message(model=[ResponseModelName])
async def handle_response(ctx: Context, sender: str, msg: [ResponseModelName]):
    result = [ResponseModel].parse_obj(msg.result_data)
    # Process result
```

### Configuration
Environment variables for deployment:
```bash
[AGENT_NAME]_SEED=your_secret_seed_phrase
AI_AGENT_CHOICE=openai  # or 'claude'
[CONFIG_VAR_1]=value
[CONFIG_VAR_2]=value
```
