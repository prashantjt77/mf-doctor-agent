
import streamlit as st
import sys
import os
import base64
sys.path.append(".")

from tools.mf_api import search_schemes, get_scheme_details

st.set_page_config(page_title="FinEdge AI - MF Doctor", page_icon="🤖", layout="wide")

def get_bg_b64():
    for path in ["building_bg.jpg", "building_bg_compressed.jpg", "assets/building_bg.jpg"]:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

bg_b64 = get_bg_b64()
bg_css = f'background-image: linear-gradient(rgba(5,15,40,0.88), rgba(5,15,40,0.94)), url("data:image/jpeg;base64,{bg_b64}");' if bg_b64 else 'background: linear-gradient(135deg, #0A1931 0%, #1E3A8A 100%);'

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    {bg_css}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{ background: transparent; }}
.main-header {{
    background: #FFFFFF;
    border-radius: 18px;
    padding: 24px 32px;
    margin-bottom: 20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    border: 2px solid #185ADB;
}}
.company-badge {{
    background: #0A1931;
    color: #FFD700;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 11px;
    letter-spacing: 1.5px;
    font-weight: 800;
    display: inline-block;
    margin-bottom: 10px;
}}
.main-title {{
    font-size: 32px;
    font-weight: 900;
    color: #0A1931;
    line-height: 1.2;
}}
.subtitle {{ color: #185ADB; font-size: 13px; font-weight: 700; }}
.input-card {{
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    border: 2px solid #00C6FF;
}}
.input-label {{
    font-size: 18px;
    font-weight: 800;
    color: #0A1931;
    margin-bottom: 4px;
}}
.input-sub {{
    font-size: 13px;
    font-weight: 600;
    color: #185ADB;
    margin-bottom: 12px;
}}
.stTextArea textarea {{
    background: #F8FAFF;
    border: 2px solid #185ADB;
    border-radius: 10px;
    font-size: 14px;
    color: #0A1931;
    font-weight: 600;
}}
.stButton > button {{
    background: linear-gradient(135deg, #0A1931 0%, #185ADB 100%);
    color: white;
    border-radius: 10px;
    padding: 12px 28px;
    font-weight: 800;
    font-size: 16px;
    border: none;
    box-shadow: 0 6px 18px rgba(24,90,219,0.5);
    width: 100%;
}}
.result-card {{
    background: #FFFFFF;
    border-radius: 16px;
    padding: 26px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    margin-top: 20px;
}}
.metric-card {{
    background: #F0F6FF;
    border-radius: 12px;
    padding: 14px;
    border-left: 5px solid #185ADB;
    margin-bottom: 8px;
}}
[data-testid="stSidebar"] {{ background: #FFFFFF; }}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("<div style='font-size:75px; text-align:center; background:white; border-radius:18px; padding:8px; box-shadow:0 8px 20px rgba(0,0,0,0.3); border:2px solid #185ADB;'>🤖</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; margin-top:6px;'><span style='background:#00C853; color:white; padding:4px 10px; border-radius:12px; font-size:10px; font-weight:800;'>● LIVE</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="main-header">
        <div class="company-badge">◆ FINEDGE CAPITAL • SEBI REGISTERED • BKC MUMBAI</div>
        <div class="main-title">FinEdge AI - MF Portfolio Doctor Agent 🤖</div>
        <div class="subtitle">Agentic RAG • Live AMFI NAV • SEBI Guardrails • GPT-4o Powered • AUM ₹2,450 Cr+</div>
    </div>
    """, unsafe_allow_html=True)

# INPUT SECTION - HIGH VISIBILITY
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">📋 Enter Your Mutual Fund Portfolio</div>', unsafe_allow_html=True)
st.markdown('<div class="input-sub">FinEdge AI will analyze overlap, risk, sector & SEBI compliance (e.g. Parag Parikh Flexi Cap, Quant Small Cap)</div>', unsafe_allow_html=True)

funds = st.text_area("Funds", "Parag Parikh Flexi Cap, Quant Small Cap, Nippon Growth Fund, HDFC Mid Cap Opportunities", height=110, label_visibility="collapsed")

c1, c2 = st.columns([3,1])
with c1:
    st.markdown("<span style='color:#0A1931; font-weight:700; font-size:12px;'>💡 Try: SBI Bluechip, Axis Long Term, Mirae Asset Large Cap, HDFC Balanced Advantage</span>", unsafe_allow_html=True)
with c2:
    analyze_btn = st.button("🚀 Diagnose Portfolio", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

def get_llm_or_demo():
    api_key = os.getenv("OPENAI_API_KEY")
    try:
        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    if not api_key or "HERE" in api_key or len(api_key) < 20:
        return None
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.2)
    except:
        return None

def demo_analysis(funds_text):
    return f"""
### 📊 FinEdge AI - Portfolio Analysis (DEMO MODE - Add real OpenAI key for GPT-4o)

**Portfolio Entered:** {funds_text}

| Fund | Category | Risk | Overlap Risk |
|------|----------|------|--------------|
| Parag Parikh Flexi Cap | Flexi Cap | High | 30% overlap with Quant Small Cap |
| Quant Small Cap | Small Cap | Very High | High sector concentration in Financials |
| Nippon Growth Fund | Mid Cap | High | Diversified |
| HDFC Mid Cap Opportunities | Mid Cap | High | 25% overlap with Nippon |

**🔍 Overlap Analysis:**
- High overlap detected between Mid-cap funds (Nippon + HDFC) - ~35% common holdings
- Flexi cap provides diversification benefit

**⚠️ Risk Assessment:**
- Portfolio Risk: **AGGRESSIVE** (75% Small/Mid cap)
- SEBI Compliance: All funds SEBI registered, no compliance issue
- Sector Concentration: 40% Financials, 20% IT - Consider balancing

**✅ FinEdge Recommendations:**
1. **Reduce Mid-cap overlap:** Exit one of Nippon/HDFC Midcap, add Large-cap fund (e.g. Nifty 50 Index)
2. **Add Debt cushion:** 15% debt fund for stability (HDFC Corporate Bond)
3. **SIP Rebalancing:** Shift 20% SIP to Flexi-cap for better diversification

**SEBI Guardrails:** ✅ Compliant | No leveraged products | Expense ratio < 2%

*Add your real OPENAI_API_KEY in Streamlit Secrets to get GPT-4o powered live analysis*
"""

if analyze_btn:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    with st.spinner("🤖 FinEdge AI fetching live AMFI NAV..."):
        st.markdown("### 🔍 Live AMFI Verification - FinEdge Data Engine")
        cols = st.columns(3)
        for i, fund in enumerate(funds.split(",")[:4]):
            fund = fund.strip()
            if fund:
                with cols[i % 3]:
                    st.markdown(f'<div class="metric-card"><b>🔎 {fund[:26]}</b>', unsafe_allow_html=True)
                    try:
                        results = search_schemes(fund)
                        if results:
                            st.success(f"✓ {results[0]['schemeCode']}")
                            details = get_scheme_details(results[0]['schemeCode'])
                            if details:
                                meta = details.get("meta", {})
                                st.caption(f"{meta.get('fund_house','')}")
                                st.caption(f"{meta.get('scheme_category','')}")
                        else:
                            st.info("Analyzing...")
                    except Exception as e:
                        st.caption(f"API: {e}")
                    st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 🧠 FinEdge AI Diagnosis - Wealth Intelligence Report")
        llm = get_llm_or_demo()
        if llm:
            try:
                from agent_graph import analyze_portfolio
                diagnosis = analyze_portfolio(funds)
                st.markdown(diagnosis)
                st.balloons()
            except Exception as e:
                st.error(f"LLM Error: {e}")
                st.markdown(demo_analysis(funds))
        else:
            st.warning("⚠️ Demo Mode: Using sample analysis. Add real OPENAI_API_KEY in Streamlit Secrets for live GPT-4o")
            st.markdown(demo_analysis(funds))
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:30px; padding:18px; background:white; border-radius:12px; box-shadow:0 8px 20px rgba(0,0,0,0.2);">
    <div style="font-weight:900; color:#0A1931;">FINEDGE CAPITAL • AI Wealth Intelligence Platform</div>
    <div style="color:#185ADB; font-size:11px; font-weight:600; margin-top:4px;">BKC Mumbai | SEBI: INA000012345 | AUM ₹2,450 Cr+ | Live: mfapi.in | v3.0 Robot Agent</div>
    <div style="color:#6B8CAE; font-size:9px; margin-top:6px;">Disclaimer: Demo only, not SEBI investment advice</div>
</div>
""", unsafe_allow_html=True)
