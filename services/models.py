"""
Data models for AgentMCP services using Pydantic for validation.

This module provides validated data models for all business entities
to ensure data integrity and security throughout the application.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field, confloat, constr, validator


class ClientStatus(str, Enum):
    """Enum for client status values."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECT = "prospect"
    ARCHIVED = "archived"


class EmployeeStatus(str, Enum):
    """Enum for employee status values."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"


class OrderStatus(str, Enum):
    """Enum for order status values."""

    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderPriority(str, Enum):
    """Enum for order priority values."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Base Models
class BaseEntity(BaseModel):
    """Base model for all entities with common fields."""

    id: constr(min_length=1, max_length=100) = Field(
        ..., description="Unique identifier"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update timestamp"
    )

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True
        validate_assignment = True
        use_enum_values = True


# Client Models
class ClientCreate(BaseModel):
    """Model for creating a new client."""

    name: constr(min_length=1, max_length=200) = Field(..., description="Client name")
    email: EmailStr = Field(..., description="Client email address")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[constr(max_length=500)] = Field(
        None, description="Client address"
    )
    status: ClientStatus = Field(
        default=ClientStatus.PROSPECT, description="Client status"
    )
    balance: confloat(ge=0) = Field(default=0.0, description="Account balance")

    @validator("name")
    def validate_name(cls, v):
        """Validate client name."""
        if not v or v.isspace():
            raise ValueError("Name cannot be empty or only whitespace")
        return v.strip()

    @validator("email")
    def validate_email_domain(cls, v):
        """Additional email validation."""
        if "@" not in v or "." not in v.split("@")[1]:
            raise ValueError("Invalid email format")
        return v.lower()

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True
        validate_assignment = True


class ClientUpdate(BaseModel):
    """Model for updating an existing client."""

    name: Optional[constr(min_length=1, max_length=200)] = Field(
        None, description="Client name"
    )
    email: Optional[EmailStr] = Field(None, description="Client email address")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[constr(max_length=500)] = Field(
        None, description="Client address"
    )
    status: Optional[ClientStatus] = Field(None, description="Client status")
    balance: Optional[confloat(ge=0)] = Field(None, description="Account balance")

    @validator("email")
    def validate_email_if_provided(cls, v):
        """Validate email if provided."""
        if v:
            return v.lower()
        return v

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True
        validate_assignment = True


class Client(BaseEntity):
    """Complete client model."""

    name: constr(min_length=1, max_length=200) = Field(..., description="Client name")
    email: EmailStr = Field(..., description="Client email address")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[constr(max_length=500)] = Field(
        None, description="Client address"
    )
    status: ClientStatus = Field(
        default=ClientStatus.PROSPECT, description="Client status"
    )
    balance: confloat(ge=0) = Field(default=0.0, description="Account balance")


# Employee Models
class EmployeeCreate(BaseModel):
    """Model for creating a new employee."""

    first_name: constr(min_length=1, max_length=100) = Field(
        ..., description="First name"
    )
    last_name: constr(min_length=1, max_length=100) = Field(
        ..., description="Last name"
    )
    email: EmailStr = Field(..., description="Employee email address")
    phone: Optional[str] = Field(None, description="Phone number")
    department: constr(min_length=1, max_length=100) = Field(
        ..., description="Department"
    )
    position: constr(min_length=1, max_length=100) = Field(
        ..., description="Job position"
    )
    salary: confloat(gt=0) = Field(..., description="Salary amount")
    hire_date: datetime = Field(..., description="Hire date")
    status: EmployeeStatus = Field(
        default=EmployeeStatus.ACTIVE, description="Employee status"
    )

    @validator("salary")
    def validate_salary(cls, v):
        """Validate salary amount."""
        if v <= 0:
            raise ValueError("Salary must be greater than zero")
        return v

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True
        validate_assignment = True


class Employee(BaseEntity):
    """Complete employee model."""

    first_name: constr(min_length=1, max_length=100) = Field(
        ..., description="First name"
    )
    last_name: constr(min_length=1, max_length=100) = Field(
        ..., description="Last name"
    )
    email: EmailStr = Field(..., description="Employee email address")
    phone: Optional[str] = Field(None, description="Phone number")
    department: constr(min_length=1, max_length=100) = Field(
        ..., description="Department"
    )
    position: constr(min_length=1, max_length=100) = Field(
        ..., description="Job position"
    )
    salary: confloat(gt=0) = Field(..., description="Salary amount")
    hire_date: datetime = Field(..., description="Hire date")
    status: EmployeeStatus = Field(
        default=EmployeeStatus.ACTIVE, description="Employee status"
    )


