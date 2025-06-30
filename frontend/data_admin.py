import streamlit as st
import json
import os
from pathlib import Path

st.set_page_config(
    page_title="AgentMCP Data Admin",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Lovable-style CSS ---
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, .stApp { background: #181c24; color: #f3f6fa; font-family: 'Inter', sans-serif; }
    .main { background: #181c24; }
    .block-container { padding-top: 60px !important; max-width: 100vw !important; margin-top: 0 !important; }
    .lovable-header {
        position: fixed;
        top: 0; left: 0; right: 0;
        background: #181c24;
        z-index: 100000;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 3vw;
        box-shadow: 0 2px 16px #0003;
        border-bottom: 1.5px solid #23283a;
    }
    .lovable-logo {
        font-size: 1.5rem;
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
        height: 1.5rem;
        width: 1.5rem;
        display: inline-block;
    }
    </style>
''', unsafe_allow_html=True)

# --- Header ---
st.markdown('''
<div class="lovable-header">
    <div class="lovable-logo">
        <svg viewBox="0 0 32 32" fill="none"><defs><linearGradient id="g1" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse"><stop stop-color="#ff6f91"/><stop offset="1" stop-color="#6fffb0"/></linearGradient></defs><path d="M16 29s-9-6.5-9-14.5A7 7 0 0 1 16 7a7 7 0 0 1 9 7.5C25 22.5 16 29 16 29Z" fill="url(#g1)"/><circle cx="16" cy="13.5" r="3.5" fill="#fff"/><rect x="13.5" y="21" width="5" height="5" rx="2.5" fill="#3b82f6"/><rect x="10" y="25.5" width="12" height="3" rx="1.5" fill="#22c55e"/></svg>
        AgentMCP Data Admin
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

# --- Tabs ---
tabs = st.tabs(["CRM Data", "ERP Data", "Products", "Settings"])

# --- CRM Data Tab ---
with tabs[0]:
    st.markdown('<h2 style="font-size:2rem; font-weight:900; color:#fff; margin-bottom:1.2rem;">CRM Data – Clients</h2>', unsafe_allow_html=True)
    clients_path = Path("data/clients.json")
    if clients_path.exists():
        with open(clients_path) as f:
            clients = json.load(f)
        if clients:
            st.dataframe(clients, use_container_width=True, hide_index=True)
        else:
            st.info("No clients found.")
    else:
        st.error("clients.json not found in data/ directory.")

# --- ERP Data Tab ---
with tabs[1]:
    st.markdown('<h2 style="font-size:2rem; font-weight:900; color:#fff; margin-bottom:1.2rem;">ERP Data – Orders</h2>', unsafe_allow_html=True)
    orders_path = Path("data/orders.json")
    if orders_path.exists():
        with open(orders_path) as f:
            orders = json.load(f)
        if orders:
            st.dataframe(orders, use_container_width=True, hide_index=True)
        else:
            st.info("No orders found.")
    else:
        st.error("orders.json not found in data/ directory.")

# --- Products Tab ---
with tabs[2]:
    st.markdown('<h2 style="font-size:2rem; font-weight:900; color:#fff; margin-bottom:1.2rem;">Products</h2>', unsafe_allow_html=True)
    products_path = Path("data/products.json")
    if products_path.exists():
        with open(products_path) as f:
            products = json.load(f)
        if products:
            st.dataframe(products, use_container_width=True, hide_index=True)
        else:
            st.info("No products found.")
    else:
        st.error("products.json not found in data/ directory.")

# --- Settings Tab (placeholder) ---
with tabs[3]:
    st.markdown('<h2 style="font-size:2rem; font-weight:900; color:#fff; margin-bottom:1.2rem;">Settings</h2>', unsafe_allow_html=True)
    st.info("Data reset and configuration options coming soon.") 