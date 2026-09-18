
import streamlit as st
import sys
import os
import base64
sys.path.append(".")

from tools.mf_api import search_schemes, get_scheme_details
from agent_graph import analyze_portfolio

st.set_page_config(page_title="FinEdge AI - MF Doctor", page_icon="🤖", layout="wide")

# Load background image from file if exists, else fallback to gradient
def get_bg_b64():
    for path in ["building_bg.jpg", "building_bg_compressed.jpg", "assets/building_bg.jpg", "giant-building-with-sun.jpg"]:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

bg_b64 = get_bg_b64()

if bg_b64:
    bg_css = f'background-image: linear-gradient(rgba(10,25,60,0.85), rgba(10,25,60,0.92)), url("data:image/jpeg;base64,{bg_b64}");'
else:
    bg_css = 'background: linear-gradient(135deg, #0A1931 0%, #1E3A8A 50%, #3B82F6 100%);'

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
[data-testid="stAppViewContainer"] {{
    {bg_css}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{ background: transparent; }}
.main-header {{
    background: linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(235,245,255,0.95) 100%);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 28px 35px;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}}
.company-badge {{
    background: linear-gradient(135deg, #0A1931 0%, #185ADB 100%);
    color: white;
    padding: 6px 18px;
    border-radius: 30px;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 12px;
}}
.main-title {{
    font-family: 'Inter', sans-serif;
    font-size: 34px;
    font-weight: 800;
    background: linear-gradient(135deg, #0A1931 0%, #185ADB 50%, #00C6FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}}
.subtitle {{ color: #4A6FA5; font-size: 13px; font-weight: 600; }}
.glass-card {{
    background: rgba(255, 255, 255, 0.97);
    backdrop-filter: blur(16px);
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    border: 1px solid rgba(255,255,255,0.5);
}}
.stButton > button {{
    background: linear-gradient(135deg, #0A1931 0%, #185ADB 100%);
    color: white;
    border-radius: 12px;
    padding: 12px 28px;
    font-weight: 700;
    font-size: 16px;
    border: none;
    box-shadow: 0 8px 20px rgba(24,90,219,0.4);
    width: 100%;
}}
.metric-card {{
    background: rgba(255,255,255,0.95);
    border-radius: 14px;
    padding: 16px;
    border-left: 4px solid #185ADB;
    margin-bottom: 10px;
}}
[data-testid="stSidebar"] {{ background: rgba(255,255,255,0.97); }}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 6])
with col1:
    st.markdown("<div style='font-size:85px; text-align:center; background:white; border-radius:20px; padding:10px; box-shadow:0 10px 30px rgba(0,0,0,0.2);'>🤖</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; margin-top:8px;'><span style='background:#185ADB; color:white; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:700;'>AI AGENT LIVE</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="main-header">
        <div class="company-badge">◆ FINEDGE CAPITAL • EST. 2012 • SEBI REGISTERED AMC PARTNER</div>
        <div class="main-title">FinEdge AI - MF Portfolio Doctor Agent</div>
        <div class="subtitle">Agentic RAG • Live NAV via AMFI • SEBI Compliance Guardrails • Powered by GPT-4o | Mumbai BKC</div>
        <div style="margin-top:12px; display:flex; gap:15px; font-size:12px; color:#6B8CAE;">
            <span>🏢 Corporate Park, BKC</span><span>•</span><span>📊 AUM ₹2,450 Cr+</span><span>•</span><span>🤖 AI-First WealthTech</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📋 Enter Your Mutual Fund Portfolio", unsafe_allow_html=True)
    st.caption("FinEdge AI will analyze overlap, risk, sector & SEBI compliance")
    funds = st.text_area("", "Parag Parikh Flexi Cap, Quant Small Cap, Nippon Growth Fund, HDFC Mid Cap Opportunities", height=115, label_visibility="collapsed")
    c1, c2, c3 = st.columns([2,2,1])
    with c1:
        st.caption("💡 Try: SBI Bluechip, Axis Long Term, Mirae Asset Large Cap")
    with c3:
        analyze_btn = st.button("🚀 Diagnose Portfolio", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not funds.strip():
            st.warning("Please enter fund")
        else:
            st.markdown('<div class="glass-card" style="margin-top:25px;">', unsafe_allow_html=True)
            with st.spinner("🤖 FinEdge AI fetching live NAVs..."):
                st.markdown("### 🔍 Live AMFI Verification")
                cols = st.columns(3)
                for i, fund in enumerate(funds.split(",")[:3]):
                    fund = fund.strip()
                    if fund:
                        with cols[i % 3]:
                            st.markdown(f'<div class="metric-card"><b>🔎 {fund[:28]}</b>', unsafe_allow_html=True)
                            results = search_schemes(fund)
                            if results:
                                st.success(f"✓ Code: {results[0]['schemeCode']}")
                                details = get_scheme_details(results[0]['schemeCode'])
                                if details:
                                    meta = details.get("meta", {})
                                    st.caption(f"{meta.get('fund_house','')} | {meta.get('scheme_category','')}")
                            st.markdown('</div>', unsafe_allow_html=True)
                st.divider()
                st.markdown("### 🧠 FinEdge AI Diagnosis")
                try:
                    diagnosis = analyze_portfolio(funds)
                    st.markdown(diagnosis)
                    st.balloons()
                except Exception as e:
                    st.error("Set OPENAI_API_KEY in Secrets")
                    st.code(str(e))
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:40px; padding:22px; background:rgba(255,255,255,0.90); border-radius:14px;">
    <div style="font-weight:800; color:#0A1931;">FINEDGE CAPITAL • AI Wealth Intelligence Platform</div>
    <div style="color:#4A6FA5; font-size:12px; margin-top:6px;">BKC, Mumbai | SEBI: INA000012345 | AUM ₹2,450 Cr+ | Live: mfapi.in | Built by prashantjt77</div>
</div>
""", unsafe_allow_html=True)
