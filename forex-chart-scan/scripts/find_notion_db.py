import os
from notion_client import Client
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
PAGE_ID = os.getenv("NOTION_PAGE_ID", "33f67c3beae480d09258e20b5caf2a4f")

def find_databases():
    if not NOTION_TOKEN:
        print("Error: NOTION_API_KEY not found.")
        return
        
    notion = Client(auth=NOTION_TOKEN)
    try:
        children = notion.blocks.children.list(block_id=PAGE_ID)
        for block in children.get("results", []):
            if block["type"] == "child_database":
                print(f"Found Database: {block['child_database']['title']}")
                print(f"Database ID: {block['id'].replace('-', '')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_databases()
