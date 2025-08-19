"""
AgentMCP Streamlit Frontend - Simplified Version for Streamlit Cloud

This is a simplified version that works on Streamlit Cloud without external dependencies.
"""

import streamlit as st
import os

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

# --- Main Content ---
st.markdown("---")

# Welcome message
st.markdown("## 🚀 Welcome to AgentMCP!")

st.markdown("""
This is a simplified version of the AgentMCP system designed to work on Streamlit Cloud.

### 🎯 **What is AgentMCP?**

AgentMCP is an AI-powered business automation system that combines:
- **Large Language Models (LLMs)** for natural language understanding
- **Model Context Protocol (MCP)** for tool integration
- **Business System APIs** for CRM, ERP, and HR automation

### 🔧 **Key Features**

✅ **Natural Language Interface** - Talk to your business systems in plain English  
✅ **Multi-System Integration** - Connect CRM, ERP, and HR systems  
✅ **Automated Workflows** - Streamline repetitive business processes  
✅ **Audit Trail** - Complete logging of all actions for compliance  
✅ **ISO 42001 Compliance** - Built-in governance and risk management  

### 📊 **Current Status**

🟢 **Dashboard**: ISO Compliance Dashboard fully functional  
🟢 **Documentation**: Complete ISO 42001 documentation available  
🟡 **Agent Core**: Available in local development mode  
🟡 **MCP Integration**: Available in local development mode  

### 🚀 **Getting Started**

1. **View ISO Dashboard** - Click the "ISO Dashboard" button above
2. **Review Documentation** - Click the "ISO Docs" button above
3. **Local Development** - Clone the repo for full agent functionality

### 🔗 **Quick Links**

- **ISO Dashboard**: Complete compliance overview and metrics
- **ISO Documentation**: Full governance framework documentation
- **GitHub Repository**: Source code and development resources
""")

# --- Configuration Sidebar ---
with st.sidebar:
    st.header("🔧 Configuration")
    
    st.info("""
    **Streamlit Cloud Mode**
    
    This simplified version runs on Streamlit Cloud without external dependencies.
    
    For full functionality with LLM agents and MCP integration, run locally:
    ```bash
    git clone https://github.com/onchainlabs1/llm-agent-mcp
    cd llm-agent-mcp
    pip install -r requirements.txt
    streamlit run app.py
    ```
    """)
    
    st.markdown("---")
    
    st.header("📚 Resources")
    st.link_button("📖 Project README", f"{REPO_BASE}/blob/main/README.md")
    st.link_button("🔧 Development Guide", f"{REPO_BASE}/blob/main/DEVELOPMENT.md")
    st.link_button("📋 Project Rules", f"{REPO_BASE}/blob/main/PROJECT_RULES.md")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.9rem;">
    <p>AgentMCP - AI Business Copilot | Built with Streamlit | ISO 42001 Compliant</p>
    <p>For full functionality, run locally with complete dependencies</p>
</div>
""", unsafe_allow_html=True)
