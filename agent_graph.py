
from langchain_openai import ChatOpenAI
import os

def get_llm():
    api_key = os.getenv("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    # fallback to streamlit secrets
    try:
        import streamlit as st
        if not api_key and "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    return ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.2)

def analyze_portfolio(funds_text):
    llm = get_llm()
    prompt = f"""
    You are MF Portfolio Doctor Agent - BFSI Expert.
    
    User Portfolio: {funds_text}
    
    Analyze and give:
    1. Overlap Analysis
    2. Risk Level
    3. Sector Concentration
    4. SEBI Compliance Issues (if any)
    5. 3 Actionable Recommendations
    
    Be crisp, use tables and bullet points. If fund not found, suggest closest match.
    Keep tone professional for BFSI.
    """
    resp = llm.invoke(prompt)
    return resp.content
