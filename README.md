# Garmin Health Analysis

A Clawdbot skill for accessing and visualizing Garmin Connect health data.

## Features

- 📊 **Fetch health metrics**: Sleep, Body Battery, HRV, heart rate, activities, stress
- 📈 **Interactive charts**: Beautiful HTML dashboards with Chart.js
- 🧠 **Health analysis**: Science-backed interpretation of your data
- 💾 **Local authentication**: Secure token storage, no cloud dependencies

## Quick Start

### 1. Install Dependencies

```bash
pip3 install garminconnect
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

## Available Metrics

| Metric | Description | Data Source |
|--------|-------------|-------------|
| **Sleep** | Duration, stages (light/deep/REM), scores | Sleep tracking |
| **Body Battery** | Recovery metric (0-100) | HRV, stress, sleep, activity |
| **HRV** | Heart rate variability (ms) | Overnight measurement |
| **Heart Rate** | Resting, max, min (bpm) | 24/7 monitoring |
| **Activities** | Workouts, calories, duration | GPS + activity tracking |
| **Stress** | All-day stress levels (0-100) | HRV-based analysis |

## Project Structure

```
/projects/garmin/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── scripts/
│   ├── garmin_auth.py         # Authentication (login, status)
│   ├── garmin_data.py         # Data fetching (JSON output)
│   └── garmin_chart.py        # Chart generation (HTML)
└── references/
    ├── api.md                 # Garmin Connect API documentation
    └── health_analysis.md     # Health data interpretation guide
```

## Usage with Clawdbot

Once set up, you can ask your Clawdbot agent:

- "How did I sleep last night?"
- "Show me my recovery for the last month"
- "What's my HRV trend looking like?"
- "Generate a health dashboard for the last 2 weeks"
- "What workouts did I do this week?"

The agent will use the scripts to fetch and analyze your data, providing insights based on the health analysis framework in `references/health_analysis.md`.

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
- **Library**: `garminconnect` (installed via pip)
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

1.0.0 - Initial release (2026-01-25)
