from langchain_openai import ChatOpenAI
import os

def get_llm():
    api_key = os.getenv("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    try:
        import streamlit as st
        if not api_key and "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in env or Streamlit Secrets")
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
    4. SEBI Compliance Issues
    5. 3 Actionable Recommendations
    Be crisp, use tables and bullet points. For BFSI interview demo.
    """
    resp = llm.invoke(prompt)
    return resp.content

# Compatibility for old app.py that imports get_agent
def get_agent():
    return get_llm()

# Also alias
get_agent_old = get_agent
