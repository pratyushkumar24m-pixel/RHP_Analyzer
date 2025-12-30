import streamlit as st
import pandas as pd
import io
import re
import os
import yfinance as yf
from PyPDF2 import PdfReader
from financial_core import compute_all_metrics

# --------------------------------------------------
# 1. GLOBAL STATE & NAVIGATION
# --------------------------------------------------
if "entity_name" not in st.session_state:
    st.session_state["entity_name"] = "Reliance Industries"

def update_entity():
    st.session_state["entity_name"] = st.session_state["entity_temp"]

def clear_qual_data():
    if "qualitative_results" in st.session_state:
        del st.session_state["qualitative_results"]
    st.toast("QUALITATIVE ASSESSMENT RESET.")

# --------------------------------------------------
# 2. TERMINAL UX ENGINE & CUSTOM CSS
# --------------------------------------------------
st.set_page_config(page_title="QUALITATIVE LAB | TERMINAL", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    /* Institutional Terminal Core Theme */
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&display=swap');
    
    .stApp { background-color: #0c0c0c; }

    /* Global Typography - Terminal Amber & Monospace */
    html, body, [class*="css"], .stMarkdown, p, span, div, label, li {
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
        padding: 2.5rem;
        border: 1px solid #333333;
        border-top: 4px solid #0056b3; /* Institutional Blue Accent */
        margin-bottom: 20px;
    }

    /* Sub-title Styling */
    .sub-title {
        color: #00bcff !important;
        font-weight: 700;
        border-bottom: 1px solid #222222;
        padding-bottom: 8px;
        margin-top: 30px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    /* Analyst Recommendation Cards */
    .recommendation-card {
        background: #111111;
        padding: 20px;
        border-radius: 4px;
        border: 1px solid #333333;
        border-top: 4px solid #00bcff;
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

    /* Semantic Sentiment Colors */
    .up { color: #00ff00 !important; font-weight: bold; }   
    .down { color: #ff3b30 !important; font-weight: bold; } 
    .ticker-item { margin-right: 60px; display: inline-block; }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #000; border-bottom: 1px solid #333; }
    .stTabs [data-baseweb="tab"] { color: #ffb900 !important; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #00bcff !important; color: #fff !important; }

    /* Input/Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #333333; }
    .stTextArea textarea { background-color: #000 !important; color: #ffb900 !important; border: 1px solid #444 !important; }
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
            items.append(f'<span class="ticker-item">{name} <span class="{color}">{info["last_price"]:,.2f} {"▲" if pct_change >= 0 else "▼"} {abs(pct_change):.2f}%</span></span>')
        strip = " ".join(items)
        return strip + " &nbsp;&nbsp;&nbsp;&nbsp; " + strip
    except:
        return "MARKET DATA OFFLINE (RECONNECTING...)"

# --------------------------------------------------
# 4. SIDEBAR & PRECONDITION
# --------------------------------------------------
with st.sidebar:
    st.markdown("### <GO> SEARCH")
    st.text_input("ENTITY NAME", value=st.session_state["entity_name"], key="entity_temp", on_change=update_entity)
    if "qualitative_results" in st.session_state:
        st.button("🗑️ CLEAR QUALITATIVE DATA", on_click=clear_qual_data, use_container_width=True)
    entity = st.session_state["entity_name"]
    st.info(f"TERMINAL ACTIVE: {entity}")

if "financial_data" not in st.session_state:
    st.error("⚠️ FINANCIAL ANALYSIS MISSING. COMPLETE STEP 1.")
    st.stop()

# --------------------------------------------------
# 5. HEADER & TICKER
# --------------------------------------------------
st.markdown(f'<div class="ticker-wrap"><div class="ticker-content">{get_live_market_data()}</div></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="hero-container">
    <div style="background: #0056b3; color: #fff; padding: 4px 12px; border-radius: 2px; font-size: 11px; font-weight: 700; display: inline-block; margin-bottom: 10px;">
        FINAL STAGE: VERDICT ENGINE
    </div>
    <h1>🧠 QUALITATIVE ASSESSMENT & VERDICT: {entity}</h1>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 6. QUALITATIVE INPUT MODULES
# --------------------------------------------------
st.markdown('<div class="sub-title">🛡️ ASSESSMENT METHODOLOGY</div>', unsafe_allow_html=True)

method_tabs = st.tabs(["🧠 ANALYST JUDGMENT", "📄 AUTOMATED RHP FETCHER", "✍️ NARRATIVE SUMMARY"])

if "qualitative_results" not in st.session_state:
    st.session_state["qualitative_results"] = {"tone": "Balanced", "auditor": "Clean", "disclosure": "Standard"}

current_qual = st.session_state["qualitative_results"]

with method_tabs[0]:
    c1, c2, c3 = st.columns(3)
    t_opts = ["Conservative", "Balanced", "Aggressive"]
    a_opts = ["Clean", "Emphasis of Matter", "Qualified"]
    d_opts = ["Detailed", "Standard", "Weak"]
    
    tone_sel = c1.selectbox("MANAGEMENT TONE", t_opts, index=t_opts.index(current_qual.get("tone", "Balanced")))
    auditor_sel = c2.selectbox("AUDITOR OPINION", a_opts, index=a_opts.index(current_qual.get("auditor", "Clean")))
    disclosure_sel = c3.selectbox("RISK DISCLOSURE QUALITY", d_opts, index=d_opts.index(current_qual.get("disclosure", "Standard")))
    
    if st.button("💾 SAVE ANALYST JUDGMENT", use_container_width=True):
        st.session_state["qualitative_results"] = {"tone": tone_sel, "auditor": auditor_sel, "disclosure": disclosure_sel}
        st.rerun()

with method_tabs[1]:
    st.write("### 📄 RHP AUTOMATED SENTIMENT FETCHER")
    uploaded_pdf = st.file_uploader("UPLOAD RHP PDF FOR SCAN", type=["pdf"])
    if uploaded_pdf:
        with st.spinner("RAPID SCAN IN PROGRESS..."):
            try:
                reader = PdfReader(uploaded_pdf)
                text = ""
                for i in range(min(len(reader.pages), 15)):
                    text += reader.pages[i].extract_text().lower()
                
                agg_keywords = ['exponential', 'aggressive', 'unmatched', 'market-leading', 'extraordinary', 'vast']
                con_keywords = ['contingent', 'cautious', 'prudent', 'risk', 'uncertainty', 'mitigate', 'provisions']
                
                agg_count = sum(len(re.findall(rf'\b{word}\b', text)) for word in agg_keywords)
                con_count = sum(len(re.findall(rf'\b{word}\b', text)) for word in con_keywords)
                
                detected_tone = "Aggressive" if agg_count > con_count + 5 else ("Conservative" if con_count > agg_count + 5 else "Balanced")
                detected_aud = "Emphasis of Matter" if "emphasis of matter" in text else "Clean"
                if "qualified opinion" in text: detected_aud = "Qualified"
                
                st.session_state["qualitative_results"] = {"tone": detected_tone, "auditor": detected_aud, "disclosure": "Standard"}
                st.rerun()
            except Exception as e: st.error(f"READ ERROR: {e}")

with method_tabs[2]:
    mgt_comm = st.text_area("MANAGEMENT DISCUSSION (MD&A) SUMMARY")
    aud_comm = st.text_area("AUDITOR REMARKS / KEY AUDIT MATTERS")
    if st.button("💾 SAVE SUMMARIES", use_container_width=True):
        derived_aud = "Qualified" if "qualified" in aud_comm.lower() else ("Emphasis of Matter" if "emphasis" in aud_comm.lower() else "Clean")
        st.session_state["qualitative_results"] = {"tone": "Balanced", "auditor": derived_aud, "disclosure": "Standard"}
        st.rerun()

# --------------------------------------------------
# 7. VERDICT ENGINE & DISPLAY
# --------------------------------------------------
financial_results = compute_all_metrics(st.session_state["financial_data"])
qual = st.session_state["qualitative_results"]

fin_flags = sum([1 for k, v in financial_results.items() if k in ['beneish_mscore', 'altman_z', 'sloan_accrual', 'leverage_index'] and (
    (k == 'beneish_mscore' and v > -1.78) or (k == 'altman_z' and v < 2) or (k == 'sloan_accrual' and abs(v) > 0.1) or (k == 'leverage_index' and v > 1.2)
)])

qual_flags = (3 if qual["auditor"] == "Qualified" else (2 if qual["auditor"] == "Emphasis of Matter" else 0)) + (1 if qual["tone"] == "Aggressive" else 0) + (1 if qual["disclosure"] == "Weak" else 0)
total_score = fin_flags + qual_flags

if qual["auditor"] == "Qualified": verdict = "HIGH RISK"
elif fin_flags == 0 and qual_flags < 2: verdict = "SAFE"
elif total_score <= 3: verdict = "CAUTION"
else: verdict = "HIGH RISK"

colors = {"SAFE": "#00ff00", "CAUTION": "#ffb900", "HIGH RISK": "#ff3b30"}

st.markdown(f"""
    <div style="background:#000; padding:45px; border-radius:4px; border:1px solid #333; text-align:center; color:#fff; border-top: 5px solid {colors[verdict]};">
        <h1 style="color:{colors[verdict]}; margin:0; font-size:52px; letter-spacing:2px;">{verdict}</h1>
        <hr style="border-color:#333; margin:25px 0;">
        <div style="display:flex; justify-content: space-around; font-size:16px; color:#ffb900;">
            <div>QUANTITATIVE FLAGS: <b>{fin_flags}</b></div>
            <div>QUALITATIVE FLAGS: <b>{qual_flags}</b></div>
            <div>AGGREGATE SCORE: <b>{total_score}</b></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 8. RECOMMENDATIONS
# --------------------------------------------------
st.markdown('<div class="sub-title">📌 ANALYST STRATEGY & RECOMMENDATIONS</div>', unsafe_allow_html=True)
rec1, rec2 = st.columns(2)

with rec1:
    st.markdown("### 🔍 RISK DRIVER BREAKDOWN")
    if fin_flags > 0: st.error(f"FINANCIAL FORENSICS: {fin_flags} RED FLAGS IDENTIFIED.")
    else: st.success("FINANCIAL FORENSICS: NO RED FLAGS DETECTED.")
    if qual["auditor"] != "Clean": st.warning(f"AUDIT INTEGRITY: {qual['auditor']} OPINION ISSUED.")

with rec2:
    st.markdown(f"### 🎯 STRATEGIC ACTION PLAN")
    if verdict == "SAFE":
        st.markdown(f'<div class="recommendation-card"><b>PROCEED:</b> MAINTAIN LONG POSITION; MONITOR QUARTERLY TRENDS.</div>', unsafe_allow_html=True)
    elif verdict == "CAUTION":
        st.markdown(f'<div class="recommendation-card"><b>VERIFY:</b> CONDUCT DEEP-DIVE ON AUDITOR NOTES; STRESS-TEST CASH FLOWS.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="recommendation-card"><b>AVOID:</b> MATERIAL GOVERNANCE RISKS DETECTED. POTENTIAL MANIPULATION.</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption(f"Forensic Risk Terminal | {entity} | Created by Pratyush Kumar")