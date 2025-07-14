"""
AgentMCP - Services Package

This package contains business logic modules for different domains (CRM, ERP, HR).
"""

from .crm_service import CRMService
from .erp_service import ERPService
from .hr_service import HRService
from .models import (
    ApiResponse,
    Client,
    ClientCreate,
    ClientSearchFilter,
    ClientStatus,
    ClientUpdate,
    Employee,
    EmployeeCreate,
    EmployeeSearchFilter,
    EmployeeStatus,
    Order,
    OrderCreate,
    OrderItem,
    OrderPriority,
    OrderStatus,
    ValidationError,
)

__all__ = [
    "CRMService",
    "ERPService",
    "HRService",
    # Models
    "Client",
    "ClientCreate",
    "ClientUpdate",
    "ClientSearchFilter",
    "Employee",
    "EmployeeCreate",
    "EmployeeSearchFilter",
    "Order",
    "OrderCreate",
    "OrderItem",
    "ApiResponse",
    "ValidationError",
    # Enums
    "ClientStatus",
    "EmployeeStatus",
    "OrderStatus",
    "OrderPriority",
]
