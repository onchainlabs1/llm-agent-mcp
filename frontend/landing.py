import streamlit as st

st.set_page_config(
    page_title="AgentMCP – AI Tool Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Lovable-style CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, .stApp { background: #181c24; color: #f3f6fa; font-family: 'Inter', sans-serif; }
    .main { background: #181c24; }
    .block-container { padding-top: 146px !important; padding-bottom: 0 !important; max-width: 100vw !important; margin-top: 0 !important; }
    /* Header Lovable */
    .lovable-header {
        position: fixed;
        top: 3.5rem;
        left: 0; right: 0;
        background: #181c24;
        z-index: 100000;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 3vw;
        box-shadow: 0 2px 16px #0003;
        border-bottom: 1.5px solid #23283a;
    }
    .lovable-logo {
        font-size: 2.2rem;
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
        height: 2.2rem;
        width: 2.2rem;
        display: inline-block;
    }
    .lovable-nav {
        display: flex;
        gap: 2.7rem;
        align-items: center;
    }
    .lovable-nav a {
        color: #f3f6fa;
        font-size: 1.15rem;
        font-weight: 700;
        text-decoration: none;
        transition: color 0.2s;
        letter-spacing: 0.01em;
        padding: 2px 0;
        border-bottom: 2.5px solid transparent;
    }
    .lovable-nav a:hover {
        color: #6f47eb;
        border-bottom: 2.5px solid #6f47eb;
    }
    .lovable-search {
        background: #23283a;
        border-radius: 8px;
        padding: 0.5rem 1.3rem;
        color: #fff;
        border: none;
        font-size: 1.08rem;
        margin-left: 1.7rem;
        min-width: 190px;
    }
    .lovable-search::placeholder { color: #b0b8c9; }
    /* Hero Lovable */
    .hero-bg {
        background: linear-gradient(90deg, #23283a 0%, #3b82f6 60%, #06d6a0 100%);
        border-radius: 22px;
        padding: 4.2rem 2.5rem 3.2rem 2.5rem;
        margin: 0 auto 4.5rem auto;
        text-align: center;
        box-shadow: 0 4px 32px #0002;
        max-width: 1100px;
        min-width: 700px;
    }
    .hero-title {
        font-size: 3.3rem;
        font-weight: 900;
        color: #fff;
        margin-bottom: 1.3rem;
        letter-spacing: -1px;
        line-height: 1.18;
        text-shadow: none;
    }
    .hero-sub {
        font-size: 1.18rem;
        color: #c9d6e9;
        margin-bottom: 2.7rem;
        font-weight: 400;
        line-height: 1.6;
    }
    .cta-btn {
        background: #22c55e;
        color: #fff;
        border-radius: 12px;
        padding: 1.1rem 3.2rem;
        font-size: 1.25rem;
        font-weight: 900;
        border: none;
        margin-bottom: 2.5rem;
        box-shadow: 0 2px 12px #0002;
        cursor: pointer;
        transition: 0.2s;
        letter-spacing: 0.01em;
    }
    .cta-btn:hover { filter: brightness(1.08); }
    .section-title {
        font-size: 2.7rem;
        font-weight: 900;
        margin-top: 5.5rem;
        margin-bottom: 3.2rem;
        color: #fff;
        text-align: center;
        letter-spacing: -0.5px;
    }
    .features-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2.7rem;
        margin-bottom: 4.5rem;
    }
    .feature-card {
        background: #23283a;
        border-radius: 20px;
        padding: 2.2rem 2.1rem 1.7rem 2.1rem;
        min-width: 300px;
        max-width: 350px;
        flex: 1 1 300px;
        box-shadow: 0 2px 16px #0002;
        text-align: left;
        margin-bottom: 0.5rem;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .feature-icon {
        width: 48px; height: 48px;
        margin-bottom: 1.1rem;
        display: block;
    }
    .feature-title {
        font-size: 1.25rem;
        font-weight: 900;
        margin-bottom: 0.7rem;
        color: #fff;
    }
    .feature-desc {
        font-size: 1.08rem;
        color: #b0b8c9;
    }
    .example-list li { margin-bottom: 0.8rem; font-size: 1.18rem; }
    .roadmap-list li { margin-bottom: 0.8rem; font-size: 1.18rem; }
    .github-btn {
        background: #3b82f6;
        color: #fff;
        border-radius: 12px;
        padding: 1.1rem 2.8rem;
        font-size: 1.18rem;
        font-weight: 900;
        border: none;
        margin: 4.5rem auto 0 auto;
        display: block;
        box-shadow: 0 2px 12px #0002;
        text-align: center;
        transition: 0.2s;
        letter-spacing: 0.01em;
    }
    .github-btn:hover { filter: brightness(1.08); }
    a { color: #3b82f6; text-decoration: none; }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Header ---
st.markdown(
    """
<div class="lovable-header">
    <div class="lovable-logo">
        <svg viewBox="0 0 32 32" fill="none"><defs><linearGradient id="g1" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse"><stop stop-color="#ff6f91"/><stop offset="1" stop-color="#6fffb0"/></linearGradient></defs><path d="M16 29s-9-6.5-9-14.5A7 7 0 0 1 16 7a7 7 0 0 1 9 7.5C25 22.5 16 29 16 29Z" fill="url(#g1)"/><circle cx="16" cy="13.5" r="3.5" fill="#fff"/><rect x="13.5" y="21" width="5" height="5" rx="2.5" fill="#3b82f6"/><rect x="10" y="25.5" width="12" height="3" rx="1.5" fill="#22c55e"/></svg>
        AgentMCP
    </div>
    <div class="lovable-nav">
        <a href="#">Home</a>
        <a href="#features">Features</a>
        <a href="#examples">Examples</a>
        <a href="#try-it-locally">Try It</a>
        <a href="https://github.com/onchainlabs1/llm-agent-mcp" target="_blank">GitHub</a>
        <input class="lovable-search" type="text" placeholder="Search..." disabled />
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- Hero Section ---
st.markdown(
    """
<div class="hero-bg">
    <div class="hero-title">AgentMCP – Autonomous AI Tool Hub for Business Operations</div>
    <div class="hero-sub">The LLM-powered agent that executes real CRM & ERP actions from natural language.<br>Secure, auditable, and fully extensible via the Model Context Protocol (MCP).</div>
    <a href="#try-it-locally"><button class="cta-btn">🚀 Try AgentMCP on Your Data</button></a>
</div>
""",
    unsafe_allow_html=True,
)

# --- Features ---
st.markdown(
    '<div class="section-title" id="features">What It Can Do</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="features-row">
    <div class="feature-card">
        <svg class="feature-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="#6fffb0" stroke-width="2.5"/><path d="M8 12l2 2 4-4" stroke="#6fffb0" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <div class="feature-title">CRM Automation</div>
        <div class="feature-desc">Instantly create, update, and query client records using plain English. Manage balances, contacts, and more—no manual data entry.</div>
    </div>
    <div class="feature-card">
        <svg class="feature-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="13" rx="2" stroke="#00c6fb" stroke-width="2.5"/><path d="M16 3v4M8 3v4" stroke="#00c6fb" stroke-width="2.5" stroke-linecap="round"/></svg>
        <div class="feature-title">ERP Operations</div>
        <div class="feature-desc">Place and track orders, update statuses, and list all transactions. Simulate real business flows with full auditability.</div>
    </div>
    <div class="feature-card">
        <svg class="feature-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="#fbbf24" stroke-width="2.5"/><path d="M12 8v4l3 3" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/></svg>
        <div class="feature-title">Auditing & Traceability</div>
        <div class="feature-desc">Every action is logged with tool, parameters, and outcome. Full transparency for compliance and debugging.</div>
    </div>
    <div class="feature-card">
        <svg class="feature-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="4" stroke="#a78bfa" stroke-width="2.5"/><path d="M8 12h8M12 8v8" stroke="#a78bfa" stroke-width="2.5" stroke-linecap="round"/></svg>
        <div class="feature-title">Extensible by Design</div>
        <div class="feature-desc">Add new business domains or tools by simply updating MCP schemas and service modules. Built for rapid prototyping and enterprise integration.</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- How It Works (Lovable Card Style) ---
st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="howitworks-row">
  <div class="howitworks-card"><div class="howitworks-num">1</div><div><b>User Prompt</b><br><span>Enter a natural language instruction (e.g., "Create client Anna with balance 5000").</span></div></div>
  <div class="howitworks-card"><div class="howitworks-num">2</div><div><b>Tool Selection via MCP</b><br><span>AgentMCP parses your request, matches it to the right tool using the Model Context Protocol.</span></div></div>
  <div class="howitworks-card"><div class="howitworks-num">3</div><div><b>Parameter Extraction</b><br><span>The agent extracts all required parameters from your prompt using LLM and regex logic.</span></div></div>
  <div class="howitworks-card"><div class="howitworks-num">4</div><div><b>Secure Execution</b><br><span>The mapped service function is called—no direct database or shell access.</span></div></div>
  <div class="howitworks-card"><div class="howitworks-num">5</div><div><b>Result & Logging</b><br><span>The result is shown instantly, and the full action (tool, params, result) is logged for audit.</span></div></div>
</div>
""",
    unsafe_allow_html=True,
)

# --- Examples (Lovable Card Style) ---
st.markdown(
    '<div class="section-title" id="examples">Examples</div>', unsafe_allow_html=True
)
st.markdown(
    """
<div class="examples-row">
                      <div class="example-card">💡 <span>Get client <b>john123</b></span></div>
  <div class="example-card">💡 <span>List all orders</span></div>
  <div class="example-card">💡 <span>Update order <b>ORD-20250601-001</b> to shipped</span></div>
                      <div class="example-card">💡 <span>Create client <b>Anna</b> with email <b>anna@example.com</b> and balance <b>5000</b></span></div>
                      <div class="example-card">💡 <span>Create order for client <b>john123</b> with total amount <b>1200</b></span></div>
</div>
""",
    unsafe_allow_html=True,
)

# --- Try It Locally (Lovable Card Style) ---
st.markdown(
    '<div class="section-title" id="try-it-locally">Try It Locally</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="try-card">
  <div class="try-icon">🖥️</div>
  <div class="try-steps">
    <div class="try-step"><b>1. Clone the repo</b></div>
    <pre class="try-code">git clone https://github.com/onchainlabs1/llm-agent-mcp.git
cd llm-agent-mcp</pre>
    <div class="try-step"><b>2. Install dependencies</b></div>
    <pre class="try-code">pip install -r requirements.txt</pre>
    <div class="try-step"><b>3. Run the Streamlit app</b></div>
    <pre class="try-code">streamlit run frontend/app.py</pre>
    <div class="try-step"><b>4. Open in your browser</b></div>
    <pre class="try-code">http://localhost:8501</pre>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- Tech Stack ---
st.markdown('<div class="section-title">Tech Stack</div>', unsafe_allow_html=True)
st.markdown(
    """
- <b>Python 3.11</b> – Core logic and services
- <b>Streamlit</b> – Modern, interactive frontend
- <b>Model Context Protocol (MCP)</b> – Secure tool discovery & execution
- <b>JSON</b> – Lightweight, file-based persistence
- <b>pytest</b> – Automated testing
- <b>Structured Logging</b> – Full audit trail of all actions
""",
    unsafe_allow_html=True,
)

# --- Roadmap ---
st.markdown(
    '<div class="section-title">Roadmap / Future Additions</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<ul class="roadmap-list">
<li>🔒 <b>User Authentication & Role-Based Access</b></li>
<li>🌐 <b>Multi-domain Support (HR, Finance, Custom Tools)</b></li>
<li>📊 <b>Advanced Analytics & Dashboarding</b></li>
<li>☁️ <b>Cloud Deployment & API Integrations</b></li>
</ul>
""",
    unsafe_allow_html=True,
)

# --- GitHub CTA ---
st.markdown(
    '<a href="https://github.com/onchainlabs1/llm-agent-mcp" target="_blank"><button class="github-btn">View the AgentMCP Repository on GitHub →</button></a>',
    unsafe_allow_html=True,
)

# --- Lovable Card CSS ---
st.markdown(
    """
<style>
.howitworks-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2.2rem;
  margin: 0 auto 3.5rem auto;
  max-width: 1200px;
}
.howitworks-card {
  background: #23283a;
  border-radius: 18px;
  box-shadow: 0 2px 16px #0002;
  padding: 2.1rem 2.2rem 1.5rem 2.2rem;
  min-width: 260px;
  max-width: 320px;
  flex: 1 1 260px;
  display: flex;
  align-items: flex-start;
  gap: 1.2rem;
  font-size: 1.08rem;
  color: #f3f6fa;
}
.howitworks-num {
  font-size: 2.2rem;
  font-weight: 900;
  color: #6fffb0;
  min-width: 2.7rem;
  text-align: center;
  margin-top: -0.2rem;
}
.howitworks-card b { font-size: 1.13rem; color: #fff; }
.howitworks-card span { color: #b0b8c9; font-size: 1.05rem; }

.examples-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.7rem;
  margin: 0 auto 3.5rem auto;
  max-width: 1100px;
}
.example-card {
  background: #23283a;
  border-radius: 16px;
  box-shadow: 0 2px 12px #0002;
  padding: 1.3rem 2.1rem;
  font-size: 1.13rem;
  color: #f3f6fa;
  min-width: 260px;
  max-width: 350px;
  flex: 1 1 220px;
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.example-card b { color: #6fffb0; }

.try-card {
  background: #23283a;
  border-radius: 18px;
  box-shadow: 0 2px 16px #0002;
  padding: 2.2rem 2.2rem 1.5rem 2.2rem;
  max-width: 600px;
  margin: 0 auto 3.5rem auto;
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
}
.try-icon {
  font-size: 2.3rem;
  margin-top: 0.2rem;
}
.try-steps { flex: 1; }
.try-step { font-size: 1.13rem; color: #fff; margin-top: 0.7rem; margin-bottom: 0.2rem; }
.try-code {
  background: #181c24;
  color: #6fffb0;
  font-family: 'Fira Mono', 'Consolas', 'Menlo', monospace;
  font-size: 1.08rem;
  border-radius: 8px;
  padding: 0.7rem 1.1rem;
  margin-bottom: 0.7rem;
  margin-top: 0.1rem;
  overflow-x: auto;
}
</style>
""",
    unsafe_allow_html=True,
)
