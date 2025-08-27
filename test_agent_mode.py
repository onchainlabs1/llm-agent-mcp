#!/usr/bin/env python3
"""
Agent Mode Test for Streamlit Cloud

Simple test to verify agent functionality works in Streamlit Cloud environment.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Agent Mode Test",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agent Mode Test")
st.write("Testing agent functionality in Streamlit Cloud environment.")

# Test 1: Basic imports
st.write("## ✅ Basic Imports Test")
try:
    from agent.agent_core import call_llm
    st.success("✅ Agent core imported successfully")
except ImportError as e:
    st.error(f"❌ Agent core import failed: {e}")

# Test 2: Configuration
st.write("## ✅ Configuration Test")
try:
    from agent_config import agent_config
    st.success("✅ Agent config imported successfully")
    st.write(f"LLM Provider: {agent_config.llm_provider}")
    st.write(f"Simulated Mode: {agent_config.is_simulated_mode()}")
except ImportError as e:
    st.error(f"❌ Agent config import failed: {e}")

# Test 3: ISO Controls
st.write("## ✅ ISO Controls Test")
try:
    from agent.iso_controls import ISO42001Controls
    iso_controls = ISO42001Controls()
    st.success("✅ ISO controls imported and initialized successfully")
    
    # Test prompt sanitization
    test_prompt = "Hello <script>alert('test')</script> world"
    sanitized = iso_controls.sanitize_prompt(test_prompt)
    st.write(f"Original prompt: {test_prompt}")
    st.write(f"Sanitized prompt: {sanitized}")
    
except ImportError as e:
    st.error(f"❌ ISO controls import failed: {e}")

# Test 4: MCP Tools
st.write("## ✅ MCP Tools Test")
try:
    from agent.tools_mcp_client import MCPToolRegistry
    st.success("✅ MCP tools imported successfully")
except ImportError as e:
    st.error(f"❌ MCP tools import failed: {e}")

# Test 5: Data Access
st.write("## ✅ Data Access Test")
try:
    data_path = Path("data")
    if data_path.exists():
        st.success("✅ Data directory accessible")
        files = list(data_path.glob("*.json"))
        st.write(f"Found {len(files)} JSON files")
        for file in files[:5]:  # Show first 5 files
            st.write(f"- {file.name}")
    else:
        st.warning("⚠️ Data directory not found")
except Exception as e:
    st.error(f"❌ Data access failed: {e}")

# Test 6: Agent Functionality
st.write("## ✅ Agent Functionality Test")
try:
    if 'call_llm' in locals():
        # Test simulated response
        test_response = call_llm("Hello, this is a test prompt")
        if isinstance(test_response, dict):
            st.success("✅ Agent LLM function working (simulated mode)")
            st.write("Response structure:", list(test_response.keys()))
        else:
            st.success("✅ Agent LLM function working (direct response)")
    else:
        st.warning("⚠️ Agent LLM function not available")
except Exception as e:
    st.error(f"❌ Agent functionality test failed: {e}")

st.success("🎉 Agent mode test completed!")
st.info("If all tests pass, the agent mode is ready for use in Streamlit Cloud.")
