---
name: forex-chart-scan
description: Run and maintain the 27-pair FOREXCOM long-term chart-scan workflow for daily, weekly, and monthly timeframes using tvDatafeed, batch pulls, and vectorized ICT-style rules. Use when an agent needs to scan FX charts, package the Python workflow as a reusable skill, or adapt the scan for another agent/platform that reads SKILL.md bundles.
---

# Forex Chart Scan

Use this skill to run the portable FX chart-scan workflow or to hand it to another agent that can follow a `SKILL.md` skill bundle.

LTP means Long Term Perspective.

## Canonical workflow

1. Fetch FOREXCOM OHLCV data with `tvDatafeed`.
2. Clean columns to lowercase.
3. Trim the ongoing candle when requested.
4. Scan the 27-pair basket in batches.
5. Apply vectorized ICT-style rules.
6. Report the matching symbols and signal flags.
7. Stop after the requested timeframe and ask the user before moving to the next timeframe.

## Output and handoff rules

- Treat this skill as an alerting workflow, not an execution workflow.
- Never place orders, size positions, or present a signal as a final trading decision.
- After a `1D` run, pause and ask whether to continue with `1W` and `1M`.
- If the user requests only one timeframe, do not auto-run the other timeframes.
- If signals are found, report them clearly and wait for human confirmation before any further action.

## Default scan setup

- Universe: 27 FOREXCOM FX pairs
- Candles: 5
- Batch size: 9
- Pause between batches: 2 seconds
- Supported timeframes: `1D`, `1W`, `1M`

## Script entrypoints

- `scripts/scan_major_fx.py` is the canonical runner for the full three-signal scan.
- `scripts/scan_profiles.py` is the lighter runner for Seek and Destroy plus Aim For Range Low.
Use CLI arguments or env vars:

```bash
python scripts/scan_major_fx.py --timeframe 1D
python scripts/scan_major_fx.py --timeframe 1W
python scripts/scan_major_fx.py --timeframe 1M
```

Environment overrides:

- `SCAN_TIMEFRAME`
- `SCAN_BARS`
- `SCAN_TRIM_ONGOING`
- `SCAN_BATCH_SIZE`
- `SCAN_SLEEP_BETWEEN_BATCHES`

## Signal rules

See [references/profiles.md](references/profiles.md) for the exact candle conditions.

Current profiles:

- Seek and Destroy
- Aim For Range Low
- Aim For Range High

## Implementation notes

- Keep logic vectorized with pandas.
- Return boolean series aligned to the input index.
- Force the first row to `False`.
- Handle tvDatafeed failures per symbol so one timeout does not stop the whole run.
- Keep batch pulls sequential to reduce websocket churn.
- Ask for confirmation before any step that would move beyond the requested scan timeframe.

## Portability

This bundle is meant to be readable by any agent or platform that understands `SKILL.md`-style skills. If another system needs a wrapper prompt, point it at this folder and the scripts above.
