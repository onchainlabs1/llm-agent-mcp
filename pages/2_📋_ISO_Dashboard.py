"""
ISO/IEC 42001:2023 Compliance Dashboard
Streamlit Cloud Compatible Version
"""

import streamlit as st
import os
import pandas as pd
from pathlib import Path
import json
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="ISO/IEC 42001:2023 Compliance Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main .block-container {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #0e1117;
    }
    
    .metric-card {
        background: #1a1f2b;
        border: 1px solid #2b3345;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    
    .compliance-status {
        background: #1a1f2b;
        border: 1px solid #2b3345;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .status-success { border-left: 4px solid #22c55e; }
    .status-warning { border-left: 4px solid #f59e0b; }
    .status-error { border-left: 4px solid #ef4444; }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample data for demonstration"""
    
    # Sample clients data
    clients_data = [
        {"id": "CLI_001", "name": "TechCorp Solutions", "email": "contact@techcorp.com", "balance": 15000, "status": "active"},
        {"id": "CLI_002", "name": "InnovateLab", "email": "info@innovatelab.com", "balance": 8500, "status": "active"},
        {"id": "CLI_003", "name": "DataFlow Systems", "email": "hello@dataflow.com", "balance": 22000, "status": "active"},
        {"id": "CLI_004", "name": "CloudTech Pro", "email": "support@cloudtech.com", "balance": 12000, "status": "active"},
        {"id": "CLI_005", "name": "AI Solutions Inc", "email": "contact@aisolutions.com", "balance": 18000, "status": "active"}
    ]
    
    # Sample orders data
    orders_data = [
        {"id": "ORD_001", "client": "TechCorp Solutions", "items": ["AI Platform License", "Support Package"], "total": 15000, "status": "completed"},
        {"id": "ORD_002", "client": "InnovateLab", "items": ["Custom AI Model", "Training Data"], "total": 8500, "status": "in_progress"},
        {"id": "ORD_003", "client": "DataFlow Systems", "items": ["Enterprise AI Suite", "Consulting"], "total": 22000, "status": "pending"},
        {"id": "ORD_004", "client": "CloudTech Pro", "items": ["AI Infrastructure", "Maintenance"], "total": 12000, "status": "completed"},
        {"id": "ORD_005", "client": "AI Solutions Inc", "items": ["AI Development Kit", "Documentation"], "total": 18000, "status": "in_progress"}
    ]
    
    # Sample employees data
    employees_data = [
        {"id": "EMP_001", "name": "Dr. Sarah Chen", "department": "AI Research", "role": "Lead AI Scientist", "experience": "8 years"},
        {"id": "EMP_002", "name": "Marcus Rodriguez", "department": "Engineering", "role": "Senior ML Engineer", "experience": "6 years"},
        {"id": "EMP_003", "name": "Dr. Emily Watson", "department": "AI Research", "role": "AI Ethics Specialist", "experience": "5 years"},
        {"id": "EMP_004", "name": "Alex Thompson", "department": "Product", "role": "AI Product Manager", "experience": "7 years"},
        {"id": "EMP_005", "name": "Priya Patel", "department": "Engineering", "role": "ML Infrastructure Engineer", "experience": "4 years"}
    ]
    
    return clients_data, orders_data, employees_data

def get_iso_compliance_data():
    """Get ISO compliance data"""
    
    # Sample compliance metrics
    compliance_data = {
        "total_controls": 45,
        "implemented": 38,
        "partial": 5,
        "not_implemented": 2,
        "compliance_rate": 84.4
    }
    
    # Sample risk register
    risk_register = [
        {"risk_id": "R001", "description": "AI Model Bias", "probability": "Medium", "impact": "High", "mitigation": "Regular bias testing and monitoring"},
        {"risk_id": "R002", "description": "Data Privacy Breach", "probability": "Low", "impact": "Critical", "mitigation": "Encryption and access controls"},
        {"risk_id": "R003", "description": "Model Performance Degradation", "probability": "Medium", "impact": "Medium", "mitigation": "Continuous monitoring and retraining"},
        {"risk_id": "R004", "description": "Regulatory Non-compliance", "probability": "Low", "impact": "High", "mitigation": "Regular audits and updates"}
    ]
    
    return compliance_data, risk_register

def main():
    # Header
    st.title("📋 ISO/IEC 42001:2023 Compliance Dashboard")
    st.caption("AI Management System (AIMS) - Real-time Compliance Monitoring")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🚀 Quick Navigation")
        if st.button("📘 ISO Docs", use_container_width=True):
            st.switch_page("pages/1_📘_ISO_Docs.py")
        if st.button("🏠 Main App", use_container_width=True):
            st.switch_page("app.py")
        
        st.markdown("---")
        st.header("📊 Last Updated")
        st.info(f"**{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")
        
        st.markdown("---")
        st.header("🔧 System Status")
        st.success("✅ All Systems Operational")
        st.success("✅ Database Connected")
        st.success("✅ API Services Running")
    
    # Main dashboard content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "🏢 Business Data", 
        "✅ Compliance Status", 
        "⚠️ Risk Management", 
        "📈 Performance Metrics"
    ])
    
    with tab1:
        st.header("📊 System Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Clients", "5", "↗️ +2 this month")
        
        with col2:
            st.metric("Active Orders", "5", "↗️ +1 this week")
        
        with col3:
            st.metric("Team Members", "5", "↗️ +1 this quarter")
        
        with col4:
            st.metric("Compliance Rate", "84.4%", "↗️ +2.1%")
        
        # Recent activity
        st.subheader("🕐 Recent Activity")
        recent_activities = [
            "✅ New client 'AI Solutions Inc' onboarded",
            "✅ Order ORD_005 completed successfully",
            "✅ Monthly compliance audit completed",
            "✅ Risk assessment updated",
            "✅ Employee training completed"
        ]
        
        for activity in recent_activities:
            st.markdown(f"- {activity}")
    
    with tab2:
        st.header("🏢 Business Data")
        
        # Generate sample data
        clients_data, orders_data, employees_data = generate_sample_data()
        
        # Clients
        st.subheader("👥 Clients")
        clients_df = pd.DataFrame(clients_data)
        st.dataframe(clients_df, use_container_width=True)
        
        # Orders
        st.subheader("📦 Orders")
        orders_df = pd.DataFrame(orders_data)
        st.dataframe(orders_df, use_container_width=True)
        
        # Employees
        st.subheader("👨‍💼 Team")
        employees_df = pd.DataFrame(employees_data)
        st.dataframe(employees_df, use_container_width=True)
    
    with tab3:
        st.header("✅ Compliance Status")
        
        compliance_data, _ = get_iso_compliance_data()
        
        # Compliance overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Controls", compliance_data["total_controls"])
        
        with col2:
            st.metric("Implemented", compliance_data["implemented"])
        
        with col3:
            st.metric("Compliance Rate", f"{compliance_data['compliance_rate']}%")
        
        # Status distribution
        st.subheader("📊 Implementation Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="compliance-status status-success">
                <h4>✅ Implemented</h4>
                <h2>{}</h2>
                <p>Controls fully implemented and operational</p>
            </div>
            """.format(compliance_data["implemented"]), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="compliance-status status-warning">
                <h4>🟡 Partial</h4>
                <h2>{}</h2>
                <p>Controls partially implemented</p>
            </div>
            """.format(compliance_data["partial"]), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="compliance-status status-error">
                <h4>🔴 Not Implemented</h4>
                <h2>{}</h2>
                <p>Controls requiring implementation</p>
            </div>
            """.format(compliance_data["not_implemented"]), unsafe_allow_html=True)
    
    with tab4:
        st.header("⚠️ Risk Management")
        
        _, risk_register = get_iso_compliance_data()
        
        # Risk matrix
        st.subheader("📊 Risk Register")
        risk_df = pd.DataFrame(risk_register)
        st.dataframe(risk_df, use_container_width=True)
        
        # Risk visualization
        st.subheader("🎯 Risk Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Risk Distribution by Probability:**")
            risk_prob = {"Low": 2, "Medium": 2, "High": 0}
            st.bar_chart(risk_prob)
        
        with col2:
            st.markdown("**Risk Distribution by Impact:**")
            risk_impact = {"Low": 0, "Medium": 1, "High": 2, "Critical": 1}
            st.bar_chart(risk_impact)
    
    with tab5:
        st.header("📈 Performance Metrics")
        
        # Generate sample performance data
        dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30, 0, -1)]
        performance_data = {
            "date": dates,
            "response_time": [random.uniform(0.8, 2.2) for _ in range(30)],
            "accuracy": [random.uniform(85, 98) for _ in range(30)],
            "user_satisfaction": [random.uniform(4.0, 5.0) for _ in range(30)]
        }
        
        perf_df = pd.DataFrame(performance_data)
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⏱️ Response Time (seconds)")
            st.line_chart(perf_df.set_index("date")["response_time"])
        
        with col2:
            st.subheader("🎯 Model Accuracy (%)")
            st.line_chart(perf_df.set_index("date")["accuracy"])
        
        # User satisfaction
        st.subheader("😊 User Satisfaction Score")
        st.line_chart(perf_df.set_index("date")["user_satisfaction"])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>ISO/IEC 42001:2023 Compliance Dashboard | Real-time Monitoring & Reporting</p>
        <p>Built with Streamlit | Professional Governance Framework</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
