"""
AgentMCP HR Service Module

This module provides Human Resources (HR) functionality including
employee management, payroll tracking, and organizational structure.
The service simulates a real HR system with JSON-based data persistence.

Key features:
- Employee creation and management
- Department and role management
- Salary and benefits tracking
- Performance evaluation
- Organizational reporting
"""

import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Employee(BaseModel):
    """Model representing an HR employee."""

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique employee identifier"
    )
    employee_id: str = Field(description="Human-readable employee ID")
    first_name: str = Field(description="Employee first name")
    last_name: str = Field(description="Employee last name")
    email: str = Field(description="Employee email address")
    phone: Optional[str] = Field(default=None, description="Employee phone number")
    department: str = Field(description="Employee department")
    position: str = Field(description="Employee job position")
    salary: Decimal = Field(description="Annual salary")
    hire_date: datetime = Field(description="Date of hire")
    manager_id: Optional[str] = Field(default=None, description="Manager's employee ID")
    status: str = Field(
        default="active", description="Employee status (active, inactive, terminated)"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )


class Department(BaseModel):
    """Model representing an HR department."""

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique department identifier"
    )
    name: str = Field(description="Department name")
    code: str = Field(description="Department code")
    description: Optional[str] = Field(
        default=None, description="Department description"
    )
    manager_id: Optional[str] = Field(default=None, description="Department manager ID")
    budget: Optional[Decimal] = Field(default=None, description="Department budget")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )


class PerformanceReview(BaseModel):
    """Model representing an employee performance review."""

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique review identifier"
    )
    employee_id: str = Field(description="Employee ID being reviewed")
    reviewer_id: str = Field(description="Reviewer's employee ID")
    review_date: datetime = Field(description="Date of review")
    review_period: str = Field(description="Review period (e.g., 'Q1 2024')")
    overall_rating: int = Field(description="Overall performance rating (1-5)")
    comments: str = Field(description="Review comments")
    goals: List[str] = Field(description="Goals for next period")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )


