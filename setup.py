#!/usr/bin/env python3
"""
Setup script for AgentMCP - AI-Powered Business Assistant

This setup script allows the project to be installed as a Python package,
which resolves import issues and makes development easier.

Installation:
    pip install -e .  # For development (editable install)
    pip install .     # For production install
"""

from pathlib import Path
from setuptools import setup, find_packages

# Read the README file for long description
README_PATH = Path(__file__).parent / "README.md"
if README_PATH.exists():
    with open(README_PATH, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "AI-Powered Business Assistant using Model Context Protocol"

# Read requirements from requirements.txt
REQUIREMENTS_PATH = Path(__file__).parent / "requirements.txt"
requirements = []
if REQUIREMENTS_PATH.exists():
    with open(REQUIREMENTS_PATH, "r", encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#") and not line.startswith("-")
        ]

# Separate development dependencies
dev_requirements = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0", 
    "pytest-mock>=3.11.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
    "isort>=5.12.0",
]

# Core requirements (excluding dev tools)
core_requirements = [
    req for req in requirements 
    if not any(dev_tool in req for dev_tool in ["pytest", "black", "flake8", "mypy", "isort"])
]

setup(
    name="agentmcp",
    version="1.0.0",
    description="AI-Powered Business Assistant using Model Context Protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="OnchainLabs",
    author_email="figueiredo.fabio@gmail.com",
    url="https://github.com/onchainlabs1/llm-agent-mcp",
    license="MIT",
    packages=find_packages(exclude=["tests*", "docs*"]),
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt", "*.yaml", "*.yml"],
        "mcp_server": ["*.json"],
        "data": ["*.json"],
        "logs": [".gitkeep"],
    },
    install_requires=core_requirements,
    extras_require={
        "dev": dev_requirements,
        "all": requirements,
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
    ],
    keywords=[
        "ai", "llm", "mcp", "model-context-protocol", "crm", "erp", "business-automation",
        "natural-language-processing", "streamlit", "pydantic"
    ],
    entry_points={
        "console_scripts": [
            "agentmcp-app=frontend.app:main",
            "agentmcp-setup=setup:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/onchainlabs1/llm-agent-mcp/issues",
        "Source": "https://github.com/onchainlabs1/llm-agent-mcp",
        "Documentation": "https://github.com/onchainlabs1/llm-agent-mcp#readme",
    },
    zip_safe=False,
)
 