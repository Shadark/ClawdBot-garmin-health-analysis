# Garmin Health Analysis

Talk to your Garmin data naturally with Claude - works with **Clawdbot**, **Claude Desktop**, **Claude Code**, and any MCP client.

## Features

- 🤖 **Works everywhere**: Clawdbot, Claude Desktop, Claude Code, any MCP client
- 📊 **Comprehensive health metrics**: Sleep, Body Battery, HRV, heart rate, activities, stress, and 15+ more
- 🎯 **Time-based queries**: "What was my heart rate at 3pm?" - instant answers
- 🗺️ **Activity file analysis**: Download and parse FIT/GPX files with GPS, elevation, pace, power data
- 📈 **Interactive charts**: Beautiful HTML dashboards with Chart.js (Clawdbot)
- 🧠 **Health analysis**: Science-backed interpretation of your data
- 💾 **Local authentication**: Secure token storage, no cloud dependencies

## Quick Start

### For Claude Desktop / Claude Code

See **[CLAUDE_DESKTOP.md](CLAUDE_DESKTOP.md)** for MCP server installation.

**TL;DR:**
```bash
pip install mcp garminconnect fitparse gpxpy
```

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "garmin": {
      "command": "python",
      "args": ["/path/to/garmin-health-analysis/mcp_server.py"],
      "env": {
        "GARMIN_EMAIL": "your@email.com",
        "GARMIN_PASSWORD": "yourpass"
      }
    }
  }
}
```

Then ask Claude: "How did I sleep last night?" or "What was my fastest speed snowboarding?"

---

### For Clawdbot

### 1. Install Dependencies

```bash
pip3 install garminconnect fitparse gpxpy
```

### 2. Configure Credentials

**Option A: Clawdbot Config (Recommended)**

Add to `~/.clawdbot/clawdbot.json`:
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

Or set through the Clawdbot UI in Skills settings.

**Option B: Local Config File**
```bash
# Copy the example config
cp config.example.json config.json

# Edit config.json and add your Garmin credentials
nano config.json
```

### 3. Authenticate

```bash
# Login using configured credentials
python3 scripts/garmin_auth.py login

# Or pass credentials directly
python3 scripts/garmin_auth.py login \
  --email your-email@example.com \
  --password your-password
```

### 4. Fetch Data

```bash
# Get a summary of the last 7 days
python3 scripts/garmin_data.py summary --days 7

# Get sleep data
python3 scripts/garmin_data.py sleep --days 14

# Get Body Battery (recovery)
python3 scripts/garmin_data.py body_battery --days 30
```

### 5. Generate Charts

```bash
# Full health dashboard
python3 scripts/garmin_chart.py dashboard --days 30

# Individual charts
python3 scripts/garmin_chart.py sleep --days 30
python3 scripts/garmin_chart.py body_battery --days 30
python3 scripts/garmin_chart.py hrv --days 90
python3 scripts/garmin_chart.py activities --days 30
```

## 🎯 Time-Based Queries (NEW in v1.1+)

Ask questions about specific times:

```bash
# Heart rate at specific time
python3 scripts/garmin_query.py heart_rate "3:00 PM"
python3 scripts/garmin_query.py heart_rate "15:30" --date 2026-01-24

# Stress level at time
python3 scripts/garmin_query.py stress "10:30 AM"

# Body Battery at time
python3 scripts/garmin_query.py body_battery "noon"

# Steps at time
python3 scripts/garmin_query.py steps "17:00"
```

**Supported time formats:** `3:00 PM`, `15:30`, `2026-01-24 14:30`, etc.

## 📈 Extended Metrics (NEW in v1.1+)

Access 15+ additional health metrics:

```bash
# Training & Performance
python3 scripts/garmin_data_extended.py training_readiness
python3 scripts/garmin_data_extended.py training_status
python3 scripts/garmin_data_extended.py endurance_score
python3 scripts/garmin_data_extended.py hill_score
python3 scripts/garmin_data_extended.py max_metrics
python3 scripts/garmin_data_extended.py fitness_age

