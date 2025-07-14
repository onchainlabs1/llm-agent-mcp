"""
Unit tests for HRService module

This module provides comprehensive testing for HR functionality including:
- Employee creation and management
- Department operations
- Performance review management
- Data validation and edge cases
- Error handling and file operations
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

from services.hr_service import HRService, Employee, Department, PerformanceReview


class TestHRService(unittest.TestCase):
    """Test cases for HRService class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.employees_file = os.path.join(self.test_dir, "test_employees.json")
        self.departments_file = os.path.join(self.test_dir, "test_departments.json")
        self.reviews_file = os.path.join(self.test_dir, "test_reviews.json")
        
        self.hr_service = HRService(
            employees_file=self.employees_file,
            departments_file=self.departments_file,
            reviews_file=self.reviews_file
        )

        # Sample valid employee data for testing
        self.valid_employee_data = {
            "employee_id": "EMP001",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@company.com",
            "phone": "+1-555-0123",
            "department": "Engineering",
            "position": "Software Engineer",
            "salary": "75000.00",
            "hire_date": "2024-01-15T09:00:00",
            "manager_id": "EMP002"
        }

        # Sample valid department data
        self.valid_department_data = {
            "name": "Engineering",
            "code": "ENG",
            "description": "Software development department",
            "manager_id": "EMP002",
            "budget": "1000000.00"
        }

        # Sample valid performance review data
        self.valid_review_data = {
            "employee_id": "EMP001",
            "reviewer_id": "EMP002",
            "review_date": "2024-06-15T14:00:00",
            "review_period": "Q2 2024",
            "overall_rating": 4,
            "comments": "Excellent performance with strong technical skills",
            "goals": ["Mentor junior developers", "Lead new project"]
        }

    def tearDown(self):
        """Clean up after each test method."""
        # Remove test files
        for file_path in [self.employees_file, self.departments_file, self.reviews_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.rmdir(self.test_dir)

    def test_init_creates_data_files(self):
        """Test that HRService initialization creates all required data files."""
        self.assertTrue(os.path.exists(self.employees_file))
        self.assertTrue(os.path.exists(self.departments_file))
        self.assertTrue(os.path.exists(self.reviews_file))
        
        # Verify files contain valid JSON structure
        with open(self.employees_file, 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, list)

    def test_create_employee_success(self):
        """Test successful employee creation with valid data."""
        result = self.hr_service.create_employee(self.valid_employee_data)
        
        # Verify return structure
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('employee', result)
        self.assertIn('employee_id', result)
        
        # Verify employee data
        employee = result['employee']
        self.assertEqual(employee['first_name'], self.valid_employee_data['first_name'])
        self.assertEqual(employee['last_name'], self.valid_employee_data['last_name'])
        self.assertEqual(employee['email'], self.valid_employee_data['email'])
        self.assertEqual(employee['status'], 'active')  # Default status
        self.assertIn('id', employee)
        self.assertIn('created_at', employee)

    def test_create_employee_invalid_email(self):
        """Test employee creation with invalid email format."""
        invalid_data = self.valid_employee_data.copy()
        invalid_data['email'] = 'invalid-email-format'
        
        result = self.hr_service.create_employee(invalid_data)
        
        self.assertIn('success', result)
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_create_employee_duplicate_employee_id(self):
        """Test employee creation with duplicate employee ID."""
        # Create first employee
        self.hr_service.create_employee(self.valid_employee_data)
        
        # Try to create another with same employee_id
        result = self.hr_service.create_employee(self.valid_employee_data)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_create_employee_missing_required_fields(self):
        """Test employee creation with missing required fields."""
        incomplete_data = {
            "first_name": "John",
            "last_name": "Smith"
            # Missing required fields
        }
        
        result = self.hr_service.create_employee(incomplete_data)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_get_employee_existing(self):
        """Test retrieving an existing employee."""
        # Create an employee first
        create_result = self.hr_service.create_employee(self.valid_employee_data)
        employee_id = create_result['employee_id']
        
        # Retrieve the employee
        result = self.hr_service.get_employee(employee_id)
        
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('employee', result)
        self.assertEqual(result['employee']['employee_id'], employee_id)

    def test_get_employee_nonexistent(self):
        """Test retrieving a non-existent employee."""
        result = self.hr_service.get_employee("NONEXISTENT")
        
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_update_employee_success(self):
        """Test successful employee update."""
        # Create an employee first
        create_result = self.hr_service.create_employee(self.valid_employee_data)
        employee_id = create_result['employee_id']
        
        # Update employee
        update_data = {
            "salary": "80000.00",
            "position": "Senior Software Engineer"
        }
        result = self.hr_service.update_employee(employee_id, update_data)
        
        self.assertTrue(result['success'])
        self.assertIn('employee', result)
        self.assertEqual(result['employee']['salary'], "80000.00")
        self.assertEqual(result['employee']['position'], "Senior Software Engineer")
        self.assertIn('updated_at', result['employee'])

    def test_update_employee_nonexistent(self):
        """Test updating non-existent employee."""
        update_data = {"salary": "80000.00"}
        result = self.hr_service.update_employee("NONEXISTENT", update_data)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_terminate_employee_success(self):
        """Test successful employee termination."""
        # Create an employee first
        create_result = self.hr_service.create_employee(self.valid_employee_data)
        employee_id = create_result['employee_id']
        
        # Terminate employee
        termination_date = datetime.now()
        result = self.hr_service.terminate_employee(employee_id, termination_date)
        
        self.assertTrue(result)
        
        # Verify employee status changed
        employee = self.hr_service.get_employee(employee_id)
        self.assertEqual(employee['employee']['status'], 'terminated')

    def test_terminate_employee_nonexistent(self):
        """Test terminating non-existent employee."""
        termination_date = datetime.now()
        result = self.hr_service.terminate_employee("NONEXISTENT", termination_date)
        
        self.assertFalse(result)

    def test_list_employees_empty(self):
        """Test listing employees when no employees exist."""
        result = self.hr_service.list_employees()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_list_employees_with_data(self):
        """Test listing employees when employees exist."""
        # Create multiple employees
        self.hr_service.create_employee(self.valid_employee_data)
        
        second_employee = self.valid_employee_data.copy()
        second_employee['employee_id'] = 'EMP003'
        second_employee['email'] = 'jane.doe@company.com'
        self.hr_service.create_employee(second_employee)
        
        result = self.hr_service.list_employees()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_list_employees_with_filters(self):
        """Test listing employees with department filter."""
        # Create employees in different departments
        emp1 = self.valid_employee_data.copy()
        emp1['department'] = 'Engineering'
        emp1['employee_id'] = 'EMP001'
        self.hr_service.create_employee(emp1)
        
        emp2 = self.valid_employee_data.copy()
        emp2['department'] = 'Marketing'
        emp2['employee_id'] = 'EMP002'
        emp2['email'] = 'jane@company.com'
        self.hr_service.create_employee(emp2)
        
        # Filter by department
        result = self.hr_service.list_employees(filters={'department': 'Engineering'})
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['department'], 'Engineering')

    def test_search_employees(self):
        """Test employee search functionality."""
        # Create an employee
        self.hr_service.create_employee(self.valid_employee_data)
        
        # Search by name
        result = self.hr_service.search_employees("John")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['first_name'], 'John')

    def test_search_employees_no_results(self):
        """Test employee search with no results."""
        # Create an employee
        self.hr_service.create_employee(self.valid_employee_data)
        
        # Search for non-existent name
        result = self.hr_service.search_employees("NonexistentName")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_create_department_success(self):
        """Test successful department creation."""
        result = self.hr_service.create_department(self.valid_department_data)
        
        self.assertTrue(result['success'])
        self.assertIn('department', result)
        self.assertIn('department_id', result)
        
        department = result['department']
        self.assertEqual(department['name'], self.valid_department_data['name'])
        self.assertEqual(department['code'], self.valid_department_data['code'])

    def test_create_department_duplicate_code(self):
        """Test department creation with duplicate code."""
        # Create first department
        self.hr_service.create_department(self.valid_department_data)
        
        # Try to create another with same code
        result = self.hr_service.create_department(self.valid_department_data)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_get_department_existing(self):
        """Test retrieving existing department."""
        # Create department first
        create_result = self.hr_service.create_department(self.valid_department_data)
        dept_id = create_result['department_id']
        
        # Retrieve department
        result = self.hr_service.get_department(dept_id)
        
        self.assertTrue(result['success'])
        self.assertIn('department', result)
        self.assertEqual(result['department']['name'], self.valid_department_data['name'])

    def test_get_department_nonexistent(self):
        """Test retrieving non-existent department."""
        result = self.hr_service.get_department("NONEXISTENT")
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_list_departments(self):
        """Test listing all departments."""
        # Create a department
        self.hr_service.create_department(self.valid_department_data)
        
        result = self.hr_service.list_departments()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_create_performance_review_success(self):
        """Test successful performance review creation."""
        result = self.hr_service.create_performance_review(self.valid_review_data)
        
        self.assertTrue(result['success'])
        self.assertIn('review', result)
        self.assertIn('review_id', result)
        
        review = result['review']
        self.assertEqual(review['employee_id'], self.valid_review_data['employee_id'])
        self.assertEqual(review['overall_rating'], self.valid_review_data['overall_rating'])

    def test_create_performance_review_invalid_rating(self):
        """Test performance review creation with invalid rating."""
        invalid_data = self.valid_review_data.copy()
        invalid_data['overall_rating'] = 10  # Rating should be 1-5
        
        result = self.hr_service.create_performance_review(invalid_data)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_get_employee_reviews(self):
        """Test retrieving employee performance reviews."""
        # Create a review
        self.hr_service.create_performance_review(self.valid_review_data)
        
        # Get reviews for employee
        result = self.hr_service.get_employee_reviews("EMP001")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['employee_id'], "EMP001")

    def test_get_employee_reviews_no_reviews(self):
        """Test retrieving reviews for employee with no reviews."""
        result = self.hr_service.get_employee_reviews("NONEXISTENT")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_get_department_employees(self):
        """Test retrieving employees by department."""
        # Create employees in same department
        emp1 = self.valid_employee_data.copy()
        emp1['employee_id'] = 'EMP001'
        self.hr_service.create_employee(emp1)
        
        emp2 = self.valid_employee_data.copy()
        emp2['employee_id'] = 'EMP002'
        emp2['email'] = 'jane@company.com'
        self.hr_service.create_employee(emp2)
        
        # Get employees by department name
        result = self.hr_service.get_department_employees("Engineering")
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_get_organizational_chart(self):
        """Test generating organizational chart."""
        # Create employees with manager relationship
        manager_data = self.valid_employee_data.copy()
        manager_data['employee_id'] = 'MGR001'
        manager_data['email'] = 'manager@company.com'
        manager_data['position'] = 'Engineering Manager'
        manager_data['manager_id'] = None  # Top level
        self.hr_service.create_employee(manager_data)
        
        # Create subordinate
        emp_data = self.valid_employee_data.copy()
        emp_data['manager_id'] = 'MGR001'
        self.hr_service.create_employee(emp_data)
        
        result = self.hr_service.get_organizational_chart()
        
        self.assertIsInstance(result, dict)
        self.assertIn('chart', result)

    def test_get_salary_report(self):
        """Test generating salary report."""
        # Create employees with different salaries
        self.hr_service.create_employee(self.valid_employee_data)
        
        emp2_data = self.valid_employee_data.copy()
        emp2_data['employee_id'] = 'EMP002'
        emp2_data['email'] = 'jane@company.com'
        emp2_data['salary'] = '90000.00'
        self.hr_service.create_employee(emp2_data)
        
        result = self.hr_service.get_salary_report()
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_employees', result)
        self.assertIn('total_salary_cost', result)
        self.assertIn('average_salary', result)
        self.assertIn('department_breakdown', result)

    @patch('services.hr_service.logger')
    def test_error_logging(self, mock_logger):
        """Test that errors are properly logged."""
        # Try to create employee with invalid data
        self.hr_service.create_employee({})
        
        # Verify error was logged
        mock_logger.error.assert_called()

    def test_file_corruption_recovery(self):
        """Test handling of corrupted data files."""
        # Write invalid JSON to employees file
        with open(self.employees_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle gracefully and recreate file
        new_service = HRService(employees_file=self.employees_file)
        result = new_service.create_employee(self.valid_employee_data)
        
        self.assertTrue(result['success'])

    def test_decimal_salary_handling(self):
        """Test that salary values are properly handled as Decimal."""
        result = self.hr_service.create_employee(self.valid_employee_data)
        employee_id = result['employee_id']
        
        # Retrieve employee and verify salary
        stored_employee = self.hr_service.get_employee(employee_id)
        salary = stored_employee['employee']['salary']
        
        # Should be able to convert to Decimal
        decimal_salary = Decimal(str(salary))
        self.assertIsInstance(decimal_salary, Decimal)


class TestHRModels(unittest.TestCase):
    """Test cases for HR Pydantic models."""

    def test_employee_model_validation(self):
        """Test Employee model validation."""
        valid_employee_data = {
            "employee_id": "EMP001",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@company.com",
            "department": "Engineering",
            "position": "Software Engineer",
            "salary": "75000.00",
            "hire_date": datetime.now()
        }
        
        employee = Employee(**valid_employee_data)
        
        self.assertEqual(employee.employee_id, "EMP001")
        self.assertEqual(employee.first_name, "John")
        self.assertEqual(employee.status, "active")  # Default value
        self.assertIsInstance(employee.salary, Decimal)

    def test_department_model_validation(self):
        """Test Department model validation."""
        valid_department_data = {
            "name": "Engineering",
            "code": "ENG",
            "description": "Software development",
            "budget": "1000000.00"
        }
        
        department = Department(**valid_department_data)
        
        self.assertEqual(department.name, "Engineering")
        self.assertEqual(department.code, "ENG")
        self.assertIsInstance(department.budget, Decimal)

    def test_performance_review_model_validation(self):
        """Test PerformanceReview model validation."""
        valid_review_data = {
            "employee_id": "EMP001",
            "reviewer_id": "MGR001",
            "review_date": datetime.now(),
            "review_period": "Q2 2024",
            "overall_rating": 4,
            "comments": "Great work",
            "goals": ["Goal 1", "Goal 2"]
        }
        
        review = PerformanceReview(**valid_review_data)
        
        self.assertEqual(review.employee_id, "EMP001")
        self.assertEqual(review.overall_rating, 4)
        self.assertIsInstance(review.goals, list)


if __name__ == '__main__':
    unittest.main() 