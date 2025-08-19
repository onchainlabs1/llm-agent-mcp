"""
AgentMCP Streamlit Frontend - Streamlit Cloud Compatible

This version works on Streamlit Cloud with full functionality but simulated mode.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import streamlit as st

# Configure for Streamlit Cloud deployment
# Force simulated mode by default for cloud deployment
os.environ.setdefault('LLM_PROVIDER', 'simulated')

# Configure Streamlit page
st.set_page_config(
    page_title="AgentMCP – AI Business Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Dark theme CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    /* Main background and text colors */
    .main .block-container {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #0e1117;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1f2b;
    }
    
    /* Custom component styling */
    .prompt-chips { display: flex; gap: 1.1rem; margin-bottom: 1.2rem; flex-wrap: wrap; }
    .chip-btn {
        background: #1a1f2b; color: #6fffb0; border: 1px solid #2b3345; border-radius: 16px;
        padding: 0.5rem 1.1rem; font-size: 1rem; font-weight: 700; cursor: pointer; margin-bottom: 0.2rem;
    }
    .chip-btn:hover { background: #3b82f6; color: #ffffff; }
    .response-card { background: #111827; border: 1px solid #2b3345; border-radius: 12px; padding: 1.4rem; }
    .response-title { font-size: 1.15rem; font-weight: 800; color: #6fffb0; margin-bottom: 0.6rem; }
    .response-status { font-size: 1rem; font-weight: 700; margin-bottom: 0.4rem; }
    .response-success { color: #22c55e; }
    .response-error { color: #ef4444; }
    .response-reason { color: #9ca3af; font-size: 0.98rem; margin-bottom: 0.6rem; }
    .response-params { color: #e5e7eb; font-size: 0.98rem; margin-bottom: 0.6rem; }
    .response-result { color: #e5e7eb; font-size: 1rem; }
    .history-expander .stExpanderHeader { font-size: 1.03rem; font-weight: 700; }
    
    /* Override Streamlit default colors for dark theme */
    .stTextInput > div > div > input {
        background-color: #1a1f2b !important;
        color: #ffffff !important;
        border-color: #2b3345 !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #1a1f2b !important;
        color: #ffffff !important;
        border-color: #2b3345 !important;
    }
    
    .stSelectbox > div > div > div {
        background-color: #1a1f2b !important;
        color: #ffffff !important;
        border-color: #2b3345 !important;
    }
    
    .stButton > button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
    }
    
    .stButton > button:hover {
        background-color: #2563eb !important;
        border-color: #2563eb !important;
    }
    
    /* Data display styling */
    .stJson {
        background-color: #1a1f2b !important;
        border: 1px solid #2b3345 !important;
        border-radius: 8px !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1a1f2b !important;
        color: #6fffb0 !important;
        border-color: #2b3345 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Quick navigation links
REPO_BASE = "https://github.com/onchainlabs1/llm-agent-mcp"

# --- Header / Title ---
st.markdown('<div style="height: 6px"></div>', unsafe_allow_html=True)
st.title("AgentMCP – AI Business Copilot")
st.caption("Automate CRM & ERP actions with natural language. Powered by LLM + MCP.")

# Top navigation buttons
nav1, nav2, nav3 = st.columns(3)
with nav1:
    st.link_button("📘 ISO Docs", "/iso_docs", use_container_width=True)
with nav2:
    st.link_button("📋 ISO Dashboard", "/iso_dashboard", use_container_width=True)
with nav3:
    st.link_button("📚 GitHub", REPO_BASE, use_container_width=True)

# --- Configuration Sidebar ---
with st.sidebar:
    st.header("🔧 Configuration")
    
    # API Key Configuration
    st.subheader("🔑 API Keys")
    
    # Current LLM provider
    current_provider = "simulated"  # Default for Streamlit Cloud
    st.info(f"Current LLM Provider: **{current_provider}**")
    
    # Groq API Key input
    groq_api_key = st.text_input(
        "Groq API Key",
        value="",
        type="password",
        help="Enter your Groq API key for better LLM performance",
    )
    
    # OpenAI API Key input
    openai_api_key = st.text_input(
        "OpenAI API Key",
        value="",
        type="password",
        help="Enter your OpenAI API key (optional)",
    )
    
    # Provider selection
    selected_provider = st.selectbox(
        "LLM Provider",
        ["simulated", "groq", "openai", "anthropic"],
        index=0,  # Default to simulated
        help="Select your preferred LLM provider",
    )
    
    # Update configuration button
    if st.button("💾 Update Configuration"):
        # Store in session state
        st.session_state["llm_provider"] = selected_provider
        st.session_state["groq_api_key"] = groq_api_key
        st.session_state["openai_api_key"] = openai_api_key
        
        st.success("✅ Configuration updated! (Note: Full functionality requires local deployment)")
    
    # Status indicators
    st.subheader("📊 System Status")
    
    # Check API key status
    if groq_api_key and groq_api_key != "your-groq-api-key-here":
        st.success("✅ Groq API Key configured")
    else:
        st.warning("⚠️ No Groq API Key (using simulated mode)")
    
    # Check data files
    data_files = [
        ("data/clients.json", "CRM Data"),
        ("mcp_server/crm_mcp.json", "MCP Schema"),
        ("logs/actions.log", "Action Logs"),
    ]
    
    for file_path, description in data_files:
        if os.path.exists(file_path):
            st.success(f"✅ {description}")
        else:
            st.error(f"❌ {description}")
    
    # Available tools information
    st.subheader("🔧 Available Tools")
    st.markdown(
        """
    **CRM Tools:**
    - **get_client_by_id** - Retrieve client information
    - **create_client** - Create new client records
    - **update_client_balance** - Update client account balance
    - **list_all_clients** - List all registered clients
    
    **ERP Tools:**
    - **get_order_by_id** - Retrieve order information
    - **create_order** - Create new order records
    - **update_order_status** - Update order status
    - **list_all_orders** - List all orders
    """
    )
    
    st.subheader("💡 Example Commands")
    st.markdown(
        """
    - "List all clients"
    - "Create a new client named John Doe with email john@example.com"
    - "Update client balance to 5000"
    - "Show all orders"
    - "Create order for client with 2 laptops"
    """
    )
    
    st.info("""
    **Streamlit Cloud Mode**
    
    This version runs on Streamlit Cloud with simulated functionality.
    
    For full functionality with LLM agents and MCP integration, run locally:
    ```bash
    git clone https://github.com/onchainlabs1/llm-agent-mcp
    cd llm-agent-mcp
    pip install -r requirements.txt
    streamlit run app_full.py
    ```
    """)

# --- Main prompt input ---
user_input = st.text_area(
    "Enter your request:",
    placeholder="Ex: Create a new client named John Doe with email john@example.com and balance 1000",
    height=80,
    help="Describe what you want to do in natural language",
)

col1, col2 = st.columns([1, 2])
with col1:
    send_button = st.button("🚀 Execute", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

# --- Simulated agent functionality ---
def simulate_agent_response(user_input):
    """Simulate agent response for Streamlit Cloud compatibility."""
    
    # Simple keyword-based responses for demo
    input_lower = user_input.lower()
    
    if "client" in input_lower and "create" in input_lower:
        return {
            "success": True,
            "reasoning": "Creating new client based on user request",
            "parameters": {"action": "create_client", "input": user_input},
            "result": {
                "client_id": "CLI_001",
                "name": "John Doe",
                "email": "john@example.com",
                "balance": 1000,
                "status": "created"
            }
        }
    elif "client" in input_lower and "list" in input_lower:
        return {
            "success": True,
            "reasoning": "Listing all clients from CRM system",
            "parameters": {"action": "list_clients"},
            "result": [
                {"id": "CLI_001", "name": "John Doe", "email": "john@example.com", "balance": 1000},
                {"id": "CLI_002", "name": "Jane Smith", "email": "jane@example.com", "balance": 2500}
            ]
        }
    elif "order" in input_lower and "create" in input_lower:
        return {
            "success": True,
            "reasoning": "Creating new order based on user request",
            "parameters": {"action": "create_order", "input": user_input},
            "result": {
                "order_id": "ORD_001",
                "client_id": "CLI_001",
                "items": ["2 laptops"],
                "status": "pending",
                "total": 2400
            }
        }
    elif "order" in input_lower and "list" in input_lower:
        return {
            "success": True,
            "reasoning": "Listing all orders from ERP system",
            "parameters": {"action": "list_orders"},
            "result": [
                {"id": "ORD_001", "client": "John Doe", "items": ["2 laptops"], "total": 2400, "status": "pending"}
            ]
        }
    else:
        return {
            "success": False,
            "reasoning": "Request not recognized in simulated mode",
            "error_message": "This is a simulated response. For full functionality, run locally with app_full.py",
            "parameters": {"input": user_input}
        }

# --- Session state for history ---
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- Process request ---
if send_button and user_input.strip():
    with st.spinner("Processing your request..."):
        response = simulate_agent_response(user_input)
        st.session_state["history"].append(
            {
                "input": user_input,
                "response": response,
                "timestamp": datetime.now().isoformat(),
            }
        )
        user_input = ""
        st.rerun()

if clear_button:
    st.session_state["history"] = []
    st.rerun()

# --- Show last response in a card ---
if st.session_state["history"]:
    last = st.session_state["history"][-1]
    resp = last["response"]
    st.markdown('<div class="response-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="response-title">Result for: <span style="color:#6f47eb;">{last["input"]}</span></div>',
        unsafe_allow_html=True,
    )
    if resp.get("success"):
        st.markdown(
            '<div class="response-status response-success">✅ Success</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="response-status response-error">❌ Error</div>',
            unsafe_allow_html=True,
        )
    if resp.get("reasoning"):
        st.markdown(
            f'<div class="response-reason"><b>Agent Reasoning:</b> {resp["reasoning"]}</div>',
            unsafe_allow_html=True,
        )
    if resp.get("parameters"):
        st.markdown(
            '<div class="response-params"><b>Parameters:</b></div>',
            unsafe_allow_html=True,
        )
        st.json(resp["parameters"])
    if resp.get("result"):
        st.markdown(
            '<div class="response-result"><b>Result:</b></div>', unsafe_allow_html=True
        )
        st.json(resp["result"])
    if resp.get("error_message"):
        st.markdown(
            f'<div class="response-result response-error"><b>Error:</b> {resp["error_message"]}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# --- History expander ---
with st.expander("🕑 Interaction History", expanded=False):
    for h in reversed(st.session_state["history"]):
        st.markdown(
            f'<div style="color:#b0b8c9; font-size:1.05rem; margin-bottom:0.2rem;"><b>{h["timestamp"][:19]}</b> — <span style="color:#6fffb0;">{h["input"]}</span></div>',
            unsafe_allow_html=True,
        )
        resp = h["response"]
        if resp.get("success"):
            st.markdown(
                '<span style="color:#22c55e;">✅ Success</span>', unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span style="color:#ef4444;">❌ Error</span>', unsafe_allow_html=True
            )
        if resp.get("result"):
            st.json(resp["result"])
        st.markdown(
            '<hr style="border:0;border-top:1px solid #23283a;">',
            unsafe_allow_html=True,
        )

# --- Help/Examples section ---
st.markdown('<div style="margin-top:2.5rem;"></div>', unsafe_allow_html=True)

st.markdown('<div style="margin-bottom:2.5rem;"></div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown('<div style="margin-top:3rem;"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "AgentMCP - AI Business Assistant | Powered by Model Context Protocol"
    "</div>",
    unsafe_allow_html=True,
)
