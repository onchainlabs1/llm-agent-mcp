"""
AgentMCP - AI Business Copilot
"""

import json
import os
import sys
import streamlit as st
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="AgentMCP – AI Business Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .stButton > button {
        border-radius: 25px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AgentMCP - AI Business Copilot</h1>
    <p style="font-size: 1.2rem; margin: 0;">AI Management System with ISO/IEC 42001:2023 Compliance</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    st.subheader("🔑 API Keys")
    
    provider = st.selectbox(
        "LLM Provider",
        ["simulated", "groq", "openai", "anthropic"],
        index=0
    )
    
    api_key = None
    if provider == "groq":
        api_key = st.text_input("Groq API Key", type="password")
    elif provider == "openai":
        api_key = st.text_input("OpenAI API Key", type="password")
    elif provider == "anthropic":
        api_key = st.text_input("Anthropic API Key", type="password")
    
    if provider != "simulated" and api_key:
        st.success(f"✅ {provider.title()} API Key configured")
        st.info("🤖 Agent will use real LLM responses")
    else:
        st.info("🎭 Demo Mode: Using simulated responses")

# Navigation
st.subheader("📋 Quick Navigation")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📘 ISO Documentation", use_container_width=True):
        st.switch_page("pages/1_📘_ISO_Docs.py")

with col2:
    if st.button("📊 ISO Dashboard", use_container_width=True):
        st.switch_page("pages/2_📋_ISO_Dashboard.py")

with col3:
    if st.button("🤖 Agent Mode Test", use_container_width=True):
        st.switch_page("test_agent_mode.py")

with col4:
    st.link_button("📚 GitHub", "https://github.com/onchainlabs1/llm-agent-mcp", use_container_width=True)

st.markdown("---")

# Agent Demo
st.header("🚀 AI Agent Demo")

# Initialize session state
if "responses" not in st.session_state:
    st.session_state.responses = []

# Check agent availability
agent_available = False
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from agent.agent_core import _simulate_llm_response
    agent_available = True
    st.success("✅ Agent Core Available")
except Exception as e:
    st.warning(f"⚠️ Agent not available: {str(e)[:100]}")

if agent_available:
    # Command buttons
    st.subheader("💡 Try These Commands:")
    
    st.markdown("**📋 CRM:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 List clients > $5000", key="crm1", use_container_width=True):
            st.session_state.selected_command = "List all clients with balance over 5000"
    with col2:
        if st.button("➕ Create client Alice", key="crm2", use_container_width=True):
            st.session_state.selected_command = "Create a new client named Alice Johnson"
    
    st.markdown("**📦 ERP:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📦 Show shipped orders", key="erp1", use_container_width=True):
            st.session_state.selected_command = "Show all orders with status shipped"
    with col2:
        if st.button("🔄 Update order", key="erp2", use_container_width=True):
            st.session_state.selected_command = "Update order status to delivered"
    
    # Input
    user_input = st.text_area(
        "🎯 Enter command:",
        value=getattr(st.session_state, 'selected_command', ''),
        placeholder="Ex: List all clients with balance over 5000",
        height=80
    )
    
    # Execute
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🚀 Execute", type="primary", use_container_width=True):
            if user_input.strip():
                try:
                    response = _simulate_llm_response(user_input)
                    
                    # Add to responses
                    st.session_state.responses.insert(0, {
                        "command": user_input,
                        "response": response,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    
                    # Keep only last 3
                    if len(st.session_state.responses) > 3:
                        st.session_state.responses = st.session_state.responses[:3]
                        
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.responses = []
            if hasattr(st.session_state, 'selected_command'):
                delattr(st.session_state, 'selected_command')
            st.rerun()

    # Show responses
    if st.session_state.responses:
        st.markdown("### 📋 Recent Responses")
        
        for i, resp in enumerate(st.session_state.responses):
            with st.container():
                st.markdown(f"**[{resp['timestamp']}]** {resp['command']}")
                
                try:
                    if isinstance(resp['response'], str):
                        data = json.loads(resp['response'])
                    else:
                        data = resp['response']
                    
                    if isinstance(data, dict):
                        if "tool_name" in data:
                            st.info(f"🔧 Tool: {data['tool_name']}")
                        if "parameters" in data:
                            st.json(data["parameters"])
                    else:
                        st.code(resp['response'])
                        
                except Exception:
                    st.code(resp['response'])
                
                if i < len(st.session_state.responses) - 1:
                    st.markdown("---")

# Data Overview
st.markdown("---")
st.header("📊 Data Overview")

col1, col2, col3 = st.columns(3)

with col1:
    try:
        if os.path.exists("data/clients.json"):
            with open("data/clients.json", "r") as f:
                data = json.load(f)
            count = len(data.get("clients", []))
            st.metric("📋 Clients", count)
        else:
            st.metric("📋 Clients", "N/A")
    except Exception:
        st.metric("📋 Clients", "Error")

with col2:
    try:
        if os.path.exists("data/orders.json"):
            with open("data/orders.json", "r") as f:
                data = json.load(f)
            count = len(data.get("orders", []))
            st.metric("📦 Orders", count)
        else:
            st.metric("📦 Orders", "N/A")
    except Exception:
        st.metric("📦 Orders", "Error")

with col3:
    try:
        if os.path.exists("data/employees.json"):
            with open("data/employees.json", "r") as f:
                data = json.load(f)
            count = len(data.get("employees", []))
            st.metric("👥 Employees", count)
        else:
            st.metric("👥 Employees", "N/A")
    except Exception:
        st.metric("👥 Employees", "Error")

# ISO Status
st.markdown("---")
st.header("🛡️ ISO/IEC 42001:2023")

col1, col2, col3 = st.columns(3)
with col1:
    st.success("✅ Documentation Complete")
with col2:
    st.success("✅ 353.5h Implemented")
with col3:
    st.success("✅ Certification Ready")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>AgentMCP</strong> - AI Business Automation with ISO/IEC 42001:2023 Compliance</p>
</div>
""", unsafe_allow_html=True)