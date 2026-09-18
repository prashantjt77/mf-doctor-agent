import streamlit as st
from agent_graph import get_agent
from datetime import datetime

st.set_page_config(page_title="MF Portfolio Doctor", page_icon="📈", layout="wide")

st.title("📈 MF Portfolio Doctor Agent")
st.caption("BFSI Use Case | Agentic RAG + AMFI Data | Educational Analysis Only")
st.warning("⚠️ Disclaimer: This tool is for educational purposes only. It is NOT SEBI-registered investment advice. Data sourced from AMFI via mfapi.in. Please consult a SEBI Registered Investment Advisor.")

with st.sidebar:
    st.header("How to use")
    st.markdown("""
    1. Enter 2-4 fund names
    2. Select Goal & Risk
    3. Click Diagnose
    """)
    st.divider()
    st.markdown("**Data Source:** `mfapi.in` (AMFI)")
    st.markdown("**Stack:** LangGraph + Tavily + Streamlit")
    st.markdown("**Built for:** Portfolio Review")
    st.divider()
    st.info("Tip: Use full fund names like 'Parag Parikh Flexi Cap Fund' for best results.")

funds_input = st.text_area(
    "Enter your Mutual Funds (comma separated)", 
    "Parag Parikh Flexi Cap Fund, Quant Small Cap Fund, HDFC Mid Cap Fund", 
    height=100
)

col1, col2 = st.columns(2)
with col1:
    goal = st.selectbox("Goal", ["Retirement (15Y+)", "Wealth Creation (5-10Y)", "Child Education (10Y+)", "Short Term (<3Y)"])
with col2:
    risk_profile = st.selectbox("Your Risk Profile", ["Moderate", "Aggressive", "Conservative"])

if st.button("🩺 Diagnose My Portfolio", type="primary", use_container_width=True):
    if not funds_input.strip():
        st.error("Please enter at least one fund")
    else:
        with st.spinner("🤖 Agent fetching live AMFI NAVs, checking category, overlap & goal alignment..."):
            try:
                agent = get_agent()
                query = f"Analyze portfolio: {funds_input}. Goal: {goal}, Risk Profile: {risk_profile}. Give detailed health report with citations."
                result = agent.invoke({"messages": [("human", query)]})
                final_answer = result['messages'][-1].content

                st.success(f"Report Generated | {datetime.now().strftime('%d %b %Y, %I:%M %p IST')}")
                st.markdown(final_answer)
                
                st.divider()
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button("📥 Download Report", final_answer, file_name=f"MF_Health_Report_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)
                with col_b:
                    st.caption(f"Sources: AMFI NAV via mfapi.in | Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M IST')} | Not financial advice.")

            except Exception as e:
                st.error(f"Agent error: {e}")
                st.info("Check: 1. OPENAI_API_KEY is set in Streamlit Secrets 2. You have billing enabled on OpenAI")

st.divider()
st.caption("Built by Prashant Tripathi | BFSI AI Prototype | For Educational Demo")
