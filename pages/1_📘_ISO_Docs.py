"""
ISO/IEC 42001:2023 Documentation Browser
Streamlit Cloud Compatible Version
"""

import streamlit as st
import os
import subprocess
from pathlib import Path
import re

# Page configuration
st.set_page_config(
    page_title="ISO/IEC 42001:2023 Documentation Browser",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .compliance-badge {
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
    }
    .document-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f8f9fa;
    }
    .readme-badge {
        background: #ffc107;
        color: #212529;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def get_git_commit_hash():
    """Get the current Git commit hash"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return "Unknown"

def get_document_stats():
    """Calculate document statistics"""
    docs_path = Path(__file__).parent.parent / "docs"
    total_files = 0
    total_lines = 0
    
    if docs_path.exists():
        for root, dirs, files in os.walk(docs_path):
            for file in files:
                if file.endswith('.md'):
                    total_files += 1
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            total_lines += len(f.readlines())
                    except:
                        pass
    
    return total_files, total_lines

def get_clause_folders():
    """Get all clause folders from docs directory"""
    docs_path = Path(__file__).parent.parent / "docs"
    clause_folders = []
    
    if docs_path.exists():
        for item in docs_path.iterdir():
            if item.is_dir() and item.name.startswith('Clause'):
                clause_folders.append(item)
    
    # Sort by clause number
    clause_folders.sort(key=lambda x: int(re.search(r'\d+', x.name).group()) if re.search(r'\d+', x.name) else 0)
    return clause_folders

def get_readme_content(folder_path):
    """Get README content from a folder"""
    readme_path = folder_path / "README.md"
    if readme_path.exists():
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract title from first heading
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else folder_path.name
                return title, content
        except:
            pass
    return folder_path.name, ""

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📘 ISO/IEC 42001:2023 Documentation Browser</h1>
        <p>AI Management System (AIMS) - Complete Governance Framework</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with project info
    with st.sidebar:
        st.header("📊 Project Information")
        
        # Git commit info
        commit_hash = get_git_commit_hash()
        st.info(f"**Git Commit:** {commit_hash}")
        
        # Document statistics
        total_files, total_lines = get_document_stats()
        st.metric("📄 Total Documents", total_files)
        st.metric("📝 Total Lines", f"{total_lines:,}")
        
        # Compliance status
        st.markdown("---")
        st.header("✅ Compliance Status")
        st.markdown("""
        - **Clause 4**: Context & Scope ✅
        - **Clause 5**: Leadership & Policy ✅
        - **Clause 6**: Planning & Risk Management ✅
        - **Clause 7**: Support & Resources ✅
        - **Clause 8**: Operations & Control ✅
        - **Clause 9**: Performance Evaluation ✅
        - **Clause 10**: Improvement ✅
        """)
        
        # Quick navigation
        st.markdown("---")
        st.header("🚀 Quick Navigation")
        if st.button("📋 ISO Dashboard", use_container_width=True):
            st.switch_page("iso_dashboard.py")
        if st.button("🏠 Main App", use_container_width=True):
            st.switch_page("app.py")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📚 Documentation Structure")
        st.markdown("""
        This project implements a complete ISO/IEC 42001:2023 AI Management System (AIMS) 
        governance framework. All documentation is organized by ISO clauses and includes 
        procedures, policies, and evidence templates.
        """)
        
        # Compliance badge
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <span class="compliance-badge">ISO 42001:2023 COMPLIANT</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.header("🎯 Key Features")
        st.markdown("""
        ✅ **Complete Framework** - All ISO clauses covered  
        ✅ **Procedures** - Step-by-step implementation guides  
        ✅ **Templates** - Ready-to-use forms and checklists  
        ✅ **Evidence** - Audit-ready documentation  
        ✅ **Risk Management** - Comprehensive risk register  
        ✅ **Continuous Improvement** - PDCA cycle implementation  
        """)
    
    # Clause folders
    st.markdown("---")
    st.header("📖 Clause Documentation")
    
    clause_folders = get_clause_folders()
    
    if not clause_folders:
        st.warning("No clause folders found. Please check the docs directory structure.")
        return
    
    # Create tabs for each clause
    tab_names = [folder.name for folder in clause_folders]
    tabs = st.tabs(tab_names)
    
    for i, (tab, folder) in enumerate(zip(tabs, clause_folders)):
        with tab:
            st.subheader(f"📋 {folder.name}")
            
            # Get README content
            title, content = get_readme_content(folder)
            if content:
                st.markdown(f"**{title}**")
                st.markdown(content)
            else:
                st.info(f"No README found in {folder.name}")
            
            # List files in folder
            st.markdown("**📄 Documents in this clause:**")
            files = list(folder.glob("*.md"))
            if files:
                for file in files:
                    if file.name != "README.md":
                        st.markdown(f"- 📄 [{file.stem}]({file})")
            else:
                st.info("No additional documents found")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>ISO/IEC 42001:2023 AI Management System Documentation</p>
        <p>Built with Streamlit | Professional Governance Framework</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
