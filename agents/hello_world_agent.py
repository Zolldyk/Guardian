"""Hello World Agent - Learning uAgents framework basics."""

import logging
from uagents import Agent, Context, Model
from shared.config import HELLO_WORLD_AGENT_SEED, LOG_LEVEL

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)


# Define message models
class HelloRequest(Model):
    """Request message to say hello."""
    name: str


class HelloResponse(Model):
    """Response message from hello agent."""
    message: str


# Create agent instance
agent = Agent(
    name="hello_world_agent",
    seed=HELLO_WORLD_AGENT_SEED,  # Loaded from environment via config.py
    port=8000,
    endpoint=["http://localhost:8000/submit"],
)

logger.info(f"Hello World Agent address: {agent.address}")


# Message handler for HelloRequest
@agent.on_message(model=HelloRequest)
async def handle_hello_request(ctx: Context, sender: str, msg: HelloRequest):
    """
    Handle incoming hello requests.

    Args:
        ctx: Agent context for sending responses
        sender: Address of the message sender
        msg: HelloRequest message containing the name
    """
    logger.info(f"Received HelloRequest from {sender}: name={msg.name}")

    try:
        # Create response
        response = HelloResponse(
            message=f"Hello, {msg.name}! Welcome to the Guardian uAgents framework."
        )

        # Send response back to sender
        await ctx.send(sender, response)
        logger.info(f"Sent HelloResponse to {sender}")

    except Exception as e:
        logger.error(f"Error handling HelloRequest: {e}")


# Startup handler
@agent.on_event("startup")
async def startup(ctx: Context):
    """Execute on agent startup."""
    logger.info("Hello World Agent started successfully!")
    logger.info(f"Agent name: {agent.name}")
    logger.info(f"Agent address: {agent.address}")


# Interval handler - periodic task every 60 seconds
@agent.on_interval(period=60.0)
async def periodic_task(ctx: Context):
    """Execute periodic task every 60 seconds."""
    logger.info("Hello World Agent is running...")


if __name__ == "__main__":
    logger.info("Starting Hello World Agent...")
    agent.run()
