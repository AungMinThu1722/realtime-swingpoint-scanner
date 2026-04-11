---
name: realtime-dashboard-automation
description: Maintain and operate the MMXM Alpha Dashboard (Vercel) and its automated GitHub Action sync to JSONBin.io.
---

# MMXM Dashboard & Automation Skill

This skill is for managing the **Live Trading Dashboard** and its **Automated Daily Scanner**.

## Architecture
- **Frontend:** `index.html` (Vercel-ready, Tailwind CSS, Glassmorphism).
- **Automation:** GitHub Action `.github/workflows/scan.yml` (Runs 00:00 UTC daily).
- **Database:** JSONBin.io (Synced via `sync_to_jsonbin.py`).
- **Logic:** Ported from `forex-chart-scan/` ICT rules.

## Key Operations

### 1. Manual Dashboard Update
Run this to force an update of the Vercel/JSONBin dashboard:
```bash
export PYTHONPATH=./forex-chart-scan
python3 forex-chart-scan/scripts/sync_to_jsonbin.py --timeframe 1D
```

### 2. Manual Notion Sync
Run this to push active signals to your Notion database:
```bash
export PYTHONPATH=./forex-chart-scan
python3 forex-chart-scan/scripts/sync_to_notion.py --timeframe 1D
```

### 3. Verify GitHub Actions
Check the **Actions** tab in the `realtime-swingpoint-scanner` repository.
- **Workflow Name:** `Daily MMXM Scan`
- **Schedule:** 00:00 UTC Daily.
- **Manual Trigger:** Possible via "Run workflow".

## Configuration (Environment Variables)
Ensure these are set in your local `.env` or GitHub Secrets:
- `NOTION_API_KEY`: Internal Integration Token.
- `NOTION_DATABASE_ID`: The specific database ID for signals.
- `JSONBIN_API_KEY`: JSONBin.io Master Key.
- `JSONBIN_BIN_ID`: The specific Bin ID for the dashboard.

## Maintenance Notes
- If signals are not appearing, check the `tvDatafeed` connection first.
- If the dashboard shows "Failed to load", verify the `JSONBIN_API_KEY` in `index.html` (or your fetch headers).
- The original ICT logic remains in the `forex-chart-scan/` subdirectory and should not be modified unless the core strategy changes.
