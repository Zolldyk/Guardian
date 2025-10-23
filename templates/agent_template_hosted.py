"""
[AgentName] - Agentverse Hosted Version with ASI1 LLM Integration

[Brief description of what this agent does - 2-3 sentences]

AGENTVERSE DEPLOYMENT TEMPLATE
This template ensures your agent is compatible with Agentverse hosted platform:
✅ Uses only supported libraries (no pandas/numpy unless absolutely necessary)
✅ Integrates chat protocol for ASI1 LLM compatibility
✅ Includes AI-powered parameter extraction
✅ Proper error handling and logging
✅ Session management for multi-turn conversations

Deployment Instructions:
1. Create agent on Agentverse → Agents → Launch an Agent → Blank Agent
2. Copy this entire file into agent.py (replace template placeholders)
3. Add comprehensive README in Overview section (use README template)
4. Set environment variables in Agentverse dashboard
5. Click "Start" to deploy
6. Copy agent address from logs and update .env file

Environment Variables (set in Agentverse dashboard):
- [AGENT_NAME]_SEED (required - your secret seed phrase)
- AI_AGENT_CHOICE=openai  # or 'claude'
- [OTHER_CONFIG_VARS]=value
"""

import os
import time
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, Dict, List

import requests
from pydantic import BaseModel, ConfigDict, Field
from uagents import Agent, Context, Model, Protocol
from uagents_core.models import ErrorMessage

# Import chat protocol components for ASI1 LLM integration
from uagents_core.contrib.protocols.chat import (
    chat_protocol_spec,
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    StartSessionContent,
    EndSessionContent,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

def get_env_var(key: str, default: str = "") -> str:
    """Get environment variable with optional default value."""
    value = os.getenv(key, default)
    if not value and key.endswith("_SEED"):
        print(f"⚠️ {key} not set, using default seed (NOT SECURE for production)")
        return f"{key.lower()}_insecure_default_change_me"
    return value

# Agent configuration
AGENT_SEED = get_env_var("[AGENT_NAME]_SEED")

# AI Agent selection for parameter extraction
AI_AGENT_CHOICE = get_env_var("AI_AGENT_CHOICE", "openai")
OPENAI_AGENT = 'agent1qtlpfshtlcxekgrfcpmv7m9zpajuwu7d5jfyachvpa4u3dkt6k0uwwp2lct'
CLAUDE_AGENT = 'agent1qvk7q2av3e2y5gf5s90nfzkc8a48q3wdqeevwrtgqfdl0k78rspd6f2l4dx'
AI_AGENT_ADDRESS = OPENAI_AGENT if AI_AGENT_CHOICE == "openai" else CLAUDE_AGENT

# Add your configuration variables here
# Example:
# THRESHOLD_VALUE = float(get_env_var("THRESHOLD_VALUE", "85"))
# API_ENDPOINT = get_env_var("API_ENDPOINT", "https://api.example.com")

print(f"✅ Configuration loaded")

# =============================================================================
# DATA MODELS (Pydantic)
# =============================================================================

class YourRequestModel(BaseModel):
    """
    Define your request data model here.
    This should match what you expect from users or other agents.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "field1": "example_value",
                "field2": 123,
            }
        }
    )

    field1: str = Field(
        ...,
        description="Clear description of what this field represents"
    )
    field2: int = Field(
        ...,
        gt=0,
        description="Another field with validation"
    )


class YourResponseModel(BaseModel):
    """
    Define your response data model here.
    This is what your agent returns after processing.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "result": "example_result",
                "confidence": 95,
            }
        }
    )

    result: str = Field(..., description="The main result of your analysis")
    confidence: int = Field(..., ge=0, le=100, description="Confidence score")
    narrative: str = Field(..., description="Plain English explanation")


# =============================================================================
# uAGENTS MESSAGE MODELS
# =============================================================================

class AgentRequest(Model):
    """Request message sent from other agents or via chat protocol."""
    request_id: str
    # Add fields from YourRequestModel with descriptions for AI extraction
    field1: str = Field(
        ...,
        description="Clear description for AI to understand what to extract"
    )
    field2: int = Field(
        ...,
        description="Another field with context for AI"
    )
    requested_by: str


