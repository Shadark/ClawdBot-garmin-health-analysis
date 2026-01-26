# Claude Desktop / Code Installation

Use this Garmin Health Analysis skill with **Claude Desktop**, **Claude Code**, or any MCP-compatible client.

## Quick Start

### 1. Install Dependencies

```bash
pip install mcp garminconnect fitparse gpxpy
```

### 2. Configure Claude Desktop

Edit your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the Garmin MCP server:

```json
{
  "mcpServers": {
    "garmin": {
      "command": "python",
      "args": [
        "/path/to/garmin-health-analysis/mcp_server.py"
      ],
      "env": {
        "GARMIN_EMAIL": "your-email@example.com",
        "GARMIN_PASSWORD": "your-password"
      }
    }
  }
}
```

**Replace:**
- `/path/to/garmin-health-analysis/` with the actual path to this skill folder
- `your-email@example.com` with your Garmin Connect email
- `your-password` with your Garmin Connect password

### 3. Restart Claude Desktop

Quit and restart Claude Desktop completely.

### 4. Verify Installation

In Claude Desktop, you should see the Garmin tools available. Try asking:
- "How did I sleep last night?"
- "What was my heart rate at 3pm?"
- "Show me my activities this week"
- "What was my fastest speed snowboarding?"

## Available Tools

The MCP server exposes these tools to Claude:

### Health Metrics
- `get_sleep_data` - Sleep duration, stages (deep/light/REM), scores
- `get_body_battery` - Recovery metric (0-100)
- `get_hrv_data` - Heart rate variability
- `get_activities` - Workouts and activities
- `get_heart_rate` - Resting, max, min heart rate
- `get_health_summary` - Comprehensive health summary

### Time-Based Queries
- `query_heart_rate_at_time` - "What was my HR at 3pm?"
- `query_stress_at_time` - "What was my stress at noon?"
- `query_body_battery_at_time` - "What was my Body Battery at 10am?"

### Extended Metrics
- `get_training_readiness` - Daily readiness score
- `get_body_composition` - Weight, body fat %, muscle mass
- `get_spo2` - Blood oxygen saturation

### Activity File Analysis
- `download_activity_file` - Download FIT/GPX files
- `analyze_activity_file` - Get detailed stats from activity files

## Example Conversations

**Sleep Analysis:**
```
You: How did I sleep last night?
Claude: [calls get_sleep_data] You slept 7.5 hours with a sleep score of 82/100...
```

**Time Queries:**
```
You: What was my heart rate at 3pm yesterday?
Claude: [calls query_heart_rate_at_time] Your heart rate at 3pm was 95 bpm...
```

**Activity Analysis:**
```
You: What was my fastest speed snowboarding last week?
Claude: [calls get_activities] Looking at your snowboarding sessions, your fastest speed was 60.8 km/h (37.8 mph) on Dec 28...
```

**Recovery Tracking:**
```
You: Am I ready to train today?
Claude: [calls get_training_readiness, get_body_battery, get_hrv_data] Based on your training readiness score of 85, Body Battery at 92, and HRV of 45ms, you're well-recovered...
```

## Troubleshooting

### "MCP server not found"
- Check the path in `claude_desktop_config.json` is correct
- Make sure Python is in your PATH
- Try using absolute paths (e.g., `/usr/bin/python3` or `C:\Python39\python.exe`)

### "Not authenticated"
- Verify your GARMIN_EMAIL and GARMIN_PASSWORD are correct in the config
- Check you can login at https://connect.garmin.com

### "No data returned"
- Ensure your Garmin device has synced recently
- Check you're wearing a compatible device (Body Battery requires HRV-capable devices)
- Try a different date range

### Testing the MCP Server

Run the server directly to test:

```bash
# Set credentials
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"

# Test the server
python mcp_server.py
```

You should see JSON-RPC messages if it's working.

## Privacy & Security

**Authentication:**
- Credentials are only stored in your local Claude Desktop config
- Session tokens are cached in `~/.clawdbot/garmin-tokens.json` (or `~/.garmin-tokens.json`)
- Tokens use 0600 permissions (only you can read them)

**Data:**
- No data is sent anywhere except to Garmin's official servers
- All processing happens locally on your machine
- Claude can access the data through the MCP protocol

**Revoking Access:**
- Remove the Garmin entry from `claude_desktop_config.json`
- Delete token files: `~/.clawdbot/garmin-tokens.json` or `~/.garmin-tokens.json`
- Restart Claude Desktop

## Claude Code (VS Code Extension)

The same MCP server works with Claude Code! Add to your VS Code settings:

1. Open VS Code settings (JSON)
2. Add to `claude.mcpServers`:

```json
{
  "claude.mcpServers": {
    "garmin": {
      "command": "python",
      "args": ["/path/to/garmin-health-analysis/mcp_server.py"],
      "env": {
        "GARMIN_EMAIL": "your-email@example.com",
        "GARMIN_PASSWORD": "your-password"
      }
    }
  }
}
```

## Other MCP Clients

This server works with any MCP-compatible client. Just point the client to:

```bash
python /path/to/garmin-health-analysis/mcp_server.py
```

With environment variables:
- `GARMIN_EMAIL`
- `GARMIN_PASSWORD`

## Learn More

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop Guide](https://claude.ai/download)
- [Garmin Connect](https://connect.garmin.com)
- [GitHub Repository](https://github.com/eversonl/ClawdBot-garmin-health-analysis)
