"""
Health check endpoints for system monitoring.
"""

import time
import psutil
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint.
    
    Returns:
        dict: Basic health status
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "service": "AgentMCP API"
    }


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with system metrics.
    
    Returns:
        dict: Detailed system health information
    """
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Test service connections
        services_status = await _check_services()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "1.0.0",
            "service": "AgentMCP API",
            "system": {
                "cpu_usage_percent": cpu_percent,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "usage_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "usage_percent": round((disk.used / disk.total) * 100, 2)
                }
            },
            "services": services_status
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )


async def _check_services() -> Dict[str, str]:
    """Check the status of internal services."""
    services = {}
    
    try:
        # Test CRM service
        from ..dependencies import get_crm_service
        crm = get_crm_service()
        # Simple test - try to list clients
        crm.list_all_clients()
        services["crm"] = "healthy"
    except Exception:
        services["crm"] = "unhealthy"
    
    try:
        # Test ERP service
        from ..dependencies import get_erp_service
        erp = get_erp_service()
        # Simple test - try to list orders
        erp.list_all_orders()
        services["erp"] = "healthy"
    except Exception:
        services["erp"] = "unhealthy"
    
    try:
        # Test Agent service
        from ..dependencies import get_agent_core
        agent = get_agent_core()
        services["agent"] = "healthy"
    except Exception:
        services["agent"] = "unhealthy"
    
    return services


@router.get("/health/status")
async def service_status() -> Dict[str, str]:
    """
    Quick service status check.
    
    Returns:
        dict: Status of each service
    """
    return await _check_services()
