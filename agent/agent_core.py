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
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

# --- LLM integration ---
import openai

# Import config and services using package imports
try:
    # Try relative imports (when used as a package)
    from ..config import config
    from ..services.crm_service import CRMService
    from ..services.erp_service import ERPService
except ImportError:
    try:
        # Try absolute package imports (recommended: pip install -e .)
        from agentmcp.config import config
        from agentmcp.services.crm_service import CRMService
        from agentmcp.services.erp_service import ERPService
    except ImportError:
        # Final fallback for development (avoid sys.path when possible)
import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))
        from config import config
from services.crm_service import CRMService
from services.erp_service import ERPService


def call_llm(prompt, model=None):
    """
    Call LLM API based on configured provider.
    Falls back to simulated mode if API key is missing or API call fails.
    """
    if model is None:
        model = config.llm.model

    provider = config.llm.provider
    api_key = config.get_llm_api_key()

    # If no API key or invalid key, use simulated mode
    if not api_key or api_key == "your-api-key-here":
        return _simulate_llm_response(prompt)

    try:
        if provider == "groq":
            return _call_groq_llm(prompt, model, api_key)
        elif provider == "openai":
            return _call_openai_llm(prompt, model, api_key)
        elif provider == "anthropic":
            return _call_anthropic_llm(prompt, model, api_key)
        else:
            return _simulate_llm_response(prompt)
    except Exception as e:
        print(f"LLM API call failed: {e}. Falling back to simulated mode.")
        return _simulate_llm_response(prompt)


def _call_groq_llm(prompt, model, api_key):
    """Call Groq LLM API."""
    openai.api_key = api_key
    openai.api_base = "https://api.groq.com/openai/v1"
    response = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def _call_openai_llm(prompt, model, api_key):
    """Call OpenAI LLM API."""
    openai.api_key = api_key
    openai.api_base = "https://api.openai.com/v1"
    response = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def _call_anthropic_llm(prompt, model, api_key):
    """Call Anthropic LLM API."""
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model, max_tokens=1000, messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except ImportError:
        raise Exception(
            "Anthropic library not installed. Install with: pip install anthropic"
        )


def _simulate_llm_response(prompt):
    """
    Simulate LLM response for testing/demo purposes.
    Uses regex patterns to extract intent and parameters.
    """
    prompt_lower = prompt.lower()

    # Simple pattern matching for tool selection - more specific balance criteria detection
    import re

    # Check for "under/below/less than" patterns FIRST to avoid conflicts
    if "balance" in prompt_lower and (
        re.search(r"balance\s+under\s+(\d+)", prompt_lower)
        or re.search(r"balance\s+below\s+(\d+)", prompt_lower)
        or re.search(r"balance\s+less.*?(\d+)", prompt_lower)
        or re.search(r"under\s+(\d+)", prompt_lower)
    ):
        balance_match = re.search(r"(\d+)", prompt_lower)
        max_balance = int(balance_match.group(1)) if balance_match else 1000
        return f'{{"tool_name": "filter_clients_by_balance", "parameters": {{"max_balance": {max_balance}}}}}'

    # Check for "over/above/greater than" patterns
    elif "balance" in prompt_lower and (
        re.search(r"balance\s+over\s+(\d+)", prompt_lower)
        or re.search(r"balance\s+above\s+(\d+)", prompt_lower)
        or re.search(r"balance\s+greater.*?(\d+)", prompt_lower)
        or re.search(r"over\s+(\d+)", prompt_lower)
    ):
        balance_match = re.search(r"(\d+)", prompt_lower)
        min_balance = int(balance_match.group(1)) if balance_match else 5000
        return f'{{"tool_name": "filter_clients_by_balance", "parameters": {{"min_balance": {min_balance}}}}}'
    elif "list" in prompt_lower and "client" in prompt_lower:
        return '{"tool_name": "list_all_clients", "parameters": {}}'
    elif "create" in prompt_lower and "client" in prompt_lower:
        return '{"tool_name": "create_client", "parameters": {"name": "Test Client", "email": "test@example.com", "balance": 1000}}'
    elif "get" in prompt_lower and "client" in prompt_lower:
        return '{"tool_name": "get_client_by_id", "parameters": {"client_id": "test-client-id"}}'
    elif "update" in prompt_lower and "balance" in prompt_lower:
        return '{"tool_name": "update_client_balance", "parameters": {"client_id": "test-client-id", "new_balance": 2000}}'
    elif "create" in prompt_lower and "order" in prompt_lower:
        return '{"tool_name": "create_order", "parameters": {"client_id": "test-client-id", "total_amount": 500, "items": [{"name": "Product", "quantity": 1, "price": 500}]}}'
    elif "list" in prompt_lower and "order" in prompt_lower:
        return '{"tool_name": "list_all_orders", "parameters": {}}'
    elif "get" in prompt_lower and "order" in prompt_lower:
        return '{"tool_name": "get_order_by_id", "parameters": {"order_id": "test-order-id"}}'
    elif "update" in prompt_lower and "order" in prompt_lower:
        return '{"tool_name": "update_order_status", "parameters": {"order_id": "test-order-id", "new_status": "shipped"}}'
    else:
        return '{"tool_name": "list_all_clients", "parameters": {}}'


