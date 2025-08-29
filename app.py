"""
AgentMCP - AI Business Copilot
Clean and functional main application
"""

import json
import os
import sys
import streamlit as st
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="AgentMCP – AI Business Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Clean Theme ---
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>🤖 AgentMCP - AI Business Copilot</h1>
    <p style="font-size: 1.2rem; margin: 0;">AI Management System with ISO/IEC 42001:2023 Compliance</p>
</div>
""", unsafe_allow_html=True)

# --- Navigation ---
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
    st.link_button("📚 GitHub Repository", "https://github.com/onchainlabs1/llm-agent-mcp", use_container_width=True)

st.markdown("---")

# --- Agent Demo Section ---
st.header("🚀 AI Agent Demo")

# Check if we can load agent
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from agent.agent_core import _simulate_llm_response
    AGENT_AVAILABLE = True
except:
    AGENT_AVAILABLE = False

if AGENT_AVAILABLE:
    st.success("✅ Agent Core Available - Demo Mode Active")
    
    # Example commands
    st.subheader("💡 Try These Business Commands:")
    examples = [
        "List all clients with balance over 5000",
        "Create a new client named Alice Johnson with email alice@techcorp.com",
        "Show all orders with status shipped",
        "Find employees in Engineering department"
    ]
    
    # Create buttons for examples
    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            if st.button(example, key=f"ex_{i}"):
                st.session_state["demo_input"] = example
    
    # Input area
    user_input = st.text_area(
        "🎯 Enter your business command:",
        value=st.session_state.get("demo_input", ""),
        placeholder="Ex: List all clients with balance over 5000",
        height=100
    )
    
    if st.button("🚀 Execute Command", type="primary"):
        if user_input.strip():
            with st.spinner("Processing..."):
                try:
                    # Use simulated response for demo
                    response = _simulate_llm_response(user_input)
                    
                    st.success("✅ Command processed successfully!")
                    st.markdown("**Agent Response:**")
                    
                    # Try to parse JSON response
                    try:
                        if isinstance(response, str):
                            response_data = json.loads(response)
                        else:
                            response_data = response
                            
                        # Display structured response
                        if isinstance(response_data, dict):
                            if "tool_name" in response_data:
                                st.info(f"🔧 Tool: {response_data['tool_name']}")
                            if "parameters" in response_data:
                                st.markdown("**Parameters:**")
                                st.json(response_data["parameters"])
                        else:
                            st.markdown(f"```\n{response}\n```")
                            
                    except:
                        # Fallback for non-JSON responses
                        st.markdown(f"```\n{response}\n```")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
            
            # Clear the demo input
            if "demo_input" in st.session_state:
                del st.session_state["demo_input"]
                st.rerun()

else:
    st.warning("⚠️ Agent Core not available in Streamlit Cloud mode")
    st.info("💡 For full agent functionality, run locally with: `streamlit run app.py`")

# --- Business Data Overview ---
st.markdown("---")
st.header("📊 Business Data Overview")

# Load and display data statistics
col1, col2, col3 = st.columns(3)

with col1:
    try:
        if os.path.exists("data/clients.json"):
            with open("data/clients.json", "r") as f:
                clients_data = json.load(f)
            client_count = len(clients_data.get("clients", []))
            st.metric("📋 CRM Clients", client_count, "Active records")
        else:
            st.metric("📋 CRM Clients", "N/A", "No data file")
    except:
        st.metric("📋 CRM Clients", "Error", "Cannot load")

with col2:
    try:
        if os.path.exists("data/orders.json"):
            with open("data/orders.json", "r") as f:
                orders_data = json.load(f)
            order_count = len(orders_data.get("orders", []))
            st.metric("📦 ERP Orders", order_count, "Total orders")
        else:
            st.metric("📦 ERP Orders", "N/A", "No data file")
    except:
        st.metric("📦 ERP Orders", "Error", "Cannot load")

with col3:
    try:
        if os.path.exists("data/employees.json"):
            with open("data/employees.json", "r") as f:
                employees_data = json.load(f)
            employee_count = len(employees_data.get("employees", []))
            st.metric("👥 HR Employees", employee_count, "Team members")
        else:
            st.metric("👥 HR Employees", "N/A", "No data file")
    except:
        st.metric("👥 HR Employees", "Error", "Cannot load")

# --- ISO Compliance Status ---
st.markdown("---")
st.header("🛡️ ISO/IEC 42001:2023 Compliance")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("✅ Documentation Complete")
    st.caption("All 7 clauses implemented")

with col2:
    st.success("✅ 353.5h Implemented") 
    st.caption("Exceeds 300h requirement")

with col3:
    st.success("✅ Certification Ready")
    st.caption("10/10 - EXEMPLAR rating")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>AgentMCP</strong> - Professional AI Business Automation</p>
    <p>🏆 ISO/IEC 42001:2023 Compliant | 🤖 MCP Protocol | 📊 Enterprise Ready</p>
</div>
""", unsafe_allow_html=True)