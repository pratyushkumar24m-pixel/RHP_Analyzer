import streamlit as st
import pandas as pd
import os
import yfinance as yf
from financial_core import compute_all_metrics

# --------------------------------------------------
# 1. GLOBAL STATE & SYNC
# --------------------------------------------------
if "entity_name" not in st.session_state:
    st.session_state["entity_name"] = "Reliance Industries"

def update_entity():
    st.session_state["entity_name"] = st.session_state["entity_temp"]

# --------------------------------------------------
# 2. CLEAR DATA FUNCTION
# --------------------------------------------------
def clear_financial_data():
    if "financial_data" in st.session_state:
        del st.session_state["financial_data"]
    if "results" in st.session_state:
        del st.session_state["results"]
    st.toast("DATA CLEARED. TERMINAL RESET.")

# --------------------------------------------------
# 3. INSTITUTIONAL UI/UX (FULL DARK MODE)
# --------------------------------------------------
st.set_page_config(page_title="FINANCIAL ANALYSIS | TERMINAL", page_icon="📊", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&display=swap');
    
    /* 1. Global Background Reset (Removes all white areas) */
    .stApp, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: #0c0c0c !important;
    }

    /* 2. Global Typography - Terminal Amber & Monospace */
    html, body, [class*="css"], .stMarkdown, p, span, div, label, li {
        font-family: 'Roboto Mono', monospace !important;
        color: #ffb900 !important; /* Classic Amber */
    }

    h1, h2, h3, h4 { color: #ffffff !important; text-transform: uppercase; letter-spacing: 1px; }

    /* 3. Sidebar Specific Fix (Force Dark) */
    [data-testid="stSidebar"] section {
        background-color: #0c0c0c !important;
    }
    
    /* 4. Containers */
    .hero-container {
        background: #000000; padding: 2rem; border-radius: 4px; border: 1px solid #333333;
        border-top: 4px solid #0056b3; margin-bottom: 2rem;
    }
    
    .sub-title {
        color: #00bcff !important; font-weight: 700; border-bottom: 1px solid #222222;
        padding-bottom: 8px; margin-top: 30px; margin-bottom: 20px; text-transform: uppercase;
    }
    
    /* 5. Threshold and Download Boxes */
    .threshold-box, .download-box {
        background: #111111 !important; padding: 15px; border-radius: 4px; border: 1px solid #333333 !important;
        color: #ffb900 !important;
    }
    .download-box { border-style: dashed !important; text-align: center; }
    .download-box:hover { border-color: #00bcff !important; background: #1a1a1a !important; }

    /* 6. Form and Widget Dark Mode Fixes */
    [data-testid="stForm"], [data-testid="stFileUploader"] {
        border: 1px solid #333333 !important;
        background-color: #000000 !important;
    }

    /* Radio Button Fix */
    div[data-testid="stRadio"] label {
        color: #ffffff !important;
    }

    /* 7. Market Ticker */
    .ticker-wrap {
        width: 100%; background-color: #000000; overflow: hidden;
        white-space: nowrap; padding: 8px 0; border-top: 1px solid #444;
        border-bottom: 1px solid #444; margin-bottom: 20px;
    }
    .ticker-content {
        display: inline-block; animation: ticker-move 60s linear infinite;
        font-size: 14px; color: #ffffff !important;
    }
    @keyframes ticker-move { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    .up { color: #00ff00 !important; font-weight: bold; }
    .down { color: #ff3b30 !important; font-weight: bold; }

    /* 8. Input Styling Overrides */
    .stTextInput input, .stNumberInput input {
        background-color: #000000 !important;
        color: #ffb900 !important;
        border: 1px solid #444 !important;
    }
    
    /* Sidebar Input Text Color */
    section[data-testid="stSidebar"] .stTextInput input {
        background-color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 4. MARKET DATA (TICKER)
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
            items.append(f'<span class="ticker-item" style="margin-right:60px; display:inline-block;">{name} <span class="{color}">{info["last_price"]:,.2f} {"▲" if pct_change >= 0 else "▼"} {abs(pct_change):.2f}%</span></span>')
        strip = " ".join(items)
        return strip + " &nbsp;&nbsp;&nbsp;&nbsp; " + strip
    except:
        return "MARKET DATA OFFLINE"

# --------------------------------------------------
# 5. SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("### <GO> SCREENING")
    st.text_input("ENTITY NAME", value=st.session_state["entity_name"], key="entity_temp", on_change=update_entity)
    st.markdown("---")
    if "financial_data" in st.session_state:
        st.button("🗑️ RESET FINANCIALS", on_click=clear_financial_data, use_container_width=True)
    entity = st.session_state["entity_name"]

# --------------------------------------------------
# 6. HEADER & TICKER
# --------------------------------------------------
st.markdown(f'<div class="ticker-wrap"><div class="ticker-content">{get_live_market_data()}</div></div>', unsafe_allow_html=True)

st.markdown(f"""<div class="hero-container">
    <div style="color: #00bcff; font-weight: 700; font-size: 11px; text-transform: uppercase; margin-bottom: 8px;">QUANTITATIVE ENGINE</div>
    <h1>📊 FINANCIAL ANALYSIS: {entity}</h1>
    <p style="font-size: 14px;">Upload or enter data to calculate forensic scores and solvency indicators.</p>
</div>""", unsafe_allow_html=True)

# --------------------------------------------------
# 7. EXCEL TEMPLATE DOWNLOADS
# --------------------------------------------------
st.markdown('<div class="sub-title">📥 PREPARATION TEMPLATES</div>', unsafe_allow_html=True)

col_dl1, col_dl2 = st.columns(2)
TEMPLATE_PATH = "assets/financial_template.xlsx"
SAMPLE_PATH = "assets/financial_sample_filled.xlsx"

with col_dl1:
    st.markdown('<div class="download-box">', unsafe_allow_html=True)
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "rb") as f:
            st.download_button("⬇️ BLANK TEMPLATE", f, file_name="financial_template.xlsx", use_container_width=True)
    else:
        st.error("TEMPLATE MISSING")
    st.markdown('</div>', unsafe_allow_html=True)

with col_dl2:
    st.markdown('<div class="download-box">', unsafe_allow_html=True)
    if os.path.exists(SAMPLE_PATH):
        with open(SAMPLE_PATH, "rb") as f:
            st.download_button("⬇️ SAMPLE (FILED)", f, file_name="financial_sample_filled.xlsx", use_container_width=True)
    else:
        st.error("SAMPLE MISSING")
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# 8. DATA INPUT LOGIC
# --------------------------------------------------
if "financial_data" not in st.session_state:
    st.markdown('<div class="sub-title">🧾 FINANCIAL DATA INPUT</div>', unsafe_allow_html=True)
    input_method = st.radio("CHOOSE INPUT METHOD", ["Upload Excel", "Manual Entry"], horizontal=True)

    if input_method == "Upload Excel":
        uploaded_file = st.file_uploader("UPLOAD STANDARDIZED EXCEL FILE", type=["xlsx"])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file).set_index("Year")
                new_data = {year: df.loc[year].to_dict() for year in df.index}
                st.session_state["financial_data"] = new_data
                st.session_state["results"] = compute_all_metrics(new_data)
                st.rerun()
            except Exception as e:
                st.error(f"ERROR READING FILE: {e}")
    else:
        with st.form("manual_entry_form"):
            st.markdown("### 📗 MANUAL FINANCIAL INPUT")
            def input_row(label):
                c = st.columns(4)
                return {
                    "Revenue": c[0].number_input(f"REVENUE ({label})", min_value=0.0),
                    "COGS": c[1].number_input(f"COGS ({label})", min_value=0.0),
                    "Net Profit": c[2].number_input(f"NET PROFIT ({label})"),
                    "Total Assets": c[3].number_input(f"TOTAL ASSETS ({label})"),
                    "CFO": c[0].number_input(f"CFO ({label})"),
                    "Current Assets": c[1].number_input(f"CURR. ASSETS ({label})"),
                    "Current Liabilities": c[2].number_input(f"CURR. LIAB ({label})"),
                    "Receivables": c[3].number_input(f"RECEIVABLES ({label})")
                }
            cy = input_row("CY")
            py = input_row("PY")
            if st.form_submit_button("SUBMIT DATA"):
                manual_data = {"CY": cy, "PY": py}
                st.session_state["financial_data"] = manual_data
                st.session_state["results"] = compute_all_metrics(manual_data)
                st.rerun()

# --------------------------------------------------
# 9. ENHANCED METRICS DISPLAY
# --------------------------------------------------
else:
    res = st.session_state["results"]
    st.markdown('<div class="sub-title">📌 FORENSIC RATIOS & RISK MARKERS</div>', unsafe_allow_html=True)

    CYAN, GREEN, ORANGE, RED = "#00bcff", "#00ff00", "#ffb900", "#ff3b30"

    def get_color(val, safe_thresh, risk_thresh, higher_is_better=False):
        if higher_is_better:
            if val >= safe_thresh: return GREEN
            if val >= risk_thresh: return ORANGE
            return RED
        return GREEN if val <= safe_thresh else (ORANGE if val <= risk_thresh else RED)

    def metric_tile(label, val, color):
        st.markdown(f"""
            <div style="background:#000; padding:22px; border-radius:4px; border-left: 5px solid {color}; text-align:left; color:#fff; margin-bottom:15px; border-top: 1px solid #333; border-right: 1px solid #333; border-bottom: 1px solid #333;">
                <div style="font-size:11px; color:#aaa; text-transform:uppercase; letter-spacing:1px;">{label}</div>
                <div style="font-size:32px; font-weight:700; color:{color}; margin: 5px 0;">{val:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    with c1: metric_tile("BENEISH M-SCORE", res['beneish_mscore'], get_color(res['beneish_mscore'], -2.22, -1.78))
    with c2: metric_tile("ALTMAN Z-SCORE", res['altman_z'], GREEN if res['altman_z'] > 2.99 else (ORANGE if res['altman_z'] > 1.81 else RED))
    with c3: metric_tile("SLOAN RATIO", res['sloan_accrual'], get_color(abs(res['sloan_accrual']), 0.10, 0.20))
    with c4: metric_tile("LEVERAGE INDEX", res.get('leverage_index', 0), get_color(res.get('leverage_index', 1), 1.0, 1.2))
    with c5: metric_tile("DSO CHANGE (DAYS)", res.get('dso_change', 0), get_color(res.get('dso_change', 0), 5.0, 15.0))
    with c6: metric_tile("EARNINGS QUALITY", res.get('quality_of_earnings', 0), get_color(res.get('quality_of_earnings', 1), 1.0, 0.7, higher_is_better=True))

    st.markdown("""
        <div class="threshold-box">
            <b>💡 INTERPRETATION GUIDE:</b><br>
            • <b>BENEISH M-SCORE:</b> Values above -1.78 suggest potential manipulation.<br>
            • <b>ALTMAN Z-SCORE:</b> Values below 1.8 indicate bankruptcy risk.<br>
            • <b>SLOAN RATIO:</b> Accruals > 10% signal poor earnings quality.
        </div>
    """, unsafe_allow_html=True)
    
    st.success(f"TERMINAL DATA LOCKED FOR {st.session_state['entity_name']}. PROCEED TO QUALITATIVE LAB.")

st.markdown("---")
st.caption(f"Forensic Risk Terminal | Data Engine v2.4 | Created by Pratyush Kumar")