class AgentConfig:
    """Configuration for the agent."""
    
    def __init__(
        self,
                 llm_provider: str = "simulated",
                 llm_model: str = "gpt-4",
        api_key: Optional[str] = None,
                 max_retries: int = 3,
                 timeout: int = 30,
        log_level: str = "INFO",
    ):
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.api_key = api_key
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
    
    def __init__(
        self,
        success: bool,
        result: Any,
        error_message: Optional[str] = None,
        execution_time: float = 0.0,
    ):
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
        logger.setLevel(config.get_log_level())
        
        # Create logs directory if it doesn't exist
        log_file_path = Path(config.logging.file)
        log_file_path.parent.mkdir(exist_ok=True)
        
        # Add structured logging handler
        handler = logging.FileHandler(config.logging.file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
            with open(schema_file, "r") as f:
                schema_data = json.load(f)
            
            for tool in schema_data.get("tools", []):
                tool_name = tool["name"]
                self.available_tools[tool_name] = tool
                
            self.logger.info(
                f"Loaded {len(schema_data.get('tools', []))} tools from {schema_file}"
            )
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
            self.logger.info(
                f"Successfully loaded {len(self.available_tools)} total tools from all schemas"
            )
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
            self.conversation_history.append(
                {
                "timestamp": start_time.isoformat(),
                "type": "user_input",
                    "content": user_input,
                }
            )
            
            # Select appropriate tool based on user input
            tool_call = self._select_tool(user_input)
            if not tool_call:
                return {
                    "success": False,
                    "error": "No appropriate tool found for the request",
                    "execution_time": (datetime.now() - start_time).total_seconds(),
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
                "execution_time": tool_result.execution_time,
            }
            
            self.logger.info(
                f"Request completed in {response['execution_time']:.2f}s using tool: {tool_call.tool_name}"
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds(),
            }
    
    def _select_tool(self, user_input: str) -> Optional[ToolCall]:
        """
        Select appropriate tool based on user input using configured LLM.
        Args:
            user_input: Natural language request
        Returns:
            ToolCall object if tool found, None otherwise
        """
        try:
            # Use configured LLM to interpret the user input
            prompt = (
                "You are an AI agent that maps user requests to business tools. "
                "Given the following user request, return a JSON object with two fields: "
                "'tool_name' (the best matching tool from this list: get_client_by_id, create_client, update_client_balance, list_all_clients, filter_clients_by_balance, create_order, get_order_by_id, update_order_status, list_all_orders) "
                "and 'parameters' (a JSON object with the required parameters for the tool, or empty if none). "
                "IMPORTANT: Use 'filter_clients_by_balance' when users ask for clients with specific balance criteria (e.g., 'clients with balance over 5000', 'clients with balance under 1000', etc.). "
                "For filter_clients_by_balance, use parameters like {'min_balance': 5000} for 'over 5000' or {'max_balance': 1000} for 'under 1000'. "
                f"User request: {user_input}\n"
                "Respond ONLY with the JSON object."
            )
            llm_response = call_llm(prompt)
            import json as _json

            parsed = _json.loads(llm_response)
            tool_name = parsed.get("tool_name")
            parameters = parsed.get("parameters", {})
            if tool_name:
                return ToolCall(
                    tool_name=tool_name,
                    parameters=parameters,
                    reasoning=f"LLM ({config.llm.provider}) mapped user input to tool '{tool_name}' with parameters {parameters}",
                )
            return None
        except Exception as e:
            self.logger.error(f"LLM tool selection failed: {str(e)}")
            # Fallback to regex-based tool selection
            return self._fallback_tool_selection(user_input)

    def _fallback_tool_selection(self, user_input: str) -> Optional[ToolCall]:
        """
        Fallback tool selection using regex patterns when LLM fails.

        Args:
            user_input: Natural language input

        Returns:
            ToolCall object if pattern matches, None otherwise
        """
        user_input_lower = user_input.lower()

        # Client operations with balance filtering - check "under" patterns first
        # Check for "under/below/less than" patterns FIRST
        if "balance" in user_input_lower and (
            re.search(r"balance\s+under\s+(\d+)", user_input_lower)
            or re.search(r"balance\s+below\s+(\d+)", user_input_lower)
            or re.search(r"balance\s+less.*?(\d+)", user_input_lower)
            or re.search(r"under\s+(\d+)", user_input_lower)
        ):
            balance_match = re.search(r"(\d+)", user_input_lower)
            max_balance = int(balance_match.group(1)) if balance_match else 1000
            return ToolCall(
                "filter_clients_by_balance",
                {"max_balance": max_balance},
                "Regex pattern: filter clients by balance (maximum)",
            )

        # Check for "over/above/greater than" patterns
        elif "balance" in user_input_lower and (
            re.search(r"balance\s+over\s+(\d+)", user_input_lower)
            or re.search(r"balance\s+above\s+(\d+)", user_input_lower)
            or re.search(r"balance\s+greater.*?(\d+)", user_input_lower)
            or re.search(r"over\s+(\d+)", user_input_lower)
        ):
            balance_match = re.search(r"(\d+)", user_input_lower)
            min_balance = int(balance_match.group(1)) if balance_match else 5000
            return ToolCall(
                "filter_clients_by_balance",
                {"min_balance": min_balance},
                "Regex pattern: filter clients by balance (minimum)",
            )

        elif "list" in user_input_lower and (
            "client" in user_input_lower or "customer" in user_input_lower
        ):
            return ToolCall("list_all_clients", {}, "Regex pattern: list clients")

        elif "create" in user_input_lower and (
            "client" in user_input_lower or "customer" in user_input_lower
        ):
            client_data = self._extract_client_data(user_input)
            if client_data:
                return ToolCall(
                    "create_client", client_data, "Regex pattern: create client"
                )

        elif "get" in user_input_lower and (
            "client" in user_input_lower or "customer" in user_input_lower
        ):
            client_id = self._extract_client_id(user_input)
            if client_id:
                return ToolCall(
                    "get_client_by_id",
                    {"client_id": client_id},
                    "Regex pattern: get client",
                )

        elif "update" in user_input_lower and "balance" in user_input_lower:
            balance_data = self._extract_balance_data(user_input)
            if balance_data:
                return ToolCall(
                    "update_client_balance",
                    balance_data,
                    "Regex pattern: update balance",
                )

        # Order operations
        elif "list" in user_input_lower and "order" in user_input_lower:
            return ToolCall("list_all_orders", {}, "Regex pattern: list orders")

        elif "create" in user_input_lower and "order" in user_input_lower:
            order_data = self._extract_order_data(user_input)
            if order_data:
                return ToolCall(
                    "create_order", order_data, "Regex pattern: create order"
                )

        elif "get" in user_input_lower and "order" in user_input_lower:
            order_id = self._extract_order_id(user_input)
            if order_id:
                return ToolCall(
                    "get_order_by_id",
                    {"order_id": order_id},
                    "Regex pattern: get order",
                )

        elif (
            "update" in user_input_lower
            and "order" in user_input_lower
            and "status" in user_input_lower
        ):
            status_data = self._extract_order_status_data(user_input)
            if status_data:
                return ToolCall(
                    "update_order_status",
                    status_data,
                    "Regex pattern: update order status",
                )

        # Default fallback
        return ToolCall("list_all_clients", {}, "Default fallback: no pattern matched")
    
    def _extract_client_id(self, user_input: str) -> Optional[str]:
        """
        Extract client ID from user input using regex patterns.
        
        Args:
            user_input: Natural language input
            
        Returns:
            Client ID if found, None otherwise
        """
        # Pattern for UUID-like IDs
        uuid_pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        match = re.search(uuid_pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(0)
        
        # Pattern for simple IDs (numbers or alphanumeric)
        id_pattern = r"(?:client\s+)?(?:id\s+)?([a-zA-Z0-9]+)"
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
        name_pattern = (
            r"(?:named|name\s+is|called)\s+([A-Za-z\s]+?)(?:\s+with|\s+email|$)"
        )
        name_match = re.search(name_pattern, user_input, re.IGNORECASE)
        
        # Extract email
        email_pattern = (
            r"email\s+(?:is\s+)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
        )
        email_match = re.search(email_pattern, user_input, re.IGNORECASE)
        
        # Extract balance
        balance_pattern = r"balance\s+(?:of\s+)?(\d+(?:\.\d+)?)"
        balance_match = re.search(balance_pattern, user_input, re.IGNORECASE)
        
        if name_match and email_match:
            client_data = {
                "id": str(uuid4()),  # Generate new UUID
                "name": name_match.group(1).strip(),
                "email": email_match.group(1),
                "balance": float(balance_match.group(1)) if balance_match else 0.0,
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
        balance_pattern = r"(?:to|as|balance\s+of)\s+(\d+(?:\.\d+)?)"
        balance_match = re.search(balance_pattern, user_input, re.IGNORECASE)
        
        if client_id and balance_match:
            return {
                "client_id": client_id,
                "new_balance": float(balance_match.group(1)),
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
        order_pattern = r"ORD-\d{8}-\d{3}"
        match = re.search(order_pattern, user_input, re.IGNORECASE)
        if match:
            return match.group(0)
        
        # Pattern for simple order numbers
        id_pattern = r"(?:order\s+)?(?:id\s+)?([a-zA-Z0-9-]+)"
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
        amount_pattern = (
            r"(?:total\s+)?(?:amount|cost|price)\s+(?:of\s+)?(\d+(?:\.\d+)?)"
        )
        amount_match = re.search(amount_pattern, user_input, re.IGNORECASE)
        
        # Extract description
        desc_pattern = (
            r"(?:description|for|with)\s+([^.]+?)(?:\s+with|\s+total|\s+amount|$)"
        )
        desc_match = re.search(desc_pattern, user_input, re.IGNORECASE)
        
        # Extract priority
        priority_pattern = r"priority\s+(low|medium|high)"
        priority_match = re.search(priority_pattern, user_input, re.IGNORECASE)
        
        # Extract items (simplified - in real implementation would be more complex)
        items_pattern = (
            r"(?:items?|products?)\s+([^.]+?)(?:\s+with|\s+total|\s+amount|$)"
        )
        items_match = re.search(items_pattern, user_input, re.IGNORECASE)
        
        if client_id and amount_match:
            order_data = {
                "client_id": client_id,
                "total_amount": float(amount_match.group(1)),
                "items": [
                    {
                        "name": "Product",
                        "quantity": 1,
                        "price": float(amount_match.group(1)),
                    }
                ],  # Simplified
                "description": desc_match.group(1).strip() if desc_match else "",
                "priority": priority_match.group(1) if priority_match else "medium",
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
        status_pattern = (
            r"(?:to|as|status\s+)(pending|processing|shipped|delivered|cancelled)"
        )
        status_match = re.search(status_pattern, user_input, re.IGNORECASE)
        
        if order_id and status_match:
            return {"order_id": order_id, "new_status": status_match.group(1).lower()}
        
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
            self.logger.info(
                f"Executing tool: {tool_call.tool_name} with parameters: {tool_call.parameters}"
            )
            
            # Execute CRM service methods
            if tool_call.tool_name == "get_client_by_id":
                result = self.crm_service.get_client_by_id(
                    tool_call.parameters["client_id"]
                )
                
            elif tool_call.tool_name == "create_client":
                result = self.crm_service.create_client(tool_call.parameters)
                
            elif tool_call.tool_name == "update_client_balance":
                result = self.crm_service.update_client_balance(
                    tool_call.parameters["client_id"],
                    tool_call.parameters["new_balance"],
                )
                
            elif tool_call.tool_name == "list_all_clients":
                result = self.crm_service.list_all_clients()
            
            elif tool_call.tool_name == "filter_clients_by_balance":
                min_balance = tool_call.parameters.get("min_balance")
                max_balance = tool_call.parameters.get("max_balance")
                result = self.crm_service.filter_clients_by_balance(
                    min_balance, max_balance
                )

            # Execute ERP service methods
            elif tool_call.tool_name == "create_order":
                result = self.erp_service.create_order(tool_call.parameters)
                
            elif tool_call.tool_name == "get_order_by_id":
                result = self.erp_service.get_order_by_id(
                    tool_call.parameters["order_id"]
                )
                
            elif tool_call.tool_name == "update_order_status":
                result = self.erp_service.update_order_status(
                    tool_call.parameters["order_id"], tool_call.parameters["new_status"]
                )
                
            elif tool_call.tool_name == "list_all_orders":
                result = self.erp_service.list_all_orders()
                
            else:
                return ToolResult(
                    success=False,
                    result=None,
                    error_message=f"Unknown tool: {tool_call.tool_name}",
                    execution_time=(datetime.now() - start_time).total_seconds(),
                )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(
                f"Tool {tool_call.tool_name} executed successfully in {execution_time:.2f}s"
            )
            
            return ToolResult(
                success=True, result=result, execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error executing tool {tool_call.tool_name}: {str(e)}")
            
            return ToolResult(
                success=False,
                result=None,
                error_message=str(e),
                execution_time=execution_time,
            )
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history.copy()
    
    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        self.logger.info("Conversation history cleared")
