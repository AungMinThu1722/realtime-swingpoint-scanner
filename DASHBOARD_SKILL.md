---
name: realtime-dashboard-automation
description: Maintain and operate the MMXM Alpha Dashboard (Vercel) and its automated GitHub Action sync to GitHub Gist.
---

# MMXM Dashboard & Automation Skill

This skill is for managing the **Live Trading Dashboard** and its **Automated Daily Scanner**.

## Architecture
- **Frontend:** `index.html` (Vercel-ready, Tailwind CSS, Glassmorphism).
- **Automation:** GitHub Action `.github/workflows/scan.yml` (Runs every 15 min).
- **Database:** GitHub Gist (Synced via `sync_to_jsonbin.py` → GitHub Gist API).
- **Logic:** Ported from `forex-chart-scan/` ICT rules.

## Key Operations

### 1. Manual Dashboard Update
Run this to force an update of the Vercel/Gist dashboard:
```bash
export PYTHONPATH=./forex-chart-scan
python3 forex-chart-scan/scripts/sync_to_jsonbin.py
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
- **Schedule:** Every 15 minutes.
- **Manual Trigger:** Possible via "Run workflow".

## Configuration

### Quick Fix — No GitHub Secret Needed
The script has a PAT fallback built in, so API calls work out of the box on GitHub Actions without modifying the workflow YAML.

### Recommended (for security)
Create a repository secret named `GIST_TOKEN` with your GitHub PAT, then add to `.github/workflows/scan.yml`:
```yaml
env:
  GIST_TOKEN: ${{ secrets.GIST_TOKEN }}
```

## Maintenance Notes
- If signals are not appearing, check the `tvDatafeed` connection first.
- If the dashboard shows "Sync Failed", verify the Gist ID `9d1d74c2c9b868f2c6c0653b43c344dc` is correct and the Gist is public.
- The Gist is public — the frontend fetches data without authentication.
- To view raw data: https://gist.github.com/AungMinThu1722/9d1d74c2c9b868f2c6c0653b43c344dc
- The original ICT logic remains in the `forex-chart-scan/` subdirectory and should not be modified unless the core strategy changes.
