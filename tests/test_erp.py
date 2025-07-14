"""
Unit tests for ERPService module

This module provides comprehensive testing for ERP functionality including:
- Order creation and management
- Data validation and edge cases
- Error handling and file operations
- Business logic validation
"""

import json
import os
import tempfile
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from services.erp_service import ERPService, Order, Product


class TestERPService(unittest.TestCase):
    """Test cases for ERPService class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.test_dir, "test_orders.json")
        self.erp_service = ERPService(data_file=self.test_data_file)

        # Sample valid order data for testing
        self.valid_order_data = {
            "client_id": "ACME001",
            "order_number": "ORD-2024-001",
            "items": [
                {"sku": "WIDGET-001", "quantity": 10, "unit_price": "29.99"},
                {"sku": "GADGET-002", "quantity": 5, "unit_price": "199.99"},
            ],
            "shipping_address": {
                "name": "John Doe",
                "street": "123 Main St",
                "city": "Anytown",
                "state": "NY",
                "zip": "12345",
                "country": "USA"
            },
            "notes": "Expedite shipping"
        }

    def tearDown(self):
        """Clean up after each test method."""
        # Remove test files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        os.rmdir(self.test_dir)

    def test_init_creates_data_file(self):
        """Test that ERPService initialization creates data file if it doesn't exist."""
        self.assertTrue(os.path.exists(self.test_data_file))
        
        # Verify file contains valid JSON structure
        with open(self.test_data_file, 'r') as f:
            data = json.load(f)
        
        self.assertIn('orders', data)
        self.assertIn('products', data)
        self.assertIn('inventory', data)
        self.assertIsInstance(data['orders'], list)

    def test_create_order_success(self):
        """Test successful order creation with valid data."""
        result = self.erp_service.create_order(self.valid_order_data)
        
        # Verify return structure
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('order', result)
        self.assertIn('order_id', result)
        
        # Verify order data
        order = result['order']
        self.assertEqual(order['client_id'], self.valid_order_data['client_id'])
        self.assertEqual(order['order_number'], self.valid_order_data['order_number'])
        self.assertEqual(order['status'], 'pending')
        self.assertIn('id', order)
        self.assertIn('created_at', order)
        self.assertIn('total_amount', order)

    def test_create_order_calculates_total(self):
        """Test that order creation correctly calculates total amount."""
        result = self.erp_service.create_order(self.valid_order_data)
        order = result['order']
        
        expected_total = Decimal('10') * Decimal('29.99') + Decimal('5') * Decimal('199.99')
        actual_total = Decimal(str(order['total_amount']))
        
        self.assertEqual(actual_total, expected_total)

    def test_create_order_invalid_data(self):
        """Test order creation with invalid data."""
        invalid_data = {
            "client_id": "",  # Empty client_id
            "items": []  # Empty items list
        }
        
        result = self.erp_service.create_order(invalid_data)
        
        self.assertIn('success', result)
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_create_order_missing_required_fields(self):
        """Test order creation with missing required fields."""
        incomplete_data = {
            "client_id": "TEST001"
            # Missing items and other required fields
        }
        
        result = self.erp_service.create_order(incomplete_data)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_create_order_invalid_items_format(self):
        """Test order creation with invalid items format."""
        invalid_items_data = self.valid_order_data.copy()
        invalid_items_data['items'] = [
            {"sku": "WIDGET-001"},  # Missing quantity and unit_price
            {"quantity": 5}  # Missing sku and unit_price
        ]
        
        result = self.erp_service.create_order(invalid_items_data)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_get_order_by_id_existing(self):
        """Test retrieving an existing order by ID."""
        # Create an order first
        create_result = self.erp_service.create_order(self.valid_order_data)
        order_id = create_result['order_id']
        
        # Retrieve the order
        result = self.erp_service.get_order_by_id(order_id)
        
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('order', result)
        self.assertEqual(result['order']['id'], order_id)

    def test_get_order_by_id_nonexistent(self):
        """Test retrieving a non-existent order by ID."""
        result = self.erp_service.get_order_by_id("nonexistent-id")
        
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_get_order_by_id_empty_string(self):
        """Test retrieving order with empty string ID."""
        result = self.erp_service.get_order_by_id("")
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_update_order_status_success(self):
        """Test successful order status update."""
        # Create an order first
        create_result = self.erp_service.create_order(self.valid_order_data)
        order_id = create_result['order_id']
        
        # Update status
        result = self.erp_service.update_order_status(order_id, "confirmed")
        
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('order', result)
        self.assertEqual(result['order']['status'], 'confirmed')
        self.assertIn('updated_at', result['order'])

    def test_update_order_status_invalid_status(self):
        """Test order status update with invalid status."""
        # Create an order first
        create_result = self.erp_service.create_order(self.valid_order_data)
        order_id = create_result['order_id']
        
        # Try to update with invalid status
        result = self.erp_service.update_order_status(order_id, "invalid_status")
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_update_order_status_nonexistent_order(self):
        """Test updating status of non-existent order."""
        result = self.erp_service.update_order_status("nonexistent-id", "confirmed")
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_list_all_orders_empty(self):
        """Test listing orders when no orders exist."""
        result = self.erp_service.list_all_orders()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_list_all_orders_with_data(self):
        """Test listing orders when orders exist."""
        # Create multiple orders
        self.erp_service.create_order(self.valid_order_data)
        
        second_order = self.valid_order_data.copy()
        second_order['order_number'] = 'ORD-2024-002'
        self.erp_service.create_order(second_order)
        
        result = self.erp_service.list_all_orders()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        
        # Verify order structure
        for order in result:
            self.assertIn('id', order)
            self.assertIn('client_id', order)
            self.assertIn('status', order)
            self.assertIn('created_at', order)

    def test_generate_order_id_uniqueness(self):
        """Test that generated order IDs are unique."""
        id1 = self.erp_service._generate_order_id()
        id2 = self.erp_service._generate_order_id()
        
        self.assertNotEqual(id1, id2)
        self.assertTrue(id1.startswith('ORD-'))
        self.assertTrue(id2.startswith('ORD-'))

    def test_validate_order_data_valid(self):
        """Test validation with valid order data."""
        is_valid = self.erp_service._validate_order_data(self.valid_order_data)
        self.assertTrue(is_valid)

    def test_validate_order_data_invalid(self):
        """Test validation with invalid order data."""
        invalid_data = {
            "client_id": "",
            "items": []
        }
        is_valid = self.erp_service._validate_order_data(invalid_data)
        self.assertFalse(is_valid)

    @patch('services.erp_service.logger')
    def test_error_logging(self, mock_logger):
        """Test that errors are properly logged."""
        # Try to create order with invalid data
        self.erp_service.create_order({})
        
        # Verify error was logged
        mock_logger.error.assert_called()

    def test_concurrent_access_safety(self):
        """Test basic safety for concurrent file access."""
        # This is a basic test - in production you might want more sophisticated
        # concurrency testing
        results = []
        
        # Simulate multiple order creations
        for i in range(5):
            order_data = self.valid_order_data.copy()
            order_data['order_number'] = f'ORD-2024-{i:03d}'
            result = self.erp_service.create_order(order_data)
            results.append(result)
        
        # All should succeed
        for result in results:
            self.assertTrue(result['success'])
        
        # All should be stored
        all_orders = self.erp_service.list_all_orders()
        self.assertEqual(len(all_orders), 5)

    def test_json_serialization_decimal_handling(self):
        """Test that Decimal values are properly handled in JSON serialization."""
        result = self.erp_service.create_order(self.valid_order_data)
        order_id = result['order_id']
        
        # Retrieve order and verify total_amount can be loaded
        stored_order = self.erp_service.get_order_by_id(order_id)
        total_amount = stored_order['order']['total_amount']
        
        # Should be able to convert back to Decimal
        decimal_total = Decimal(str(total_amount))
        self.assertIsInstance(decimal_total, Decimal)

    def test_file_corruption_recovery(self):
        """Test handling of corrupted data file."""
        # Write invalid JSON to the file
        with open(self.test_data_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully and recreate file
        new_service = ERPService(data_file=self.test_data_file)
        result = new_service.create_order(self.valid_order_data)
        
        self.assertTrue(result['success'])


class TestERPModels(unittest.TestCase):
    """Test cases for ERP Pydantic models."""

    def test_product_model_validation(self):
        """Test Product model validation."""
        valid_product_data = {
            "sku": "WIDGET-001",
            "name": "Test Widget",
            "category": "Electronics",
            "price": "29.99",
            "cost": "15.00",
            "stock_quantity": 100
        }
        
        product = Product(**valid_product_data)
        
        self.assertEqual(product.sku, "WIDGET-001")
        self.assertEqual(product.price, Decimal("29.99"))
        self.assertEqual(product.cost, Decimal("15.00"))
        self.assertEqual(product.stock_quantity, 100)
        self.assertEqual(product.min_stock_level, 10)  # Default value

    def test_product_model_invalid_data(self):
        """Test Product model with invalid data."""
        invalid_data = {
            "sku": "",  # Empty SKU
            "name": "Test Widget",
            "category": "Electronics",
            "price": "invalid_price",  # Invalid price
            "cost": "15.00",
            "stock_quantity": -1  # Negative stock
        }
        
        with self.assertRaises(Exception):
            Product(**invalid_data)

    def test_order_model_validation(self):
        """Test Order model validation."""
        valid_order_data = {
            "client_id": "ACME001",
            "order_number": "ORD-2024-001",
            "items": [{"sku": "WIDGET-001", "quantity": 10}],
            "total_amount": "299.90",
            "shipping_address": {
                "name": "John Doe",
                "street": "123 Main St",
                "city": "Anytown",
                "state": "NY",
                "zip": "12345"
            }
        }
        
        order = Order(**valid_order_data)
        
        self.assertEqual(order.client_id, "ACME001")
        self.assertEqual(order.status, "pending")  # Default value
        self.assertIsInstance(order.total_amount, Decimal)
        self.assertIsInstance(order.created_at, datetime)


if __name__ == '__main__':
    unittest.main() 