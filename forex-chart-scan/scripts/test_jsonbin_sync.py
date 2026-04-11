import pandas as pd
import requests

BIN_ID = "69d9d5f9aaba882197e809b7"
API_KEY = "$2a$10$BxfPEZZ3z3.3Cz6dvMCtxeR19LBBAzGJGO5q7MI.kHV5IlFx/sb/G"

def update_jsonbin(df):
    url = f'https://api.jsonbin.io/v3/b/{BIN_ID}'
    headers = {
        'Content-Type': 'application/json',
        'X-Master-Key': API_KEY
    }
    data = df.to_dict(orient="records")
    try:
        req = requests.put(url, json=data, headers=headers)
        if req.status_code == 200:
            print("Successfully updated scanner data to Dashboard (JSONBin)!")
            print("Response:", req.json().get("metadata", {}))
        else:
            print(f"Failed to update. Status Code: {req.status_code}, Response: {req.text}")
    except Exception as e:
        print(f"Error sending data to JSONBin: {e}")

if __name__ == "__main__":
    # Create example data
    example_data = [
        {"pair": "EURUSD", "timeframe": "1D", "status": "Seek & Destroy, Aim Low"},
        {"pair": "GBPUSD", "timeframe": "1D", "status": "Aim High"},
        {"pair": "AUDJPY", "timeframe": "1W", "status": "Seek & Destroy"},
        {"pair": "TEST-SUCCESS", "timeframe": "NOW", "status": "Integration Working!"}
    ]
    
    df = pd.DataFrame(example_data)
    print("Testing JSONBin integration with example data...")
    print(df)
    update_jsonbin(df)
