import argparse
import requests
import pandas as pd
from scan_major_fx import scan

BIN_ID = "69d9d5f9aaba882197e809b7"
API_KEY = "$2a$10$BxfPEZZ3z3.3Cz6dvMCtxeR19LBBAzGJGO5q7MI.kHV5IlFx/sb/G"

def update_jsonbin(df):
    """
    Convert pandas dataframe to JSON and PUT it to JSONBin.io
    """
    url = f'https://api.jsonbin.io/v3/b/{BIN_ID}'
    headers = {
        'Content-Type': 'application/json',
        'X-Master-Key': API_KEY
    }
    
    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")
    
    try:
        req = requests.put(url, json=data, headers=headers)
        if req.status_code == 200:
            print("Successfully updated scanner data to Dashboard (JSONBin)!")
        else:
            print(f"Failed to update. Status Code: {req.status_code}, Response: {req.text}")
    except Exception as e:
        print(f"Error sending data to JSONBin: {e}")

def run_and_sync(timeframe="1D"):
    print(f"Running scanner for {timeframe}...")
    results = scan(timeframe=timeframe)
    
    # Format data for the Dashboard
    formatted_results = []
    for r in results:
        active_patterns = []
        if r.get("seek_and_destroy"): active_patterns.append("Seek & Destroy")
        if r.get("aim_for_range_low"): active_patterns.append("Aim Low")
        if r.get("aim_for_range_high"): active_patterns.append("Aim High")
        
        # Only include pairs with active signals
        if active_patterns:
            formatted_results.append({
                "pair": r["symbol"],
                "timeframe": timeframe,
                "status": ", ".join(active_patterns)
            })
    
    if not formatted_results:
        print("No active signals found. Updating Dashboard with empty list.")
        df = pd.DataFrame(columns=["pair", "timeframe", "status"])
    else:
        df = pd.DataFrame(formatted_results)
    
    update_jsonbin(df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeframe", default="1D", help="1D, 1W, or 1M")
    args = parser.parse_args()
    
    run_and_sync(timeframe=args.timeframe)