# Body Composition & Health
python3 scripts/garmin_data_extended.py body_composition
python3 scripts/garmin_data_extended.py weigh_ins --start 2026-01-01 --end 2026-01-25
python3 scripts/garmin_data_extended.py spo2
python3 scripts/garmin_data_extended.py respiration

# Activity Metrics
python3 scripts/garmin_data_extended.py steps
python3 scripts/garmin_data_extended.py floors
python3 scripts/garmin_data_extended.py intensity_minutes
python3 scripts/garmin_data_extended.py hydration
python3 scripts/garmin_data_extended.py stress_detailed
python3 scripts/garmin_data_extended.py hr_intraday
```

## 🗺️ Activity File Analysis (NEW in v1.1+)

Download and analyze FIT/GPX files for detailed activity insights:

```bash
# Download activity file (get activity ID from Garmin Connect URL)
python3 scripts/garmin_activity_files.py download --activity-id 12345678 --format fit

# Parse FIT file (GPS, elevation, HR, cadence, power)
python3 scripts/garmin_activity_files.py parse --file /tmp/activity_12345678.fit

# Query data at specific distance
python3 scripts/garmin_activity_files.py query --file /tmp/activity_12345678.fit --distance 1500

# Query data at specific time during activity
python3 scripts/garmin_activity_files.py query --file /tmp/activity_12345678.fit --time "2026-01-24T10:15:30"

# Get comprehensive activity statistics
python3 scripts/garmin_activity_files.py analyze --file /tmp/activity_12345678.fit
```

**Use cases:**
- "What was my elevation at mile 2?"
- "Show me my route on a map" (GPX files work with Leaflet.js, Google Maps)
- "What was my heart rate when climbing that hill?"
- "Analyze my pace per kilometer with elevation profile"

## Available Metrics

### Core Metrics

| Metric | Description | Data Source |
|--------|-------------|-------------|
| **Sleep** | Duration, stages (light/deep/REM), scores | Sleep tracking |
| **Body Battery** | Recovery metric (0-100) | HRV, stress, sleep, activity |
| **HRV** | Heart rate variability (ms) | Overnight measurement |
| **Heart Rate** | Resting, max, min (bpm) | 24/7 monitoring |
| **Activities** | Workouts, calories, duration | GPS + activity tracking |
| **Stress** | All-day stress levels (0-100) | HRV-based analysis |

### Extended Metrics (v1.1+)

| Metric | Description | Script |
|--------|-------------|--------|
| **Training Readiness** | Daily readiness score | `garmin_data_extended.py` |
| **Training Status** | Load, VO2 max trends | `garmin_data_extended.py` |
| **Body Composition** | Weight, body fat %, muscle, BMI | `garmin_data_extended.py` |
| **SPO2** | Blood oxygen saturation | `garmin_data_extended.py` |
| **Respiration** | Breathing rate throughout day | `garmin_data_extended.py` |
| **Steps (detailed)** | Time-series step data | `garmin_data_extended.py` |
| **Floors** | Floors climbed | `garmin_data_extended.py` |
| **Intensity Minutes** | Vigorous/moderate activity | `garmin_data_extended.py` |
| **Hydration** | Water intake tracking | `garmin_data_extended.py` |
| **Fitness Age** | Calculated fitness age | `garmin_data_extended.py` |
| **Endurance Score** | Endurance performance | `garmin_data_extended.py` |
| **Hill Score** | Hill running/climbing ability | `garmin_data_extended.py` |

### Activity File Data (FIT/GPX)

- GPS coordinates (latitude/longitude)
- Elevation/altitude profiles
- Heart rate during activity
- Cadence (steps/min or rpm)
- Power (watts, for cycling)
- Speed & pace
- Temperature
- Lap splits

## Project Structure

```
garmin-health-analysis/
├── SKILL.md                         # Main skill documentation
├── README.md                        # This file
├── CHANGELOG.md                     # Version history
├── scripts/
│   ├── garmin_auth.py              # Authentication (login, status)
│   ├── garmin_data.py              # Core data fetching (JSON output)
│   ├── garmin_data_extended.py     # Extended metrics (v1.1+)
│   ├── garmin_query.py             # Time-based queries (v1.1+)
│   ├── garmin_activity_files.py    # FIT/GPX file analysis (v1.1+)
│   └── garmin_chart.py             # Chart generation (HTML)
└── references/
    ├── api.md                      # Garmin Connect API documentation
    ├── health_analysis.md          # Health data interpretation guide
    └── extended_capabilities.md    # Extended features guide (v1.1+)
