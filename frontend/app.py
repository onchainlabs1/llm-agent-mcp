"""
AgentMCP Streamlit Frontend

This file implements the user interface for the AgentMCP system using Streamlit.
It allows end users to interact with the LLM agent via natural language, view
results, and monitor actions performed in the simulated business systems.

Key features:
- Natural language input for user requests
- Display of agent responses and tool actions
- Visualization of CRM, ERP, and HR data
- Action log viewer for audit and debugging
- Configuration management for API keys

All UI elements and comments must be in English.
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import agent modules
sys.path.append(str(Path(__file__).parent.parent))

from agent.agent_core import AgentCore, AgentConfig
from config import config

# Configure Streamlit page
st.set_page_config(
    page_title="AgentMCP – AI Business Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Lovable-style CSS (reutilizado da landing) ---
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, .stApp { background: #181c24; color: #f3f6fa; font-family: 'Inter', sans-serif; }
    .main { background: #181c24; }
    .block-container { padding-top: 110px !important; max-width: 100vw !important; margin-top: 0 !important; }
    .lovable-header {
        position: fixed;
        top: 0; left: 0; right: 0;
        background: #181c24;
        z-index: 100000;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 3vw;
        box-shadow: 0 2px 16px #0003;
        border-bottom: 1.5px solid #23283a;
    }
    .lovable-logo {
        font-size: 2.2rem;
        font-weight: 900;
        color: #6fffb0;
        letter-spacing: -1px;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        line-height: 1;
        user-select: none;
    }
    .lovable-logo svg {
        height: 2.2rem;
        width: 2.2rem;
        display: inline-block;
    }
    .lovable-nav {
        display: flex;
        gap: 2.7rem;
        align-items: center;
    }
    .lovable-nav a {
        color: #f3f6fa;
        font-size: 1.15rem;
        font-weight: 700;
        text-decoration: none;
        transition: color 0.2s;
        letter-spacing: 0.01em;
        padding: 2px 0;
        border-bottom: 2.5px solid transparent;
    }
    .lovable-nav a:hover {
        color: #6f47eb;
        border-bottom: 2.5px solid #6f47eb;
    }
    .prompt-chips {
        display: flex;
        gap: 1.1rem;
        margin-bottom: 1.2rem;
        flex-wrap: wrap;
    }
    .chip-btn {
        background: #23283a;
        color: #6fffb0;
        border: none;
        border-radius: 16px;
        padding: 0.5rem 1.3rem;
        font-size: 1.08rem;
        font-weight: 700;
        cursor: pointer;
        margin-bottom: 0.2rem;
        transition: background 0.2s, color 0.2s;
    }
    .chip-btn:hover { background: #3b82f6; color: #fff; }
    .response-card {
        background: #23283a;
        border-radius: 18px;
        box-shadow: 0 2px 16px #0002;
        padding: 2.1rem 2.2rem 1.5rem 2.2rem;
        margin-bottom: 2.5rem;
        margin-top: 1.2rem;
    }
    .response-title { font-size: 1.35rem; font-weight: 900; color: #6fffb0; margin-bottom: 0.7rem; }
    .response-status { font-size: 1.08rem; font-weight: 700; margin-bottom: 0.5rem; }
    .response-success { color: #22c55e; }
    .response-error { color: #ef4444; }
    .response-reason { color: #b0b8c9; font-size: 1.08rem; margin-bottom: 0.7rem; }
    .response-params { color: #fff; font-size: 1.05rem; margin-bottom: 0.7rem; }
    .response-result { color: #fff; font-size: 1.08rem; }
    .history-expander .stExpanderHeader { font-size: 1.13rem; font-weight: 700; }
    </style>
''', unsafe_allow_html=True)

# --- Configuration Sidebar ---
with st.sidebar:
    st.header("🔧 Configuration")
    
    # API Key Configuration
    st.subheader("🔑 API Keys")
    
    # Current LLM provider
    current_provider = config.llm.provider
    st.info(f"Current LLM Provider: **{current_provider}**")
    
    # Groq API Key input
    groq_api_key = st.text_input(
        "Groq API Key",
        value=config.llm.groq_api_key or "",
        type="password",
        help="Enter your Groq API key for better LLM performance"
    )
    
    # OpenAI API Key input
    openai_api_key = st.text_input(
        "OpenAI API Key",
        value=config.llm.openai_api_key or "",
        type="password",
        help="Enter your OpenAI API key (optional)"
    )
    
    # Provider selection
    selected_provider = st.selectbox(
        "LLM Provider",
        ["groq", "openai", "anthropic", "simulated"],
        index=["groq", "openai", "anthropic", "simulated"].index(current_provider),
        help="Select your preferred LLM provider"
    )
    
    # Update configuration button
    if st.button("💾 Update Configuration"):
        # Update environment variables
        if groq_api_key:
            os.environ['GROQ_API_KEY'] = groq_api_key
        if openai_api_key:
            os.environ['OPENAI_API_KEY'] = openai_api_key
        if selected_provider:
            os.environ['LLM_PROVIDER'] = selected_provider
        
        # Write to .env file
        env_content = f"""# AgentMCP Configuration
