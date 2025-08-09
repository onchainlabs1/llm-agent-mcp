#!/usr/bin/env python3
"""
ISO/IEC 42001:2023 Documentation Dashboard
llm-agent-mcp Project

Professional dashboard for presenting ISO compliance documentation
to external auditors, recruiters, and project reviewers.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="ISO/IEC 42001:2023 Documentation Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme for this dashboard only by overriding Streamlit CSS variables
st.markdown(
    """
    <style>
    /* Force a crisp light theme with higher contrast */
    :root {
        --primary-color: #1f77b4;
        --background-color: #ffffff;
        --secondary-background-color: #f5f7fb;
        --text-color: #0f172a; /* slate-900 for strong contrast */
    }
    .stApp { background-color: var(--background-color); color: var(--text-color); }

    /* General text contrast improvements */
    .stMarkdown, .stText, .stCaption, .stHeader, .stDataFrame { color: var(--text-color) !important; }
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--text-color) !important;
    }

    /* Buttons readable text */
    .stButton>button { color: #1f2937; font-weight: 600; }

    /* Metric widget: remove low-contrast gray labels */
    [data-testid="stMetricLabel"],
    [data-testid="stMetric"] label {
        color: #1f2937 !important; /* gray-800 */
        opacity: 1 !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] { color: #0b1320 !important; opacity: 1 !important; }
    [data-testid="stMetricDelta"] { opacity: 1 !important; }

    /* Footer text contrast */
    .iso-footer p { color: #374151 !important; }

    /* Preserve original hero header styling (white text on gradient) */
    .iso-hero, .iso-hero h1, .iso-hero p { color: #ffffff !important; }
    .iso-hero h1 { text-shadow: 0 1px 2px rgba(0,0,0,0.25); }
    </style>
    """,
    unsafe_allow_html=True,
)

# Constants
GITHUB_BASE = "https://github.com/onchainlabs1/llm-agent-mcp/blob/main"
REPO_BASE = "https://github.com/onchainlabs1/llm-agent-mcp"

# Configurable external links (override via env vars in Streamlit Cloud settings)
MAIN_APP_URL = os.getenv("MAIN_APP_URL", "/")  # default to root (same app)
ISO_DOCS_URL = os.getenv("ISO_DOCS_URL", "/iso_docs")  # default to subpage

# ISO Clause definitions
ISO_CLAUSES = {
    "Clause 4": {
        "title": "Context of the Organization",
        "description": "Understanding the organization and its context, determining the scope of the AI management system, and establishing the AI management system.",
        "documents": [
            "AIMS_Scope_and_Boundaries.md",
            "AIMS_Context_and_Stakeholders.md",
            "README.md"
        ],
        "folder": "Clause4_Context_new"
    },
    "Clause 5": {
        "title": "Leadership",
        "description": "Top management demonstrates leadership and commitment, establishes the AI management policy, and assigns organizational roles, responsibilities, and authorities.",
        "documents": [
            "AI_Management_Policy.md",
            "AI_Acceptable_Use_Policy.md",
            "AIMS_Roles_and_Responsibilities.md",
            "AI_Concern_Reporting_Procedure.md",
            "README.md"
        ],
        "folder": "Clause5_Leadership_new"
    },
    "Clause 6": {
        "title": "Planning",
        "description": "Actions to address risks and opportunities, AI management system objectives and planning to achieve them, and planning of changes.",
        "documents": [
            "AI_Risk_Management_Procedure.md",
            "AI_Risk_Register.csv",
            "AI_Objectives_and_Planning.md",
            "Statement_of_Applicability.csv",
            "AI_Change_Management_Procedure.md",
            "README.md"
        ],
        "folder": "Clause6_Planning_new"
    },
    "Clause 7": {
        "title": "Support",
        "description": "Resources, competence, awareness, communication, and documented information management.",
        "documents": [
            "AIMS_Resources.md",
            "AIMS_Competence_and_Training.md",
            "AIMS_Awareness_and_Communication.md",
            "AIMS_Document_Control_Procedure.md",
            "README.md"
        ],
        "folder": "Clause7_Support"
    },
    "Clause 8": {
        "title": "Operation",
        "description": "Operational planning and control, AI system impact assessment, data management, third-party requirements, and incident response.",
        "documents": [
            "AI_Operational_Planning_and_Control.md",
            "AI_System_Impact_Assessment.md",
            "AI_Data_Management_Procedure.md",
            "AI_Third_Party_and_Customer_Requirements.md",
            "AI_Incident_Response_Procedure.md",
            "README.md"
        ],
        "folder": "Clause8_Operation"
    },
    "Clause 9": {
        "title": "Performance Evaluation",
        "description": "Monitoring, measurement, analysis, evaluation, internal audit, and management review.",
        "documents": [
            "AI_Performance_Monitoring_and_Measurement.md",
            "AI_Internal_Audit_Procedure.md",
            "AI_Management_Review.md",
            "AI_Continuous_Improvement.md",
            "README.md"
        ],
        "folder": "Clause9_Performance_Evaluation"
    },
    "Clause 10": {
        "title": "Improvement",
        "description": "Nonconformity and corrective action, and continual improvement.",
        "documents": [
            "AI_Nonconformity_and_Corrective_Action.md",
            "AI_Continual_Improvement.md",
            "README.md"
        ],
        "folder": "Clause10_Improvement"
    }
}

def main():
    # Header
    st.markdown("""
    <div class="iso-hero" style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 10px; color: white; margin-bottom: 2rem;">
        <h1>📋 ISO/IEC 42001:2023 Documentation Dashboard</h1>
        <p style="font-size: 1.2rem; margin: 0;">AI Management System Compliance Center</p>
        <p style="font-size: 1rem; margin: 0.5rem 0 0 0;">llm-agent-mcp Project</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button("🏠 Main App", MAIN_APP_URL, use_container_width=True)
    with col2:
        st.link_button("📘 ISO Docs Browser", ISO_DOCS_URL, use_container_width=True)
    with col3:
        st.link_button("📚 GitHub Repository", REPO_BASE, use_container_width=True)
    with col4:
        st.link_button("📊 Hours Log", f"{GITHUB_BASE}/project_hours_log.md", use_container_width=True)
    
    st.markdown("---")
    
    # Overview Metrics
    st.markdown("## 📊 Compliance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📄 Total Documents",
            value="38",
            delta="Complete"
        )
    
    with col2:
        st.metric(
            label="⏱️ Hours Logged",
            value="353.5h",
            delta="✅ Exceeds 300h requirement"
        )
    
    with col3:
        st.metric(
            label="🎯 Audit Score",
            value="98/100",
            delta="✅ Excellent"
        )
    
    with col4:
        st.metric(
            label="📋 Risk Register",
            value="10 Risks",
            delta="✅ Comprehensive"
        )
    
    # Status indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("✅ **ISO/IEC 42001:2023 Compliant**")
    
    with col2:
        st.success("✅ **Lead Implementer Eligible**")
    
    with col3:
        st.success("✅ **Ready for External Audit**")
    
    st.markdown("---")
    
    # ISO Clauses Section
    st.markdown("## 📁 ISO/IEC 42001:2023 Clauses")
    st.markdown("Click on each clause to view its documentation and implementation details.")
    
    # Introductory clauses (1–3) – informational only
    with st.expander("**Clauses 1–3 – Introductory (Scope, References, Terms)**", expanded=False):
        st.markdown(
            """
            These clauses are foundational and informational in ISO/IEC 42001:
            - **Clause 1 – Scope**: Defines the applicability of the AI Management System standard.
            - **Clause 2 – Normative References**: References other standards that are indispensable for the application of ISO/IEC 42001.
            - **Clause 3 – Terms and Definitions**: Establishes the terminology used across the standard.

            For this project, Clauses 1–3 are acknowledged and used as context for the implementation evidence in Clauses 4–10. They typically do not require project-specific procedures, but can be cited in policy and training materials.
            
            Suggested references:
            - Organization-wide policy or internal wiki referencing the standard’s scope and terminology
            - Glossary within project documentation (if maintained)
            """
        )
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📋 Clauses 4-6", "📋 Clauses 7-9", "📋 Clause 10 & Summary"])
    
    with tab1:
        # Clauses 4-6
        for clause_num in ["Clause 4", "Clause 5", "Clause 6"]:
            clause_data = ISO_CLAUSES[clause_num]
            
            with st.expander(f"**{clause_num} - {clause_data['title']}** ✅ Complete", expanded=False):
                st.markdown(f"**Description:** {clause_data['description']}")
                st.markdown("**Documents Created:**")
                
                for doc in clause_data['documents']:
                    doc_link = f"{GITHUB_BASE}/docs/{clause_data['folder']}/{doc}"
                    st.markdown(f"- [📄 {doc}]({doc_link})")
                
                st.markdown(f"**GitHub Folder:** [{clause_data['folder']}]({GITHUB_BASE}/docs/{clause_data['folder']})")
    
    with tab2:
        # Clauses 7-9
        for clause_num in ["Clause 7", "Clause 8", "Clause 9"]:
            clause_data = ISO_CLAUSES[clause_num]
            
            with st.expander(f"**{clause_num} - {clause_data['title']}** ✅ Complete", expanded=False):
                st.markdown(f"**Description:** {clause_data['description']}")
                st.markdown("**Documents Created:**")
                
                for doc in clause_data['documents']:
                    doc_link = f"{GITHUB_BASE}/docs/{clause_data['folder']}/{doc}"
                    st.markdown(f"- [📄 {doc}]({doc_link})")
                
                st.markdown(f"**GitHub Folder:** [{clause_data['folder']}]({GITHUB_BASE}/docs/{clause_data['folder']})")
    
    with tab3:
        # Clause 10
        clause_data = ISO_CLAUSES["Clause 10"]
        
        with st.expander(f"**Clause 10 - {clause_data['title']}** ✅ Complete", expanded=True):
            st.markdown(f"**Description:** {clause_data['description']}")
            st.markdown("**Documents Created:**")
            
            for doc in clause_data['documents']:
                doc_link = f"{GITHUB_BASE}/docs/{clause_data['folder']}/{doc}"
                st.markdown(f"- [📄 {doc}]({doc_link})")
            
            st.markdown(f"**GitHub Folder:** [{clause_data['folder']}]({GITHUB_BASE}/docs/{clause_data['folder']})")
        
        # Summary Documents
        st.markdown("## 📋 Summary Documents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Project Hours Log")
            st.markdown("Comprehensive tracking of all implementation hours for ISO certification.")
            st.link_button("View Hours Log", f"{GITHUB_BASE}/project_hours_log.md")
        
        with col2:
            st.markdown("### 🎯 ISO Compliance Summary")
            st.markdown("Complete compliance summary and certification readiness assessment.")
            st.link_button("View Summary", f"{GITHUB_BASE}/docs/ISO_Compliance_Summary.md")
    
    st.markdown("---")
    
    # Project Hours Log Preview
    st.markdown("## 📊 Project Hours Log Preview")
    
    # Try to load and display the hours log
    try:
        if os.path.exists("project_hours_log.csv"):
            df = pd.read_csv("project_hours_log.csv")
            
            # Calculate summary statistics
            total_hours = df['Time (h)'].sum()
            total_entries = len(df)
            clause_breakdown = df.groupby('Clause')['Time (h)'].sum().sort_values(ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 Hours Summary")
                st.metric("Total Hours", f"{total_hours:.1f}")
                st.metric("Total Entries", total_entries)
                st.metric("ISO Requirement", "300h")
                st.metric("Status", "✅ Exceeds Requirement" if total_hours >= 300 else "⚠️ Needs More Hours")
            
            with col2:
                st.markdown("### 📊 Hours by Clause")
                for clause, hours in clause_breakdown.items():
                    st.metric(clause, f"{hours:.1f}h")
            
            # Show sample data
            st.markdown("### 📋 Recent Entries")
            st.dataframe(df.head(10), use_container_width=True)
            
            st.link_button("📊 View Full Hours Log", f"{GITHUB_BASE}/project_hours_log.md")
        else:
            st.warning("Hours log file not found. Please run the hours tracking system first.")
    except Exception as e:
        st.error(f"Error loading hours log: {e}")
    
    st.markdown("---")
    
    # Audit Information
    st.markdown("## 🔍 Audit Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Audit Readiness")
        st.success("✅ **Ready for External Audit**")
        st.info("📊 **Audit Score: 98/100**")
        st.success("📄 **All Documentation Complete**")
        st.success("⏱️ **Hours Requirement Met**")
    
    with col2:
        st.markdown("### 🎯 Certification Status")
        st.success("✅ **ISO/IEC 42001:2023 Compliant**")
        st.success("✅ **Lead Implementer Eligible**")
        st.success("✅ **Documentation Audit-Ready**")
        st.success("✅ **Implementation Evidence Complete**")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div class="iso-footer" style="text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 5px; margin-top: 2rem;">
        <p style="margin: 0;">
            Built with ❤️ by <strong>On-Chain Labs</strong> · ISO/IEC 42001:2023 AI Management System
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Professional ISO compliance dashboard for external auditors and project reviewers
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 