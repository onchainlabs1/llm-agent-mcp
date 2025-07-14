#!/usr/bin/env python3
"""
AgentMCP Initialization Script

This script initializes the AgentMCP project by creating necessary directories,
files, and configurations. Run this script before starting the application.

Usage:
    python init_setup.py
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def create_directories():
    """Create necessary directories for the project."""
    directories = [
        "logs",
        "data", 
        "mcp_server",
        "tests",
        "frontend",
        "agent",
        "services",
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True, parents=True)
        print(f"✓ Created directory: {directory}/")


def create_log_file():
    """Create initial log file with proper structure."""
    log_file = Path("logs/actions.log")
    log_file.parent.mkdir(exist_ok=True)

    # Create initial log entry
    initial_log = f"{datetime.now().isoformat()} - agentmcp.setup - INFO - AgentMCP initialized successfully\n"

    with open(log_file, "w") as f:
        f.write(initial_log)

    print(f"✓ Created log file: {log_file}")


def create_env_example():
    """Create .env.example file."""
    env_example_content = """# AgentMCP Configuration File
# Copy this file to .env and fill in your actual values

# ===== LLM Configuration =====
# Groq API Key for LLM integration
GROQ_API_KEY=your-groq-api-key-here

# Alternative LLM providers (uncomment to use)
# OPENAI_API_KEY=your-openai-api-key-here
# ANTHROPIC_API_KEY=your-anthropic-api-key-here

# ===== Agent Configuration =====
# LLM provider: groq, openai, anthropic, simulated
LLM_PROVIDER=groq
LLM_MODEL=llama3-70b-8192
MAX_RETRIES=3
TIMEOUT=30

# ===== Logging Configuration =====
LOG_LEVEL=INFO
LOG_FILE=logs/actions.log

# ===== MCP Configuration =====
MCP_SERVER_URL=http://localhost:8000
MCP_SCHEMAS_PATH=mcp_server/

# ===== Database Configuration =====
# JSON file paths
CRM_DATA_FILE=data/clients.json
ERP_DATA_FILE=data/orders.json
HR_DATA_FILE=data/employees.json

# ===== Application Configuration =====
# Web interface
STREAMLIT_HOST=localhost
STREAMLIT_PORT=8501

# Development mode
DEBUG=false
DEVELOPMENT=true

# ===== Security Configuration =====
# API rate limiting
MAX_REQUESTS_PER_MINUTE=60
MAX_REQUESTS_PER_HOUR=1000

# Session timeout (in seconds)
SESSION_TIMEOUT=3600
"""

    with open(".env.example", "w") as f:
        f.write(env_example_content)
    print("✓ Created .env.example file")


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    env_example = Path(".env.example")
    env_file = Path(".env")

    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print(f"✓ Created .env file from .env.example")
        print("  ⚠️  Please edit .env file with your actual API keys")
    elif env_file.exists():
        print("✓ .env file already exists")
    else:
        print("❌ .env.example not found")


def validate_data_files():
    """Ensure data files exist with proper structure."""
    data_files = {
        "data/clients.json": {"clients": []},
        "data/orders.json": {
            "orders": [],
            "metadata": {"created_at": datetime.now().isoformat()},
        },
        "data/employees.json": {"employees": []},
        "data/departments.json": {"departments": []},
        "data/reviews.json": {"reviews": []},
    }

    for file_path, default_structure in data_files.items():
        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            with open(file_path_obj, "w") as f:
                json.dump(default_structure, f, indent=2)
            print(f"✓ Created data file: {file_path}")
        else:
            print(f"✓ Data file exists: {file_path}")


def validate_mcp_schemas():
    """Validate MCP schema files exist and are properly formatted."""
    schema_files = [
        "mcp_server/crm_mcp.json",
        "mcp_server/erp_mcp.json", 
        "mcp_server/hr_mcp.json",
    ]

    for schema_file in schema_files:
        if Path(schema_file).exists():
            try:
                with open(schema_file, "r") as f:
                    schema_data = json.load(f)

                if "tools" in schema_data:
                    print(f"✓ MCP schema valid: {schema_file}")
                else:
                    print(f"⚠️  MCP schema missing 'tools' key: {schema_file}")
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON in: {schema_file}")
        else:
            print(f"❌ Missing MCP schema: {schema_file}")


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import openai
        import pydantic
        import streamlit

        print("✓ Core dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")


def main():
    """Main setup function."""
    print("🚀 Setting up AgentMCP...")
    print("=" * 50)

    create_directories()
    create_log_file()
    create_env_example()
    create_env_file()
    validate_data_files()
    validate_mcp_schemas()
    check_dependencies()

    print("=" * 50)
    print("✅ AgentMCP setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Install in development mode: pip install -e .")
    print("3. Or install dependencies: pip install -r requirements.txt")
    print("4. Run the application: streamlit run frontend/app.py")


if __name__ == "__main__":
    main() 