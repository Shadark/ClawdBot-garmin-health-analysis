---
name: garmin-health-analysis
description: Query your Garmin Connect health & activity data (sleep, Body Battery, HRV, heart rate, activities) and generate interactive HTML charts/dashboards.
version: 1.2.2
author: EversonL & Claude
homepage: https://github.com/eversonl/ClawdBot-garmin-health-analysis
metadata: {"openclaw":{"emoji":"⌚","requires":{"env":["GARMIN_EMAIL","GARMIN_PASSWORD"]},"install":[{"id":"garminconnect","kind":"python","package":"garminconnect","label":"Install garminconnect (pip)"},{"id":"fitparse","kind":"python","package":"fitparse","label":"Install fitparse (pip)"},{"id":"gpxpy","kind":"python","package":"gpxpy","label":"Install gpxpy (pip)"}]}}
---

# Garmin Health Analysis

Use the scripts in `scripts/` to authenticate to Garmin Connect, fetch health metrics as JSON, and generate interactive HTML charts.

## Install

```bash
pip3 install garminconnect fitparse gpxpy
```

## Configure credentials (pick one)

### Option A: OpenClaw config (recommended)

Add env vars under this skill entry in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "garmin-health-analysis": {
        "enabled": true,
        "env": {
          "GARMIN_EMAIL": "your-email@example.com",
          "GARMIN_PASSWORD": "your-password"
        }
      }
    }
  }
}
```

### Option B: Local config file (in the skill directory)

```bash
cd ~/.openclaw/skills/garmin-health-analysis
cp config.example.json config.json
# edit config.json
```

### Option C: CLI args

```bash
python3 scripts/garmin_auth.py login \
  --email your-email@example.com \
  --password 'your-password'
```

## Authenticate

```bash
python3 scripts/garmin_auth.py login
python3 scripts/garmin_auth.py status
```

Tokens are stored locally in `~/.openclaw/garmin/`.
If you have legacy tokens in `~/.clawdbot/garmin/`, they are still recognized.

## Fetch data (JSON)

```bash
python3 scripts/garmin_data.py summary --days 7
python3 scripts/garmin_data.py sleep --days 14
python3 scripts/garmin_data.py body_battery --days 30
python3 scripts/garmin_data.py hrv --days 30
python3 scripts/garmin_data.py activities --days 14
```

For a custom range:

```bash
python3 scripts/garmin_data.py sleep --start 2026-01-01 --end 2026-01-15
```

## Generate charts (HTML)

```bash
python3 scripts/garmin_chart.py dashboard --days 30
python3 scripts/garmin_chart.py sleep --days 30
python3 scripts/garmin_chart.py hrv --days 90
```

## Notes

- Garmin rate-limits API calls; prefer `summary` when possible.
- Some metrics require specific Garmin devices and may be missing on unsupported hardware.

## References (optional)

- `references/health_analysis.md` — interpretation framework (informational, not medical advice)
- `references/api.md` — Garmin Connect API notes (unofficial)
- `references/extended_capabilities.md` — additional endpoints and ideas
