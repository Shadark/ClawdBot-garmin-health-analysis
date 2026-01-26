# Garmin Health Analysis

> **Talk to your Garmin data naturally** - "what was my fastest speed snowboarding?", "how did I sleep last night?", "what was my heart rate at 3pm?"

Access 20+ metrics from your Garmin device: sleep stages, Body Battery, HRV, VO2 max, training readiness, body composition, SPO2, and more. Download FIT/GPX files, query elevation/pace at any point, and generate interactive health dashboards.

## 🚀 Quick Start

### Choose Your Path

#### Option 1: Clawdbot Skill (Automation & Proactive Monitoring)

**Best for**: Scheduled health check-ins, automated reporting, integration with other Clawdbot skills

```bash
# Install via clawdhub
clawdhub install garmin-health-analysis

# Or manually
cd ~/.clawdbot/skills
git clone https://github.com/eversonl/ClawdBot-garmin-health-analysis.git garmin-health-analysis

# Install dependencies
pip3 install garminconnect fitparse gpxpy

# Configure credentials and authenticate
python3 scripts/garmin_auth.py login
```

**[📖 Full Clawdbot Setup Guide](SKILL.md)**

#### Option 2: MCP Server (Standard Claude Desktop)

**Best for**: Ad-hoc queries in Claude Desktop, no Clawdbot required

```bash
# Clone the MCP server repo
git clone https://github.com/eversonl/garmin-health-mcp-server.git
cd garmin-health-mcp-server

# Install dependencies
npm install
pip3 install garminconnect fitparse gpxpy

# Configure Claude Desktop
# Add to claude_desktop_config.json (see guide)
```

**[📖 Full MCP Server Setup Guide](references/mcp_setup.md)**

## ⚡ Features

- **Natural language queries**: "How's my recovery this week?" → instant Body Battery analysis
- **Sleep analysis**: Hours, stages (light/deep/REM), quality scores, trends
- **Recovery tracking**: Body Battery, HRV, training readiness, stress levels
- **Workout data**: Activities by type, calories, duration, pace, elevation
- **Health metrics**: Resting heart rate, VO2 max, body composition, SPO2
- **Activity files**: Download FIT/GPX for detailed route and performance analysis
- **Interactive charts**: Beautiful HTML dashboards with Chart.js visualizations
- **Science-backed insights**: Interpret trends with expert analysis framework

## 📊 Example Queries

**Clawdbot or Claude Desktop:**

> "How did I sleep last night?"
> 
> "Show me my health dashboard for the last month"
> 
> "Is my HRV improving?"
> 
> "What was my fastest speed during yesterday's bike ride?"
> 
> "How's my recovery vs. training load balance?"
> 
> "Download the GPX file for my Sunday run"

## 🛠️ Key Metrics

| Metric | Range | What It Means |
|--------|-------|---------------|
| **Body Battery** | 0-100 | Garmin's recovery score (higher = more energy) |
| **Sleep Score** | 0-100 | Overall sleep quality (90+ = excellent) |
| **HRV** | 20-200+ ms | Heart rate variability (higher = better recovery) |
| **Resting HR** | 40-80 bpm | Lower is generally better (athletes: 40-60) |
| **Stress** | Low/Med/High | Based on HRV throughout the day |

## 📦 What's Included

```
garmin-health-analysis/
├── SKILL.md                    # Clawdbot setup & usage
├── README.md                   # This file
├── scripts/
│   ├── garmin_auth.py         # Authentication helper
│   ├── garmin_data.py         # Fetch JSON data
│   └── garmin_chart.py        # Generate HTML charts
├── references/
│   ├── api.md                 # Garmin Connect API docs
│   ├── health_analysis.md     # Metric interpretation guide
│   ├── extended_capabilities.md  # Advanced features
│   └── mcp_setup.md           # MCP server installation
└── config.example.json        # Credentials template
```

## 🔒 Privacy & Security

- Credentials stored locally (never sent to third parties)
- Session tokens auto-refresh (no repeated logins)
- Connects only to Garmin's official API
- No cloud storage or external data sharing
- Open source - audit the code yourself

## 🤝 Can I Use Both?

**Yes!** You can run both the Clawdbot skill and the MCP server simultaneously. They share authentication tokens, so you only need to log in once.

**Use cases:**
- **Clawdbot**: Morning health summaries, workout notifications, weekly reports
- **Claude Desktop**: Quick ad-hoc queries during the day

## 📚 Documentation

- **[SKILL.md](SKILL.md)** - Complete Clawdbot setup, commands, troubleshooting
- **[references/mcp_setup.md](references/mcp_setup.md)** - MCP server for Claude Desktop
- **[references/health_analysis.md](references/health_analysis.md)** - Science-backed metric interpretation
- **[references/api.md](references/api.md)** - Garmin Connect API details
- **[references/extended_capabilities.md](references/extended_capabilities.md)** - Advanced features

## 🐛 Troubleshooting

**Authentication issues?**
- Run `python3 scripts/garmin_auth.py login` to refresh tokens
- Check credentials in config.json or environment variables
- Try logging into Garmin Connect web to verify account

**Missing data?**
- Some metrics require specific devices (Body Battery needs HRV-capable watches)
- Check device was worn during the time period
- New accounts may have limited history

**Rate limits?**
- Garmin limits API requests - wait a few minutes and try again
- Batch queries when possible (use `summary` instead of individual calls)

## 🙏 Credits

- **Author**: EversonL & Claude
- **Version**: 1.2.0
- **License**: MIT
- **Dependencies**: [python-garminconnect](https://github.com/cyberjunky/python-garminconnect), fitparse, gpxpy

## 🔗 Links

- **Clawdbot**: [clawdbot.com](https://clawdbot.com)
- **ClawdHub**: [clawdhub.com](https://clawdhub.com)
- **Garmin Connect**: [connect.garmin.com](https://connect.garmin.com)

---

**Questions?** Open an issue on GitHub or ask in the Clawdbot Discord!
