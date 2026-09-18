import streamlit as st
import sys
sys.path.append(".")

from tools.mf_api import search_schemes, get_scheme_details
from agent_graph import analyze_portfolio

st.set_page_config(page_title="MF Doctor Agent", page_icon="💊", layout="wide")

st.title("💊 MF Portfolio Doctor Agent - BFSI")
st.caption("Agentic RAG | Live NAV via mfapi.in | SEBI Guardrails")

with st.sidebar:
    st.header("Settings")
    st.success("✅ Live")
    if st.button("Clear"):
        st.session_state.clear()

funds = st.text_area("Enter your Mutual Funds (comma separated)", 
                      "Parag Parikh Flexi Cap, Quant Small Cap, Nippon Growth Fund",
                      height=100)

if st.button("🔍 Diagnose Portfolio", type="primary"):
    if not funds.strip():
        st.warning("Please enter fund names")
    else:
        with st.spinner("Fetching live NAV and analyzing..."):
            st.subheader("Live Scheme Search")
            for fund in funds.split(",")[:3]:
                fund = fund.strip()
                if fund:
                    results = search_schemes(fund)
                    if results:
                        st.write(f"**{fund}** -> {results[0]['schemeName']} (Code: {results[0]['schemeCode']})")
                        details = get_scheme_details(results[0]['schemeCode'])
                        if details:
                            meta = details.get("meta", {})
                            st.json({"fund_house": meta.get("fund_house"), "category": meta.get("scheme_category")})
            
            st.divider()
            st.subheader("AI Diagnosis")
            try:
                diagnosis = analyze_portfolio(funds)
                st.markdown(diagnosis)
            except Exception as e:
                st.error(f"Set OPENAI_API_KEY in Streamlit Secrets. Error: {e}")
                st.info("Go to Streamlit Dashboard > Settings > Secrets")

st.markdown("---")
st.caption("Built by prashantjt77 | Live Data: mfapi.in | For BFSI Demo")
