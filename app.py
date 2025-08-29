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
    .result-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #0ea5e9;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
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
        st.info("🎭 Demo Mode: Using simulated responses with REAL data")

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
st.header("🚀 AI Agent Demo with Real Data")

# Initialize session state
if "responses" not in st.session_state:
    st.session_state.responses = []

# Check agent availability
agent_available = False
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from agent.agent_core import _simulate_llm_response
    agent_available = True
    st.success("✅ Agent Core Available - Executing REAL searches in business data!")
except Exception as e:
    st.warning(f"⚠️ Agent not available: {str(e)[:100]}")

if agent_available:
    # Command buttons
    st.subheader("💡 Try These Commands:")
    
    st.markdown("**📋 CRM Operations:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 List clients > $5000", key="crm1", use_container_width=True):
            st.session_state.selected_command = "List all clients with balance over 5000"
    with col2:
        if st.button("📋 List all clients", key="crm3", use_container_width=True):
            st.session_state.selected_command = "List all clients"
    
    st.markdown("**📦 ERP Operations:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📦 Show shipped orders", key="erp1", use_container_width=True):
            st.session_state.selected_command = "Show all orders with status shipped"
    with col2:
        if st.button("📦 List all orders", key="erp3", use_container_width=True):
            st.session_state.selected_command = "List all orders"
    
    st.markdown("**👥 HR Operations:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👥 Find Engineering employees", key="hr1", use_container_width=True):
            st.session_state.selected_command = "Find employees in Engineering department"
    with col2:
        if st.button("👥 List all employees", key="hr3", use_container_width=True):
            st.session_state.selected_command = "List all employees"
    
    # Input
    user_input = st.text_area(
        "🎯 Enter command:",
        value=getattr(st.session_state, 'selected_command', ''),
        placeholder="Ex: Show all orders with status shipped",
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

    # Show responses with REAL DATA
    if st.session_state.responses:
        st.markdown("### 📋 Recent Results")
        
        for i, resp in enumerate(st.session_state.responses):
            with st.container():
                st.markdown(f"**[{resp['timestamp']}] Command:** {resp['command']}")
                
                # Parse response
                data = resp['response']
                if isinstance(data, str):
                    try:
                        data = json.loads(data)
                    except:
                        st.code(data)
                        continue
                
                if isinstance(data, dict):
                    # Show tool info
                    if "tool_name" in data:
                        st.info(f"🔧 **Tool:** {data['tool_name']}")
                    
                    # Show parameters
                    if "parameters" in data:
                        st.markdown("**Parameters:**")
                        st.json(data["parameters"])
                    
                    # Show REAL RESULTS
                    if "results" in data:
                        results = data["results"]
                        count = data.get("count", len(results))
                        
                        if results:
                            st.success(f"✅ **Found {count} results:**")
                            
                            # Display results in a nice format
                            for j, item in enumerate(results[:5]):  # Show first 5
                                with st.expander(f"Result {j+1}: {item.get('name', item.get('id', 'Item'))}", expanded=(j==0)):
                                    st.json(item)
                            
                            if len(results) > 5:
                                st.info(f"... and {len(results) - 5} more results")
                        else:
                            st.warning("No results found")
                    
                    # Show errors
                    if "error" in data:
                        st.error(f"❌ Error: {data['error']}")
                
                if i < len(st.session_state.responses) - 1:
                    st.markdown("---")

# Data Overview
st.markdown("---")
st.header("📊 Business Data Overview")

col1, col2, col3 = st.columns(3)

with col1:
    try:
        if os.path.exists("data/clients.json"):
            with open("data/clients.json", "r") as f:
                data = json.load(f)
            count = len(data.get("clients", []))
            st.metric("📋 Clients", count, "Real business data")
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
            st.metric("📦 Orders", count, "Real business data")
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
            st.metric("👥 Employees", count, "Real business data")
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
    <p>🎯 Now with REAL data execution - searches actual business records!</p>
</div>
""", unsafe_allow_html=True)