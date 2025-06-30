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
"""

import json
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

import httpx
from pydantic import BaseModel, Field


class MCPToolSchema(BaseModel):
    """Schema definition for an MCP tool."""
    
    name: str = Field(description="Tool name")
    description: str = Field(description="Tool description")
    input_schema: Dict[str, Any] = Field(description="JSON schema for input parameters")
    output_schema: Optional[Dict[str, Any]] = Field(default=None, description="JSON schema for output")


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


class MCPClient:
    """
    Client for communicating with the MCP server.
    
    This class handles all MCP protocol interactions including:
    - Server connection management
    - Tool registration and discovery
    - Tool execution
    - Error handling and retries
    """
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        """
        Initialize the MCP client.
        
        Args:
            server_url: URL of the MCP server
        """
        self.server_url = server_url
        self.logger = logging.getLogger("agentmcp.mcp_client")
        self.registered_tools: Dict[str, MCPToolSchema] = {}
        self.tool_handlers: Dict[str, Callable] = {}
        
    async def connect(self) -> bool:
        """
        Connect to the MCP server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.server_url}/health")
                if response.status_code == 200:
                    self.logger.info("Successfully connected to MCP server")
                    return True
                else:
                    self.logger.error(f"Failed to connect to MCP server: {response.status_code}")
                    return False
        except Exception as e:
            self.logger.error(f"Error connecting to MCP server: {str(e)}")
            return False
    
    def register_tool(self, tool_schema: MCPToolSchema, handler: Callable) -> bool:
        """
        Register a tool with the MCP server.
        
        Args:
            tool_schema: Schema definition for the tool
            handler: Function to handle tool execution
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Store locally
            self.registered_tools[tool_schema.name] = tool_schema
            self.tool_handlers[tool_schema.name] = handler
            
            # TODO: Register with MCP server
            self.logger.info(f"Registered tool: {tool_schema.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error registering tool {tool_schema.name}: {str(e)}")
            return False
    
    def get_available_tools(self) -> List[MCPToolSchema]:
        """
        Get list of all available tools.
        
        Returns:
            List of registered tool schemas
        """
        return list(self.registered_tools.values())
    
    async def execute_tool(self, tool_call: MCPToolCall) -> MCPToolResult:
        """
        Execute a tool call.
        
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
                    error=f"Tool '{tool_call.tool_name}' not found"
                )
            
            # Execute the tool
            handler = self.tool_handlers[tool_call.tool_name]
            result = await handler(**tool_call.arguments)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Tool {tool_call.tool_name} executed in {execution_time:.2f}s")
            
            return MCPToolResult(
                call_id=tool_call.call_id,
                success=True,
                result=result
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error executing tool {tool_call.tool_name}: {str(e)}")
            
            return MCPToolResult(
                call_id=tool_call.call_id,
                success=False,
                error=str(e)
            )
    
    def load_tool_schemas_from_file(self, schema_file: str) -> bool:
        """
        Load tool schemas from a JSON file.
        
        Args:
            schema_file: Path to the schema file
            
        Returns:
            True if loading successful, False otherwise
        """
        try:
            with open(schema_file, 'r') as f:
                schemas_data = json.load(f)
            
            for schema_data in schemas_data.get('tools', []):
                schema = MCPToolSchema(**schema_data)
                self.registered_tools[schema.name] = schema
                
            self.logger.info(f"Loaded {len(schemas_data.get('tools', []))} tool schemas from {schema_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading tool schemas from {schema_file}: {str(e)}")
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
    
    def validate_tool_parameters(self, tool_name: str, parameters: Dict[str, Any]) -> bool:
        """
        Validate parameters for a tool call.
        
        Args:
            tool_name: Name of the tool
            parameters: Parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        # TODO: Implement JSON schema validation
        # This should validate parameters against the tool's input_schema
        return True 