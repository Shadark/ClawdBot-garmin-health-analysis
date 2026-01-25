# Changelog

## v1.0.1 (2026-01-25)

### Bug Fixes
- Fixed sleep data extraction - properly parse nested `dailySleepDTO` object from Garmin API
- Sleep time and scores now display correctly in all charts and dashboards

## v1.0.0 (2026-01-25)

### Initial Release

**Features:**
- Fetch health data from Garmin Connect (sleep, Body Battery, HRV, heart rate, activities, stress)
- Generate interactive HTML charts with Chart.js
- Science-backed health analysis framework
- Support for multiple credential configuration methods
- Automatic token refresh

**Data Available:**
- Sleep: duration, stages (deep/light/REM), scores, HRV during sleep
- Body Battery: Garmin's recovery metric (0-100)
- HRV: nightly heart rate variability with baseline tracking
- Heart Rate: resting, max, min throughout the day
- Activities: workouts with calories, duration, heart rate, GPS data
- Stress: all-day stress levels based on HRV analysis

**Charts:**
- Sleep analysis (hours + scores)
- Body Battery recovery (color-coded by level)
- HRV & Resting Heart Rate trends
- Activities summary (by type with calories)
- Full dashboard combining all metrics

**Configuration:**
- UI-configurable via Clawdbot config (`skills.entries.garmin-health-analysis.env`)
- Local config.json support
- Command-line arguments
- Environment variables

**Requirements:**
- Python 3.7+
- garminconnect library (installed via pip)
- Garmin Connect account with wearable device

**Security:**
- Session tokens stored locally in `~/.clawdbot/garmin/`
- Tokens auto-refresh
- No data sent anywhere except Garmin's official servers
