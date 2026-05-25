"""Quick test to verify GitHub Gist integration is working."""
import json
import os
import requests

GIST_ID = "9d1d74c2c9b868f2c6c0653b43c344dc"
GIST_TOKEN = (
    os.environ.get("GIST_TOKEN")
    or os.environ.get("GITHUB_TOKEN")
) or None
GIST_FILENAME = "scanner_data.json"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"


def update_gist(data):
    headers = {
        "Authorization": f"token {GIST_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": json.dumps(data, indent=2)
            }
        }
    }
    try:
        req = requests.patch(GIST_API_URL, json=payload, headers=headers)
        if req.status_code == 200:
            print("✅ Test data synced to GitHub Gist!")
            print(f"   API Response: updated_at={req.json().get('updated_at', 'N/A')}")
        else:
            print(f"❌ Failed. Status: {req.status_code}, Response: {req.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    example_data = [
        {"pair": "EURUSD", "timeframe": "1D", "status": "Seek & Destroy, Aim Low"},
        {"pair": "GBPUSD", "timeframe": "1D", "status": "Aim High"},
        {"pair": "AUDJPY", "timeframe": "1W", "status": "Seek & Destroy"},
        {"pair": "TEST-SUCCESS", "timeframe": "NOW", "status": "Gist Integration Working!"}
    ]

    payload = {
        "1D": example_data,
        "1W": [],
        "1M": [],
        "updated_at": "TEST-RUN"
    }

    print("Testing GitHub Gist integration with example data...")
    update_gist(payload)
