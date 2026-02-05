---
name: garmin-health-analysis
description: Query your Garmin Connect health & activity data (sleep, Body Battery, HRV, heart rate, activities) and generate interactive HTML charts/dashboards.
version: 1.2.2
author: EversonL & Claude
homepage: https://github.com/eversonl/ClawdBot-garmin-health-analysis
metadata: {"openclaw":{"emoji":"⌚","requires":{"env":["GARMIN_EMAIL","GARMIN_PASSWORD"]},"install":[{"id":"garminconnect","kind":"python","package":"garminconnect","label":"Install garminconnect (pip)"},{"id":"fitparse","kind":"python","package":"fitparse","label":"Install fitparse (pip)"},{"id":"gpxpy","kind":"python","package":"gpxpy","label":"Install gpxpy (pip)"}]}}
---

# Garmin Health Analysis

Talk to your Garmin data naturally:

- “How did I sleep last night?”
- “Is my HRV improving this month?”
- “How’s my recovery vs. training load?”
- “What was my fastest speed on yesterday’s ride?”

This skill authenticates to Garmin Connect, fetches health/activity metrics as JSON, and can generate interactive Chart.js HTML dashboards.

## Two installation paths (Skill vs MCP)

This repository is the **OpenClaw skill**.

If you want to use Garmin data with **standard Claude Desktop** (via MCP), use the dedicated MCP server repo instead:

- For the MCP path, see **[references/mcp_setup.md](references/mcp_setup.md)**

These can **coexist**:
- OpenClaw skill → automation (scheduled summaries, proactive check-ins)
- MCP server → ad-hoc “talk to my data” queries in Claude Desktop

They share the same locally stored Garmin session tokens.

---

## Install the skill

### Via ClawHub (recommended)

```bash
clawhub install garmin-health-analysis
```

### Manual install

```bash
mkdir -p ~/.openclaw/skills
cd ~/.openclaw/skills
git clone https://github.com/eversonl/ClawdBot-garmin-health-analysis.git garmin-health-analysis
```

## Install Python dependencies

```bash
pip3 install garminconnect fitparse gpxpy
```

Notes:
- `garminconnect` is required for API access.
- `fitparse` and `gpxpy` are used for FIT/GPX activity file parsing.

---

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

Tip: setting env vars here is the simplest way to ensure OpenClaw runs the scripts with the right credentials.

### Option B: Local config file (in the skill directory)

```bash
cd ~/.openclaw/skills/garmin-health-analysis
cp config.example.json config.json
# edit config.json
```

Example `config.json`:

```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

`config.json` is gitignored so you can keep credentials local.

### Option C: CLI args (one-off)

```bash
python3 scripts/garmin_auth.py login \
  --email your-email@example.com \
  --password 'your-password'
```

### Credential lookup order

When you run `garmin_auth.py login`, credentials are resolved in this order:

1. CLI args (`--email`, `--password`)
2. Local `config.json` (if present)
3. Environment variables (`GARMIN_EMAIL`, `GARMIN_PASSWORD`)

(When OpenClaw executes the skill, Option A effectively provides #3.)

---

## Authenticate

Login once to create session tokens:

```bash
python3 scripts/garmin_auth.py login
python3 scripts/garmin_auth.py status
```

Token storage:
- New tokens are written to: `~/.openclaw/garmin/`
- Legacy tokens are also recognized from: `~/.clawdbot/garmin/`

This is what makes “skill + MCP server” coexistence possible.

---

## Common workflows

### Fetch data (JSON)

Use `scripts/garmin_data.py` (JSON to stdout):

```bash
python3 scripts/garmin_data.py summary --days 7
python3 scripts/garmin_data.py sleep --days 14
python3 scripts/garmin_data.py body_battery --days 30
python3 scripts/garmin_data.py hrv --days 30
python3 scripts/garmin_data.py heart_rate --days 14
python3 scripts/garmin_data.py stress --days 7
python3 scripts/garmin_data.py activities --days 14
python3 scripts/garmin_data.py profile
```

Custom range:

```bash
python3 scripts/garmin_data.py sleep --start 2026-01-01 --end 2026-01-15
```

### Generate charts (HTML)

Use `scripts/garmin_chart.py` (opens a browser, or write a file):

```bash
python3 scripts/garmin_chart.py dashboard --days 30
python3 scripts/garmin_chart.py sleep --days 30
python3 scripts/garmin_chart.py body_battery --days 30
python3 scripts/garmin_chart.py hrv --days 90
python3 scripts/garmin_chart.py activities --days 30

