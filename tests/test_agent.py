"""
Test suite for AgentCore

This file contains automated tests for the AgentCore class, covering user request
processing, tool selection, tool execution, error handling, and logging. All tests use pytest
and should mock external dependencies where appropriate.

All test names, comments, and docstrings must be in English.
"""

import json
import os
import tempfile
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

# Import the modules to test using relative imports
from ..agent.agent_core import AgentConfig, AgentCore, ToolCall, ToolResult


class TestAgentCore:
    """Test class for AgentCore functionality."""

    @pytest.fixture
    def mock_crm_service(self):
        """Create a mock CRM service for testing."""
        mock_service = Mock()

        # Mock successful responses
        mock_service.get_client_by_id.return_value = {
            "id": "test-client-123",
            "name": "John Silva",
            "email": "joao@test.com",
            "balance": 1000.0,
        }

        mock_service.create_client.return_value = {
            "id": "new-client-456",
            "name": "Alice Johnson",
            "email": "alice@email.com",
            "balance": 3000.0,
        }

        mock_service.update_client_balance.return_value = {
            "id": "test-client-123",
            "name": "John Silva",
            "email": "joao@test.com",
            "balance": 2500.0,
        }

        mock_service.list_all_clients.return_value = [
            {"id": "client-1", "name": "Client 1", "email": "client1@test.com"},
            {"id": "client-2", "name": "Client 2", "email": "client2@test.com"},
        ]

        return mock_service

    @pytest.fixture
    def mock_erp_service(self):
        """Create a mock ERP service for testing."""
        mock_service = Mock()

        # Mock successful responses
        mock_service.create_order.return_value = {
            "id": "ORD-20241201-001",
            "client_id": "test-client-123",
            "items": [{"name": "Product", "quantity": 1, "price": 500.0}],
            "total_amount": 500.0,
            "description": "Test order",
            "priority": "medium",
            "status": "pending",
            "created_at": "2024-12-01T10:00:00",
            "updated_at": "2024-12-01T10:00:00",
        }

        mock_service.get_order_by_id.return_value = {
            "id": "ORD-20241201-001",
            "client_id": "test-client-123",
            "items": [{"name": "Product", "quantity": 1, "price": 500.0}],
            "total_amount": 500.0,
            "description": "Test order",
            "priority": "medium",
            "status": "pending",
            "created_at": "2024-12-01T10:00:00",
            "updated_at": "2024-12-01T10:00:00",
        }

        mock_service.update_order_status.return_value = {
            "id": "ORD-20241201-001",
            "client_id": "test-client-123",
            "items": [{"name": "Product", "quantity": 1, "price": 500.0}],
            "total_amount": 500.0,
            "description": "Test order",
            "priority": "medium",
            "status": "shipped",
            "created_at": "2024-12-01T10:00:00",
            "updated_at": "2024-12-01T11:00:00",
        }

        mock_service.list_all_orders.return_value = [
            {
                "id": "ORD-20241201-001",
                "client_id": "client-1",
                "total_amount": 500.0,
                "status": "pending",
            },
            {
                "id": "ORD-20241201-002",
                "client_id": "client-2",
                "total_amount": 750.0,
                "status": "shipped",
            },
        ]

        return mock_service

    @pytest.fixture
    def temp_crm_mcp_schema(self):
        """Create a temporary CRM MCP schema file for testing."""
        schema_data = {
            "tools": [
                {
                    "name": "get_client_by_id",
                    "description": "Retrieve a client by their unique ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "client_id": {
                                "type": "string",
                                "description": "The unique identifier of the client to retrieve",
                            }
                        },
                        "required": ["client_id"],
                    },
                },
                {
                    "name": "create_client",
                    "description": "Create a new client with basic information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "balance": {"type": "number"},
                        },
                        "required": ["id", "name", "email", "balance"],
                    },
                },
                {
                    "name": "update_client_balance",
                    "description": "Update the balance of an existing client.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "client_id": {"type": "string"},
                            "new_balance": {"type": "number"},
                        },
                        "required": ["client_id", "new_balance"],
                    },
                },
                {
                    "name": "list_all_clients",
                    "description": "Return a list of all registered clients.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(schema_data, f)
            temp_file = f.name

        yield temp_file

        # Cleanup
        os.unlink(temp_file)

    @pytest.fixture
    def temp_erp_mcp_schema(self):
        """Create a temporary ERP MCP schema file for testing."""
        schema_data = {
            "tools": [
                {
                    "name": "create_order",
                    "description": "Create a new order in the ERP system.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "client_id": {
                                "type": "string",
                                "description": "ID of the client placing the order.",
                            },
                            "items": {
                                "type": "array",
                                "description": "List of items in the order.",
                            },
                            "total_amount": {
                                "type": "number",
                                "description": "Total cost of the order.",
                            },
                            "description": {
                                "type": "string",
                                "description": "Order description.",
                                "optional": True,
                            },
                            "priority": {
                                "type": "string",
                                "description": "Order priority (low, medium, high).",
                                "optional": True,
                            },
                        },
                        "required": ["client_id", "items", "total_amount"],
                    },
                },
                {
                    "name": "get_order_by_id",
                    "description": "Retrieve order information by order ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "Unique identifier of the order.",
                            }
                        },
                        "required": ["order_id"],
                    },
                },
                {
                    "name": "update_order_status",
                    "description": "Update the status of an existing order.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "Unique identifier of the order.",
                            },
                            "new_status": {
                                "type": "string",
                                "description": "New status for the order (pending, processing, shipped, delivered, cancelled).",
                            },
                        },
                        "required": ["order_id", "new_status"],
                    },
                },
                {
                    "name": "list_all_orders",
                    "description": "List all orders in the ERP system.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(schema_data, f)
            temp_file = f.name

        yield temp_file

        # Cleanup
        os.unlink(temp_file)

    @pytest.fixture
    def temp_mcp_schema(self):
        """Create a temporary MCP schema file for testing."""
        schema_data = {
            "tools": [
                {
                    "name": "get_client_by_id",
                    "description": "Retrieve a client by their unique ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "client_id": {
                                "type": "string",
                                "description": "The unique identifier of the client to retrieve",
                            }
                        },
                        "required": ["client_id"],
                    },
                },
                {
                    "name": "create_client",
                    "description": "Create a new client with basic information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "balance": {"type": "number"},
                        },
                        "required": ["id", "name", "email", "balance"],
                    },
                },
                {
                    "name": "update_client_balance",
                    "description": "Update the balance of an existing client.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "client_id": {"type": "string"},
                            "new_balance": {"type": "number"},
                        },
                        "required": ["client_id", "new_balance"],
                    },
                },
                {
                    "name": "list_all_clients",
                    "description": "Return a list of all registered clients.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(schema_data, f)
            temp_file = f.name

        yield temp_file

        # Cleanup
        os.unlink(temp_file)

    @pytest.fixture
    def agent_core(
        self,
        mock_crm_service,
        mock_erp_service,
        temp_crm_mcp_schema,
        temp_erp_mcp_schema,
    ):
        """Create an AgentCore instance with mocked dependencies."""
        config = AgentConfig()

        with patch("agent.agent_core.CRMService", return_value=mock_crm_service), patch(
            "agent.agent_core.ERPService", return_value=mock_erp_service
        ):
            agent = AgentCore(config)
            agent.load_mcp_schema(temp_crm_mcp_schema)
            agent.load_mcp_schema(temp_erp_mcp_schema)
            return agent

    def test_agent_initialization(self):
        """Test that AgentCore initializes correctly."""
        config = AgentConfig()
        agent = AgentCore(config)

        assert agent is not None
        assert agent.config == config
        assert agent.conversation_history == []
        assert agent.available_tools == {}

    def test_load_mcp_schema_success(self, agent_core, temp_mcp_schema):
        """Test successful loading of MCP schema."""
        agent = AgentCore(AgentConfig())
        result = agent.load_mcp_schema(temp_mcp_schema)

        assert result is True
        assert len(agent.available_tools) == 4
        assert "get_client_by_id" in agent.available_tools
        assert "create_client" in agent.available_tools
        assert "update_client_balance" in agent.available_tools
        assert "list_all_clients" in agent.available_tools

    def test_load_all_mcp_schemas_success(self, agent_core):
        """Test successful loading of all MCP schemas (CRM and ERP)."""
        agent = AgentCore(AgentConfig())

        with patch.object(agent, "load_mcp_schema") as mock_load:
            mock_load.side_effect = [True, True]  # CRM and ERP both succeed
            result = agent.load_all_mcp_schemas()

            assert result is True
            assert mock_load.call_count == 2
            mock_load.assert_any_call("mcp_server/crm_mcp.json")
            mock_load.assert_any_call("mcp_server/erp_mcp.json")

    def test_load_all_mcp_schemas_partial_failure(self, agent_core):
        """Test loading MCP schemas when one fails."""
        agent = AgentCore(AgentConfig())

        with patch.object(agent, "load_mcp_schema") as mock_load:
            mock_load.side_effect = [True, False]  # CRM succeeds, ERP fails
            result = agent.load_all_mcp_schemas()

            assert result is False
            assert mock_load.call_count == 2

    def test_load_mcp_schema_file_not_found(self, agent_core):
        """Test loading MCP schema with non-existent file."""
        agent = AgentCore(AgentConfig())
        result = agent.load_mcp_schema("non_existent_file.json")

        assert result is False

    # CRM Tests
    def test_get_client_by_id_request(self, agent_core, mock_crm_service):
        """Test processing a request to get client by ID."""
        user_input = "Get client joao123"

        response = agent_core.process_user_request(user_input)

        # Verify response structure
        assert response["success"] is True
        assert response["tool_used"] == "get_client_by_id"
        assert response["parameters"] == {"client_id": "joao123"}
        assert "reasoning" in response
        assert "execution_time" in response

        # Verify CRM service was called correctly
        mock_crm_service.get_client_by_id.assert_called_once_with("joao123")

        # Verify result contains expected client data
        assert response["result"]["id"] == "test-client-123"
        assert response["result"]["name"] == "John Silva"

    def test_create_client_request(self, agent_core, mock_crm_service):
        """Test processing a request to create a new client."""
        user_input = "Create client Alice with email alice@email.com and balance 3000"

        response = agent_core.process_user_request(user_input)

        # Verify response structure
        assert response["success"] is True
        assert response["tool_used"] == "create_client"
        assert "reasoning" in response
        assert "execution_time" in response

        # Verify parameters were extracted correctly
        params = response["parameters"]
        assert "id" in params
        assert params["name"] == "Alice"
        assert params["email"] == "alice@email.com"
        assert params["balance"] == 3000.0

        # Verify CRM service was called correctly
        mock_crm_service.create_client.assert_called_once()
        call_args = mock_crm_service.create_client.call_args[0][0]
        assert call_args["name"] == "Alice"
        assert call_args["email"] == "alice@email.com"
        assert call_args["balance"] == 3000.0

    def test_update_client_balance_request(self, agent_core, mock_crm_service):
        """Test processing a request to update client balance."""
        user_input = "Update client balance for joao123 to 2500"

        response = agent_core.process_user_request(user_input)

        # Verify response structure
        assert response["success"] is True
        assert response["tool_used"] == "update_client_balance"
        assert response["parameters"] == {"client_id": "joao123", "new_balance": 2500.0}
        assert "reasoning" in response
        assert "execution_time" in response

        # Verify CRM service was called correctly
        mock_crm_service.update_client_balance.assert_called_once_with(
            "joao123", 2500.0
        )

        # Verify result contains updated balance
        assert response["result"]["balance"] == 2500.0

    def test_list_all_clients_request(self, agent_core, mock_crm_service):
        """Test processing a request to list all clients."""
        user_input = "List all clients"

        response = agent_core.process_user_request(user_input)

        # Verify response structure
        assert response["success"] is True
        assert response["tool_used"] == "list_all_clients"
        assert response["parameters"] == {}
        assert "reasoning" in response
        assert "execution_time" in response

        # Verify CRM service was called correctly
        mock_crm_service.list_all_clients.assert_called_once()

        # Verify result contains list of clients
        assert len(response["result"]) == 2
        assert response["result"][0]["id"] == "client-1"
        assert response["result"][1]["id"] == "client-2"

    # ERP Tests
    def test_create_order_request(self, agent_core, mock_erp_service):
        """Test processing a request to create a new order."""
        user_input = "Create order for client test-client-123 with total amount 500"

        response = agent_core.process_user_request(user_input)

        # Verify response structure
        assert response["success"] is True
        assert response["tool_used"] == "create_order"
        assert "reasoning" in response
        assert "execution_time" in response

        # Verify parameters were extracted correctly
        params = response["parameters"]
        assert params["client_id"] == "test-client-123"
        assert params["total_amount"] == 500.0
        assert "items" in params
        assert "description" in params
        assert "priority" in params

        # Verify ERP service was called correctly
        mock_erp_service.create_order.assert_called_once()
        call_args = mock_erp_service.create_order.call_args[0][0]
        assert call_args["client_id"] == "test-client-123"
        assert call_args["total_amount"] == 500.0

        # Verify result contains expected order data
        assert response["result"]["id"] == "ORD-20241201-001"
        assert response["result"]["client_id"] == "test-client-123"
        assert response["result"]["total_amount"] == 500.0

    def test_get_order_by_id_request(self, agent_core, mock_erp_service):
        """Test processing a request to get order by ID."""
        user_input = "Get order ORD-20241201-001"

        response = agent_core.process_user_request(user_input)

        # Verify response structure
        assert response["success"] is True
        assert response["tool_used"] == "get_order_by_id"
        assert response["parameters"] == {"order_id": "ORD-20241201-001"}
        assert "reasoning" in response
        assert "execution_time" in response

        # Verify ERP service was called correctly
        mock_erp_service.get_order_by_id.assert_called_once_with("ORD-20241201-001")

        # Verify result contains expected order data
        assert response["result"]["id"] == "ORD-20241201-001"
        assert response["result"]["client_id"] == "test-client-123"
        assert response["result"]["status"] == "pending"

    def test_update_order_status_request(self, agent_core, mock_erp_service):
        """Test processing a request to update order status."""
        user_input = "Update order ORD-20241201-001 to shipped"

        response = agent_core.process_user_request(user_input)

        # Verify response structure
        assert response["success"] is True
        assert response["tool_used"] == "update_order_status"
        assert response["parameters"] == {
            "order_id": "ORD-20241201-001",
            "new_status": "shipped",
        }
        assert "reasoning" in response
        assert "execution_time" in response

        # Verify ERP service was called correctly
        mock_erp_service.update_order_status.assert_called_once_with(
            "ORD-20241201-001", "shipped"
        )

        # Verify result contains updated status
        assert response["result"]["status"] == "shipped"

    def test_list_all_orders_request(self, agent_core, mock_erp_service):
        """Test processing a request to list all orders."""
        user_input = "List all orders"

        response = agent_core.process_user_request(user_input)

        # Verify response structure
        assert response["success"] is True
        assert response["tool_used"] == "list_all_orders"
        assert response["parameters"] == {}
        assert "reasoning" in response
        assert "execution_time" in response

        # Verify ERP service was called correctly
        mock_erp_service.list_all_orders.assert_called_once()

        # Verify result contains list of orders
        assert len(response["result"]) == 2
        assert response["result"][0]["id"] == "ORD-20241201-001"
        assert response["result"][1]["id"] == "ORD-20241201-002"

    # Error Handling Tests
    def test_invalid_request_no_tool_found(self, agent_core):
        """Test processing a request that doesn't match any tool."""
        user_input = "Do something completely unrelated"

        response = agent_core.process_user_request(user_input)

        assert response["success"] is False
        assert "No appropriate tool found" in response["error"]
        assert "execution_time" in response

    def test_empty_request(self, agent_core):
        """Test processing an empty request."""
        user_input = ""

        response = agent_core.process_user_request(user_input)

        assert response["success"] is False
        assert "No appropriate tool found" in response["error"]

    # Parameter Extraction Tests
    def test_extract_client_id_uuid_format(self, agent_core):
        """Test extracting client ID in UUID format."""
        user_input = "Get client 123e4567-e89b-12d3-a456-426614174000"
        client_id = agent_core._extract_client_id(user_input)

        assert client_id == "123e4567-e89b-12d3-a456-426614174000"

    def test_extract_client_id_simple_format(self, agent_core):
        """Test extracting client ID in simple format."""
        user_input = "Get client joao123"
        client_id = agent_core._extract_client_id(user_input)

        assert client_id == "joao123"

    def test_extract_client_data_complete(self, agent_core):
        """Test extracting complete client data."""
        user_input = "Create client named Alice Johnson with email alice@email.com"
        client_data = agent_core._extract_client_data(user_input)

        assert client_data is not None
        assert client_data["name"] == "Alice Johnson"
        assert client_data["email"] == "alice@email.com"
        assert "id" in client_data
        assert "balance" in client_data

    def test_extract_client_data_incomplete(self, agent_core):
        """Test extracting incomplete client data."""
        user_input = "Create client named Alice"  # Missing email
        client_data = agent_core._extract_client_data(user_input)

        assert client_data is None

    def test_extract_balance_data(self, agent_core):
        """Test extracting balance update data."""
        user_input = "Update client balance for joao123 to 2500"
        balance_data = agent_core._extract_balance_data(user_input)

        assert balance_data is not None
        assert balance_data["client_id"] == "joao123"
        assert balance_data["new_balance"] == 2500.0

    def test_extract_balance_data_missing_client_id(self, agent_core):
        """Test extracting balance data with missing client ID."""
        user_input = "Update balance to 2500"  # Missing client ID
        balance_data = agent_core._extract_balance_data(user_input)

        assert balance_data is None

    # ERP Parameter Extraction Tests
    def test_extract_order_id_standard_format(self, agent_core):
        """Test extracting order ID in standard format."""
        user_input = "Get order ORD-20241201-001"
        order_id = agent_core._extract_order_id(user_input)

        assert order_id == "ORD-20241201-001"

    def test_extract_order_id_simple_format(self, agent_core):
        """Test extracting order ID in simple format."""
        user_input = "Get order 12345"
        order_id = agent_core._extract_order_id(user_input)

        assert order_id == "12345"

    def test_extract_order_data_complete(self, agent_core):
        """Test extracting complete order data."""
        user_input = "Create order for client test-client-123 with total amount 500 and description Test order"
        order_data = agent_core._extract_order_data(user_input)

        assert order_data is not None
        assert order_data["client_id"] == "test-client-123"
        assert order_data["total_amount"] == 500.0
        assert order_data["description"] == "Test order"
        assert "items" in order_data
        assert "priority" in order_data

    def test_extract_order_data_incomplete(self, agent_core):
        """Test extracting incomplete order data."""
        user_input = "Create order with total amount 500"  # Missing client_id
        order_data = agent_core._extract_order_data(user_input)

        assert order_data is None

    def test_extract_order_status_data(self, agent_core):
        """Test extracting order status update data."""
        user_input = "Update order ORD-20241201-001 to shipped"
        status_data = agent_core._extract_order_status_data(user_input)

        assert status_data is not None
        assert status_data["order_id"] == "ORD-20241201-001"
        assert status_data["new_status"] == "shipped"

    def test_extract_order_status_data_invalid_status(self, agent_core):
        """Test extracting order status data with invalid status."""
        user_input = "Update order ORD-20241201-001 to invalid_status"
        status_data = agent_core._extract_order_status_data(user_input)

        assert status_data is None

    def test_extract_order_status_data_missing_order_id(self, agent_core):
        """Test extracting order status data with missing order ID."""
        user_input = "Update order status to shipped"  # Missing order ID
        status_data = agent_core._extract_order_status_data(user_input)

        assert status_data is None

    # Service Error Handling Tests
    def test_crm_service_error_handling(self, agent_core, mock_crm_service):
        """Test handling of CRM service errors."""
        mock_crm_service.get_client_by_id.side_effect = Exception("CRM service error")

        user_input = "Get client joao123"
        response = agent_core.process_user_request(user_input)

        assert response["success"] is False
        assert "CRM service error" in response["error_message"]
        assert "execution_time" in response

    def test_erp_service_error_handling(self, agent_core, mock_erp_service):
        """Test handling of ERP service errors."""
        mock_erp_service.create_order.side_effect = Exception("ERP service error")

        user_input = "Create order for client test-client-123 with total amount 500"
        response = agent_core.process_user_request(user_input)

        assert response["success"] is False
        assert "ERP service error" in response["error_message"]
        assert "execution_time" in response

    # Malformed Data Tests
    def test_create_order_missing_client_id(self, agent_core):
        """Test creating order with missing client ID."""
        user_input = "Create order with total amount 500"

        response = agent_core.process_user_request(user_input)

        assert response["success"] is False
        assert "No appropriate tool found" in response["error"]

    def test_create_order_missing_amount(self, agent_core):
        """Test creating order with missing amount."""
        user_input = "Create order for client test-client-123"

        response = agent_core.process_user_request(user_input)

        assert response["success"] is False
        assert "No appropriate tool found" in response["error"]

    def test_update_order_status_invalid_status(self, agent_core):
        """Test updating order status with invalid status."""
        user_input = "Update order ORD-20241201-001 to invalid_status"

        response = agent_core.process_user_request(user_input)

        assert response["success"] is False
        assert "No appropriate tool found" in response["error"]

    def test_get_order_invalid_id_format(self, agent_core):
        """Test getting order with invalid ID format."""
        user_input = "Get order invalid-id-format"

        response = agent_core.process_user_request(user_input)

        assert response["success"] is False
        assert "No appropriate tool found" in response["error"]

    # Conversation History Tests
    def test_conversation_history_tracking(self, agent_core):
        """Test that conversation history is properly tracked."""
        user_input = "List all clients"

        # Process request
        agent_core.process_user_request(user_input)

        # Check conversation history
        history = agent_core.get_conversation_history()
        assert len(history) == 1
        assert history[0]["type"] == "user_input"
        assert history[0]["content"] == user_input
        assert "timestamp" in history[0]

    def test_clear_conversation_history(self, agent_core):
        """Test clearing conversation history."""
        user_input = "List all clients"
        agent_core.process_user_request(user_input)

        # Verify history exists
        assert len(agent_core.get_conversation_history()) == 1

        # Clear history
        agent_core.clear_conversation_history()

        # Verify history is cleared
        assert len(agent_core.get_conversation_history()) == 0

    # Utility Class Tests
    def test_tool_call_creation(self):
        """Test ToolCall object creation."""
        tool_call = ToolCall(
            tool_name="test_tool",
            parameters={"param1": "value1"},
            reasoning="Test reasoning",
        )

        assert tool_call.tool_name == "test_tool"
        assert tool_call.parameters == {"param1": "value1"}
        assert tool_call.reasoning == "Test reasoning"

    def test_tool_result_creation(self):
        """Test ToolResult object creation."""
        tool_result = ToolResult(
            success=True, result={"data": "test"}, execution_time=1.5
        )

        assert tool_result.success is True
        assert tool_result.result == {"data": "test"}
        assert tool_result.execution_time == 1.5
        assert tool_result.error_message is None

    def test_tool_result_with_error(self):
        """Test ToolResult object creation with error."""
        tool_result = ToolResult(
            success=False, result=None, error_message="Test error", execution_time=0.5
        )

        assert tool_result.success is False
        assert tool_result.result is None
        assert tool_result.error_message == "Test error"
        assert tool_result.execution_time == 0.5

    def test_agent_config_creation(self):
        """Test AgentConfig object creation."""
        config = AgentConfig(
            llm_provider="test_provider",
            llm_model="test_model",
            max_retries=5,
            timeout=60,
            log_level="DEBUG",
        )

        assert config.llm_provider == "test_provider"
        assert config.llm_model == "test_model"
        assert config.max_retries == 5
        assert config.timeout == 60
        assert config.log_level == "DEBUG"

    # Logging Tests
    @patch("builtins.open", side_effect=Exception("File error"))
    def test_logging_setup_error_handling(self, mock_open):
        """Test handling of logging setup errors."""
        config = AgentConfig()

        # Should not raise exception, should handle gracefully
        agent = AgentCore(config)
        assert agent is not None


if __name__ == "__main__":
    pytest.main([__file__])