GROQ_API_KEY={groq_api_key}
OPENAI_API_KEY={openai_api_key}
LLM_PROVIDER={selected_provider}
LLM_MODEL=llama3-70b-8192
LOG_LEVEL=INFO
LOG_FILE=logs/actions.log
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        # Store in session state
        st.session_state['llm_provider'] = selected_provider
        st.session_state['groq_api_key'] = groq_api_key
        st.session_state['openai_api_key'] = openai_api_key
        
        # Clear agent cache to force reinitialization
        st.cache_resource.clear()
        
        st.success("✅ Configuration updated! Agent will use new settings.")
    
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
        ("logs/actions.log", "Action Logs")
    ]
    
    for file_path, description in data_files:
        if os.path.exists(file_path):
            st.success(f"✅ {description}")
        else:
            st.error(f"❌ {description}")
    
    # Available tools information
    st.subheader("🔧 Available Tools")
    st.markdown("""
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
    """)
    
    st.subheader("💡 Example Commands")
    st.markdown("""
    - "List all clients"
    - "Create a new client named John Doe with email john@example.com"
    - "Update client balance to 5000"
    - "Show all orders"
    - "Create order for client with 2 laptops"
    """)

# --- Header ---
st.markdown('''
<div class="lovable-header">
    <div class="lovable-logo">
        <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="g1" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#ff6f91"/>
                    <stop offset="1" stop-color="#6fffb0"/>
                </linearGradient>
            </defs>
            <path d="M16 29s-9-6.5-9-14.5A7 7 0 0 1 16 7a7 7 0 0 1 9 7.5C25 22.5 16 29 16 29Z" fill="url(#g1)"/>
            <circle cx="16" cy="13.5" r="3.5" fill="#fff"/>
            <rect x="13.5" y="21" width="5" height="5" rx="2.5" fill="#3b82f6"/>
            <rect x="10" y="25.5" width="12" height="3" rx="1.5" fill="#22c55e"/>
        </svg>
        AgentMCP
    </div>
    <div class="lovable-nav">
        <a href="#agent">Agent</a>
        <a href="#crm">CRM</a>
        <a href="#erp">ERP</a>
        <a href="#logs">Logs</a>
        <a href="#help">Help</a>
    </div>
</div>
''', unsafe_allow_html=True)

# --- Page Title ---
st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
st.markdown('<h1 style="text-align:center; font-size:2.5rem; font-weight:900; color:#fff; margin-bottom:0.7rem;">AgentMCP – AI Business Copilot</h1>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#b0b8c9; font-size:1.18rem; margin-bottom:2.2rem;">Automate CRM & ERP actions with natural language. Powered by LLM + MCP.</div>', unsafe_allow_html=True)

