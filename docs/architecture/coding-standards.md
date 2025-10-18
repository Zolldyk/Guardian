# Coding Standards

## Critical Fullstack Rules

These are **project-specific rules** that prevent common mistakes. All AI development agents must follow these standards.

- **Message Model Imports:** Always import message models from `agents/shared/models.py`. Never define message models locally in agent files—this causes serialization mismatches.

- **Agent Address Configuration:** Never hardcode agent addresses. Always load from environment variables via `os.getenv("AGENT_ADDRESS")` or `agents/shared/config.py`.

- **Error Handling:** All message handlers must wrap logic in try/except blocks and send `ErrorMessage` on failure. Never let exceptions crash agents silently.

- **MeTTa Fallback:** All MeTTa queries must implement JSON fallback. If `query_metta()` raises an exception, fall back to `data/historical_crashes.json` or `data/sector_mappings.json`.

- **Portfolio Validation:** Always validate portfolio data with Pydantic before processing. Invalid data should return `ErrorMessage`, not crash the agent.

- **Logging Requirements:** All inter-agent messages must be logged at INFO level with request_id for tracing. Format: `logger.info(f"Received AnalysisRequest {request_id} from {sender}")`

- **Timeout Handling:** All `ctx.wait_for_message()` calls must specify timeout parameter. Default: 10 seconds. Never wait indefinitely.

- **Testing Requirement:** Every new agent message handler must have at least one integration test in `tests/test_integration.py` before deployment.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Agent Files | snake_case | `correlation_agent.py` |
| Agent Names | snake_case | `correlation_agent` |
| Message Models | PascalCase | `AnalysisRequest` |
| Message Handlers | snake_case with `handle_` prefix | `handle_analysis_request` |
| Data Files | kebab-case | `demo-wallets.json` |
| Environment Variables | SCREAMING_SNAKE_CASE | `CORRELATION_AGENT_ADDRESS` |

---
