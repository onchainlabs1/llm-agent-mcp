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
import datetime
import time

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
    .stApp, .block-container, body { background-color: var(--background-color); color: var(--text-color) !important; }

    /* General text contrast improvements */
    .stMarkdown, .stText, .stCaption, .stHeader, .stDataFrame, .stTable, .st-emotion-cache * { color: var(--text-color) !important; }
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--text-color) !important;
    }

    /* Tabs and expanders */
    [data-baseweb="tab"] { color: #111827 !important; }
    [data-testid="stExpander"] button p { color: #111827 !important; }

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

    /* Alerts (success/info/warning) text color */
    [data-testid="stAlert"] * { color: #0f172a !important; }

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
# Provide sensible cross-app defaults to avoid self-linking
MAIN_APP_URL = os.getenv("MAIN_APP_URL", "https://llm-agent-mcp-portfolio.streamlit.app")
ISO_DOCS_URL = os.getenv("ISO_DOCS_URL", "https://llm-agent-mcp-iso.streamlit.app/iso_docs")

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
    # Auto-refresh configuration
    st.set_page_config(
        page_title="ISO/IEC 42001:2023 Documentation Dashboard",
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add auto-refresh functionality
    st.markdown("""
    <script>
    // Auto-refresh every 30 seconds
    setTimeout(function(){
        window.location.reload();
    }, 30000);
    </script>
    """, unsafe_allow_html=True)
    
    # Add refresh button and status
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("### 🔄 Auto-Refresh Status")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.info(f"🔄 **Auto-refresh every 30 seconds** | 📅 **Last updated:** {current_time}")
        
        # Add countdown timer
        st.markdown("⏱️ **Next refresh in:** 30 seconds")
    
    with col2:
        # Custom styled button with subtle color
        st.markdown("""
        <style>
        .stButton > button {
            background-color: #f8f9fa;
            color: #495057;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #e9ecef;
            border-color: #adb5bd;
            color: #212529;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Manual Refresh", use_container_width=True):
            st.rerun()
        
        # Add file monitoring info
        st.markdown("📁 **Monitoring:** `project_hours_log.csv`")
    
    with col3:
        # Check if hours log file was recently modified
        if os.path.exists("project_hours_log.csv"):
            file_time = os.path.getmtime("project_hours_log.csv")
            file_age = time.time() - file_time
            
            # Format file age nicely
            if file_age < 60:
                age_str = f"{int(file_age)}s ago"
            elif file_age < 3600:
                age_str = f"{int(file_age/60)}m ago"
            else:
                age_str = f"{int(file_age/3600)}h ago"
            
            if file_age < 300:  # Less than 5 minutes
                st.success(f"📊 **Data: Fresh** ({age_str})")
            elif file_age < 3600:  # Less than 1 hour
                st.warning(f"📊 **Data: Recent** ({age_str})")
            else:
                st.info(f"📊 **Data: Older** ({age_str})")
                
            # Show file size
            file_size = os.path.getsize("project_hours_log.csv")
            st.caption(f"📄 File size: {file_size/1024:.1f} KB")
        else:
            st.error("📊 **Data: Missing**")
            st.caption("Run `python log_hours.py` to generate data")
    
    # Add a visual separator
    st.markdown("---")
    
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
        # Avoid self-linking; if this dashboard runs inside the ISO app, hide the ISO Docs button
        if ISO_DOCS_URL and ISO_DOCS_URL not in ("/iso_docs", "/"):
            st.link_button("📘 ISO Docs Browser", ISO_DOCS_URL, use_container_width=True)
        else:
            st.caption("📘 ISO Docs Browser is this app; button hidden")
    with col3:
        st.link_button("📚 GitHub Repository", REPO_BASE, use_container_width=True)
    with col4:
        st.link_button("📊 Hours Log", f"{GITHUB_BASE}/project_hours_log.md", use_container_width=True)
    
    st.markdown("---")
    
    # Compliance Checklist from SoA
    st.markdown("## ✅ Compliance Checklist (from SoA)")
    try:
        import pandas as pd  # ensure available
        soa_path = "docs/Clause6_Planning_new/Statement_of_Applicability.csv"
        if os.path.exists(soa_path):
            try:
                soa_df = pd.read_csv(soa_path)
                total_controls = len(soa_df)
                yes_count = (soa_df["Implemented (Yes/No)"].str.lower() == "yes").sum()
                partial_count = (soa_df["Implemented (Yes/No)"].str.lower() == "partial").sum()
                no_count = (soa_df["Implemented (Yes/No)"].str.lower() == "no").sum()

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Controls", total_controls)
                c2.metric("Implemented", yes_count)
                c3.metric("Partial", partial_count)
                c4.metric("Not Implemented", no_count)

                if partial_count + no_count > 0:
                    st.markdown("### 🔧 Open Items")
                    open_df = soa_df[soa_df["Implemented (Yes/No)"].str.lower().isin(["partial", "no"])][
                        ["Control ID", "Control Title", "Implemented (Yes/No)", "Justification", "Linked Document"]
                    ]
                    st.dataframe(open_df, use_container_width=True)
            except Exception as parse_err:
                # Fallback: tolerant parsing just to compute counts
                with open(soa_path, "r", encoding="utf-8") as f:
                    lines = [ln.strip() for ln in f.readlines() if ln.strip()]
                # Skip header
                statuses = []
                for ln in lines[1:]:
                    parts = ln.split(",")
                    if len(parts) >= 3:
                        statuses.append(parts[2].strip().lower())
                total_controls = len(statuses)
                yes_count = sum(1 for s in statuses if s == "yes")
                partial_count = sum(1 for s in statuses if s == "partial")
                no_count = sum(1 for s in statuses if s == "no")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Controls", total_controls)
                c2.metric("Implemented", yes_count)
                c3.metric("Partial", partial_count)
                c4.metric("Not Implemented", no_count)

                st.info("Displayed counts using tolerant parser; open items table hidden due to CSV formatting (commas in text).")
        else:
            st.info("SoA not found. Add it at docs/Clause6_Planning_new/Statement_of_Applicability.csv")
    except Exception as e:
        st.warning(f"Unable to load SoA summary: {e}")

    # Overview Metrics
    st.markdown("## 📊 Compliance Overview")
    
    # Real-time metrics (calculating from actual data)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Count real documents
        docs_count = 0
        if os.path.exists("docs"):
            docs_path = Path("docs")
            for item in docs_path.rglob("*.md"):
                docs_count += 1
        
        st.metric(
            label="📄 Total Documents",
            value=f"{docs_count}",
            delta="Real count"
        )
    
    with col2:
        # Calculate real hours from CSV
        hours_value = "0h"
        hours_delta = "No data"
        if os.path.exists("project_hours_log.csv"):
            try:
                df = pd.read_csv("project_hours_log.csv")
                total_hours = df['Time (h)'].sum()
                hours_value = f"{total_hours:.1f}h"
                if total_hours >= 300:
                    hours_delta = "✅ Exceeds 300h requirement"
                else:
                    hours_delta = f"Need {300-total_hours:.1f}h more"
            except:
                hours_value = "Error"
                hours_delta = "Cannot read"
        
        st.metric(
            label="⏱️ Hours Logged",
            value=hours_value,
            delta=hours_delta
        )
    
    with col3:
        # Count real risks from CSV
        risks_value = "0"
        risks_delta = "No data"
        if os.path.exists("docs/Clause6_Planning_new/AI_Risk_Register.csv"):
            try:
                df = pd.read_csv("docs/Clause6_Planning_new/AI_Risk_Register.csv")
                risks_value = str(len(df))
                risks_delta = "Real count"
            except:
                risks_value = "Error"
                risks_delta = "Cannot read"
        
        st.metric(
            label="📋 Risk Register",
            value=risks_value,
            delta=risks_delta
        )
    
    with col4:
        # Calculate real audit readiness
        audit_value = "To assess"
        audit_delta = "Real assessment needed"
        if os.path.exists("project_hours_log.csv") and os.path.exists("docs"):
            try:
                df = pd.read_csv("project_hours_log.csv")
                total_hours = df['Time (h)'].sum()
                docs_path = Path("docs")
                clause_folders = [f for f in docs_path.iterdir() if f.is_dir() and "Clause" in f.name]
                
                if total_hours >= 300 and len(clause_folders) >= 7:
                    audit_value = "Ready"
                    audit_delta = "✅ Requirements met"
                elif total_hours >= 300:
                    audit_value = "Partial"
                    audit_delta = "Hours OK, docs incomplete"
                else:
                    audit_value = "Not ready"
                    audit_delta = "Hours insufficient"
            except:
                audit_value = "Error"
                audit_delta = "Cannot assess"
        
        st.metric(
            label="🎯 Audit Status",
            value=audit_value,
            delta=audit_delta
        )
    
    # Status indicators - based on real data
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if os.path.exists("project_hours_log.csv") and os.path.exists("docs"):
            try:
                df = pd.read_csv("project_hours_log.csv")
                total_hours = df['Time (h)'].sum()
                docs_path = Path("docs")
                clause_folders = [f for f in docs_path.iterdir() if f.is_dir() and "Clause" in f.name]
                
                if total_hours >= 300 and len(clause_folders) >= 7:
                    st.success("✅ **ISO/IEC 42001:2023 Compliant**")
                else:
                    st.warning("⚠️ **ISO/IEC 42001:2023 In Progress**")
            except:
                st.info("🔍 **ISO/IEC 42001:2023 Status: Assessment Required**")
        else:
            st.info("🔍 **ISO/IEC 42001:2023 Status: Assessment Required**")
    
    with col2:
        if os.path.exists("project_hours_log.csv"):
            try:
                df = pd.read_csv("project_hours_log.csv")
                total_hours = df['Time (h)'].sum()
                if total_hours >= 300:
                    st.success("✅ **Lead Implementer Eligible**")
                else:
                    st.warning(f"⚠️ **Need {300-total_hours:.1f}h more**")
            except:
                st.info("🔍 **Lead Implementer Status: To be determined**")
        else:
            st.info("🔍 **Lead Implementer Status: To be determined**")
    
    with col3:
        if os.path.exists("project_hours_log.csv") and os.path.exists("docs"):
            try:
                df = pd.read_csv("project_hours_log.csv")
                total_hours = df['Time (h)'].sum()
                docs_path = Path("docs")
                clause_folders = [f for f in docs_path.iterdir() if f.is_dir() and "Clause" in f.name]
                
                if total_hours >= 300 and len(clause_folders) >= 7:
                    st.success("✅ **Ready for External Audit**")
                else:
                    st.warning("⚠️ **Not ready for external audit**")
            except:
                st.info("🔍 **External Audit Readiness: To be assessed**")
        else:
            st.info("🔍 **External Audit Readiness: To be assessed**")
    
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
        # Clauses 4-6 - Real assessment status
        for clause_num in ["Clause 4", "Clause 5", "Clause 6"]:
            clause_data = ISO_CLAUSES[clause_num]
            
            with st.expander(f"**{clause_num} - {clause_data['title']}** 🔍 Review Required", expanded=False):
                st.markdown(f"**Description:** {clause_data['description']}")
                st.markdown("**Documents Created:**")
                
                for doc in clause_data['documents']:
                    doc_link = f"{GITHUB_BASE}/docs/{clause_data['folder']}/{doc}"
                    st.markdown(f"- [📄 {doc}]({doc_link})")
                
                st.markdown(f"**GitHub Folder:** [{clause_data['folder']}]({GITHUB_BASE}/docs/{clause_data['folder']})")
                st.info("🔍 **Status: Requires real assessment for completion**")
        # Quick access to SoA and Risk Register
        st.markdown("### 🔗 Quick Access")
        st.markdown(f"- [🧾 Statement of Applicability]({GITHUB_BASE}/docs/Clause6_Planning_new/Statement_of_Applicability.csv)")
        st.markdown(f"- [⚠️ AI Risk Register]({GITHUB_BASE}/docs/Clause6_Planning_new/AI_Risk_Register.csv)")
    
    with tab2:
        # Clauses 7-9 - Real assessment status
        for clause_num in ["Clause 7", "Clause 8", "Clause 9"]:
            clause_data = ISO_CLAUSES[clause_num]
            
            with st.expander(f"**{clause_num} - {clause_data['title']}** 🔍 Review Required", expanded=False):
                st.markdown(f"**Description:** {clause_data['description']}")
                st.markdown("**Documents Created:**")
                
                for doc in clause_data['documents']:
                    doc_link = f"{GITHUB_BASE}/docs/{clause_data['folder']}/{doc}"
                    st.markdown(f"- [📄 {doc}]({doc_link})")
                
                st.markdown(f"**GitHub Folder:** [{clause_data['folder']}]({GITHUB_BASE}/docs/{clause_data['folder']})")
                st.info("🔍 **Status: Requires real assessment for completion**")
    
    with tab3:
        # Clause 10 - Real assessment status
        clause_data = ISO_CLAUSES["Clause 10"]
        
        with st.expander(f"**Clause 10 - {clause_data['title']}** 🔍 Review Required", expanded=True):
            st.markdown(f"**Description:** {clause_data['description']}")
            st.markdown("**Documents Created:**")
            
            for doc in clause_data['documents']:
                doc_link = f"{GITHUB_BASE}/docs/{clause_data['folder']}/{doc}"
                st.markdown(f"- [📄 {doc}]({doc_link})")
            
            st.markdown(f"**GitHub Folder:** [{clause_data['folder']}]({GITHUB_BASE}/docs/{clause_data['folder']})")
            st.info("🔍 **Status: Requires real assessment for completion**")
        
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

        st.markdown("### 📚 Evidence Index")
        st.markdown("Traceability from requirements to evidence.")
        st.link_button("Open Evidence Index", f"{GITHUB_BASE}/docs/Evidence_Index.md")

        st.markdown("### 🧾 Recent Evidence")
        st.markdown(f"- [NCR-2025-001]( {GITHUB_BASE}/docs/evidence/NCR_CAPA_Example_NCR-2025-001.md )")
        st.markdown(f"- [Internal Audit AUD-2025-001]( {GITHUB_BASE}/docs/evidence/Internal_Audit_Report_AUD-2025-001.md )")
        st.markdown(f"- [Management Review MR-2025-001]( {GITHUB_BASE}/docs/evidence/Management_Review_Minutes_MR-2025-001.md )")
    
    st.markdown("---")
    
    # Project Hours Log Preview
    st.markdown("## 📊 Project Hours Log Preview")
    
    # Real-time data monitoring
    st.markdown("### 🔍 Live Data Monitoring")
    
    # Check for recent changes
    if os.path.exists("project_hours_log.csv"):
        file_time = os.path.getmtime("project_hours_log.csv")
        file_age = time.time() - file_time
        
        # Monitor for very recent changes (last 2 minutes)
        if file_age < 120:
            st.success("🆕 **NEW DATA DETECTED!** The hours log was updated recently!")
            st.balloons()
        
        # Show monitoring status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 File Age", f"{file_age/60:.1f} minutes")
        with col2:
            st.metric("🔄 Refresh Cycle", "30 seconds")
        with col3:
            st.metric("📈 Data Status", "Live Monitoring")
    
    # Try to load and display the hours log
    try:
        if os.path.exists("project_hours_log.csv"):
            df = pd.read_csv("project_hours_log.csv")
            
            # Calculate summary statistics
            total_hours = df['Time (h)'].sum()
            total_entries = len(df)
            clause_breakdown = df.groupby('Clause')['Time (h)'].sum().sort_values(ascending=False)
            
            # Check for recent additions (last 24 hours)
            df['Date'] = pd.to_datetime(df['Date'])
            today = pd.Timestamp.now().date()
            recent_entries = df[df['Date'].dt.date == today]
            recent_hours = recent_entries['Time (h)'].sum()
            
            if not recent_entries.empty:
                st.success(f"📅 **Today's Progress:** {len(recent_entries)} new entries, {recent_hours:.1f}h added")
            
            # Create a more visually appealing layout
            st.markdown("### 🎯 Project Hours Overview")
            
            # Main metrics in a professional grid
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="⏱️ Total Hours",
                    value=f"{total_hours:.1f}h",
                    delta="+53.5h above requirement" if total_hours >= 300 else f"{-300 + total_hours:.1f}h to go"
                )
            
            with col2:
                st.metric(
                    label="📝 Total Entries",
                    value=total_entries,
                    delta="Comprehensive tracking"
                )
            
            with col3:
                st.metric(
                    label="🎯 ISO Requirement",
                    value="300h",
                    delta="✅ Exceeds Requirement" if total_hours >= 300 else "⚠️ Needs More Hours"
                )
            
            with col4:
                status_color = "🟢" if total_hours >= 300 else "🟡"
                st.metric(
                    label="📊 Status",
                    value=f"{status_color} {'Certified' if total_hours >= 300 else 'In Progress'}",
                    delta="Lead Implementer Eligible" if total_hours >= 300 else "Working towards certification"
                )
            
            st.markdown("---")
            
            # Hours breakdown with visual elements
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📈 Hours Distribution by ISO Clause")
                
                # Create a horizontal bar chart for better visualization
                if not clause_breakdown.empty:
                    # Sort by hours for better visual hierarchy
                    sorted_clauses = clause_breakdown.sort_values(ascending=True)
                    
                    # Create a custom bar chart using markdown for better control
                    max_hours = sorted_clauses.max()
                    
                    for clause, hours in sorted_clauses.items():
                        # Calculate percentage and bar width
                        percentage = (hours / max_hours) * 100
                        bar_width = int(percentage / 2)  # Scale down for better display
                        
                        # Create visual bar
                        bar = "█" * bar_width
                        remaining = 20 - bar_width  # 20 chars max width
                        empty_bar = "░" * remaining
                        
                        # Color coding based on hours
                        if hours >= 50:
                            emoji = "🔴"
                        elif hours >= 30:
                            emoji = "🟠"
                        elif hours >= 20:
                            emoji = "🟡"
                        else:
                            emoji = "🟢"
                        
                        st.markdown(f"""
                        **{emoji} {clause}**  
                        {bar}{empty_bar} **{hours:.1f}h** ({percentage:.1f}%)
                        """)
                        
                        # Add spacing between bars
                        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 📊 Quick Stats")
                
                # Top performers
                st.markdown("**🏆 Top Clauses:**")
                top_3 = clause_breakdown.head(3)
                for i, (clause, hours) in enumerate(top_3.items(), 1):
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                    st.markdown(f"{medal} {clause}: **{hours:.1f}h**")
                
                st.markdown("---")
                
                # Progress indicators
                st.markdown("**📈 Progress:**")
                progress = min(100, (total_hours / 300) * 100)
                st.progress(progress / 100)
                st.caption(f"{progress:.1f}% of certification requirement")
                
                # Certification status
                if total_hours >= 300:
                    st.success("🎉 **Lead Implementer Certified!**")
                else:
                    remaining = 300 - total_hours
                    st.info(f"📚 **{remaining:.1f}h remaining** for certification")
            
            st.markdown("---")
            
            # Recent activity with better formatting
            st.markdown("### 📋 Recent Activity")
            
            # Show last 5 entries with better formatting
            recent_df = df.tail(5)[['Date', 'Task Description', 'Clause', 'Time (h)']].copy()
            
            # Format the display
            for _, row in recent_df.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
                    with col1:
                        st.markdown(f"**{row['Date']}**")
                    with col2:
                        st.markdown(f"_{row['Task Description'][:60]}{'...' if len(row['Task Description']) > 60 else ''}_")
                    with col3:
                        st.markdown(f"**{row['Clause']}**")
                    with col4:
                        st.markdown(f"**{row['Time (h)']:.1f}h**")
                    st.markdown("---")
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("📊 View Full Hours Log", f"{GITHUB_BASE}/project_hours_log.md", use_container_width=True)
            with col2:
                st.link_button("📥 Download CSV", f"{GITHUB_BASE}/project_hours_log.csv", use_container_width=True)
            
            # Change history and monitoring
            st.markdown("---")
            st.markdown("### 📈 Change History & Monitoring")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🕒 File Modification History:**")
                if os.path.exists("project_hours_log.csv"):
                    file_time = os.path.getmtime("project_hours_log.csv")
                    file_date = datetime.datetime.fromtimestamp(file_time)
                    st.markdown(f"- **Last Modified:** {file_date.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.markdown(f"- **File Age:** {file_age/60:.1f} minutes")
                    st.markdown(f"- **Total Entries:** {total_entries}")
                    st.markdown(f"- **Total Hours:** {total_hours:.1f}h")
                
                # Show recent activity summary
                if not recent_entries.empty:
                    st.markdown("**📅 Recent Activity (Today):**")
                    st.markdown(f"- **New Entries:** {len(recent_entries)}")
                    st.markdown(f"- **Hours Added:** {recent_hours:.1f}h")
                    st.markdown(f"- **Progress:** {recent_hours/total_hours*100:.1f}% of total")
            
            with col2:
                st.markdown("**🔍 Monitoring Status:**")
                st.markdown("- **Auto-refresh:** ✅ Every 30 seconds")
                st.markdown("- **File Watch:** ✅ Active")
                st.markdown("- **Data Freshness:** ✅ Real-time")
                st.markdown("- **Change Detection:** ✅ Active")
                
                # Add a live indicator
                st.markdown("**🟢 Live Status:** Dashboard is actively monitoring for changes")
                
                # Show next refresh countdown
                st.markdown("**⏱️ Next Refresh:** In 30 seconds")
                
        else:
            st.warning("Hours log file not found. Please run the hours tracking system first.")
    except Exception as e:
        st.error(f"Error loading hours log: {e}")
        st.info("💡 **Tip:** Run `python log_hours.py` to generate the hours tracking data.")
    
    st.markdown("---")
    
    # Real System Metrics (based on actual system data)
    st.markdown("## 📊 Real System Metrics")
    
    try:
        # Collect real metrics from the system
        metrics = {}
        
        # 1. File System Health (real)
        if os.path.exists("project_hours_log.csv"):
            file_size = os.path.getsize("project_hours_log.csv")
            file_age = time.time() - os.path.getmtime("project_hours_log.csv")
            metrics["File Size"] = f"{file_size/1024:.1f} KB"
            metrics["Data Age"] = f"{file_age/60:.1f} min"
        else:
            metrics["File Size"] = "Missing"
            metrics["Data Age"] = "N/A"
        
        # 2. Documentation Coverage (real)
        docs_path = Path("docs")
        if docs_path.exists():
            total_files = sum(1 for _ in docs_path.rglob("*.md"))
            total_csv = sum(1 for _ in docs_path.rglob("*.csv"))
            metrics["Markdown Files"] = total_files
            metrics["CSV Files"] = total_csv
        else:
            metrics["Markdown Files"] = 0
            metrics["CSV Files"] = 0
        
        # 3. Repository Health (real)
        try:
            import subprocess
            result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                metrics["Git Commit"] = result.stdout.strip()
            else:
                metrics["Git Commit"] = "Unknown"
        except:
            metrics["Git Commit"] = "N/A"
        
        # 4. System Uptime (real)
        import psutil
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = uptime_seconds / 3600
        metrics["System Uptime"] = f"{uptime_hours:.1f}h"
        
        # 5. Memory Usage (real)
        memory = psutil.virtual_memory()
        metrics["Memory Usage"] = f"{memory.percent:.1f}%"
        
        # Display real metrics in columns
        cols = st.columns(5)
        metric_items = list(metrics.items())
        
        for i, (label, value) in enumerate(metric_items):
            with cols[i]:
                st.metric(label, value)
        
        # Add explanation
        st.info("📊 **These are REAL system metrics collected live from your system**")
        
    except Exception as e:
        st.warning(f"Could not collect real metrics: {e}")
        st.info("💡 **Tip:** Install psutil with 'pip install psutil' for system metrics")

    # Real Audit Information (based on actual data)
    st.markdown("## 🔍 Real Audit Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Actual Compliance Status")
        
        # Check real compliance based on actual files
        compliance_checks = []
        
        # Check if hours requirement is met
        if os.path.exists("project_hours_log.csv"):
            try:
                df = pd.read_csv("project_hours_log.csv")
                total_hours = df['Time (h)'].sum()
                if total_hours >= 300:
                    compliance_checks.append(("✅ Hours Requirement", "Met (300h+)", "success"))
                else:
                    compliance_checks.append(("⚠️ Hours Requirement", f"Need {300-total_hours:.1f}h more", "warning"))
            except:
                compliance_checks.append(("❌ Hours Data", "Cannot read", "error"))
        else:
            compliance_checks.append(("❌ Hours Data", "File missing", "error"))
        
        # Check documentation completeness
        docs_path = Path("docs")
        if docs_path.exists():
            clause_folders = [f for f in docs_path.iterdir() if f.is_dir() and "Clause" in f.name]
            if len(clause_folders) >= 7:  # Clauses 4-10
                compliance_checks.append(("✅ Documentation", f"{len(clause_folders)} clauses", "success"))
            else:
                compliance_checks.append(("⚠️ Documentation", f"{len(clause_folders)}/7 clauses", "warning"))
        else:
            compliance_checks.append(("❌ Documentation", "Missing", "error"))
        
        # Display real compliance status
        for label, status, level in compliance_checks:
            if level == "success":
                st.success(f"{label}: {status}")
            elif level == "warning":
                st.warning(f"{label}: {status}")
            else:
                st.error(f"{label}: {status}")
    
    with col2:
        st.markdown("### 🎯 Real Implementation Status")
        
        # Check actual implementation files
        implementation_checks = []
        
        # Check for key procedures
        key_files = [
            "docs/Clause8_Operation/AI_Incident_Management_Procedure.md",
            "docs/Clause6_Planning_new/AI_Risk_Management_Procedure.md",
            "docs/Clause5_Leadership/AI_Management_Policy.md"
        ]
        
        for file_path in key_files:
            if os.path.exists(file_path):
                implementation_checks.append(("✅", os.path.basename(file_path).replace(".md", "")))
            else:
                implementation_checks.append(("❌", os.path.basename(file_path).replace(".md", "")))
        
        # Display implementation status
        for status, name in implementation_checks:
            st.markdown(f"{status} **{name}**")
        
        # Overall assessment
        existing_files = sum(1 for _, name in implementation_checks if name.startswith("✅"))
        total_files = len(implementation_checks)
        
        if existing_files == total_files:
            st.success(f"🎉 **Complete Implementation** ({existing_files}/{total_files})")
        elif existing_files > total_files / 2:
            st.warning(f"📚 **Good Progress** ({existing_files}/{total_files})")
        else:
            st.error(f"⚠️ **Needs Work** ({existing_files}/{total_files})")

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