```

## Usage with Clawdbot

Once set up, you can ask your Clawdbot agent:

**General Health:**
- "How did I sleep last night?"
- "Show me my recovery for the last month"
- "What's my HRV trend looking like?"
- "Generate a health dashboard for the last 2 weeks"

**Time-Based Queries:**
- "What was my heart rate at 3pm yesterday?"
- "What was my stress level at noon today?"
- "When was my Body Battery fully charged?"

**Training & Performance:**
- "What's my training readiness today?"
- "How has my VO2 max changed this month?"
- "What's my fitness age?"
- "Show me my endurance score trend"

**Activity Analysis:**
- "What workouts did I do this week?"
- "Download my last run as a FIT file"
- "What was my elevation at mile 2 in yesterday's run?"
- "Analyze my pace profile for my last cycling workout"

The agent will use the scripts to fetch and analyze your data, providing insights based on the health analysis framework in `references/health_analysis.md` and `references/extended_capabilities.md`.

## Key Health Metrics Explained

### Body Battery (0-100)
Garmin's recovery metric based on HRV, stress, sleep, and activity:
- **75-100**: Fully charged, ready for high intensity
- **50-74**: Moderate energy, good for regular activity
- **25-49**: Limited energy, recovery needed
- **0-24**: Depleted, prioritize rest

### HRV (Heart Rate Variability)
Higher values indicate better recovery and resilience. Track trends over time rather than single values.

### Sleep Score (0-100)
Composite score based on:
- Duration
- Sleep stages (deep, REM, light)
- Movement/restlessness
- Heart rate stability
- Respiration quality

## Requirements

- **Python**: 3.7+
- **Libraries**: 
  - `garminconnect` - Garmin Connect API wrapper
  - `fitparse` - FIT file parsing (v1.1+)
  - `gpxpy` - GPX file parsing (v1.1+)
- **Garmin Device**: Any Garmin watch/tracker with Garmin Connect sync
- **Internet**: Required for fetching data from Garmin servers

## Privacy & Security

- Authentication tokens stored locally in `~/.clawdbot/garmin-tokens.json`
- No data sent anywhere except to Garmin's official servers
- Tokens use 0600 permissions (readable only by you)
- You can revoke access anytime by deleting the tokens file

## Troubleshooting

### "Not authenticated" error
Run the login command again:
```bash
python3 scripts/garmin_auth.py login --email YOUR_EMAIL --password YOUR_PASSWORD
```

### "No data" for certain metrics
- Some metrics require specific Garmin devices (e.g., Body Battery needs HRV-capable devices)
- Check that your device was worn during the requested period
- Ensure your device has synced with Garmin Connect

### Rate limit errors
Garmin limits API requests. If you hit rate limits:
- Wait 15-30 minutes
- Reduce the frequency of requests
- Cache data locally instead of re-fetching

## Comparison to Whoop Skill

| Feature | Garmin | Whoop |
|---------|--------|-------|
| **Recovery metric** | Body Battery (0-100) | Recovery Score (0-100%) |
| **API** | Unofficial (garminconnect) | Official OAuth |
| **Device types** | Watches, fitness trackers | Wearable band only |
| **Activities** | Full GPS tracking | Strain-focused |
| **Stress tracking** | Yes (all-day) | No direct metric |

## Credits

- Built for [Clawdbot](https://clawd.bot)
- Uses [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) library
- Charts powered by [Chart.js](https://www.chartjs.org/)
- Health analysis based on peer-reviewed research (see `references/health_analysis.md`)

## License

MIT

## Version

**Current**: 1.1.1 (2026-01-25)

**Latest changes:**
- ✨ Time-based queries for instant answers
- ✨ 15+ extended metrics (training, body composition, SPO2, etc.)
- ✨ Activity file analysis (FIT/GPX parsing)
- 🐛 Fixed sleep data extraction
- 📚 Comprehensive documentation

See [CHANGELOG.md](CHANGELOG.md) for full version history.
