"""
Request schemas for the AgentMCP API.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any


class AgentRequest(BaseModel):
    """Request model for agent natural language processing."""
    
    command: str = Field(
        ..., 
        min_length=1,
        max_length=1000,
        description="Natural language command to process",
        example="List all clients with balance over 5000"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for the command"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "command": "Create a new client named John Smith with email john@acme.com",
                "context": {"department": "sales", "priority": "high"}
            }
        }


class ClientCreateRequest(BaseModel):
    """Request model for creating a new client."""
    
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Client name"
    )
    email: EmailStr = Field(
        ..., 
        description="Client email address"
    )
    balance: float = Field(
        default=0.0,
        ge=0,
        description="Initial account balance"
    )
    phone: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Client phone number"
    )
    address: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Client address"
    )
    company: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Client company name"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith",
                "email": "john@acme.com",
                "balance": 1000.0,
                "phone": "+1-555-0123",
                "address": "123 Main St, New York, NY",
                "company": "Acme Corp"
            }
        }


class ClientUpdateRequest(BaseModel):
    """Request model for updating an existing client."""
    
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Updated client name"
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Updated email address"
    )
    phone: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Updated phone number"
    )
    address: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Updated address"
    )
    company: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Updated company name"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith Jr.",
                "email": "john.smith@acme.com",
                "phone": "+1-555-0124"
            }
        }


class OrderCreateRequest(BaseModel):
    """Request model for creating a new order."""
    
    client_id: str = Field(
        ...,
        description="Client identifier"
    )
    total_amount: float = Field(
        ...,
        gt=0,
        description="Total order amount"
    )
    items: List[Dict[str, Any]] = Field(
        ...,
        description="Order items"
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Order notes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "client_id": "cli001",
                "total_amount": 2500.0,
                "items": [
                    {"name": "Laptop", "quantity": 2, "price": 1000.0},
                    {"name": "Mouse", "quantity": 2, "price": 25.0}
                ],
                "notes": "Urgent delivery required"
            }
        }


class OrderUpdateRequest(BaseModel):
    """Request model for updating an existing order."""
    
    status: Optional[str] = Field(
        default=None,
        description="Order status"
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Updated order notes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "status": "shipped",
                "notes": "Shipped via FedEx, tracking: 123456789"
            }
        }
