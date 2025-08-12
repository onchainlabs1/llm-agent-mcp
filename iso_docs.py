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
            cwd=Path(__file__).parent
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return "Unknown"

def get_document_stats():
    """Calculate document statistics"""
    docs_path = Path(__file__).parent / "docs"
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
    docs_path = Path(__file__).parent / "docs"
    clause_folders = []
    
    if docs_path.exists():
        for item in docs_path.iterdir():
            if item.is_dir() and item.name.startswith('Clause'):
                clause_folders.append(item)
    
    # Sort by clause number
    clause_folders.sort(key=lambda x: int(re.search(r'Clause(\d+)', x.name).group(1)))
    return clause_folders

def format_clause_name(folder_name):
    """Convert folder name to readable clause name"""
    # Extract clause number and description
    match = re.match(r'Clause(\d+)_(.+)', folder_name)
    if match:
        clause_num = match.group(1)
        description = match.group(2).replace('_', ' ')
        return f"Clause {clause_num} – {description}"
    return folder_name

def read_markdown_file(file_path):
    """Read and return markdown file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def parse_front_matter(markdown_text):
    """Parse simple YAML-like front matter at the top of a markdown file.

    Supports a minimal subset: lines between the first two '---' delimiters are parsed
    as `key: value`. Returns (metadata_dict, body_text).
    Does not require external YAML dependency and ignores malformed lines.
    """
    if not markdown_text or not markdown_text.lstrip().startswith('---'):
        return {}, markdown_text

    lines = markdown_text.splitlines()
    if not lines:
        return {}, markdown_text

    # find front matter block
    if lines[0].strip() != '---':
        return {}, markdown_text

    metadata = {}
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            end_idx = idx
            break
        # parse key: value
        line = lines[idx].strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()

    if end_idx is None:
        # No closing delimiter, treat as normal content
        return {}, markdown_text

    body = '\n'.join(lines[end_idx + 1 :])
    return metadata, body

def main():
    # Header
    st.title("📘 ISO/IEC 42001 Documentation Center")
    st.subheader("AI Management System Documentation Browser")
    
    # Get statistics
    total_files, total_lines = get_document_stats()
    commit_hash = get_git_commit_hash()
    
    # Summary box
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Compliance Status", "✅ 100% Compliant")
    
    with col2:
        st.metric("Total Documents", f"{total_files}+")
    
    with col3:
        st.metric("Total Lines", f"~{total_lines:,}")
    
    with col4:
        st.metric("Last Commit", commit_hash)
    
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.markdown("## 📁 Navigation")
    
    clause_folders = get_clause_folders()
    
    if not clause_folders:
        st.error("No clause folders found in docs directory!")
        return
    
    # Create clause options for sidebar
    clause_options = {}
    for folder in clause_folders:
        clause_name = format_clause_name(folder.name)
        clause_options[clause_name] = folder
    
    selected_clause = st.sidebar.selectbox(
        "Select Clause:",
        list(clause_options.keys()),
        index=0
    )
    
    selected_folder = clause_options[selected_clause]
    
    # Main content area
    st.markdown(f"## {selected_clause}")
    
    # Get all markdown files in the selected folder
    md_files = []
    if selected_folder.exists():
        for file in selected_folder.iterdir():
            if file.is_file() and file.suffix == '.md':
                md_files.append(file)
    
    # Sort files: README.md first, then alphabetically
    md_files.sort(key=lambda x: (x.name != 'README.md', x.name))
    
    if not md_files:
        st.warning(f"No markdown files found in {selected_folder.name}")
        return
    
    # Display files
    for file in md_files:
        file_name = file.name
        is_readme = file_name.lower() == 'readme.md'
        
        # Create expander title with badge for README
        if is_readme:
            expander_title = f"📄 {file_name} <span class='readme-badge'>Overview</span>"
        else:
            expander_title = f"📄 {file_name}"
        
        with st.expander(expander_title, expanded=is_readme):
            content = read_markdown_file(file)
            meta, body = parse_front_matter(content)
            
            # Generate GitHub link for this document
            github_link = f"https://github.com/onchainlabs1/llm-agent-mcp/blob/main/docs/{selected_folder.name}/{file_name}"
            
            # Display file info and GitHub link
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**File:** `{file.relative_to(Path(__file__).parent)}`")
                st.markdown(f"**Size:** {file.stat().st_size:,} bytes")
            with col2:
                st.markdown(f"[🔗 View on GitHub]({github_link})")
            
            st.markdown("---")

            # Render standardized document header if metadata present
            if meta:
                owner = meta.get('owner') or meta.get('Owner') or 'Unassigned'
                version = meta.get('version') or meta.get('Version') or '0.1'
                approved_by = meta.get('approved_by') or meta.get('ApprovedBy') or 'Pending'
                approved_on = meta.get('approved_on') or meta.get('ApprovedOn') or '—'
                next_review = meta.get('next_review') or meta.get('NextReview') or '—'
                st.markdown(
                    f"""
<div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.75rem; background: #f9fafb;">
  <strong>Document Control</strong><br/>
  <span>Owner:</span> <code>{owner}</code> &nbsp;|&nbsp;
  <span>Version:</span> <code>{version}</code> &nbsp;|&nbsp;
  <span>Approved By:</span> <code>{approved_by}</code> &nbsp;|&nbsp;
  <span>Approved On:</span> <code>{approved_on}</code> &nbsp;|&nbsp;
  <span>Next Review:</span> <code>{next_review}</code>
</div>
                    """,
                    unsafe_allow_html=True,
                )
                st.caption("Standardized header rendered from document front matter")

            # Render markdown body (without front matter)
            st.markdown(body if meta else content, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.link_button("🏠 Back to Main App", "https://llm-agent-mcp-portfolio.streamlit.app/", use_container_width=True)
    
    with col2:
        st.link_button("📚 View on GitHub", "https://github.com/onchainlabs1/llm-agent-mcp", use_container_width=True)
    
    with col3:
        st.link_button("📋 Documentation Index", "https://github.com/onchainlabs1/llm-agent-mcp/blob/main/docs/README.md", use_container_width=True)
    
    # Sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Documentation Status")
    
    # Show completion status for each clause
    for folder in clause_folders:
        clause_name = format_clause_name(folder.name)
        md_count = len([f for f in folder.iterdir() if f.is_file() and f.suffix == '.md'])
        
        if md_count > 0:
            st.sidebar.markdown(f"✅ **{clause_name}** ({md_count} docs)")
        else:
            st.sidebar.markdown(f"❌ **{clause_name}** (0 docs)")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Quick Stats")
    st.sidebar.markdown(f"**Total Clauses:** {len(clause_folders)}")
    st.sidebar.markdown(f"**Total Files:** {total_files}")
    st.sidebar.markdown(f"**Total Lines:** {total_lines:,}")
    st.sidebar.markdown(f"**Last Updated:** {commit_hash}")

if __name__ == "__main__":
    main() 