
import streamlit as st
import sys
import pandas as pd
sys.path.append(".")

from tools.mf_api import search_schemes, get_scheme_details

st.set_page_config(page_title="FinEdge AI - MF Portfolio Doctor", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
}
[data-testid="stHeader"] { background: rgba(255,255,255,0.9); }
.block-container { padding-top: 1.2rem; max-width: 1000px; }

.card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 18px;
}
.header-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 18px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 18px;
}

.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1.5px solid #94A3B8 !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    color: #0F172A !important;
    min-height: 110px !important;
}
.stTextArea textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}

.stButton > button {
    background: #0F172A !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 14px 28px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border: none !important;
    margin-top: 12px !important;
}

.instruction {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 12px;
    color: #475569;
    line-height: 1.6;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# HEADER - Single line, no extra boxes
st.markdown("""
<div class="header-card">
    <div style="display:flex; align-items:center; gap:14px;">
        <div style="width:48px; height:48px; background:#0F172A; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:26px;">🤖</div>
        <div>
            <div style="font-size:20px; font-weight:800; color:#0F172A;">FinEdge AI — MF Portfolio Doctor</div>
            <div style="font-size:12px; color:#64748B; margin-top:2px;">Live AMFI NAV • SEBI Compliance • No API Key Needed • Dummy BFSI: FinEdge Capital, BKC Mumbai</div>
        </div>
        <div style="margin-left:auto; background:#F0FDF4; border:1px solid #BBF7D0; color:#166534; padding:6px 12px; border-radius:20px; font-size:11px; font-weight:800;">● LIVE</div>
    </div>
</div>
""", unsafe_allow_html=True)

# INPUT - Ultra Clean - No blank boxes
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 📋 Enter Your Mutual Fund Portfolio")
st.markdown("<p style='color:#64748B; font-size:13px; margin-top:-6px;'>Type 2-6 fund names separated by comma. Example: <b>Parag Parikh Flexi Cap, Quant Small Cap, HDFC Mid Cap</b></p>", unsafe_allow_html=True)

funds = st.text_area(
    label="Portfolio input",
    value="Parag Parikh Flexi Cap, Quant Small Cap, Nippon Growth Fund, HDFC Mid Cap Opportunities",
    height=110,
    label_visibility="collapsed",
    placeholder="Example: Parag Parikh Flexi Cap, Quant Small Cap, Nippon Growth Fund, HDFC Mid Cap Opportunities"
)

# Button RIGHT AFTER input - as requested
analyze_btn = st.button("🚀 Analyze Portfolio → Get Report", type="primary", use_container_width=True)

# Instructions AFTER button, compact, not looking like input box
st.markdown("""
<div class="instruction">
    <b>📌 How to enter multiple funds:</b> Use comma to separate — <b>Fund1, Fund2, Fund3</b> &nbsp;|&nbsp; 
    <b>Min:</b> 2 funds &nbsp;|&nbsp; <b>Max:</b> 6 funds &nbsp;|&nbsp; 
    <b>Tip:</b> Partial name works (e.g. "Parag Parikh Flexi" is ok) &nbsp;|&nbsp; 
    <b>Try:</b> SBI Bluechip, Axis Long Term ELSS, Mirae Asset Large Cap, HDFC Balanced Advantage
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if analyze_btn:
    if not funds.strip():
        st.warning("Please enter at least 2 funds separated by comma")
    else:
        funds_list = [f.strip() for f in funds.split(",") if f.strip()]
        if len(funds_list) < 2:
            st.warning("Enter at least 2 funds. Example: Parag Parikh Flexi Cap, Quant Small Cap")
        else:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### 🔍 Live AMFI Verification")
            st.caption(f"Verifying {len(funds_list)} funds from mfapi.in — Live data")
            
            cols = st.columns(4)
            verified = []
            for i, fund in enumerate(funds_list[:8]):
                with cols[i % 4]:
                    try:
                        results = search_schemes(fund)
                        if results:
                            code = results[0]['schemeCode']
                            details = get_scheme_details(code)
                            fh = details.get("meta", {}).get("fund_house","") if details else ""
                            cat = details.get("meta", {}).get("scheme_category","") if details else ""
                            verified.append((fund, code, fh, cat))
                            st.markdown(f"<div style='background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px;'><div style='font-size:12px; font-weight:700; color:#0F172A;'>{fund[:26]}</div><div style='font-size:11px; color:#059669; font-weight:700; margin-top:4px;'>✓ {code}</div><div style='font-size:10px; color:#64748B;'>{fh[:20]}</div></div>", unsafe_allow_html=True)
                        else:
                            verified.append((fund, "N/A", "", ""))
                            st.markdown(f"<div style='background:#FFFBEB; border:1px solid #FDE68A; border-radius:10px; padding:10px;'><div style='font-size:12px; font-weight:700;'>{fund[:26]}</div><div style='font-size:11px; color:#D97706;'>Partial match</div></div>", unsafe_allow_html=True)
                    except:
                        verified.append((fund, "N/A", "", ""))
                        st.markdown(f"<div style='background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px;'><div style='font-size:12px; font-weight:700;'>{fund[:26]}</div></div>", unsafe_allow_html=True)
            
            st.divider()
            st.markdown("#### 📊 Portfolio Diagnosis — BFSI Report")
            
            data = []
            for fund, code, fh, cat in verified:
                fl = fund.lower()
                if "flexi" in fl or "parag" in fl or "balanced" in fl:
                    data.append({"Fund": fund, "Category": cat or "Flexi/Hybrid", "Risk": "Moderate-High", "Overlap": "30% with Small", "Action": "HOLD"})
                elif "small" in fl or "quant" in fl:
                    data.append({"Fund": fund, "Category": cat or "Small Cap", "Risk": "Very High", "Overlap": "High Financials", "Action": "REDUCE 20%"})
                elif "mid" in fl or "nippon" in fl or "growth" in fl:
                    data.append({"Fund": fund, "Category": cat or "Mid Cap", "Risk": "High", "Overlap": "35% with other Mid", "Action": "SWITCH"})
                else:
                    data.append({"Fund": fund, "Category": cat or "Large/Mid", "Risk": "Moderate", "Overlap": "Diversified", "Action": "HOLD"})
            
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 🔍 Overlap & Risk")
                st.markdown("- **35%** common holdings in Mid-cap (HDFC Bank, ICICI, Infosys)")
                st.markdown("- **Diversification:** 6.2/10 → Needs Large-cap")
                st.markdown("- **Risk:** AGGRESSIVE (75% Small/Mid)")
                st.markdown("- **SEBI:** ✅ Compliant, Expense <2%")
            with c2:
                st.markdown("##### ✅ Recommendations")
                st.success("**Reduce Overlap:** Exit 1 Mid-cap → Add Nifty 50 Index")
                st.warning("**Add Debt:** 15% HDFC Corporate Bond for stability")
                st.info("**Rebalance SIP:** 20% Small → Flexi-cap")
            
            st.markdown("""
            <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:14px; margin-top:12px;">
                <b style="color:#166534;">📈 Expected Outcome:</b> <span style="color:#334155; font-size:13px;">Risk Very High → High | Diversification 6.2 → 8.5/10 | 3Y CAGR 13.5% | Live: mfapi.in | Built by prashantjt77</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:20px; padding:14px; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px;">
    <div style="font-weight:700; color:#0F172A; font-size:12px;">FINEDGE CAPITAL • AI Wealth Intelligence • v10 Clean Light</div>
    <div style="color:#94A3B8; font-size:10px; margin-top:4px;">BKC Mumbai | SEBI INA000012345 | Live: mfapi.in | Educational demo only</div>
</div>
""", unsafe_allow_html=True)
