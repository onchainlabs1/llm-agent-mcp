"""
Response schemas for the AgentMCP API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
import time


class BaseResponse(BaseModel):
    """Base response model with common fields."""
    
    success: bool = Field(description="Whether the operation was successful")
    message: Optional[str] = Field(default=None, description="Response message")
    timestamp: float = Field(default_factory=time.time, description="Response timestamp")


class AgentResponse(BaseResponse):
    """Response model for agent operations."""
    
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
    tool_used: Optional[str] = Field(default=None, description="MCP tool that was executed")
    execution_time: Optional[float] = Field(default=None, description="Execution time in seconds")
    reasoning: Optional[str] = Field(default=None, description="Agent reasoning for tool selection")


class ClientResponse(BaseResponse):
    """Response model for single client operations."""
    
    data: Optional[Dict[str, Any]] = Field(default=None, description="Client data")


class ClientListResponse(BaseResponse):
    """Response model for client list operations."""
    
    data: List[Dict[str, Any]] = Field(default=[], description="List of clients")
    total: int = Field(description="Total number of clients")
    limit: int = Field(description="Number of clients requested")
    offset: int = Field(description="Number of clients skipped")
    has_more: bool = Field(description="Whether there are more clients available")


class OrderResponse(BaseResponse):
    """Response model for single order operations."""
    
    data: Optional[Dict[str, Any]] = Field(default=None, description="Order data")


class OrderListResponse(BaseResponse):
    """Response model for order list operations."""
    
    data: List[Dict[str, Any]] = Field(default=[], description="List of orders")
    total: int = Field(description="Total number of orders")
    limit: int = Field(description="Number of orders requested")
    offset: int = Field(description="Number of orders skipped")
    has_more: bool = Field(description="Whether there are more orders available")


class ErrorResponse(BaseResponse):
    """Response model for errors."""
    
    success: bool = Field(default=False, description="Always false for errors")
    error: Dict[str, Any] = Field(description="Error details")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "message": "Client not found",
                "timestamp": 1640995200.0,
                "error": {
                    "code": 404,
                    "type": "NotFoundError",
                    "details": "Client with ID 'cli999' does not exist"
                }
            }
        }


class HealthResponse(BaseResponse):
    """Response model for health checks."""
    
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    service: str = Field(description="Service name")
    uptime: Optional[float] = Field(default=None, description="Service uptime in seconds")


class MetricsResponse(BaseResponse):
    """Response model for system metrics."""
    
    system: Dict[str, Any] = Field(description="System metrics")
    services: Dict[str, str] = Field(description="Service statuses")
