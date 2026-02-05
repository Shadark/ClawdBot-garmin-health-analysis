# Garmin Health Analysis (OpenClaw Skill)

Query your Garmin Connect health/activity data and generate interactive HTML charts.

Example prompts you can answer with this skill:
- “How did I sleep last night?”
- “Is my HRV improving?”
- “How’s my recovery this week?”
- “What workouts did I do this month?”

## Claude Desktop (MCP) vs OpenClaw (Skill)

This repository contains the **OpenClaw skill**.

If you want Garmin data inside **standard Claude Desktop** via MCP, use the dedicated MCP server:
- https://github.com/eversonl/garmin-health-mcp-server

You can use both (they share locally stored session tokens).

## Install

### Via ClawHub

```bash
clawhub install garmin-health-analysis
```

### Manual

```bash
mkdir -p ~/.openclaw/skills
cd ~/.openclaw/skills
git clone https://github.com/eversonl/ClawdBot-garmin-health-analysis.git garmin-health-analysis
```

Then follow **[SKILL.md](SKILL.md)** for:
- Python dependencies
- Credential setup (OpenClaw config / local `config.json` / CLI)
- Authentication
- Common workflows (JSON + dashboards)

## Documentation

- Primary guide: **[SKILL.md](SKILL.md)**
- Interpretation guide (when the user asks “what does this mean?”): **[references/health_analysis.md](references/health_analysis.md)**
- MCP setup notes: **[references/mcp_setup.md](references/mcp_setup.md)**

## Privacy & security (high level)

- Credentials and tokens are stored locally
- Connects only to Garmin’s official services through the `garminconnect` library
- No third-party cloud storage in this repository

## Project links

- OpenClaw: https://openclaw.ai
- ClawHub: https://clawhub.com
- Garmin Connect: https://connect.garmin.com

## Support this project

If you find this skill useful, consider supporting its development:

<a href="https://buymeacoffee.com/leeev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
