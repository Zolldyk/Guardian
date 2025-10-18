"""Unit tests for Hello World Agent."""

import pytest
from unittest.mock import Mock, AsyncMock
import sys
import os

# Add agents directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))

from hello_world_agent import agent, HelloRequest, HelloResponse, handle_hello_request


class TestHelloWorldAgent:
    """Test suite for Hello World Agent."""

    def test_agent_initialization(self):
        """Test that agent initializes with correct properties."""
        assert agent.name == "hello_world_agent"
        assert agent.address is not None
        assert agent.address.startswith("agent1")

    def test_agent_address_deterministic(self):
        """Test that agent address is deterministic based on seed."""
        # The seed "hello_world_seed_phrase_12345" should always produce same address
        expected_address = "agent1qdv6858m9mfa3tlf2erjcz7tt7v224hrmyendyaw0r6369k3xj8lkjnrzym"
        assert agent.address == expected_address

    def test_hello_request_model(self):
        """Test HelloRequest message model."""
        request = HelloRequest(name="Alice")
        assert request.name == "Alice"

    def test_hello_response_model(self):
        """Test HelloResponse message model."""
        response = HelloResponse(message="Hello, Alice!")
        assert response.message == "Hello, Alice!"

    @pytest.mark.asyncio
    async def test_handle_hello_request(self):
        """Test hello request handler logic."""
        # Create mock context
        mock_ctx = Mock()
        mock_ctx.send = AsyncMock()

        # Create test message
        sender = "agent1qtest123"
        msg = HelloRequest(name="TestUser")

        # Call handler
        await handle_hello_request(mock_ctx, sender, msg)

        # Verify send was called
        mock_ctx.send.assert_called_once()

        # Verify response content
        call_args = mock_ctx.send.call_args
        assert call_args[0][0] == sender  # First arg is sender address
        response = call_args[0][1]  # Second arg is response message
        assert isinstance(response, HelloResponse)
        assert "TestUser" in response.message
        assert "Guardian" in response.message

    @pytest.mark.asyncio
    async def test_handle_hello_request_with_different_names(self):
        """Test handler with various input names."""
        test_names = ["Alice", "Bob", "Charlie", "Test Agent"]

        for name in test_names:
            mock_ctx = Mock()
            mock_ctx.send = AsyncMock()
            sender = "agent1qtest123"
            msg = HelloRequest(name=name)

            await handle_hello_request(mock_ctx, sender, msg)

            # Verify response includes the name
            call_args = mock_ctx.send.call_args
            response = call_args[0][1]
            assert name in response.message

    @pytest.mark.asyncio
    async def test_handle_hello_request_error_handling(self):
        """Test that handler handles errors gracefully."""
        # Create mock context that raises an error on send
        mock_ctx = Mock()
        mock_ctx.send = AsyncMock(side_effect=Exception("Network error"))

        sender = "agent1qtest123"
        msg = HelloRequest(name="TestUser")

        # Handler should not raise exception (catches internally)
        await handle_hello_request(mock_ctx, sender, msg)

    def test_message_model_validation(self):
        """Test Pydantic validation on message models."""
        # Valid request
        valid_request = HelloRequest(name="Alice")
        assert valid_request.name == "Alice"

        # Test that empty string is allowed (Pydantic default)
        empty_request = HelloRequest(name="")
        assert empty_request.name == ""

    def test_agent_has_required_handlers(self):
        """Test that agent has registered required message handlers."""
        # Get agent's message handlers
        handlers = agent._protocol._models

        # Verify HelloRequest handler is registered (check by class)
        handler_classes = [h for h in handlers.values()]
        assert HelloRequest in handler_classes


class TestAgentConfiguration:
    """Test agent configuration and setup."""

    def test_agent_port(self):
        """Test agent is configured with correct port."""
        assert agent._port == 8000

    def test_agent_endpoint(self):
        """Test agent endpoint configuration."""
        assert agent._endpoints is not None
        assert len(agent._endpoints) > 0
        # Check endpoint URL in AgentEndpoint objects
        endpoint_urls = [ep.url for ep in agent._endpoints]
        assert "http://localhost:8000/submit" in endpoint_urls


class TestMessageModels:
    """Test message model structure and validation."""

    def test_hello_request_schema(self):
        """Test HelloRequest model schema."""
        request = HelloRequest(name="test")
        # Use model_dump to verify structure instead of schema
        data = request.model_dump()

        assert "name" in data
        assert data["name"] == "test"

    def test_hello_response_schema(self):
        """Test HelloResponse model schema."""
        response = HelloResponse(message="test message")
        # Use model_dump to verify structure instead of schema
        data = response.model_dump()

        assert "message" in data
        assert data["message"] == "test message"

    def test_message_serialization(self):
        """Test message models can be serialized to JSON."""
        request = HelloRequest(name="Alice")
        request_json = request.model_dump_json()
        assert "Alice" in request_json

        response = HelloResponse(message="Hello, Alice!")
        response_json = response.model_dump_json()
        assert "Hello, Alice!" in response_json
