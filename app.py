"""
AgentMCP Streamlit Frontend - Ultra-Simplified Streamlit Cloud Version

This version works on Streamlit Cloud with minimal dependencies.
"""

import streamlit as st
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="AgentMCP – AI Business Copilot",
    page_icon="🤖",
    layout="wide",
)

# Main title
st.title("🤖 AgentMCP - AI Business Copilot")
st.markdown("AI Management System with ISO/IEC 42001:2023 Compliance")

st.markdown("---")

# Main content
st.header("🚀 Welcome to AgentMCP")
st.markdown("""
This is a reference implementation of an AI Management System (AIMS) 
compliant with ISO/IEC 42001:2023, demonstrating best practices in 
AI governance, risk management, and compliance.
""")

# Quick navigation
st.subheader("📋 Quick Navigation")
col1, col2 = st.columns(2)

with col1:
    if st.button("📘 ISO Documentation", use_container_width=True):
        st.switch_page("pages/1_📘_ISO_Docs.py")

with col2:
    if st.button("📊 ISO Dashboard", use_container_width=True):
        st.switch_page("pages/2_📋_ISO_Dashboard.py")

st.markdown("---")

# System Status
st.subheader("🔧 System Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.success("✅ ISO Controls")
    st.caption("R001, R002, R003, R008")

with col2:
    st.success("✅ Data Encryption")
    st.caption("CRM, ERP, HR Services")

with col3:
    st.success("✅ Compliance")
    st.caption("84.4% Ready")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #666;">
    AgentMCP - AI Business Assistant | Powered by Model Context Protocol
</div>
""", unsafe_allow_html=True)
