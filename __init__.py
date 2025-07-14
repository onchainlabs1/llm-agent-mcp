"""
AgentMCP - AI-Powered Business Assistant

An intelligent agent that uses the Model Context Protocol (MCP) to interpret 
natural language commands and execute CRM/ERP operations.

This project provides:
- Natural language processing for business commands
- CRM, ERP, and HR service integrations
- MCP-based tool discovery and execution
- Streamlit web interface
- Comprehensive logging and monitoring
"""

__version__ = "1.0.0"
__author__ = "AgentMCP Team"
__description__ = "AI-Powered Business Assistant using Model Context Protocol"

from .agent import AgentConfig, AgentCore
from .services import CRMService, ERPService, HRService

__all__ = ["AgentCore", "AgentConfig", "CRMService", "ERPService", "HRService"]