class HRService:
    """
    HR service for managing human resources.

    This service provides comprehensive employee and organizational
    management capabilities with JSON-based data persistence.
    """

    def __init__(
        self,
        employees_file: str = "data/employees.json",
        departments_file: str = "data/departments.json",
        reviews_file: str = "data/reviews.json",
    ):
        """
        Initialize the HR service.

        Args:
            employees_file: Path to the employees JSON data file
            departments_file: Path to the departments JSON data file
            reviews_file: Path to the performance reviews JSON data file
        """
        self.employees_file = employees_file
        self.departments_file = departments_file
        self.reviews_file = reviews_file
        self.logger = logging.getLogger("agentmcp.hr_service")
        self._ensure_data_files()

    def _ensure_data_files(self) -> None:
        """Ensure the data files exist with proper structure."""
        # Ensure employees file
        try:
            with open(self.employees_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"employees": []}
            with open(self.employees_file, "w") as f:
                json.dump(data, f, indent=2, default=str)
            self.logger.info(f"Created new employees data file: {self.employees_file}")

        # Ensure departments file
        try:
            with open(self.departments_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"departments": []}
            with open(self.departments_file, "w") as f:
                json.dump(data, f, indent=2, default=str)
            self.logger.info(
                f"Created new departments data file: {self.departments_file}"
            )

        # Ensure reviews file
        try:
            with open(self.reviews_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"reviews": []}
            with open(self.reviews_file, "w") as f:
                json.dump(data, f, indent=2, default=str)
            self.logger.info(f"Created new reviews data file: {self.reviews_file}")

    # Employee Management Methods

    def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new employee.

        Args:
            employee_data: Employee information dictionary

        Returns:
            Created employee data
        """
        try:
            # Validate and create employee
            employee = Employee(**employee_data)

            # Load existing data
            with open(self.employees_file, "r") as f:
                data = json.load(f)

            # Check if employee ID already exists
            for existing_employee in data["employees"]:
                if existing_employee["employee_id"] == employee.employee_id:
                    raise ValueError(
                        f"Employee with ID {employee.employee_id} already exists"
                    )

            # Add new employee
            data["employees"].append(employee.dict())

            # Save updated data
            with open(self.employees_file, "w") as f:
                json.dump(data, f, indent=2, default=str)

            self.logger.info(
                f"Created employee: {employee.first_name} {employee.last_name} (ID: {employee.employee_id})"
            )
            return employee.dict()

        except Exception as e:
            self.logger.error(f"Error creating employee: {str(e)}")
            raise

    def get_employee(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an employee by ID.

        Args:
            employee_id: Employee identifier

        Returns:
            Employee data if found, None otherwise
        """
        try:
            with open(self.employees_file, "r") as f:
                data = json.load(f)

            for employee in data["employees"]:
                if (
                    employee["id"] == employee_id
                    or employee["employee_id"] == employee_id
                ):
                    return employee

            return None

        except Exception as e:
            self.logger.error(f"Error retrieving employee {employee_id}: {str(e)}")
            raise

    def update_employee(
        self, employee_id: str, update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing employee.

        Args:
            employee_id: Employee identifier
            update_data: Data to update

        Returns:
            Updated employee data if successful, None if employee not found
        """
        try:
            with open(self.employees_file, "r") as f:
                data = json.load(f)

            for employee in data["employees"]:
                if (
                    employee["id"] == employee_id
                    or employee["employee_id"] == employee_id
                ):
                    # Update fields
                    for key, value in update_data.items():
                        if key in employee:
                            employee[key] = value

                    # Update timestamp
                    employee["updated_at"] = datetime.now().isoformat()

                    # Save updated data
                    with open(self.employees_file, "w") as f:
                        json.dump(data, f, indent=2, default=str)

                    self.logger.info(f"Updated employee: {employee_id}")
                    return employee

            return None

        except Exception as e:
            self.logger.error(f"Error updating employee {employee_id}: {str(e)}")
            raise

    def terminate_employee(self, employee_id: str, termination_date: datetime) -> bool:
        """
        Terminate an employee.

        Args:
            employee_id: Employee identifier
            termination_date: Date of termination

        Returns:
            True if termination successful, False if employee not found
        """
        try:
            with open(self.employees_file, "r") as f:
                data = json.load(f)

            for employee in data["employees"]:
                if (
                    employee["id"] == employee_id
                    or employee["employee_id"] == employee_id
                ):
                    employee["status"] = "terminated"
                    employee["updated_at"] = datetime.now().isoformat()

                    with open(self.employees_file, "w") as f:
                        json.dump(data, f, indent=2, default=str)

                    self.logger.info(f"Terminated employee: {employee_id}")
                    return True

            return False

        except Exception as e:
            self.logger.error(f"Error terminating employee {employee_id}: {str(e)}")
            raise

    def list_employees(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        List all employees with optional filtering.

        Args:
            filters: Optional filters to apply

        Returns:
            List of employee data
        """
        try:
            with open(self.employees_file, "r") as f:
                data = json.load(f)

            employees = data["employees"]

            # Apply filters if provided
            if filters:
                filtered_employees = []
                for employee in employees:
                    matches = True
                    for key, value in filters.items():
                        if key in employee and employee[key] != value:
                            matches = False
                            break
                    if matches:
                        filtered_employees.append(employee)
                employees = filtered_employees

            return employees

        except Exception as e:
            self.logger.error(f"Error listing employees: {str(e)}")
            raise

    def search_employees(self, query: str) -> List[Dict[str, Any]]:
        """
        Search employees by name, email, or position.

        Args:
            query: Search query string

        Returns:
            List of matching employees
        """
        try:
            with open(self.employees_file, "r") as f:
                data = json.load(f)

            query_lower = query.lower()
            matching_employees = []

            for employee in data["employees"]:
                if (
                    query_lower
                    in f"{employee.get('first_name', '')} {employee.get('last_name', '')}".lower()
                    or query_lower in employee.get("email", "").lower()
                    or query_lower in employee.get("position", "").lower()
                ):
                    matching_employees.append(employee)

            return matching_employees

        except Exception as e:
            self.logger.error(f"Error searching employees: {str(e)}")
            raise

    # Department Management Methods

    def create_department(self, department_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new department.

        Args:
            department_data: Department information dictionary

        Returns:
            Created department data
        """
        try:
            # Validate and create department
            department = Department(**department_data)

            # Load existing data
            with open(self.departments_file, "r") as f:
                data = json.load(f)

            # Check if department code already exists
            for existing_department in data["departments"]:
                if existing_department["code"] == department.code:
                    raise ValueError(
                        f"Department with code {department.code} already exists"
                    )

            # Add new department
            data["departments"].append(department.dict())

            # Save updated data
            with open(self.departments_file, "w") as f:
                json.dump(data, f, indent=2, default=str)

            self.logger.info(
                f"Created department: {department.name} (Code: {department.code})"
            )
            return department.dict()

        except Exception as e:
            self.logger.error(f"Error creating department: {str(e)}")
            raise

    def get_department(self, department_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a department by ID or code.

        Args:
            department_id: Department identifier or code

        Returns:
            Department data if found, None otherwise
        """
        try:
            with open(self.departments_file, "r") as f:
                data = json.load(f)

            for department in data["departments"]:
                if (
                    department["id"] == department_id
                    or department["code"] == department_id
                ):
                    return department

            return None

        except Exception as e:
            self.logger.error(f"Error retrieving department {department_id}: {str(e)}")
            raise

    def list_departments(self) -> List[Dict[str, Any]]:
        """
        List all departments.

        Returns:
            List of department data
        """
        try:
            with open(self.departments_file, "r") as f:
                data = json.load(f)

            return data["departments"]

        except Exception as e:
            self.logger.error(f"Error listing departments: {str(e)}")
            raise

    # Performance Review Methods

    def create_performance_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new performance review.

        Args:
            review_data: Review information dictionary

        Returns:
            Created review data
        """
        try:
            # Validate and create review
            review = PerformanceReview(**review_data)

            # Load existing data
            with open(self.reviews_file, "r") as f:
                data = json.load(f)

            # Add new review
            data["reviews"].append(review.dict())

            # Save updated data
            with open(self.reviews_file, "w") as f:
                json.dump(data, f, indent=2, default=str)

            self.logger.info(
                f"Created performance review for employee: {review.employee_id}"
            )
            return review.dict()

        except Exception as e:
            self.logger.error(f"Error creating performance review: {str(e)}")
            raise

    def get_employee_reviews(self, employee_id: str) -> List[Dict[str, Any]]:
        """
        Get all performance reviews for an employee.

        Args:
            employee_id: Employee identifier

        Returns:
            List of performance reviews
        """
        try:
            with open(self.reviews_file, "r") as f:
                data = json.load(f)

            reviews = []
            for review in data["reviews"]:
                if review["employee_id"] == employee_id:
                    reviews.append(review)

            return reviews

        except Exception as e:
            self.logger.error(
                f"Error getting reviews for employee {employee_id}: {str(e)}"
            )
            raise

    # Reporting Methods

    def get_department_employees(self, department_id: str) -> List[Dict[str, Any]]:
        """
        Get all employees in a department.

        Args:
            department_id: Department identifier or code

        Returns:
            List of employees in the department
        """
        try:
            department = self.get_department(department_id)
            if not department:
                return []

            employees = self.list_employees({"department": department["name"]})
            return employees

        except Exception as e:
            self.logger.error(f"Error getting department employees: {str(e)}")
            raise

    def get_organizational_chart(self) -> Dict[str, Any]:
        """
        Generate organizational chart data.

        Returns:
            Organizational chart structure
        """
        try:
            departments = self.list_departments()
            employees = self.list_employees()

            org_chart = {
                "departments": [],
                "total_employees": len(employees),
                "active_employees": len(
                    [e for e in employees if e["status"] == "active"]
                ),
            }

            for dept in departments:
                dept_employees = self.get_department_employees(dept["id"])
                dept_data = {
                    "department": dept,
                    "employee_count": len(dept_employees),
                    "employees": dept_employees,
                }
                org_chart["departments"].append(dept_data)

            return org_chart

        except Exception as e:
            self.logger.error(f"Error generating organizational chart: {str(e)}")
            raise

    def get_salary_report(self) -> Dict[str, Any]:
        """
        Generate salary report and statistics.

        Returns:
            Salary report data
        """
        try:
            employees = self.list_employees({"status": "active"})

            total_salary = Decimal("0")
            department_salaries = {}
            position_salaries = {}

            for employee in employees:
                salary = Decimal(str(employee["salary"]))
                total_salary += salary

                # Department totals
                dept = employee["department"]
                if dept not in department_salaries:
                    department_salaries[dept] = {"total": Decimal("0"), "count": 0}
                department_salaries[dept]["total"] += salary
                department_salaries[dept]["count"] += 1

                # Position totals
                position = employee["position"]
                if position not in position_salaries:
                    position_salaries[position] = {"total": Decimal("0"), "count": 0}
                position_salaries[position]["total"] += salary
                position_salaries[position]["count"] += 1

            return {
                "total_payroll": float(total_salary),
                "average_salary": float(total_salary / len(employees))
                if employees
                else 0,
                "employee_count": len(employees),
                "department_breakdown": {
                    dept: {
                        "total": float(data["total"]),
                        "average": float(data["total"] / data["count"]),
                        "count": data["count"],
                    }
                    for dept, data in department_salaries.items()
                },
                "position_breakdown": {
                    pos: {
                        "total": float(data["total"]),
                        "average": float(data["total"] / data["count"]),
                        "count": data["count"],
                    }
                    for pos, data in position_salaries.items()
                },
            }

        except Exception as e:
            self.logger.error(f"Error generating salary report: {str(e)}")
            raise
