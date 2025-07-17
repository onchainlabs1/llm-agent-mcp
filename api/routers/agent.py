"""
AI Agent endpoints for natural language processing.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..dependencies import get_agent_core
from ..schemas.requests import AgentRequest
from ..schemas.responses import AgentResponse

router = APIRouter()


@router.post("/agent/process", response_model=AgentResponse)
async def process_natural_language(
    request: AgentRequest,
    agent_core = Depends(get_agent_core)
) -> AgentResponse:
    """
    Process natural language business commands.
    
    This endpoint accepts natural language instructions and:
    1. Analyzes the intent and extracts parameters
    2. Selects the appropriate MCP tool
    3. Executes the business operation
    4. Returns structured results
    
    Example requests:
    - "List all clients with balance over 5000"
    - "Create a new client named John Smith with email john@acme.com"
    - "Update order ORD-001 to shipped status"
    
    Args:
        request: Natural language request with optional context
        agent_core: Injected agent core service
        
    Returns:
        AgentResponse: Structured response with results and metadata
    """
    try:
        # Process the request through the agent
        result = agent_core.process_user_request(request.command)
        
        if result.get("success", False):
            return AgentResponse(
                success=True,
                message="Command processed successfully",
                data=result,
                tool_used=result.get("tool_used"),
                execution_time=result.get("execution_time", 0),
                reasoning=result.get("reasoning", "")
            )
        else:
            return AgentResponse(
                success=False,
                message=result.get("error_message", "Command processing failed"),
                data=result,
                tool_used=result.get("tool_used"),
                execution_time=result.get("execution_time", 0),
                reasoning=result.get("reasoning", "")
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent processing error: {str(e)}"
        )


@router.get("/agent/tools")
async def list_available_tools(
    agent_core = Depends(get_agent_core)
) -> Dict[str, Any]:
    """
    List all available MCP tools and their descriptions.
    
    Returns:
        dict: Available tools organized by category
    """
    try:
        tools = agent_core.get_available_tools()
        
        # Organize tools by category
        categorized_tools = {
            "crm": [],
            "erp": [], 
            "hr": [],
            "other": []
        }
        
        for tool in tools:
            tool_name = tool.get("name", "")
            if "client" in tool_name.lower() or "crm" in tool_name.lower():
                categorized_tools["crm"].append(tool)
            elif "order" in tool_name.lower() or "erp" in tool_name.lower():
                categorized_tools["erp"].append(tool)
            elif "employee" in tool_name.lower() or "hr" in tool_name.lower():
                categorized_tools["hr"].append(tool)
            else:
                categorized_tools["other"].append(tool)
        
        return {
            "total_tools": len(tools),
            "categories": categorized_tools,
            "last_updated": agent_core.get_last_schema_update() if hasattr(agent_core, 'get_last_schema_update') else None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving tools: {str(e)}"
        )


@router.get("/agent/examples")
async def get_command_examples() -> Dict[str, Any]:
    """
    Get example natural language commands for each category.
    
    Returns:
        dict: Examples organized by business domain
    """
    return {
        "crm_examples": [
            "List all clients",
            "Get client information for ACME Corp",
            "Create a new client named John Smith with email john@acme.com",
            "Update client balance for cli001 to 5000",
            "Find all clients with balance over 10000",
            "Filter clients by balance range 1000 to 5000"
        ],
        "erp_examples": [
            "List all orders",
            "Get order details for ORD-20240101-001",
            "Create order for client cli001 with total amount 2500",
            "Update order ORD-20240101-001 to shipped status",
            "List all pending orders",
            "Show orders created this month"
        ],
        "hr_examples": [
            "List all employees",
            "Get employee information for EMP001",
            "Create new employee John Doe in Engineering department",
            "Update employee salary for EMP001 to 75000",
            "List employees in Sales department",
            "Show all department managers"
        ],
        "complex_examples": [
            "Create client ACME Corp and then create an order for them worth 15000",
            "Find all high-value clients and create a summary report",
            "Update all pending orders to processing status",
            "Create quarterly sales report for Q4 2024"
        ]
    }
