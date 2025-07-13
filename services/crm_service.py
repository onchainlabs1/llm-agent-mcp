"""
AgentMCP CRM Service Module

This module provides Customer Relationship Management (CRM) functionality
including client management, contact information, and customer interactions.
The service simulates a real CRM system with JSON-based data persistence.

Key features:
- Client creation, retrieval, and updates
- Contact information management
- Customer interaction tracking
- Search and filtering capabilities
- Data validation and integrity checks
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import uuid4

from pydantic import BaseModel, Field, EmailStr


class Client(BaseModel):
    """Model representing a CRM client."""
    
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique client identifier")
    name: str = Field(description="Client full name")
    email: str = Field(description="Client email address")
    phone: Optional[str] = Field(default=None, description="Client phone number")
    company: Optional[str] = Field(default=None, description="Company name")
    industry: Optional[str] = Field(default=None, description="Industry sector")
    status: str = Field(default="active", description="Client status (active, inactive, prospect)")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    notes: Optional[str] = Field(default=None, description="Additional notes")


class CRMService:
    """
    CRM service for managing customer relationships.
    
    This service provides comprehensive client management capabilities
    with JSON-based data persistence and full CRUD operations.
    """
    
    def __init__(self, data_file: str = "data/clients.json"):
        """
        Initialize the CRM service.
        
        Args:
            data_file: Path to the JSON data file
        """
        self.data_file = data_file
        self.logger = logging.getLogger("agentmcp.crm_service")
        self._ensure_data_file()
    
    def _ensure_data_file(self) -> None:
        """Ensure the data file exists with proper structure."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Check if file exists and has valid structure
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    if "clients" not in data:
                        data = {"clients": []}
                        with open(self.data_file, 'w') as f:
                            json.dump(data, f, indent=2, default=str)
            else:
                # Create new file with proper structure
                data = {"clients": []}
                with open(self.data_file, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                self.logger.info(f"Created new CRM data file: {self.data_file}")
                
        except Exception as e:
            self.logger.error(f"Error ensuring data file exists: {str(e)}")
            raise
    
    def _load_data(self) -> Dict[str, Any]:
        """
        Load data from the JSON file.
        
        Returns:
            Dictionary containing the loaded data
            
        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
        """
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {self.data_file}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in data file: {str(e)}", e.doc, e.pos)
    
    def _save_data(self, data: Dict[str, Any]) -> None:
        """
        Save data to the JSON file.
        
        Args:
            data: Dictionary containing the data to save
            
        Raises:
            IOError: If there's an error writing to the file
        """
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except IOError as e:
            raise IOError(f"Error saving data to file: {str(e)}")
    
    def get_client_by_id(self, client_id: str) -> Dict[str, Any]:
        """
        Retrieve a client by their unique ID.
        
        Args:
            client_id: The unique identifier of the client
            
        Returns:
            Dictionary containing the client data
            
        Raises:
            ValueError: If client_id is empty or None
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
            KeyError: If the client is not found
        """
        if not client_id:
            raise ValueError("Client ID cannot be empty or None")
        
        try:
            data = self._load_data()
            
            for client in data["clients"]:
                if client["id"] == client_id:
                    self.logger.info(f"Retrieved client: {client_id}")
                    return client
            
            raise KeyError(f"Client with ID '{client_id}' not found")
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
        except KeyError:
            self.logger.warning(f"Client not found: {client_id}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error retrieving client {client_id}: {str(e)}")
            raise
    
    def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new client in the CRM system.
        
        Args:
            client_data: Dictionary containing client information with the following keys:
                - name: Client's full name (required)
                - email: Client's email address (required)
                - phone: Client's phone number (optional)
                - company: Company name (optional)
                - industry: Industry sector (optional)
                - status: Client status - 'active', 'inactive', or 'prospect' (optional, default: 'active')
                - notes: Additional notes about the client (optional)
                - balance: Client's account balance (optional, default: 0.0)
            
        Returns:
            Dictionary containing the created client data with generated ID and timestamps
            
        Raises:
            ValueError: If required fields are missing or invalid
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
            IOError: If there's an error saving the data
        """
        # Validate required fields
        if not client_data.get("name"):
            raise ValueError("Client name is required")
        if not client_data.get("email"):
            raise ValueError("Client email is required")
        
        try:
            # Generate unique ID and timestamps
            new_client = {
                "id": str(uuid4()),
                "name": client_data["name"],
                "email": client_data["email"],
                "phone": client_data.get("phone"),
                "company": client_data.get("company"),
                "industry": client_data.get("industry"),
                "status": client_data.get("status", "active"),
                "balance": client_data.get("balance", 0.0),
                "notes": client_data.get("notes"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Load existing data
            data = self._load_data()
            
            # Check if email already exists
            for client in data["clients"]:
                if client["email"] == new_client["email"]:
                    raise ValueError(f"Client with email '{new_client['email']}' already exists")
            
            # Add new client
            data["clients"].append(new_client)
            
            # Save updated data
            self._save_data(data)
            
            self.logger.info(f"Created client: {new_client['name']} (ID: {new_client['id']})")
            return new_client
            
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error creating client: {str(e)}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error creating client: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error creating client: {str(e)}")
            raise
    
    def update_client_balance(self, client_id: str, new_balance: float) -> Dict[str, Any]:
        """
        Update the balance for a specific client.
        
        Args:
            client_id: The unique identifier of the client
            new_balance: The new balance amount
            
        Returns:
            Dictionary containing the updated client data
            
        Raises:
            ValueError: If client_id is empty or new_balance is invalid
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
            KeyError: If the client is not found
            IOError: If there's an error saving the data
        """
        if not client_id:
            raise ValueError("Client ID cannot be empty or None")
        
        if not isinstance(new_balance, (int, float)):
            raise ValueError("New balance must be a number")
        
        try:
            # Load existing data
            data = self._load_data()
            
            # Find and update client
            for client in data["clients"]:
                if client["id"] == client_id:
                    old_balance = client.get("balance", 0.0)
                    client["balance"] = float(new_balance)
                    client["updated_at"] = datetime.now().isoformat()
                    
                    # Save updated data
                    self._save_data(data)
                    
                    self.logger.info(f"Updated client {client_id} balance: {old_balance} -> {new_balance}")
                    return client
            
            raise KeyError(f"Client with ID '{client_id}' not found")
            
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error updating client balance: {str(e)}")
            raise
        except KeyError:
            self.logger.warning(f"Client not found for balance update: {client_id}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error updating client balance: {str(e)}")
            raise
    
    def list_all_clients(self) -> List[Dict[str, Any]]:
        """
        Retrieve all clients from the CRM system.
        
        Returns:
            List of dictionaries containing client data
            
        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
        """
        try:
            data = self._load_data()
            clients = data.get("clients", [])
            
            self.logger.info(f"Retrieved {len(clients)} clients")
            return clients
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading clients: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error listing clients: {str(e)}")
            raise
    
    def filter_clients_by_balance(self, min_balance: float = None, max_balance: float = None) -> List[Dict[str, Any]]:
        """
        Filter clients by their account balance.
        
        Args:
            min_balance: Minimum balance threshold (optional)
            max_balance: Maximum balance threshold (optional)
            
        Returns:
            List of clients matching the balance criteria
            
        Raises:
            ValueError: If balance parameters are invalid
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
        """
        try:
            data = self._load_data()
            clients = data.get("clients", [])
            filtered_clients = []
            
            for client in clients:
                balance = client.get("balance", 0.0)
                
                # Convert balance to float if it's a string
                if isinstance(balance, str):
                    try:
                        balance = float(balance)
                    except ValueError:
                        balance = 0.0
                
                # Apply filters
                if min_balance is not None and balance < min_balance:
                    continue
                if max_balance is not None and balance > max_balance:
                    continue
                    
                filtered_clients.append(client)
            
            self.logger.info(f"Filtered {len(filtered_clients)} clients by balance criteria")
            return filtered_clients
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error filtering clients by balance: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error filtering clients by balance: {str(e)}")
            raise
    
    def update_client(self, client_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing client's information.
        
        Args:
            client_id: The unique identifier of the client
            update_data: Dictionary containing fields to update
            
        Returns:
            Dictionary containing the updated client data
            
        Raises:
            ValueError: If client_id is empty or update_data is invalid
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
            KeyError: If the client is not found
            IOError: If there's an error saving the data
        """
        if not client_id:
            raise ValueError("Client ID cannot be empty or None")
        
        if not update_data:
            raise ValueError("Update data cannot be empty")
        
        try:
            # Load existing data
            data = self._load_data()
            
            # Find and update client
            for client in data["clients"]:
                if client["id"] == client_id:
                    # Update allowed fields
                    allowed_fields = ["name", "email", "phone", "company", "industry", "status", "notes"]
                    for field, value in update_data.items():
                        if field in allowed_fields:
                            client[field] = value
                    
                    # Update timestamp
                    client["updated_at"] = datetime.now().isoformat()
                    
                    # Save updated data
                    self._save_data(data)
                    
                    self.logger.info(f"Updated client: {client_id}")
                    return client
            
            raise KeyError(f"Client with ID '{client_id}' not found")
            
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error updating client: {str(e)}")
            raise
        except KeyError:
            self.logger.warning(f"Client not found for update: {client_id}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error updating client: {str(e)}")
            raise
    
    def delete_client(self, client_id: str) -> bool:
        """
        Delete a client from the CRM system.
        
        Args:
            client_id: The unique identifier of the client
            
        Returns:
            True if client was deleted, False if client not found
            
        Raises:
            ValueError: If client_id is empty
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
            IOError: If there's an error saving the data
        """
        if not client_id:
            raise ValueError("Client ID cannot be empty or None")
        
        try:
            # Load existing data
            data = self._load_data()
            
            # Find and remove client
            for i, client in enumerate(data["clients"]):
                if client["id"] == client_id:
                    del data["clients"][i]
                    
                    # Save updated data
                    self._save_data(data)
                    
                    self.logger.info(f"Deleted client: {client_id}")
                    return True
            
            self.logger.warning(f"Client not found for deletion: {client_id}")
            return False
            
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error deleting client: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error deleting client: {str(e)}")
            raise
    
    def search_clients(self, query: str) -> List[Dict[str, Any]]:
        """
        Search clients by name, email, or company.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching clients
            
        Raises:
            ValueError: If query is empty
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
        """
        if not query:
            raise ValueError("Search query cannot be empty")
        
        try:
            data = self._load_data()
            query_lower = query.lower()
            matching_clients = []
            
            for client in data["clients"]:
                if (query_lower in client.get("name", "").lower() or
                    query_lower in client.get("email", "").lower() or
                    query_lower in client.get("company", "").lower()):
                    matching_clients.append(client)
            
            self.logger.info(f"Found {len(matching_clients)} clients matching query: '{query}'")
            return matching_clients
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error searching clients: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error searching clients: {str(e)}")
            raise
    
    def get_client_statistics(self) -> Dict[str, Any]:
        """
        Get CRM statistics and metrics.
        
        Returns:
            Dictionary containing CRM statistics
            
        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
        """
        try:
            data = self._load_data()
            clients = data["clients"]
            total_clients = len(clients)
            
            # Count by status
            status_counts = {}
            for client in clients:
                status = client.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count by industry
            industry_counts = {}
            for client in clients:
                industry = client.get("industry", "unknown")
                industry_counts[industry] = industry_counts.get(industry, 0) + 1
            
            # Calculate total balance
            total_balance = sum(client.get("balance", 0.0) for client in clients)
            
            statistics = {
                "total_clients": total_clients,
                "status_distribution": status_counts,
                "industry_distribution": industry_counts,
                "total_balance": total_balance,
                "average_balance": total_balance / total_clients if total_clients > 0 else 0.0,
                "last_updated": datetime.now().isoformat()
            }
            
            self.logger.info(f"Generated statistics for {total_clients} clients")
            return statistics
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error getting CRM statistics: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error getting CRM statistics: {str(e)}")
            raise 