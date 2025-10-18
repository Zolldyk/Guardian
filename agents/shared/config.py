"""Shared configuration for Guardian agents.

This module provides centralized environment variable loading
to comply with project coding standards.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_var(key: str, default: str = "") -> str:
    """
    Get environment variable with optional default value.

    Args:
        key: Environment variable name
        default: Default value if variable not found

    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)


# Agent Seeds (for deterministic address generation)
HELLO_WORLD_AGENT_SEED = get_env_var("HELLO_WORLD_AGENT_SEED", "hello_world_seed_phrase_12345")
TEST_CLIENT_AGENT_SEED = get_env_var("TEST_CLIENT_AGENT_SEED", "test_client_seed_phrase_67890")

# Agent Addresses (populated after deployment)
HELLO_WORLD_AGENT_ADDRESS = get_env_var(
    "HELLO_WORLD_AGENT_ADDRESS",
    "agent1qdv6858m9mfa3tlf2erjcz7tt7v224hrmyendyaw0r6369k3xj8lkjnrzym"  # Default from seed
)
CORRELATION_AGENT_ADDRESS = get_env_var("CORRELATION_AGENT_ADDRESS")
SECTOR_AGENT_ADDRESS = get_env_var("SECTOR_AGENT_ADDRESS")
GUARDIAN_AGENT_ADDRESS = get_env_var("GUARDIAN_AGENT_ADDRESS")

# Logging Configuration
LOG_LEVEL = get_env_var("LOG_LEVEL", "INFO")

# Correlation Analysis Configuration
# Convert percentages (0-100) to decimals (0.0-1.0) for internal calculations
HIGH_CORRELATION_THRESHOLD = float(get_env_var("HIGH_CORRELATION_THRESHOLD", "85")) / 100
MODERATE_CORRELATION_THRESHOLD = float(get_env_var("MODERATE_CORRELATION_THRESHOLD", "70")) / 100
MIN_REQUIRED_DATA_DAYS = int(get_env_var("MIN_REQUIRED_DATA_DAYS", "60"))
MAX_EXCLUDED_VALUE_RATIO = float(get_env_var("MAX_EXCLUDED_VALUE_RATIO", "50")) / 100
