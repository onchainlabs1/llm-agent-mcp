"""
AgentMCP ERP Service Module

This module provides Enterprise Resource Planning (ERP) functionality
including order management, inventory tracking, and financial operations.
The service simulates a real ERP system with JSON-based data persistence.

Key features:
- Order creation and management
- Inventory tracking and updates
- Product catalog management
- Financial transaction tracking
- Reporting and analytics
"""

import json
import logging
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Product(BaseModel):
    """Model representing an ERP product."""

    sku: str = Field(description="Product SKU (Stock Keeping Unit)")
    name: str = Field(description="Product name")
    description: Optional[str] = Field(default=None, description="Product description")
    category: str = Field(description="Product category")
    price: Decimal = Field(description="Product price")
    cost: Decimal = Field(description="Product cost")
    stock_quantity: int = Field(description="Current stock quantity")
    min_stock_level: int = Field(
        default=10, description="Minimum stock level for reorder"
    )
    supplier: Optional[str] = Field(default=None, description="Supplier information")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )


class Order(BaseModel):
    """Model representing an ERP order."""

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique order identifier"
    )
    client_id: str = Field(description="Client identifier")
    order_number: str = Field(description="Human-readable order number")
    status: str = Field(
        default="pending",
        description="Order status (pending, confirmed, shipped, delivered, cancelled)",
    )
    items: List[Dict[str, Any]] = Field(
        description="Order items with product SKU and quantity"
    )
    total_amount: Decimal = Field(description="Total order amount")
    shipping_address: Dict[str, str] = Field(description="Shipping address information")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )
    notes: Optional[str] = Field(default=None, description="Order notes")


class ERPService:
    """
    ERP service for managing enterprise resources.

    This service provides comprehensive business operations management
    including orders, inventory, and financial tracking.
    """

    def __init__(self, data_file: str = "data/orders.json"):
        """Initialize the ERP service."""
        self.data_file = Path(data_file)
        self._ensure_data_file_exists()

    def _ensure_data_file_exists(self) -> None:
        """Ensure the data file exists with proper structure."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            initial_data = {
                "orders": [],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_orders": 0,
                },
            }
            self._save_data(initial_data)
            logger.info(f"Created new ERP data file: {self.data_file}")

    def _load_data(self) -> Dict[str, Any]:
        """Load order data from JSON file."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading ERP data: {e}")
            raise

    def _save_data(self, data: Dict[str, Any]) -> None:
        """Save order data to JSON file."""
        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Failed to save ERP data: {e}")
            raise

    def _generate_order_id(self) -> str:
        """Generate a unique order ID."""
        data = self._load_data()
        existing_ids = [order.get("id", "") for order in data.get("orders", [])]
        base_id = f"ORD-{datetime.now().strftime('%Y%m%d')}"
        counter = 1
        while f"{base_id}-{counter:03d}" in existing_ids:
            counter += 1
        return f"{base_id}-{counter:03d}"

    def _validate_order_data(self, order_data: Dict[str, Any]) -> bool:
        """Validate order data structure and required fields."""
        required_fields = ["client_id", "items", "total_amount"]
        for field in required_fields:
            if field not in order_data:
                return False
        if not isinstance(order_data.get("items"), list):
            return False
        if not isinstance(order_data.get("total_amount"), (int, float)):
            return False
        if order_data.get("total_amount", 0) <= 0:
            return False
        return True

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order in the ERP system.

        Args:
            order_data: Dictionary containing order information
                - client_id (str): ID of the client placing the order
                - items (list): List of items in the order
                - total_amount (float): Total cost of the order
                - description (str, optional): Order description
                - priority (str, optional): Order priority (low, medium, high)

        Returns:
            Dictionary containing the created order information
        """
        logger.info(f"Creating new order for client: {order_data.get('client_id')}")

        if not self._validate_order_data(order_data):
            raise ValueError("Invalid order data provided")

        data = self._load_data()

        new_order = {
            "id": self._generate_order_id(),
            "client_id": order_data["client_id"],
            "items": order_data["items"],
            "total_amount": order_data["total_amount"],
            "description": order_data.get("description", ""),
            "priority": order_data.get("priority", "medium"),
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        data["orders"].append(new_order)
        data["metadata"]["total_orders"] = len(data["orders"])
        data["metadata"]["last_updated"] = datetime.now().isoformat()

        self._save_data(data)
        logger.info(f"Successfully created order: {new_order['id']}")
        return new_order

    def get_order_by_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve order information by ID.

        Args:
            order_id: Unique identifier of the order

        Returns:
            Dictionary containing order information or None if not found
        """
        logger.info(f"Retrieving order: {order_id}")

        try:
            data = self._load_data()
            orders = data.get("orders", [])

            for order in orders:
                if order.get("id") == order_id:
                    logger.info(f"Found order: {order_id}")
                    return order

            logger.warning(f"Order not found: {order_id}")
            return None

        except Exception as e:
            logger.error(f"Error retrieving order {order_id}: {e}")
            return None

    def update_order_status(
        self, order_id: str, new_status: str
    ) -> Optional[Dict[str, Any]]:
        """
        Update the status of an existing order.

        Args:
            order_id: Unique identifier of the order
            new_status: New status for the order (pending, processing, shipped, delivered, cancelled)

        Returns:
            Dictionary containing updated order information or None if not found
        """
        logger.info(f"Updating order {order_id} status to: {new_status}")

        valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

        try:
            data = self._load_data()
            orders = data.get("orders", [])

            for order in orders:
                if order.get("id") == order_id:
                    order["status"] = new_status
                    order["updated_at"] = datetime.now().isoformat()
                    data["metadata"]["last_updated"] = datetime.now().isoformat()

                    self._save_data(data)
                    logger.info(
                        f"Successfully updated order {order_id} status to {new_status}"
                    )
                    return order

            logger.warning(f"Order not found for status update: {order_id}")
            return None

        except Exception as e:
            logger.error(f"Error updating order {order_id} status: {e}")
            return None

    def list_all_orders(self) -> List[Dict[str, Any]]:
        """
        Retrieve all orders from the ERP system.

        Returns:
            List of dictionaries containing order information
        """
        logger.info("Retrieving all orders")

        try:
            data = self._load_data()
            orders = data.get("orders", [])
            logger.info(f"Retrieved {len(orders)} orders")
            return orders

        except Exception as e:
            logger.error(f"Error retrieving orders: {e}")
            return []


# Global instance for easy access
erp_service = ERPService()
