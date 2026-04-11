import argparse
import os
import datetime
from notion_client import Client
from scan_major_fx import scan
from dotenv import load_dotenv

# Load from .env file (looked for in current dir and parent dirs)
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "33f67c3beae480d09258e20b5caf2a4f")

def sync_to_notion(timeframe="1D"):
    if not NOTION_TOKEN:
        print("Error: NOTION_API_KEY not found in environment or .env file.")
        return

    notion = Client(auth=NOTION_TOKEN)
    
    print(f"Running scan for {timeframe}...")
    results = scan(timeframe=timeframe)
    
    # Filter for pairs where at least one signal is True
    active_signals = [r for r in results if r["seek_and_destroy"] or r["aim_for_range_low"] or r["aim_for_range_high"]]
    
    if not active_signals:
        print("No active signals found. Nothing to sync.")
        return

    print(f"Found {len(active_signals)} active signals. Syncing to Notion...")
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    for signal in active_signals:
        try:
            notion.pages.create(
                parent={"database_id": DATABASE_ID},
                properties={
                    "Symbol": {"title": [{"text": {"content": signal["symbol"]}}]},
                    "Timeframe": {"select": {"name": timeframe}},
                    "Seek and Destroy": {"checkbox": signal["seek_and_destroy"]},
                    "Aim For Range Low": {"checkbox": signal["aim_for_range_low"]},
                    "Aim For Range High": {"checkbox": signal["aim_for_range_high"]},
                    "Date": {"date": {"start": today}}
                }
            )
            print(f"Synced {signal['symbol']} to Notion.")
        except Exception as e:
            print(f"Error syncing {signal['symbol']}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeframe", default="1D", help="1D, 1W, or 1M")
    args = parser.parse_args()
    
    sync_to_notion(timeframe=args.timeframe)
