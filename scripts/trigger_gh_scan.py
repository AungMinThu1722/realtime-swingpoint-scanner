#!/usr/bin/env python3
"""Trigger GitHub Actions workflow_dispatch for the scanner."""

import subprocess
import sys
import json
import urllib.request

REPO = "AungMinThu1722/realtime-swingpoint-scanner"
WORKFLOW_ID = "259304894"

def get_github_token():
    """Get GitHub token from git credential store."""
    try:
        result = subprocess.run(
            ["git", "credential-manager", "get"],
            input="protocol=https\nhost=github.com\n",
            capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.strip().split("\n"):
            if line.startswith("password="):
                return line.split("=", 1)[1]
    except Exception as e:
        print(f"❌ Failed to get token: {e}")
        return None
    return None

def trigger_workflow(token):
    """Trigger workflow_dispatch via GitHub API."""
    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW_ID}/dispatches"
    data = json.dumps({"ref": "main"}).encode()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 204:
                print("✅ Workflow dispatch triggered successfully")
                return True
            else:
                print(f"❌ Unexpected status: {resp.status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    token = get_github_token()
    if not token:
        print("❌ Could not get GitHub token")
        sys.exit(1)
    if trigger_workflow(token):
        sys.exit(0)
    else:
        sys.exit(1)
