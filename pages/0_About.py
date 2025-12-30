import streamlit as st
import os
import yfinance as yf

# --------------------------------------------------
# 1. GLOBAL STATE & NAVIGATION
# --------------------------------------------------
if "entity_name" not in st.session_state:
    st.session_state["entity_name"] = "Reliance Industries"

def update_entity():
    st.session_state["entity_name"] = st.session_state["entity_temp"]

# --------------------------------------------------
# 2. TERMINAL UX ENGINE & CUSTOM CSS
# --------------------------------------------------
st.set_page_config(
    page_title="About | Risk Terminal",
    page_icon="ℹ️",
    layout="wide"
)

st.markdown("""
<style>
    /* Institutional Terminal Core Theme */
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&display=swap');
    
    .stApp {
        background-color: #0c0c0c; /* Deep Terminal Black */
    }

    /* Global Typography - Terminal Amber & Monospace */
    html, body, [class*="css"], .stMarkdown, p, span, div, li {
        font-family: 'Roboto Mono', monospace !important;
        color: #ffb900 !important; /* Amber */
    }

    h1, h2, h3, h4 {
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    /* Hero Header Container */
    .about-hero {
        background: #000000;
        padding: 1.5rem 2.5rem;
        border: 1px solid #333333;
        border-top: 4px solid #0056b3; /* Institutional Blue Accent */
        margin-bottom: 20px;
    }

    /* Professional Info Cards */
    .info-card {
        background: #111111;
        padding: 24px;
        border: 1px solid #222222;
        height: 100%;
        transition: border-color 0.3s ease;
    }
    .info-card:hover {
        border-color: #00bcff;
    }
    
    .info-card h4 {
        color: #00bcff !important; /* Semantic Blue Title */
        border-bottom: 1px solid #222222;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    .sub-text {
        color: #ffb900 !important;
        font-size: 14px;
        line-height: 1.6;
    }

    /* Market Ticker Strip */
    .ticker-wrap {
        width: 100%;
        background-color: #000000;
        overflow: hidden;
        white-space: nowrap;
        padding: 8px 0;
        border-top: 1px solid #444;
        border-bottom: 1px solid #444;
        margin-bottom: 20px;
    }
    .ticker-content {
        display: inline-block;
        animation: ticker-move 60s linear infinite;
        font-size: 14px;
        color: #ffffff !important;
    }
    @keyframes ticker-move {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    /* Semantic Sentiment Colors for Ticker */
    .up { color: #00ff00 !important; font-weight: bold; }   
    .down { color: #ff3b30 !important; font-weight: bold; } 
    .ticker-item { margin-right: 60px; display: inline-block; }

    /* Customizing Tabs for Dark Theme */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #000000;
        border-bottom: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffb900 !important;
        font-family: 'Roboto Mono', monospace !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #00bcff !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #333333;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. LIVE MARKET DATA FETCHING
# --------------------------------------------------
@st.cache_data(ttl=300)
def get_live_market_data():
    try:
        indices = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
        items = []
        for name, sym in indices.items():
            t = yf.Ticker(sym)
            info = t.fast_info
            pct_change = ((info['last_price'] - info['previous_close']) / info['previous_close']) * 100
            color = "up" if pct_change >= 0 else "down"
            symbol = "▲" if pct_change >= 0 else "▼"
            items.append(f'<span class="ticker-item">{name} <span class="{color}">{info["last_price"]:,.2f} {symbol} {abs(pct_change):.2f}%</span></span>')
        strip = " ".join(items)
        return strip + " &nbsp;&nbsp;&nbsp;&nbsp; " + strip
    except:
        return "MARKET DATA OFFLINE (RECONNECTING...)"

# --------------------------------------------------
# 4. SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("### <GO> SEARCH")
    st.text_input("ENTITY NAME", value=st.session_state["entity_name"], key="entity_temp", on_change=update_entity)
    entity = st.session_state["entity_name"]
    st.markdown("---")
    st.info(f"ACTIVE ANALYSIS: {entity}")
    st.caption("Institutional Terminal v2.4.1")

# --------------------------------------------------
# 5. HEADER & TICKER
# --------------------------------------------------
st.markdown(f'<div class="ticker-wrap"><div class="ticker-content">{get_live_market_data()}</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="about-hero">
    <div style="font-size: 11px; color: #00bcff !important; margin-bottom: 8px; font-weight:bold;">PLATFORM DOCUMENTATION</div>
    <h1>ℹ️ About the Risk Terminal</h1>
    <p style="color: #ffb900 !important; font-size: 14px; margin-top: 10px;">
        Institutional-grade financial forensics and risk assessment system for professional due diligence.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 6. MAIN CONTENT: TABS
# --------------------------------------------------
tab_scope, tab_method, tab_author = st.tabs(["🎯 Mission & Scope", "🧩 Methodology", "👤 Author & Project"])

with tab_scope:
    st.write("")
    st.markdown("### 📌 Platform Objective")
    st.write(f"""
    Designed to assist analysts and auditors in identifying financial manipulation risks for **{entity}**. 
    Combines quantitative models with qualitative judgment for structured decision support.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>📊 Quantitative</h4>
            <p class="sub-text">Detection of 'window dressing' via Beneish M-Score, Altman Z-Score, and Sloan Ratio.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>🧠 Qualitative</h4>
            <p class="sub-text">Interpreting numeric context via management sentiment analysis and auditor risk signals.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="info-card">
            <h4>✅ Verdict</h4>
            <p class="sub-text">Structured posture (Safe / Caution / High Risk) derived from aggregated forensic datasets.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.error("**⚠️ LIMITATIONS:** Screening tool only. Does not replace full due diligence or professional investment advice.")

with tab_method:
    st.write("")
    st.markdown("### 🧩 Core Forensic Modules")
    
    m1, m2 = st.columns(2)
    with m1:
        st.info("**FINANCIAL FORENSICS ENGINE**")
        st.markdown("""
        - **BENEISH M-SCORE**: Detection of earnings manipulation.
        - **ALTMAN Z-SCORE**: Bankruptcy and distress assessment.
        - **SLOAN RATIO**: Evaluation of accrual quality.
        """)
    with m2:
        st.info("**QUALITATIVE ASSESSMENT**")
        st.markdown("""
        - **MANAGEMENT TONE**: NLP scan of RHP/Annual disclosures.
        - **AUDITOR SIGNALS**: Integrity and independence monitoring.
        - **GOVERNANCE SCAN**: Related Party Transactions (RPT) review.
        """)

with tab_author:
    st.write("")
    st.markdown("### 👤 About the Author")
    
    auth_col1, auth_col2 = st.columns([1, 2])
    with auth_col1:
        # Placeholder/Profile logic
        if os.path.exists("assets/profile.jpg"):
            st.image("assets/profile.jpg", use_container_width=True)
        else:
            st.image("https://via.placeholder.com/400x400/111111/ffb900?text=Pratyush+Kumar", use_container_width=True)

    with auth_col2:
        st.markdown("""
        #### **Pratyush Kumar**
        *MBA (Finance)*

        **PROJECT FOCUS:**
        - Financial Forensics & Fraud Detection
        - Equity Research Workflow Optimization
        - AI-Assisted Risk Identification

        Developed as part of the *Working with AI (WAI)* course, integrating financial accounting theory with modern analytics.
        """)

# --------------------------------------------------
# 7. FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption(f"Forensic Risk Platform | {entity} | Developed by Pratyush Kumar")