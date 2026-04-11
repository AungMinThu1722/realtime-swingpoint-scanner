import os
from notion_client import Client
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API_KEY")

def list_databases():
    if not NOTION_TOKEN:
        print("Error: NOTION_API_KEY not found in .env.")
        return

    notion = Client(auth=NOTION_TOKEN)
    
    print("Searching for databases accessible to this token...")
    try:
        # Search for everything and filter for database manually
        response = notion.search()
        
        results = response.get("results", [])
        databases = [obj for obj in results if obj["object"] == "database"]
        
        if not databases:
            print("No databases found.")
            print("Troubleshooting:")
            print("1. Ensure your 'MMXM agent' integration is connected to the database in Notion (Three dots -> Connect to).")
            print("2. Make sure you are using the correct Integration Secret (API Key).")
            return

        print(f"Found {len(databases)} database(s):")
        for db in databases:
            title_list = db.get("title", [])
            title = title_list[0].get("plain_text", "Untitled") if title_list else "Untitled"
            db_id = db.get("id").replace("-", "")
            print(f"- Name: {title}")
            print(f"  ID:   {db_id}")
            print(f"  URL:  {db.get('url')}")
            print("-" * 20)

    except Exception as e:
        print(f"Error during search: {e}")

if __name__ == "__main__":
    list_databases()
