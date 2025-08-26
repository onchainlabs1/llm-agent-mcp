"""
ISO/IEC 42001:2023 Documentation Browser
Ultra-Simplified Streamlit Cloud Version
"""

import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="ISO/IEC 42001:2023 Documentation Browser",
    page_icon="📘",
    layout="wide"
)

def main():
    st.title("📘 ISO/IEC 42001:2023 Documentation Browser")
    st.markdown("AI Management System (AIMS) Documentation")
    
    st.markdown("---")
    
    # Simple navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 Main App", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        if st.button("📊 ISO Dashboard", use_container_width=True):
            st.switch_page("pages/2_📋_ISO_Dashboard.py")
    
    st.markdown("---")
    
    # Document structure
    st.subheader("📚 Document Structure")
    
    st.markdown("""
    ### **Clause 4: Context of the Organization**
    - AIMS Context and Stakeholders
    - AIMS Scope and Boundaries
    
    ### **Clause 5: Leadership**
    - AI Management Policy
    - AI Acceptable Use Policy
    - AI Concern Reporting Procedure
    - AIMS Roles and Responsibilities
    
    ### **Clause 6: Planning**
    - AI Change Management Procedure
    - AI Objectives and Planning
    - AI Risk Management Procedure
    - AI Risk Register
    
    ### **Clause 7: Support**
    - AIMS Awareness and Communication
    - AIMS Competence and Training
    - AIMS Document Control Procedure
    - AIMS Resources
    
    ### **Clause 8: Operation**
    - AI Data Management Procedure
    - AI Incident Response Procedure
    - AI Operational Planning and Control
    - AI System Impact Assessment
    - AI Third Party and Customer Requirements
    
    ### **Clause 9: Performance Evaluation**
    - AI Continuous Improvement
    - AI Internal Audit Procedure
    - AI Management Review
    - AI Performance Monitoring and Measurement
    
    ### **Clause 10: Improvement**
    - AI Continual Improvement
    - AI Nonconformity and Corrective Action
    """)
    
    st.markdown("---")
    
    # Compliance Status
    st.subheader("✅ Compliance Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("✅ Clause 4: Context")
        st.caption("Approved")
    
    with col2:
        st.success("✅ Clause 5: Leadership")
        st.caption("Approved")
    
    with col3:
        st.success("✅ Clause 6: Planning")
        st.caption("Approved")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("✅ Clause 7: Support")
        st.caption("Approved")
    
    with col2:
        st.success("✅ Clause 8: Operation")
        st.caption("Approved")
    
    with col3:
        st.success("✅ Clause 9: Performance")
        st.caption("Approved")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #666;">
        ISO/IEC 42001:2023 Documentation Browser | Streamlit Cloud Version
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
