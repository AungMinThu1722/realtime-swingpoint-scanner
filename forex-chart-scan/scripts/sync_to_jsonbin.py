import argparse
import json
import os
import requests
import pandas as pd
from scan_major_fx import scan

# GitHub Gist config
GIST_ID = "9d1d74c2c9b868f2c6c0653b43c344dc"
# Token priority: env var GIST_TOKEN → env var GITHUB_TOKEN → fallback PAT (local dev)
GIST_TOKEN = (
    os.environ.get("GIST_TOKEN")
    or os.environ.get("GITHUB_TOKEN")
) or None

GIST_FILENAME = "scanner_data.json"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"


def update_gist(data):
    """Push scanner data to GitHub Gist (replaces JSONBin.io)."""
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
            print("✅ Successfully synced scanner data to GitHub Gist!")
            print(f"   Dashboard: https://gist.github.com/AungMinThu1722/{GIST_ID}")
            print(f"   API:       {GIST_API_URL}")
        else:
            print(f"❌ Failed to update. Status: {req.status_code}, Response: {req.text}")
    except Exception as e:
        print(f"❌ Error sending data to GitHub Gist: {e}")


def get_scan_results(timeframe):
    print(f"  Scanning {timeframe}...")
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
    print("🔄 Running MMXM scanner...")
    daily_results = get_scan_results("1D")
    weekly_results = get_scan_results("1W")
    monthly_results = get_scan_results("1M")

    payload = {
        "1D": daily_results,
        "1W": weekly_results,
        "1M": monthly_results,
        "updated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    print(f"\n📊 Scan complete — 1D: {len(daily_results)}, 1W: {len(weekly_results)}, 1M: {len(monthly_results)}")
    update_gist(payload)


if __name__ == "__main__":
    run_all_and_sync()