class AgentResponse(Model):
    """Response message with analysis results."""
    request_id: str
    result_data: dict  # YourResponseModel serialized as dict
    agent_address: str
    processing_time_ms: int


class AgentErrorMessage(Model):
    """Error message for failures."""
    request_id: str
    error_type: str  # "invalid_data" | "processing_error" | "timeout" | etc.
    error_message: str
    agent_address: str
    retry_recommended: bool


# AI Parameter Extraction Models
class StructuredOutputPrompt(Model):
    """Prompt sent to AI agent for parameter extraction."""
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    """Response from AI agent with extracted parameters."""
    output: dict[str, Any]


# =============================================================================
# CORE BUSINESS LOGIC FUNCTIONS
# =============================================================================

def process_request(request_data: YourRequestModel) -> YourResponseModel:
    """
    Main business logic function.

    Replace this with your actual processing logic.
    Use only Agentverse-supported libraries:
    - requests (HTTP calls)
    - Python built-ins (json, csv, statistics, math, etc.)
    - Database connectors (MySQLdb, pymongo if needed)
    - AI libraries (openai, langchain, etc. if needed)

    Args:
        request_data: Validated request data

    Returns:
        YourResponseModel with results

    Raises:
        ValueError: If processing cannot be completed
    """

    # Example processing logic (REPLACE WITH YOUR LOGIC)
    print(f"🔍 Processing request: {request_data.field1}")

    # Example: Fetch data from external API
    try:
        response = requests.get(
            f"https://api.example.com/data/{request_data.field1}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise ValueError(f"Failed to fetch data: {e}")

    # Example: Process the data
    result = f"Processed: {data.get('value', 'unknown')}"
    confidence = 95
    narrative = f"Analysis of {request_data.field1} completed successfully with {confidence}% confidence."

    return YourResponseModel(
        result=result,
        confidence=confidence,
        narrative=narrative
    )


# =============================================================================
# AGENT INITIALIZATION
# =============================================================================

# For Agentverse hosted: no port/endpoint
agent = Agent(
    name="[agent_name]_hosted",
    seed=AGENT_SEED,
)

print(f"✅ Agent initialized with address: {agent.address}")

# Create protocols
chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_proto = Protocol(
    name="StructuredOutputClientProtocol",
    version="0.1.0"
)

# =============================================================================
# CHAT PROTOCOL HANDLERS (ASI1 LLM Integration)
# =============================================================================

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle incoming ChatMessage from ASI1 LLM.
    Extracts user query and forwards to AI agent for parameter extraction.
    """
    ctx.logger.info(f"📨 Received ChatMessage from {sender}")

    # Store session sender for response routing
    ctx.storage.set(str(ctx.session), sender)

    # Send acknowledgement
    await ctx.send(
        sender,
        ChatAcknowledgement(
            acknowledged_msg_id=msg.msg_id,
            timestamp=datetime.now(timezone.utc)
        ),
    )

    # Process message content
    for content in msg.content:
        if isinstance(content, StartSessionContent):
            ctx.logger.info(f"🟢 Session started with {sender}")
            continue

        elif isinstance(content, EndSessionContent):
            ctx.logger.info(f"🔴 Session ended with {sender}")
            continue

        elif isinstance(content, TextContent):
            ctx.logger.info(f"💬 User query: {content.text}")

            # Forward to AI agent for structured parameter extraction
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=content.text,
                    output_schema=AgentRequest.schema()
                ),
            )


@chat_proto.on_message(ChatAcknowledgement)
async def handle_chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle chat acknowledgements."""
    ctx.logger.info(f"✅ Message {msg.acknowledged_msg_id} acknowledged by {sender}")


# =============================================================================
# AI PARAMETER EXTRACTION HANDLER
# =============================================================================

@struct_output_proto.on_message(StructuredOutputResponse)
async def handle_structured_output(ctx: Context, sender: str, msg: StructuredOutputResponse):
    """
    Handle AI agent response with extracted parameters.
    Processes request and sends result back to user.
    """
    session_sender = ctx.storage.get(str(ctx.session))

    if session_sender is None:
        ctx.logger.error("❌ No session sender found in storage")
        return

    # Check if AI couldn't extract parameters
    if "<UNKNOWN>" in str(msg.output):
        error_response = ChatMessage(
            content=[TextContent(
                text="Sorry, I couldn't understand your request. Please provide [what you need from user]."
            )],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, error_response)
        return

    start_time = time.time()

    try:
        # Parse extracted parameters
        request = AgentRequest.parse_obj(msg.output)

        ctx.logger.info(f"🔍 Processing request for {request.field1}")

        # Convert to business logic model
        request_data = YourRequestModel(
            field1=request.field1,
            field2=request.field2
        )

        # Process request
        result = process_request(request_data)

        processing_time_ms = int((time.time() - start_time) * 1000)

        ctx.logger.info(f"✅ Processing complete in {processing_time_ms}ms")

        # Format response narrative (customize this for your agent)
        response_text = f"""**[Your Agent Name] Results**

{result.narrative}

**Details:**
- Result: {result.result}
- Confidence: {result.confidence}%

**What this means:**
[Add interpretation and actionable insights here]
"""

        # Send response back to user
        response = ChatMessage(
            content=[TextContent(text=response_text)],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, response)

        ctx.logger.info(f"📤 Sent result to {session_sender}")

    except Exception as err:
        ctx.logger.error(f"❌ Error processing request: {err}")

        processing_time_ms = int((time.time() - start_time) * 1000)

        error_response = ChatMessage(
            content=[TextContent(
                text=f"Sorry, I encountered an error: {str(err)}. Please try again or contact support."
            )],
            msg_id=uuid4(),
            timestamp=datetime.now(timezone.utc)
        )
        await ctx.send(session_sender, error_response)


# =============================================================================
# DIRECT MESSAGE HANDLER (Agent-to-Agent Communication)
# =============================================================================

@agent.on_message(model=AgentRequest)
async def handle_direct_request(ctx: Context, sender: str, msg: AgentRequest):
    """
    Handle direct AgentRequest from other agents.
    Bypasses chat protocol and AI extraction for agent-to-agent communication.
    """
    ctx.logger.info(f"📨 Received direct AgentRequest {msg.request_id} from {sender}")

    start_time = time.time()

    try:
        # Convert to business logic model
        request_data = YourRequestModel(
            field1=msg.field1,
            field2=msg.field2
        )

        # Process request
        result = process_request(request_data)

        processing_time_ms = int((time.time() - start_time) * 1000)

        ctx.logger.info(f"✅ Processing complete in {processing_time_ms}ms")

        # Send response back to sender
        await ctx.send(
            sender,
            AgentResponse(
                request_id=msg.request_id,
                result_data=result.model_dump(),
                agent_address=ctx.agent.address,
                processing_time_ms=processing_time_ms,
            ),
        )

        ctx.logger.info(f"📤 Sent AgentResponse for {msg.request_id}")

    except Exception as e:
        ctx.logger.error(f"❌ Error processing {msg.request_id}: {str(e)}")

        processing_time_ms = int((time.time() - start_time) * 1000)

        await ctx.send(
            sender,
            AgentErrorMessage(
                request_id=msg.request_id,
                error_type="processing_error",
                error_message=f"Request processing failed: {str(e)}",
                agent_address=ctx.agent.address,
                retry_recommended=True,
            ),
        )

        ctx.logger.info(f"📤 Sent ErrorMessage for {msg.request_id}")


# =============================================================================
# STARTUP HANDLER
# =============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    """Log startup information."""
    ctx.logger.info("=" * 70)
    ctx.logger.info("🚀 [AgentName] (Agentverse Hosted) Started Successfully!")
    ctx.logger.info(f"📍 Agent Address: {ctx.agent.address}")
    ctx.logger.info(f"⚙️  Configuration:")
    ctx.logger.info(f"   - AI Agent: {AI_AGENT_CHOICE.upper()}")
    # Add your configuration logging here
    ctx.logger.info(f"💬 ASI1 LLM Integration: ✅ Enabled")
    ctx.logger.info(f"✅ Ready to receive messages (Chat Protocol + Direct)")
    ctx.logger.info("=" * 70)


# =============================================================================
# REGISTER PROTOCOLS
# =============================================================================

agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_proto, publish_manifest=True)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("Starting [AgentName] (Agentverse Hosted Version)...")
    agent.run()
