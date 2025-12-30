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
st.set_page_config(page_title="Forensic Risk Terminal", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    /* Institutional Terminal Core Theme */
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&display=swap');
    
    .stApp {
        background-color: #0c0c0c; /* Deep Terminal Black */
    }

    /* Global Typography - Terminal Amber & Monospace */
    html, body, [class*="css"], .stMarkdown, p, span, div {
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
    .hero-container {
        background: #000000;
        padding: 1.5rem 2.5rem;
        border: 1px solid #333333;
        border-top: 4px solid #0056b3; /* Institutional Blue Accent */
        margin-bottom: 20px;
    }

    /* Terminal Data Cards */
    .section-card {
        background: #111111;
        padding: 24px;
        border: 1px solid #222222;
        height: 100%;
        transition: border-color 0.3s ease;
    }
    .section-card:hover {
        border-color: #00bcff;
    }
    .section-card h4 {
        color: #00bcff !important; /* Semantic Blue Title */
        border-bottom: 1px solid #222222;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    /* Market Ticker Strip (Moving Tape) */
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

    /* Semantic Sentiment Colors */
    .up { color: #00ff00 !important; font-weight: bold; }   /* Terminal Green */
    .down { color: #ff3b30 !important; font-weight: bold; } /* Terminal Red */
    .ticker-item { margin-right: 60px; display: inline-block; }

    /* Command Input / Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #333333;
    }
    .stTextInput > div > div > input {
        background-color: #000 !important;
        color: #ffb900 !important;
        border: 1px solid #444 !important;
        font-family: 'Roboto Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. LIVE MARKET DATA
# --------------------------------------------------
@st.cache_data(ttl=300)
def get_live_market_data():
    try:
        indices = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI", "RELIANCE": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC BANK": "HDFCBANK.NS"}
        items = []
        for name, sym in indices.items():
            t = yf.Ticker(sym)
            info = t.fast_info
            pct_change = ((info['last_price'] - info['previous_close']) / info['previous_close']) * 100
            color = "up" if pct_change >= 0 else "down"
            items.append(f'<span class="ticker-item">{name} <span class="{color}">{info["last_price"]:,.2f} {"▲" if pct_change >= 0 else "▼"} {abs(pct_change):.2f}%</span></span>')
        strip = " ".join(items)
        return strip + " &nbsp;&nbsp;&nbsp;&nbsp; " + strip
    except:
        return "MARKET DATA OFFLINE (RECONNECTING...)"

# --------------------------------------------------
# 4. SIDEBAR (COMMAND PANEL)
# --------------------------------------------------
with st.sidebar:
    st.markdown("### <GO> SEARCH")
    st.text_input("ENTITY NAME", value=st.session_state["entity_name"], key="entity_temp", on_change=update_entity)
    entity = st.session_state["entity_name"]
    st.markdown("---")
    st.info(f"TERMINAL ACTIVE: {entity}")
    st.caption("Institutional Terminal v2.4.1")

# --------------------------------------------------
# 5. MAIN TERMINAL INTERFACE
# --------------------------------------------------

# LIVE MARKET TICKER
st.markdown(f'<div class="ticker-wrap"><div class="ticker-content">{get_live_market_data()}</div></div>', unsafe_allow_html=True)

# HERO SECTION
st.markdown(f"""
<div class="hero-container">
    <div style="font-size: 11px; color: #00bcff !important; margin-bottom: 8px; font-weight:bold;">FORENSIC INTEL PLATFORM</div>
    <h1>Forensic Auditing & IPO Risk Analyzer</h1>
    <p style="font-size: 16px; margin-top: 10px; color: #ffb900 !important;">
        Institutional Screening for <b>{entity}</b> | DATA ENGINE V2.4
    </p>
</div>
""", unsafe_allow_html=True)

# DATA GRID
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="section-card">
        <h4>📊 Financial Lab</h4>
        <p style="font-size: 14px;">
            Quantitative screening for window dressing:<br><br>
            • BENEISH M-SCORE<br>
            • ALTMAN Z-SCORE<br>
            • SLOAN RATIO
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-card">
        <h4>🧠 Qualitative Lab</h4>
        <p style="font-size: 14px;">
            Governance & Narrative Analysis:<br><br>
            • MANAGEMENT TONE SCAN<br>
            • AUDITOR RISK SIGNALS<br>
            • RPT MONITORING
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="section-card">
        <h4>✅ Risk Verdict</h4>
        <p style="font-size: 14px;">
            Integrated Decision Support:<br><br>
            • SAFE / CAUTION / HIGH RISK<br>
            • EVIDENCE LOGGING<br>
            • INVESTMENT SIGN-OFF
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("### 🧭 ANALYST WORKFLOW")
st.markdown(f"1. **FINANCIAL LAB**: INPUT DATA FOR {entity} &nbsp;&nbsp; 2. **QUALITATIVE LAB**: SCAN NARRATIVE &nbsp;&nbsp; 3. **VERDICT**: REVIEW RISK POSTURE")

st.markdown("---")
st.caption(f"Forensic Risk Platform | {entity} | Developed by Pratyush Kumar")