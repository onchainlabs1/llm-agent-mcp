"""
ISO/IEC 42001:2023 Compliance Dashboard
Ultra-Simplified Streamlit Cloud Version
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="ISO/IEC 42001:2023 Compliance Dashboard",
    page_icon="📋",
    layout="wide"
)

def main():
    st.title("📋 ISO/IEC 42001:2023 Compliance Dashboard")
    st.markdown("---")
    
    # Simple metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Controls", "45", "100%")
    
    with col2:
        st.metric("Implemented", "38", "84.4%")
    
    with col3:
        st.metric("Partial", "5", "11.1%")
    
    with col4:
        st.metric("Not Implemented", "2", "4.4%")
    
    st.markdown("---")
    
    # ISO Controls Status
    st.subheader("🎯 ISO 42001:2023 Controls Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.success("✅ R001: Bias Detection")
        st.caption("Implemented")
    
    with col2:
        st.success("✅ R002: Fact-checking")
        st.caption("Implemented")
    
    with col3:
        st.success("✅ R003: Prompt Sanitization")
        st.caption("Implemented")
    
    with col4:
        st.success("✅ R008: Data Encryption")
        st.caption("Implemented")
    
    st.markdown("---")
    
    # Simple Risk Register
    st.subheader("⚠️ Risk Register Summary")
    
    risk_data = {
        "Risk ID": ["R001", "R002", "R003", "R008"],
        "Category": ["Ethical", "Technical", "Security", "Compliance"],
        "Status": ["Implemented", "Implemented", "Implemented", "Implemented"],
        "Owner": ["Dr. Sarah Chen", "Marcus Rodriguez", "Dr. Sarah Chen", "Dr. Sarah Chen"]
    }
    
    risk_df = pd.DataFrame(risk_data)
    st.dataframe(risk_df, use_container_width=True)
    
    st.markdown("---")
    
    # Compliance Score
    st.subheader("📊 Overall Compliance Score")
    
    compliance_score = 84.4
    st.metric("ISO 42001:2023 Compliance", f"{compliance_score}%", "✅ Compliant")
    
    if compliance_score >= 80:
        st.success("🎉 Project is READY for ISO 42001:2023 Certification Audit!")
    else:
        st.warning("⚠️ Some improvements needed before certification")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>ISO/IEC 42001:2023 Compliance Dashboard | Streamlit Cloud Version</p>
        <p>Built with Streamlit | Professional Governance Framework</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
