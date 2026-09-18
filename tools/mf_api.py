import requests
import pandas as pd
BASE_URL = "https://api.mfapi.in"
def get_scheme_list():
    try:
        r = requests.get(f"{BASE_URL}/mf", timeout=30)
        return r.json()[:500]
    except:
        return []
def get_scheme_details(scheme_code):
    try:
        r = requests.get(f"{BASE_URL}/mf/{scheme_code}", timeout=30)
        return r.json()
    except:
        return None
def search_schemes(query):
    query = query.lower()
    all_schemes = get_scheme_list()
    matched = [s for s in all_schemes if query in s.get("schemeName","").lower()]
    return matched[:10]
def get_nav_history(scheme_code):
    data = get_scheme_details(scheme_code)
    if not data or "data" not in data:
        return pd.DataFrame()
    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    return df.sort_values("date")