# --- Example prompt chips ---
prompt_examples = [
    "List all clients with balance over 5000",
    "Create a new client named Alice Smith with email alice@acme.com and balance 8000",
    "Update order ORD-20250601-001 to shipped",
    "Show all orders for client Acme Corp",
    "Create order for client John Doe for 2 laptops"
]

st.markdown('<div class="prompt-chips">' + ''.join([
    f'<button class="chip-btn" onclick="navigator.clipboard.writeText(\'{ex}\');window.dispatchEvent(new Event(\'input\'));">{ex}</button>' for ex in prompt_examples
]) + '</div>', unsafe_allow_html=True)

# --- Main prompt input ---
user_input = st.text_area(
    "Enter your request:",
    placeholder="Ex: Create a new client named John Doe with email john@example.com and balance 1000",
    height=80,
    help="Describe what you want to do in natural language"
)

col1, col2 = st.columns([1, 2])
with col1:
    send_button = st.button("🚀 Execute", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

# --- Initialize agent ---
@st.cache_resource(show_spinner=False)
def get_agent():
    """Initialize the agent with current configuration."""
    # Get current configuration
    current_config = config
    
    # Override with session state values if available
    provider = st.session_state.get('llm_provider', current_config.llm.provider)
    
    agent_config = AgentConfig(
        llm_provider=provider,
        llm_model=current_config.llm.model,
        log_level=current_config.logging.level
    )
    
    agent = AgentCore(agent_config)
    agent.load_all_mcp_schemas()
    return agent

# Initialize agent
agent = get_agent()

# --- Session state for history ---
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- Process request ---
if send_button and user_input.strip():
    with st.spinner("Processing your request..."):
        response = agent.process_user_request(user_input)
        st.session_state["history"].append({
            "input": user_input,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
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
    st.markdown(f'<div class="response-title">Result for: <span style="color:#6f47eb;">{last["input"]}</span></div>', unsafe_allow_html=True)
    if resp.get("success"):
        st.markdown('<div class="response-status response-success">✅ Success</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="response-status response-error">❌ Error</div>', unsafe_allow_html=True)
    if resp.get("reasoning"):
        st.markdown(f'<div class="response-reason"><b>Agent Reasoning:</b> {resp["reasoning"]}</div>', unsafe_allow_html=True)
    if resp.get("parameters"):
        st.markdown('<div class="response-params"><b>Parameters:</b></div>', unsafe_allow_html=True)
        st.json(resp["parameters"])
    if resp.get("result"):
        st.markdown('<div class="response-result"><b>Result:</b></div>', unsafe_allow_html=True)
        st.json(resp["result"])
    if resp.get("error_message"):
        st.markdown(f'<div class="response-result response-error"><b>Error:</b> {resp["error_message"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- History expander ---
with st.expander("🕑 Interaction History", expanded=False):
    for h in reversed(st.session_state["history"]):
        st.markdown(f'<div style="color:#b0b8c9; font-size:1.05rem; margin-bottom:0.2rem;"><b>{h["timestamp"][:19]}</b> — <span style="color:#6fffb0;">{h["input"]}</span></div>', unsafe_allow_html=True)
        resp = h["response"]
        if resp.get("success"):
            st.markdown('<span style="color:#22c55e;">✅ Success</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#ef4444;">❌ Error</span>', unsafe_allow_html=True)
        if resp.get("result"):
            st.json(resp["result"])
        st.markdown('<hr style="border:0;border-top:1px solid #23283a;">', unsafe_allow_html=True)

# --- Help/Examples section ---
st.markdown('<div style="margin-top:2.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="response-card"><b>💡 Example Prompts:</b><br>' + '<br>'.join(prompt_examples) + '</div>', unsafe_allow_html=True)

st.markdown('<div style="margin-bottom:2.5rem;"></div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown('<div style="margin-top:3rem;"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "AgentMCP - AI Business Assistant | Powered by Model Context Protocol"
    "</div>",
    unsafe_allow_html=True
) 