python3 scripts/garmin_chart.py dashboard --days 90 --output ~/Desktop/garmin-health.html
```

### Download FIT/GPX/TCX activity files

Use `scripts/garmin_activity_files.py` to download and parse activities (useful for “at mile 3 what was my pace/elevation/HR?” type questions).

If you need this functionality, read **[references/extended_capabilities.md](references/extended_capabilities.md)** first (it documents the supported workflows and what data you can extract).

### Extended metrics (training readiness, VO2 max, SPO2, etc.)

Use `scripts/garmin_data_extended.py` for additional endpoints (training readiness/status, body composition, SPO2, hydration, and more).

For detailed endpoint notes, see **[references/extended_capabilities.md](references/extended_capabilities.md)**.

---

## Quick “what to run” mapping

| User asks… | Usually run… |
|---|---|
| “How did I sleep last night?” | `python3 scripts/garmin_data.py sleep --days 1` (and/or `summary --days 1`) |
| “How’s my recovery this week?” | `python3 scripts/garmin_data.py body_battery --days 7` |
| “Is my HRV improving?” | `python3 scripts/garmin_data.py hrv --days 30` (look at trend vs baseline) |
| “Show me my health dashboard for the last month” | `python3 scripts/garmin_chart.py dashboard --days 30` |
| “What workouts did I do this week?” | `python3 scripts/garmin_data.py activities --days 7` |
| “How’s my resting heart rate?” | `python3 scripts/garmin_data.py heart_rate --days 14` |

---

## Key metrics (high-level)

These are quick heuristics; for deeper interpretation and ranges, use **[references/health_analysis.md](references/health_analysis.md)**.

- **Body Battery (0–100)**: Garmin’s recovery/energy estimate. Sustained low peaks can indicate under-recovery.
- **Sleep Score (0–100)**: composite sleep quality measure (duration, stages, disturbances).
- **HRV (ms)**: trend matters more than the absolute number; drops from your baseline often correlate with stress/illness/overtraining.
- **Resting HR (bpm)**: a multi-day rise above baseline is often a fatigue/stress signal.
- **Stress**: based on HRV patterns; watch for all-day elevation.

---

## Health analysis guidance (when users ask “why”)

When a user asks for interpretation (“is this good/bad?”, “what does this mean?”, “what should I do?”), read:

- **[references/health_analysis.md](references/health_analysis.md)**

Suggested analysis workflow:
1. Fetch data (`summary` + relevant metric endpoints)
2. Compare against the user’s recent baseline (week/month) rather than single-day values
3. Explain the *pattern* (trend, variability, recovery cycles)
4. Provide practical, low-risk suggestions
5. Include a brief disclaimer: informational only, not medical advice

---

## Troubleshooting

### Authentication
- If you see “Not authenticated”: run `python3 scripts/garmin_auth.py login`
- If tokens expired: re-run `login` (it overwrites tokens in `~/.openclaw/garmin/`)
- If Garmin rate-limits: wait a few minutes and retry; prefer `summary` over many individual calls

### Missing data
- Some metrics require specific devices/features (e.g., Body Battery/HRV-capable wearables)
- Gaps happen if the device wasn’t worn, wasn’t recording, or Garmin didn’t compute the metric

### Dependency errors
- `garminconnect not installed` → `pip3 install garminconnect`
- FIT parsing requires `fitparse`; GPX parsing requires `gpxpy`

---

## References (read when needed)

- **[references/mcp_setup.md](references/mcp_setup.md)** — choose Skill vs MCP server (Claude Desktop)
- **[references/health_analysis.md](references/health_analysis.md)** — interpretation framework and ranges
- **[references/api.md](references/api.md)** — Garmin Connect API notes (unofficial)
- **[references/extended_capabilities.md](references/extended_capabilities.md)** — advanced endpoints + activity file workflows
