import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.mf_api import get_fund_details, calculate_overlap_note, get_category_average_note

def get_agent():
    """
    Returns LangGraph ReAct Agent with MF tools.
    Uses gpt-4o-mini for cost efficiency.
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0.2
    )
    
    tools = [get_fund_details, calculate_overlap_note, get_category_average_note]
    
    system_prompt = """You are MF Portfolio Doctor Agent for Indian Mutual Funds - an expert BFSI analyst.

    RULES:
    1. You MUST call get_fund_details tool for EVERY fund user mentions. Do not hallucinate NAVs.
    2. Always cite source: AMFI via mfapi.in and mention NAV date.
    3. NEVER give BUY/SELL/HOLD recommendation. Only give EDUCATIONAL analysis.
    4. Structure your answer EXACTLY like this:

    ### 📊 Portfolio Summary
    [List funds with latest NAV]

    ### 📈 Performance vs Category
    [Compare each fund vs its category - use your knowledge + tool data]

    ### ⚠️ Hidden Risks - Overlap & Concentration
    [Call calculate_overlap_note for each pair. Flag if >50% overlap suspected]

    ### 🎯 Goal Alignment Check (Riskometer)
    [Map user's risk profile + goal horizon to required debt/equity mix. As per SEBI Riskometer: Low, Low-Moderate, Moderate, Moderately High, High, Very High]

    ### 📚 Educational Next Steps
    [3 bullet points for what user should discuss with advisor - e.g., review overlap, check expense ratio, rebalance]

    5. End with mandatory disclaimer:
    ---
    **Disclaimer:** This is for educational analysis only, not SEBI-registered investment advice. Data as of today from AMFI. Past performance does not guarantee future returns. Consult SEBI Registered Investment Advisor (RIA) before investing.

    Tone: Professional, helpful, concise. Use Indian context (Lakhs, Nifty, SEBI).
    """

    agent = create_react_agent(llm, tools, state_modifier=system_prompt)
    return agent
