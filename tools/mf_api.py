import requests
from langchain_core.tools import tool

MFAPI_BASE = "https://api.mfapi.in/mf"
SEARCH_BASE = "https://api.mfapi.in/mf/search"

@tool
def get_fund_details(fund_name: str) -> str:
    """
    Fetch Indian Mutual Fund scheme details, NAV, returns. 
    Input: part of fund name like 'Parag Parikh Flexi Cap'
    Returns fund house, category, latest NAV with date.
    """
    try:
        search_url = f"{SEARCH_BASE}?q={fund_name}"
        r = requests.get(search_url, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        if not data:
            return f"No fund found for '{fund_name}'. Try full name like 'Parag Parikh Flexi Cap Fund'"
        
        # Take top 2 results to give options
        top_results = data[:2]
        output = []
        for item in top_results:
            scheme_code = item.get('schemeCode')
            detail_url = f"{MFAPI_BASE}/{scheme_code}"
            try:
                d = requests.get(detail_url, timeout=15).json()
                meta = d.get('meta', {})
                nav_history = d.get('data', [])
                latest = nav_history[0] if nav_history else {}
                output.append(
                    f"Fund: {meta.get('scheme_name')} | "
                    f"House: {meta.get('fund_house')} | "
                    f"Category: {meta.get('scheme_category')} | "
                    f"Type: {meta.get('scheme_type')} | "
                    f"Latest NAV: {latest.get('nav')} on {latest.get('date')} | "
                    f"Scheme Code: {scheme_code}"
                )
            except:
                output.append(f"Found: {item.get('schemeName')} | Code: {scheme_code}")
        
        return " | ".join(output)
    
    except Exception as e:
        return f"Error fetching fund '{fund_name}': {str(e)}. Source: mfapi.in (AMFI)"

@tool
def calculate_overlap_note(fund1: str, fund2: str) -> str:
    """
    Educational note on portfolio overlap between two funds.
    In production, this would parse factsheet holdings PDFs.
    Returns guidance on how overlap is calculated.
    """
    f1_lower = fund1.lower()
    f2_lower = fund2.lower()
    
    # Simple heuristic for demo
    if "small cap" in f1_lower and "small cap" in f2_lower:
        return f"Overlap Alert: {fund1} vs {fund2} - Both are Small Cap funds. Typically hold 60-70% overlapping stocks (e.g., same mid/small companies). High concentration risk. Suggest checking factsheets for common holdings like BSE SmallCap constituents. Diversification benefit: LOW."
    elif "flexi cap" in f1_lower and "mid cap" in f2_lower or "mid cap" in f1_lower and "flexi cap" in f2_lower:
        return f"Overlap Check: {fund1} vs {fund2} - Flexi Cap often has 30-40% mid-cap exposure. Possible 25-35% overlap with dedicated Mid Cap fund. Moderate overlap."
    else:
        return f"Overlap Check: {fund1} vs {fund2} - To calculate exact overlap, compare holdings from latest factsheets (available on AMC website / Value Research). Look for common stocks >10%. Rule of thumb: Overlap >50% means low diversification benefit."

@tool
def get_category_average_note(category: str) -> str:
    """
    Provides educational context about MF category averages and benchmarks.
    Input: category like 'Small Cap', 'Flexi Cap', 'Mid Cap'
    """
    benchmarks = {
        "small cap": "Benchmark: Nifty Smallcap 250 TRI. Category Avg XIRR (3Y) ~22-24% (volatile). SEBI Riskometer: Very High.",
        "mid cap": "Benchmark: Nifty Midcap 150 TRI. Category Avg XIRR (3Y) ~18-20%. SEBI Riskometer: Very High.",
        "flexi cap": "Benchmark: Nifty 500 TRI. Category Avg XIRR (3Y) ~14-16%. SEBI Riskometer: Very High.",
        "large cap": "Benchmark: Nifty 100 TRI. Category Avg XIRR (3Y) ~12-14%. SEBI Riskometer: Very High.",
        "elss": "Benchmark: Nifty 500 TRI. Lock-in 3Y. Category Avg XIRR (3Y) ~13-15%. SEBI Riskometer: Very High. Tax benefit u/s 80C.",
        "hybrid": "Benchmark: CRISIL Hybrid 35+65. Category Avg XIRR (3Y) ~11-13%. SEBI Riskometer: Moderately High to High.",
    }
    cat_lower = category.lower()
    for key in benchmarks:
        if key in cat_lower:
            return benchmarks[key]
    return f"Category '{category}': Check Value Research / Morningstar for category average returns, benchmark (Nifty 50 TRI / Nifty 500 TRI), and SEBI Riskometer level."
