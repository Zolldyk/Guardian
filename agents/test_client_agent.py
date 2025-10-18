"""Test Client Agent - Sends messages to Hello World Agent."""

import logging
from uagents import Agent, Context, Model
from shared.config import TEST_CLIENT_AGENT_SEED, HELLO_WORLD_AGENT_ADDRESS, LOG_LEVEL

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)


# Define message models (must match hello_world_agent)
class HelloRequest(Model):
    """Request message to say hello."""
    name: str


class HelloResponse(Model):
    """Response message from hello agent."""
    message: str


# Create test client agent
agent = Agent(
    name="test_client_agent",
    seed=TEST_CLIENT_AGENT_SEED,  # Loaded from environment via config.py
    port=8001,
    endpoint=["http://localhost:8001/submit"],
)

logger.info(f"Test Client Agent address: {agent.address}")


# Response handler
@agent.on_message(model=HelloResponse)
async def handle_hello_response(ctx: Context, sender: str, msg: HelloResponse):
    """
    Handle HelloResponse from hello world agent.

    Args:
        ctx: Agent context
        sender: Address of the message sender
        msg: HelloResponse message
    """
    logger.info(f"Received HelloResponse from {sender}: {msg.message}")


# Startup handler - send initial message
@agent.on_event("startup")
async def startup(ctx: Context):
    """Send test message on startup."""
    logger.info("Test Client Agent started!")
    logger.info(f"Agent name: {agent.name}")
    logger.info(f"Agent address: {agent.address}")

    # Note: To enable inter-agent communication:
    # 1. Verify HELLO_WORLD_AGENT_ADDRESS in .env or config.py matches running agent
    # 2. Uncomment the send_test_message interval handler below
    logger.info("To test inter-agent communication:")
    logger.info("1. Run hello_world_agent.py and verify its address")
    logger.info(f"2. Confirm HELLO_WORLD_AGENT_ADDRESS={HELLO_WORLD_AGENT_ADDRESS}")
    logger.info("3. Uncomment the send_test_message interval handler in this file")


# Interval handler to send test messages (commented out by default)
# Uncomment after verifying HELLO_WORLD_AGENT_ADDRESS matches running hello_world_agent
# @agent.on_interval(period=30.0)
# async def send_test_message(ctx: Context):
#     """Send test message to hello world agent every 30 seconds."""
#     logger.info(f"Sending HelloRequest to {HELLO_WORLD_AGENT_ADDRESS}...")
#
#     request = HelloRequest(name="Test Client")
#     await ctx.send(HELLO_WORLD_AGENT_ADDRESS, request)
#     logger.info("HelloRequest sent!")


if __name__ == "__main__":
    logger.info("Starting Test Client Agent...")
    agent.run()
