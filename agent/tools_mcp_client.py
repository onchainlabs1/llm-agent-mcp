"""
AgentMCP MCP Client Module

This module handles communication with the Model Context Protocol (MCP) server
to register and manage tools. It provides functionality to:
- Connect to MCP server
- Register tool schemas
- Execute tool calls
- Handle MCP protocol communication
- Manage tool lifecycle

The MCP client acts as a bridge between the agent core and the business services,
ensuring proper tool registration and execution according to the MCP specification.

IMPORTANT: Current Implementation Details
==========================================

SYNCHRONOUS DESIGN:
This implementation uses synchronous operations for simplicity and reliability:
- All tool executions are blocking operations
- File I/O operations are synchronous
- Network requests (when connecting to MCP server) use requests library
- Tool registration and validation happen sequentially

This approach was chosen for:
✅ Simplicity in development and debugging
✅ Predictable execution flow
✅ Easier error handling and logging
✅ Better compatibility with Streamlit frontend
✅ Reduced complexity for business logic services

FUTURE ASYNC CONSIDERATIONS:
============================

For high-performance or scalable deployments, consider migrating to async:

1. ASYNC BENEFITS:
   - Non-blocking tool execution for better concurrency
   - Parallel processing of multiple user requests
   - Better resource utilization for I/O-bound operations
   - Improved scalability for enterprise deployments

2. ASYNC MIGRATION PATH:
   ```python
   # Current synchronous pattern:
   def execute_tool(self, tool_call: MCPToolCall) -> MCPToolResult:
       result = service_method(**parameters)
       return MCPToolResult(success=True, result=result)
   
   # Future async pattern:
   async def execute_tool_async(self, tool_call: MCPToolCall) -> MCPToolResult:
       result = await service_method_async(**parameters)
       return MCPToolResult(success=True, result=result)
   ```

3. COMPONENTS THAT WOULD BENEFIT FROM ASYNC:
   - File I/O operations (reading/writing data files)
   - External API calls (if integrating with real CRM/ERP systems)
   - Database operations (when moving beyond JSON files)
   - Concurrent tool execution (parallel processing)

4. ASYNC IMPLEMENTATION CONSIDERATIONS:
   - Replace requests with httpx or aiohttp
   - Use aiofiles for asynchronous file operations
   - Implement proper async context managers
   - Handle async error propagation correctly
   - Update Streamlit integration for async support

RECOMMENDATION:
Keep the current synchronous implementation for:
- Development and testing environments
- Single-user deployments
- Simple business logic operations
- Educational or demo purposes

Consider async migration when:
- Handling multiple concurrent users (>10)
- Integrating with external APIs/databases
- Processing large datasets
- Deploying in production environments
- Performance becomes a bottleneck

The architecture is designed to support both patterns with minimal changes
to the core business logic and MCP schema definitions.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import jsonschema
import requests
from pydantic import BaseModel, Field, ValidationError


class MCPToolSchema(BaseModel):
    """Schema definition for an MCP tool."""

    name: str = Field(description="Tool name")
    description: str = Field(description="Tool description")
    input_schema: Dict[str, Any] = Field(description="JSON schema for input parameters")
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None, description="JSON schema for output"
    )
    version: str = Field(default="1.0", description="Tool version")


class MCPToolCall(BaseModel):
    """Model for MCP tool call requests."""

    tool_name: str = Field(description="Name of the tool to call")
    arguments: Dict[str, Any] = Field(description="Arguments for the tool call")
    call_id: str = Field(description="Unique identifier for this call")


class MCPToolResult(BaseModel):
    """Model for MCP tool call results."""

    call_id: str = Field(description="ID of the tool call")
    success: bool = Field(description="Whether the call was successful")
    result: Optional[Any] = Field(default=None, description="Result data")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    execution_time: float = Field(default=0.0, description="Execution time in seconds")


class MCPClient:
    """
    Synchronous MCP client for tool registration and execution.

    This client manages tool schemas and handles execution of tools
    in a synchronous manner suitable for the current architecture.
    """

    def __init__(self, server_url: str = "http://localhost:8000", timeout: int = 30):
        """
        Initialize the MCP client.

        Args:
            server_url: URL of the MCP server (currently not used in standalone mode)
            timeout: Request timeout in seconds
        """
        self.server_url = server_url
        self.timeout = timeout
        self.logger = logging.getLogger("agentmcp.mcp_client")
        self.registered_tools: Dict[str, MCPToolSchema] = {}
        self.tool_handlers: Dict[str, Callable] = {}
        self.connected = False

    def connect(self) -> bool:
        """
        Connect to the MCP server (in standalone mode, this just validates configuration).

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # In standalone mode, we don't need actual server connection
            # Just validate that we can operate
            self.logger.info("MCP Client initialized in standalone mode")
            self.connected = True
            return True

        except Exception as e:
            self.logger.error(f"Error initializing MCP client: {str(e)}")
            self.connected = False
            return False

    def register_tool(self, tool_schema: MCPToolSchema, handler: Callable) -> bool:
        """
        Register a tool with the MCP client.

        Args:
            tool_schema: Schema definition for the tool
            handler: Function to handle tool execution

        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Validate the schema
            self._validate_tool_schema(tool_schema)

            # Store locally
            self.registered_tools[tool_schema.name] = tool_schema
            self.tool_handlers[tool_schema.name] = handler

            self.logger.info(f"Registered tool: {tool_schema.name}")
            return True

        except Exception as e:
            self.logger.error(f"Error registering tool {tool_schema.name}: {str(e)}")
            return False

    def _validate_tool_schema(self, schema: MCPToolSchema) -> None:
        """
        Validate tool schema format.

        Args:
            schema: Tool schema to validate

        Raises:
            ValueError: If schema is invalid
        """
        if not schema.name or not schema.name.strip():
            raise ValueError("Tool name cannot be empty")

        if not schema.description or not schema.description.strip():
            raise ValueError("Tool description cannot be empty")

        if not isinstance(schema.input_schema, dict):
            raise ValueError("Input schema must be a dictionary")

        # Validate that input_schema is a valid JSON schema
        try:
            jsonschema.Draft7Validator.check_schema(schema.input_schema)
        except jsonschema.SchemaError as e:
            raise ValueError(f"Invalid input schema: {str(e)}")

    def get_available_tools(self) -> List[MCPToolSchema]:
        """
        Get list of all available tools.

        Returns:
            List of registered tool schemas
        """
        return list(self.registered_tools.values())

    def execute_tool(self, tool_call: MCPToolCall) -> MCPToolResult:
        """
        Execute a tool call synchronously.
        
        NOTE: SYNCHRONOUS EXECUTION
        ==========================
        This method executes tools synchronously, which means:
        - The calling thread blocks until tool execution completes
        - No parallel processing of multiple tool calls
        - Simpler error handling and debugging
        - Direct return of results without async complexity
        
        For async execution in the future, this would become:
        ```python
        async def execute_tool_async(self, tool_call: MCPToolCall) -> MCPToolResult:
            # Non-blocking execution with await
            result = await service_method_async(**parameters)
            return MCPToolResult(success=True, result=result)
        ```

        Args:
            tool_call: Tool call to execute

        Returns:
            Result of the tool execution
        """
        start_time = datetime.now()

        try:
            # Check if tool is registered
            if tool_call.tool_name not in self.tool_handlers:
                return MCPToolResult(
                    call_id=tool_call.call_id,
                    success=False,
                    error=f"Tool '{tool_call.tool_name}' not found",
                    execution_time=0.0,
                )

            # Validate parameters before execution
            if not self.validate_tool_parameters(
                tool_call.tool_name, tool_call.arguments
            ):
                return MCPToolResult(
                    call_id=tool_call.call_id,
                    success=False,
                    error=f"Invalid parameters for tool '{tool_call.tool_name}'",
                    execution_time=0.0,
                )

            # Execute the tool
            handler = self.tool_handlers[tool_call.tool_name]
            result = handler(**tool_call.arguments)

            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(
                f"Tool {tool_call.tool_name} executed in {execution_time:.2f}s"
            )

            return MCPToolResult(
                call_id=tool_call.call_id,
                success=True,
                result=result,
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error executing tool {tool_call.tool_name}: {str(e)}")

            return MCPToolResult(
                call_id=tool_call.call_id,
                success=False,
                error=str(e),
                execution_time=execution_time,
            )

    def load_tool_schemas_from_file(self, schema_file: str) -> bool:
        """
        Load tool schemas from a JSON file.
        
        NOTE: SYNCHRONOUS FILE I/O
        ==========================
        This method uses synchronous file operations:
        - Blocks until file reading completes
        - Simple error handling with try/catch
        - Direct JSON parsing without async overhead
        
        For async file operations, consider:
        ```python
        import aiofiles
        async def load_tool_schemas_async(self, schema_file: str) -> bool:
            async with aiofiles.open(schema_file, 'r') as f:
                content = await f.read()
                # Process schemas asynchronously
        ```

        Args:
            schema_file: Path to the schema file

        Returns:
            True if loading successful, False otherwise
        """
        try:
            schema_path = Path(schema_file)
            if not schema_path.exists():
                self.logger.error(f"Schema file not found: {schema_file}")
                return False

            with open(schema_path, "r", encoding="utf-8") as f:
                schemas_data = json.load(f)

            if not isinstance(schemas_data, dict) or "tools" not in schemas_data:
                self.logger.error(f"Invalid schema file format: {schema_file}")
                return False

            loaded_count = 0
            for tool_data in schemas_data.get("tools", []):
                try:
                    schema = MCPToolSchema(**tool_data)
                    self.registered_tools[schema.name] = schema
                    loaded_count += 1
                except ValidationError as e:
                    self.logger.error(f"Invalid tool schema in {schema_file}: {str(e)}")
                    continue

            self.logger.info(f"Loaded {loaded_count} tool schemas from {schema_file}")
            return loaded_count > 0

        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in schema file {schema_file}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(
                f"Error loading tool schemas from {schema_file}: {str(e)}"
            )
            return False

    def get_tool_schema(self, tool_name: str) -> Optional[MCPToolSchema]:
        """
        Get schema for a specific tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool schema if found, None otherwise
        """
        return self.registered_tools.get(tool_name)

    def validate_tool_parameters(
        self, tool_name: str, parameters: Dict[str, Any]
    ) -> bool:
        """
        Validate parameters for a tool call against its schema.

        Args:
            tool_name: Name of the tool
            parameters: Parameters to validate

        Returns:
            True if parameters are valid, False otherwise
        """
        try:
            tool_schema = self.get_tool_schema(tool_name)
            if not tool_schema:
                self.logger.error(f"Tool schema not found: {tool_name}")
                return False

            # Validate against JSON schema
            jsonschema.validate(parameters, tool_schema.input_schema)
            return True

        except jsonschema.ValidationError as e:
            self.logger.error(f"Parameter validation failed for {tool_name}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error validating parameters for {tool_name}: {str(e)}")
            return False

    def register_service_tools(self, service_instance: Any, schema_file: str) -> bool:
        """
        Register tools from a service instance using a schema file.

        Args:
            service_instance: Instance of the service containing tool handlers
            schema_file: Path to the schema file defining the tools

        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Load schemas first
            if not self.load_tool_schemas_from_file(schema_file):
                return False

            # Register handlers for each tool
            registered_count = 0
            for tool_name, schema in self.registered_tools.items():
                # Convert tool name to method name (snake_case)
                method_name = tool_name.replace("-", "_").replace(" ", "_").lower()

                if hasattr(service_instance, method_name):
                    handler = getattr(service_instance, method_name)
                    if callable(handler):
                        self.tool_handlers[tool_name] = handler
                        registered_count += 1
                        self.logger.debug(f"Registered handler for tool: {tool_name}")
                    else:
                        self.logger.warning(
                            f"Attribute {method_name} is not callable for tool {tool_name}"
                        )
                else:
                    self.logger.warning(
                        f"Handler method {method_name} not found for tool {tool_name}"
                    )

            self.logger.info(
                f"Registered {registered_count} tool handlers from service"
            )
            return registered_count > 0

        except Exception as e:
            self.logger.error(f"Error registering service tools: {str(e)}")
            return False

    def get_tool_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about registered tools.

        Returns:
            Dictionary containing tool statistics
        """
        return {
            "total_tools": len(self.registered_tools),
            "tools_with_handlers": len(self.tool_handlers),
            "tools": list(self.registered_tools.keys()),
            "connected": self.connected,
        }
