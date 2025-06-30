"""
AgentMCP Core Agent Module

This module contains the main agent orchestration logic that coordinates between
the LLM, MCP tools, and business services. The agent is responsible for:
- Understanding user intent from natural language
- Selecting appropriate tools from the MCP registry
- Executing tool calls with proper parameters
- Managing conversation context and state
- Logging all actions for audit purposes

The agent follows a tool-use pattern where it explicitly chooses which tools
to use based on the user's request and available capabilities.
"""

import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

# Import services
import sys
sys.path.append('..')
from services.crm_service import CRMService
from services.erp_service import ERPService

# --- Groq LLM integration ---
import openai
import os

def call_llm_groq(prompt, model="llama3-70b-8192"):
    """
    Call the Groq LLM API to interpret a prompt.
    Uses environment variable for API key.
    """
    api_key = os.getenv('GROQ_API_KEY', 'your-api-key-here')
    openai.api_key = api_key
    openai.api_base = "https://api.groq.com/openai/v1"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

class AgentConfig:
    """Configuration for the agent."""
    
    def __init__(self, 
                 llm_provider: str = "simulated",
                 llm_model: str = "gpt-4",
                 max_retries: int = 3,
                 timeout: int = 30,
                 log_level: str = "INFO"):
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.max_retries = max_retries
        self.timeout = timeout
        self.log_level = log_level


class ToolCall:
    """Model representing a tool call request."""
    
    def __init__(self, tool_name: str, parameters: Dict[str, Any], reasoning: str):
        self.tool_name = tool_name
        self.parameters = parameters
        self.reasoning = reasoning


class ToolResult:
    """Model representing the result of a tool call."""
    
    def __init__(self, success: bool, result: Any, error_message: Optional[str] = None, execution_time: float = 0.0):
        self.success = success
        self.result = result
        self.error_message = error_message
        self.execution_time = execution_time