# Order Models
class OrderItem(BaseModel):
    """Model for order line items."""

    name: constr(min_length=1, max_length=200) = Field(..., description="Item name")
    quantity: int = Field(..., gt=0, description="Item quantity")
    price: confloat(gt=0) = Field(..., description="Unit price")
    total: confloat(gt=0) = Field(..., description="Line total")

    @validator("total")
    def validate_total(cls, v, values):
        """Validate that total equals quantity * price."""
        if "quantity" in values and "price" in values:
            expected_total = values["quantity"] * values["price"]
            if abs(v - expected_total) > 0.01:  # Allow for minor floating point errors
                raise ValueError(
                    f"Total {v} does not match quantity * price {expected_total}"
                )
        return v

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True
        validate_assignment = True


class OrderCreate(BaseModel):
    """Model for creating a new order."""

    client_id: constr(min_length=1, max_length=100) = Field(
        ..., description="Client ID"
    )
    items: List[OrderItem] = Field(..., min_items=1, description="Order items")
    total_amount: confloat(gt=0) = Field(..., description="Total order amount")
    description: Optional[constr(max_length=1000)] = Field(
        None, description="Order description"
    )
    priority: OrderPriority = Field(
        default=OrderPriority.MEDIUM, description="Order priority"
    )
    notes: Optional[constr(max_length=1000)] = Field(
        None, description="Additional notes"
    )

    @validator("total_amount")
    def validate_total_amount(cls, v, values):
        """Validate that total_amount matches sum of item totals."""
        if "items" in values and values["items"]:
            item_total = sum(item.total for item in values["items"])
            if abs(v - item_total) > 0.01:  # Allow for minor floating point errors
                raise ValueError(
                    f"Total amount {v} does not match sum of items {item_total}"
                )
        return v

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True
        validate_assignment = True


class Order(BaseEntity):
    """Complete order model."""

    client_id: constr(min_length=1, max_length=100) = Field(
        ..., description="Client ID"
    )
    order_number: constr(min_length=1, max_length=50) = Field(
        ..., description="Order number"
    )
    items: List[OrderItem] = Field(..., min_items=1, description="Order items")
    total_amount: confloat(gt=0) = Field(..., description="Total order amount")
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="Order status")
    description: Optional[constr(max_length=1000)] = Field(
        None, description="Order description"
    )
    priority: OrderPriority = Field(
        default=OrderPriority.MEDIUM, description="Order priority"
    )
    notes: Optional[constr(max_length=1000)] = Field(
        None, description="Additional notes"
    )
    shipping_address: Optional[Dict[str, Any]] = Field(
        None, description="Shipping address"
    )


# Search and Filter Models
class ClientSearchFilter(BaseModel):
    """Model for client search and filter parameters."""

    query: Optional[constr(min_length=1, max_length=200)] = Field(
        None, description="Search query"
    )
    status: Optional[ClientStatus] = Field(None, description="Filter by status")
    min_balance: Optional[confloat(ge=0)] = Field(None, description="Minimum balance")
    max_balance: Optional[confloat(ge=0)] = Field(None, description="Maximum balance")

    @validator("max_balance")
    def validate_balance_range(cls, v, values):
        """Validate that max_balance >= min_balance."""
        if (
            v is not None
            and "min_balance" in values
            and values["min_balance"] is not None
        ):
            if v < values["min_balance"]:
                raise ValueError(
                    "Maximum balance must be greater than or equal to minimum balance"
                )
        return v

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True


class EmployeeSearchFilter(BaseModel):
    """Model for employee search and filter parameters."""

    query: Optional[constr(min_length=1, max_length=200)] = Field(
        None, description="Search query"
    )
    department: Optional[constr(min_length=1, max_length=100)] = Field(
        None, description="Filter by department"
    )
    status: Optional[EmployeeStatus] = Field(None, description="Filter by status")
    min_salary: Optional[confloat(gt=0)] = Field(None, description="Minimum salary")
    max_salary: Optional[confloat(gt=0)] = Field(None, description="Maximum salary")

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True


# Response Models
class ApiResponse(BaseModel):
    """Standard API response model."""

    success: bool = Field(..., description="Operation success status")
    message: Optional[str] = Field(None, description="Response message")
    data: Optional[Any] = Field(None, description="Response data")
    errors: Optional[List[str]] = Field(None, description="Error messages")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Response timestamp"
    )

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True


class ValidationError(BaseModel):
    """Model for validation error details."""

    field: str = Field(..., description="Field name with error")
    message: str = Field(..., description="Error message")
    value: Any = Field(None, description="Invalid value")

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True
 