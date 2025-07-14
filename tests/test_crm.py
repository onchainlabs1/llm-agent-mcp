"""
Test suite for CRMService

This file contains automated tests for the CRMService class, covering client creation,
retrieval, update, deletion, listing, searching, and statistics. All tests use pytest
and should mock file I/O where appropriate.

All test names, comments, and docstrings must be in English.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest

# Import CRM service using package imports
try:
    # Try relative imports (when used as a package)
    from ..services.crm_service import CRMService
except ImportError:
    try:
        # Try absolute package imports (recommended: pip install -e .)
        from agentmcp.services.crm_service import CRMService
    except ImportError:
        # Final fallback for development (avoid sys.path when possible)
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))
        from services.crm_service import CRMService


class TestCRMService:
    """Test class for CRMService functionality."""

    @pytest.fixture
    def temp_data_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump({"clients": []}, f)
            temp_file_path = f.name
        yield temp_file_path
        # Cleanup
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

    @pytest.fixture
    def crm_service(self, temp_data_file):
        """Create a CRMService instance with temporary data file."""
        return CRMService(data_file=temp_data_file)

    @pytest.fixture
    def sample_client_data(self):
        """Sample client data for testing."""
        return {
            "clients": [
                {
                    "id": "client-001",
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1-555-0001",
                    "address": "123 Main St, City, State",
                    "status": "active",
                    "balance": 5000.0,
                    "created_at": "2024-01-01T00:00:00",
                },
                {
                    "id": "client-002",
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "phone": "+1-555-0002",
                    "address": "456 Oak Ave, City, State",
                    "status": "active",
                    "balance": 3000.0,
                    "created_at": "2024-01-02T00:00:00",
                },
                {
                    "id": "client-003",
                    "name": "Bob Wilson",
                    "email": "bob@example.com",
                    "phone": "+1-555-0003",
                    "address": "789 Pine Rd, City, State",
                    "status": "prospect",
                    "balance": 0.0,
                    "created_at": "2024-01-03T00:00:00",
                },
            ]
        }

    def test_crm_service_initialization(self, temp_data_file):
        """Test CRMService initialization."""
        service = CRMService(data_file=temp_data_file)
        assert service.data_file == temp_data_file
        assert service.logger is not None

    def test_get_client_by_id_success(self, crm_service, sample_client_data):
        """Test successful client retrieval by ID."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            client = crm_service.get_client_by_id("client-001")

            assert client is not None
            assert client["id"] == "client-001"
            assert client["name"] == "John Doe"
            assert client["email"] == "john@example.com"

    def test_get_client_by_id_not_found(self, crm_service, sample_client_data):
        """Test client retrieval with non-existent ID."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            with pytest.raises(
                KeyError, match="Client with ID 'nonexistent' not found"
            ):
                crm_service.get_client_by_id("nonexistent")

    def test_get_client_by_id_empty_id(self, crm_service):
        """Test client retrieval with empty ID."""
        with pytest.raises(ValueError, match="Client ID cannot be empty or None"):
            crm_service.get_client_by_id("")

    def test_get_client_by_id_none_id(self, crm_service):
        """Test client retrieval with None ID."""
        with pytest.raises(ValueError, match="Client ID cannot be empty or None"):
            crm_service.get_client_by_id(None)

    def test_create_client_success(self, crm_service, sample_client_data):
        """Test successful client creation."""
        new_client = {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "phone": "+1-555-0004",
            "address": "321 Elm St, City, State",
            "status": "active",
            "balance": 2500.0,
        }

        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ) as mock_file:
            with patch("json.dump") as mock_json_dump:
                result = crm_service.create_client(new_client)

                assert result is not None
                assert "id" in result
                assert result["name"] == "Alice Johnson"
                assert result["email"] == "alice@example.com"
                assert "created_at" in result

                # Verify file was written
                mock_json_dump.assert_called_once()

    def test_create_client_missing_name(self, crm_service):
        """Test client creation with missing name."""
        client_data = {"email": "test@example.com"}

        with pytest.raises(ValueError, match="Client name is required"):
            crm_service.create_client(client_data)

    def test_create_client_missing_email(self, crm_service):
        """Test client creation with missing email."""
        client_data = {"name": "Test User"}

        with pytest.raises(ValueError, match="Client email is required"):
            crm_service.create_client(client_data)

    def test_create_client_duplicate_email(self, crm_service, sample_client_data):
        """Test client creation with duplicate email."""
        duplicate_client = {
            "name": "Duplicate User",
            "email": "john@example.com",  # Already exists in sample data
        }

        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            with pytest.raises(
                ValueError, match="Client with email 'john@example.com' already exists"
            ):
                crm_service.create_client(duplicate_client)

    def test_update_client_balance_success(self, crm_service, sample_client_data):
        """Test successful client balance update."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ) as mock_file:
            with patch("json.dump") as mock_json_dump:
                result = crm_service.update_client_balance("client-001", 7500.0)

                assert result is not None
                assert result["id"] == "client-001"
                assert result["balance"] == 7500.0

                # Verify file was written
                mock_json_dump.assert_called_once()

    def test_update_client_balance_invalid_id(self, crm_service):
        """Test balance update with invalid client ID."""
        with pytest.raises(ValueError, match="Client ID cannot be empty or None"):
            crm_service.update_client_balance("", 1000.0)

    def test_update_client_balance_invalid_amount(self, crm_service):
        """Test balance update with invalid balance amount."""
        with pytest.raises(ValueError, match="New balance must be a number"):
            crm_service.update_client_balance("client-001", "invalid")

    def test_list_all_clients_success(self, crm_service, sample_client_data):
        """Test successful listing of all clients."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.list_all_clients()

            assert len(clients) == 3
            assert clients[0]["name"] == "John Doe"
            assert clients[1]["name"] == "Jane Smith"
            assert clients[2]["name"] == "Bob Wilson"

    def test_list_all_clients_empty(self, crm_service):
        """Test listing clients when database is empty."""
        empty_data = {"clients": []}
        with patch("builtins.open", mock_open(read_data=json.dumps(empty_data))):
            clients = crm_service.list_all_clients()
            assert clients == []

    def test_filter_clients_by_balance_min_only(self, crm_service, sample_client_data):
        """Test filtering clients by minimum balance."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.filter_clients_by_balance(min_balance=3000.0)

            assert len(clients) == 2
            assert all(client["balance"] >= 3000.0 for client in clients)
            client_names = [client["name"] for client in clients]
            assert "John Doe" in client_names
            assert "Jane Smith" in client_names

    def test_filter_clients_by_balance_max_only(self, crm_service, sample_client_data):
        """Test filtering clients by maximum balance."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.filter_clients_by_balance(max_balance=3000.0)

            assert len(clients) == 2
            assert all(client["balance"] <= 3000.0 for client in clients)
            client_names = [client["name"] for client in clients]
            assert "Jane Smith" in client_names
            assert "Bob Wilson" in client_names

    def test_filter_clients_by_balance_range(self, crm_service, sample_client_data):
        """Test filtering clients by balance range."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.filter_clients_by_balance(
                min_balance=1000.0, max_balance=4000.0
            )

            assert len(clients) == 1
            assert clients[0]["name"] == "Jane Smith"
            assert 1000.0 <= clients[0]["balance"] <= 4000.0

    def test_filter_clients_by_balance_no_params(self, crm_service, sample_client_data):
        """Test filtering clients without any balance parameters."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.filter_clients_by_balance()

            # Should return all clients when no filters applied
            assert len(clients) == 3

    def test_update_client_success(self, crm_service, sample_client_data):
        """Test successful client update."""
        update_data = {"name": "John Updated", "phone": "+1-555-9999"}

        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ) as mock_file:
            with patch("json.dump") as mock_json_dump:
                result = crm_service.update_client("client-001", update_data)

                assert result is not None
                assert result["id"] == "client-001"
                assert result["name"] == "John Updated"
                assert result["phone"] == "+1-555-9999"
                assert (
                    result["email"] == "john@example.com"
                )  # Should preserve existing data

                # Verify file was written
                mock_json_dump.assert_called_once()

    def test_update_client_invalid_id(self, crm_service):
        """Test client update with invalid ID."""
        with pytest.raises(ValueError, match="Client ID cannot be empty or None"):
            crm_service.update_client("", {"name": "Test"})

    def test_update_client_empty_data(self, crm_service):
        """Test client update with empty update data."""
        with pytest.raises(ValueError, match="Update data cannot be empty"):
            crm_service.update_client("client-001", {})

    def test_delete_client_success(self, crm_service, sample_client_data):
        """Test successful client deletion."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ) as mock_file:
            with patch("json.dump") as mock_json_dump:
                result = crm_service.delete_client("client-001")

                assert result is True
                # Verify file was written
                mock_json_dump.assert_called_once()

    def test_delete_client_not_found(self, crm_service, sample_client_data):
        """Test client deletion with non-existent ID."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            result = crm_service.delete_client("nonexistent")
            assert result is False

    def test_search_clients_by_name(self, crm_service, sample_client_data):
        """Test client search by name."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.search_clients(query="John")

            assert len(clients) == 1
            assert clients[0]["name"] == "John Doe"

    def test_search_clients_by_email(self, crm_service, sample_client_data):
        """Test client search by email."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.search_clients(query="jane@example.com")

            assert len(clients) == 1
            assert clients[0]["name"] == "Jane Smith"

    def test_search_clients_case_insensitive(self, crm_service, sample_client_data):
        """Test client search is case insensitive."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.search_clients(query="JOHN")

            assert len(clients) == 1
            assert clients[0]["name"] == "John Doe"

    def test_search_clients_no_results(self, crm_service, sample_client_data):
        """Test client search with no matching results."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            clients = crm_service.search_clients(query="nonexistent")
            assert clients == []

    def test_get_crm_statistics(self, crm_service, sample_client_data):
        """Test CRM statistics generation."""
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            stats = crm_service.get_crm_statistics()

            assert stats["total_clients"] == 3
            assert stats["active_clients"] == 2
            assert stats["prospect_clients"] == 1
            assert stats["total_balance"] == 8000.0
            assert stats["average_balance"] == 8000.0 / 3

    def test_file_not_found_error(self, crm_service):
        """Test handling of file not found error."""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            with pytest.raises(FileNotFoundError, match="Data file not found"):
                crm_service.get_client_by_id("client-001")

    def test_json_decode_error(self, crm_service):
        """Test handling of JSON decode error."""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with pytest.raises(json.JSONDecodeError):
                crm_service.get_client_by_id("client-001")

    def test_io_error_on_save(self, crm_service, sample_client_data):
        """Test handling of IO error during save."""
        new_client = {"name": "Test", "email": "test@example.com"}

        with patch(
            "builtins.open", mock_open(read_data=json.dumps(sample_client_data))
        ):
            with patch("json.dump", side_effect=IOError("Permission denied")):
                with pytest.raises(IOError, match="Error saving data to file"):
                    crm_service.create_client(new_client)

    @patch("services.crm_service.logging")
    def test_logging_on_error(self, mock_logging, crm_service):
        """Test that errors are properly logged."""
        with patch("builtins.open", side_effect=Exception("Test error")):
            try:
                crm_service.get_client_by_id("client-001")
            except:
                pass

            # Verify logger.error was called
            assert mock_logging.getLogger.return_value.error.called