class AgentCore:
    """
    Main agent class that orchestrates LLM interactions and tool execution.
    
    This class is responsible for:
    - Managing conversation context
    - Interpreting user requests
    - Selecting and executing appropriate tools
    - Handling errors and retries
    - Logging all activities
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the agent with configuration.
        
        Args:
            config: Agent configuration settings
        """
        self.config = config
        self.logger = self._setup_logging()
        self.conversation_history: List[Dict[str, Any]] = []
        self.available_tools: Dict[str, Dict[str, Any]] = {}
        self.crm_service = CRMService()
        self.erp_service = ERPService()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up structured logging for the agent."""
        logger = logging.getLogger("agentmcp.core")
        logger.setLevel(getattr(logging, self.config.log_level))
        
        # Create logs directory if it doesn't exist
        Path("logs").mkdir(exist_ok=True)
        
        # Add structured logging handler
        handler = logging.FileHandler("logs/actions.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_mcp_schema(self, schema_file: str) -> bool:
        """
        Load MCP tool schemas from a JSON file.
        
        Args:
            schema_file: Path to the MCP schema file
            
        Returns:
            True if loading successful, False otherwise
        """
        try:
            with open(schema_file, 'r') as f:
                schema_data = json.load(f)
            
            for tool in schema_data.get('tools', []):
                tool_name = tool['name']
                self.available_tools[tool_name] = tool
                
            self.logger.info(f"Loaded {len(schema_data.get('tools', []))} tools from {schema_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading MCP schema from {schema_file}: {str(e)}")
            return False
    
    def load_all_mcp_schemas(self) -> bool:
        """
        Load all MCP schemas (CRM and ERP).
        
        Returns:
            True if all schemas loaded successfully, False otherwise
        """
        crm_loaded = self.load_mcp_schema("mcp_server/crm_mcp.json")
        erp_loaded = self.load_mcp_schema("mcp_server/erp_mcp.json")
        
        if crm_loaded and erp_loaded:
            self.logger.info(f"Successfully loaded {len(self.available_tools)} total tools from all schemas")
            return True
        else:
            self.logger.error("Failed to load one or more MCP schemas")
            return False
    
    def process_user_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user request and return the response.
        
        Args:
            user_input: Natural language request from user
            
        Returns:
            Dictionary containing the response and metadata
        """
        start_time = datetime.now()
        
        try:
            # Log the incoming request
            self.logger.info(f"Processing user request: {user_input}")
            
            # Add to conversation history
            self.conversation_history.append({
                "timestamp": start_time.isoformat(),
                "type": "user_input",
                "content": user_input
            })
            
            # Select appropriate tool based on user input
            tool_call = self._select_tool(user_input)
            if not tool_call:
                return {
                    "success": False,
                    "error": "No appropriate tool found for the request",
                    "execution_time": (datetime.now() - start_time).total_seconds()
                }
            
            # Execute the tool
            tool_result = self._execute_tool(tool_call)
            
            # Log the response
            response = {
                "success": tool_result.success,
                "tool_used": tool_call.tool_name,
                "parameters": tool_call.parameters,
                "reasoning": tool_call.reasoning,
                "result": tool_result.result,
                "error_message": tool_result.error_message,
                "execution_time": tool_result.execution_time
            }
            
            self.logger.info(f"Request completed in {response['execution_time']:.2f}s using tool: {tool_call.tool_name}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }
    
    def _select_tool(self, user_input: str) -> Optional[ToolCall]:
        """
        Select appropriate tool based on user input using Groq LLM.
        Args:
            user_input: Natural language request
        Returns:
            ToolCall object if tool found, None otherwise
        """
        try:
            # Use Groq LLM to interpret the user input
            prompt = (
                "You are an AI agent that maps user requests to business tools. "
                "Given the following user request, return a JSON object with two fields: "
                "'tool_name' (the best matching tool from this list: get_client_by_id, create_client, update_client_balance, list_all_clients, create_order, get_order_by_id, update_order_status, list_all_orders) "
                "and 'parameters' (a JSON object with the required parameters for the tool, or empty if none). "
                f"User request: {user_input}\n"
                "Respond ONLY with the JSON object."
            )
            llm_response = call_llm_groq(prompt)
            import json as _json
            parsed = _json.loads(llm_response)
            tool_name = parsed.get("tool_name")
            parameters = parsed.get("parameters", {})
            if tool_name:
                return ToolCall(
                    tool_name=tool_name,
                    parameters=parameters,
                    reasoning=f"LLM mapped user input to tool '{tool_name}' with parameters {parameters}"
                )
            return None
        except Exception as e:
            self.logger.error(f"LLM tool selection failed: {str(e)}")
            return None
    
    def _extract_client_id(self, user_input: str) -> Optional[str]:
        """
        Extract client ID from user input using regex patterns.
        
        Args:
            user_input: Natural language input
            
        Returns:
            Client ID if found, None otherwise
        """
        # Pattern for UUID-like IDs
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(0)
        
        # Pattern for simple IDs (numbers or alphanumeric)
        id_pattern = r'(?:client\s+)?(?:id\s+)?([a-zA-Z0-9]+)'
        match = re.search(id_pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def _extract_client_data(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Extract client creation data from user input.
        
        Args:
            user_input: Natural language input
            
        Returns:
            Dictionary with client data if found, None otherwise
        """
        # Extract name
        name_pattern = r'(?:named|name\s+is|called)\s+([A-Za-z\s]+?)(?:\s+with|\s+email|$)'
        name_match = re.search(name_pattern, user_input, re.IGNORECASE)
        
        # Extract email
        email_pattern = r'email\s+(?:is\s+)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        email_match = re.search(email_pattern, user_input, re.IGNORECASE)
        
        # Extract balance
        balance_pattern = r'balance\s+(?:of\s+)?(\d+(?:\.\d+)?)'
        balance_match = re.search(balance_pattern, user_input, re.IGNORECASE)
        
        if name_match and email_match:
            client_data = {
                "id": str(uuid4()),  # Generate new UUID
                "name": name_match.group(1).strip(),
                "email": email_match.group(1),
                "balance": float(balance_match.group(1)) if balance_match else 0.0
            }
            return client_data
        
        return None
    
    def _extract_balance_data(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Extract balance update data from user input.
        
        Args:
            user_input: Natural language input
            
        Returns:
            Dictionary with balance data if found, None otherwise
        """
        # Extract client ID
        client_id = self._extract_client_id(user_input)
        
        # Extract new balance
        balance_pattern = r'(?:to|as|balance\s+of)\s+(\d+(?:\.\d+)?)'
        balance_match = re.search(balance_pattern, user_input, re.IGNORECASE)
        
        if client_id and balance_match:
            return {
                "client_id": client_id,
                "new_balance": float(balance_match.group(1))
            }
        
        return None
    
    def _extract_order_id(self, user_input: str) -> Optional[str]:
        """
        Extract order ID from user input using regex patterns.
        
        Args:
            user_input: Natural language input
            
        Returns:
            Order ID if found, None otherwise
        """
        # Pattern for order IDs (ORD-YYYYMMDD-XXX format)
        order_pattern = r'ORD-\d{8}-\d{3}'
        match = re.search(order_pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(0)
        
        # Pattern for simple order numbers
        id_pattern = r'(?:order\s+)?(?:id\s+)?([a-zA-Z0-9-]+)'
        match = re.search(id_pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def _extract_order_data(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Extract order creation data from user input.
        
        Args:
            user_input: Natural language input
            
        Returns:
            Dictionary with order data if found, None otherwise
        """
        # Extract client ID
        client_id = self._extract_client_id(user_input)
        
        # Extract total amount
        amount_pattern = r'(?:total\s+)?(?:amount|cost|price)\s+(?:of\s+)?(\d+(?:\.\d+)?)'
        amount_match = re.search(amount_pattern, user_input, re.IGNORECASE)
        
        # Extract description
        desc_pattern = r'(?:description|for|with)\s+([^.]+?)(?:\s+with|\s+total|\s+amount|$)'
        desc_match = re.search(desc_pattern, user_input, re.IGNORECASE)
        
        # Extract priority
        priority_pattern = r'priority\s+(low|medium|high)'
        priority_match = re.search(priority_pattern, user_input, re.IGNORECASE)
        
        # Extract items (simplified - in real implementation would be more complex)
        items_pattern = r'(?:items?|products?)\s+([^.]+?)(?:\s+with|\s+total|\s+amount|$)'
        items_match = re.search(items_pattern, user_input, re.IGNORECASE)
        
        if client_id and amount_match:
            order_data = {
                "client_id": client_id,
                "total_amount": float(amount_match.group(1)),
                "items": [{"name": "Product", "quantity": 1, "price": float(amount_match.group(1))}],  # Simplified
                "description": desc_match.group(1).strip() if desc_match else "",
                "priority": priority_match.group(1) if priority_match else "medium"
            }
            return order_data
        
        return None
    
    def _extract_order_status_data(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Extract order status update data from user input.
        
        Args:
            user_input: Natural language input
            
        Returns:
            Dictionary with order status data if found, None otherwise
        """
        # Extract order ID
        order_id = self._extract_order_id(user_input)
        
        # Extract new status
        status_pattern = r'(?:to|as|status\s+)(pending|processing|shipped|delivered|cancelled)'
        status_match = re.search(status_pattern, user_input, re.IGNORECASE)
        
        if order_id and status_match:
            return {
                "order_id": order_id,
                "new_status": status_match.group(1).lower()
            }
        
        return None
    
    def _execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """
        Execute a single tool call.
        
        Args:
            tool_call: Tool call to execute
            
        Returns:
            Result of the tool execution
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Executing tool: {tool_call.tool_name} with parameters: {tool_call.parameters}")
            
            # Execute CRM service methods
            if tool_call.tool_name == "get_client_by_id":
                result = self.crm_service.get_client_by_id(tool_call.parameters["client_id"])
                
            elif tool_call.tool_name == "create_client":
                result = self.crm_service.create_client(tool_call.parameters)
                
            elif tool_call.tool_name == "update_client_balance":
                result = self.crm_service.update_client_balance(
                    tool_call.parameters["client_id"],
                    tool_call.parameters["new_balance"]
                )
                
            elif tool_call.tool_name == "list_all_clients":
                result = self.crm_service.list_all_clients()
            
            # Execute ERP service methods
            elif tool_call.tool_name == "create_order":
                result = self.erp_service.create_order(tool_call.parameters)
                
            elif tool_call.tool_name == "get_order_by_id":
                result = self.erp_service.get_order_by_id(tool_call.parameters["order_id"])
                
            elif tool_call.tool_name == "update_order_status":
                result = self.erp_service.update_order_status(
                    tool_call.parameters["order_id"],
                    tool_call.parameters["new_status"]
                )
                
            elif tool_call.tool_name == "list_all_orders":
                result = self.erp_service.list_all_orders()
                
            else:
                return ToolResult(
                    success=False,
                    result=None,
                    error_message=f"Unknown tool: {tool_call.tool_name}",
                    execution_time=(datetime.now() - start_time).total_seconds()
                )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Tool {tool_call.tool_name} executed successfully in {execution_time:.2f}s")
            
            return ToolResult(
                success=True,
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error executing tool {tool_call.tool_name}: {str(e)}")
            
            return ToolResult(
                success=False,
                result=None,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history.copy()
    
    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        self.logger.info("Conversation history cleared")


# Import uuid at the top level for the _extract_client_data method
from uuid import uuid4 