import argparse
import requests
import pandas as pd
from scan_major_fx import scan

BIN_ID = "69d9d5f9aaba882197e809b7"
API_KEY = "$2a$10$BxfPEZZ3z3.3Cz6dvMCtxeR19LBBAzGJGO5q7MI.kHV5IlFx/sb/G"

def update_jsonbin(data):
    """
    Push a dictionary containing multiple timeframe results to JSONBin.io
    """
    url = f'https://api.jsonbin.io/v3/b/{BIN_ID}'
    headers = {
        'Content-Type': 'application/json',
        'X-Master-Key': API_KEY
    }
    
    try:
        req = requests.put(url, json=data, headers=headers)
        if req.status_code == 200:
            print("Successfully updated scanner data to Dashboard (JSONBin)!")
        else:
            print(f"Failed to update. Status Code: {req.status_code}, Response: {req.text}")
    except Exception as e:
        print(f"Error sending data to JSONBin: {e}")

def get_scan_results(timeframe):
    print(f"Running scanner for {timeframe}...")
    results = scan(timeframe=timeframe)
    
    formatted_results = []
    for r in results:
        active_patterns = []
        if r.get("seek_and_destroy"): active_patterns.append("Seek & Destroy")
        if r.get("aim_for_range_low"): active_patterns.append("Aim Low")
        if r.get("aim_for_range_high"): active_patterns.append("Aim High")
        
        if active_patterns:
            formatted_results.append({
                "pair": r["symbol"],
                "timeframe": timeframe,
                "status": ", ".join(active_patterns)
            })
    return formatted_results

def run_all_and_sync():
    # Run both Daily and Weekly scans
    daily_results = get_scan_results("1D")
    weekly_results = get_scan_results("1W")
    
    # Combined payload
    payload = {
        "1D": daily_results,
        "1W": weekly_results,
        "updated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    update_jsonbin(payload)

if __name__ == "__main__":
    run_all_and_sync()
