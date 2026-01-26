# MCP Server Setup for Standard Claude Desktop

This guide covers setting up the Garmin Health Analysis as an **MCP server** for use with standard Claude Desktop (not Clawdbot).

> **Note**: If you're using Clawdbot, you don't need this - follow the main SKILL.md instead.

## What's the difference?

- **Clawdbot Skill** (SKILL.md): Uses Python scripts directly, runs in Clawdbot sessions
- **MCP Server** (this guide): Runs as a background server, connects to Claude Desktop

## Prerequisites

- Claude Desktop installed
- Node.js 18+ and npm
- Python 3.8+
- Git

## Installation

### 1. Clone the MCP Server Repository

```bash
# Clone to a directory of your choice
cd ~/Projects  # or wherever you keep code
git clone https://github.com/eversonl/garmin-health-mcp-server.git
cd garmin-health-mcp-server
```

### 2. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip3 install garminconnect fitparse gpxpy
# Or on managed systems:
pip3 install --user garminconnect fitparse gpxpy
```

### 3. Configure Credentials

Create a `.env` file in the repo directory:

```bash
cp .env.example .env
# Edit .env and add your credentials
```

**.env:**
```env
GARMIN_EMAIL=your-email@example.com
GARMIN_PASSWORD=your-password
```

### 4. Authenticate with Garmin

```bash
npm run auth
```

This will log in to Garmin Connect and save session tokens.

### 5. Configure Claude Desktop

Edit your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the MCP server:

```json
{
  "mcpServers": {
    "garmin-health": {
      "command": "node",
      "args": ["/absolute/path/to/garmin-health-mcp-server/index.js"],
      "env": {
        "GARMIN_EMAIL": "your-email@example.com",
        "GARMIN_PASSWORD": "your-password"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/garmin-health-mcp-server/` with the actual path where you cloned the repo.

### 6. Restart Claude Desktop

Completely quit and restart Claude Desktop. The MCP server should now be available.

## Verify Installation

In Claude Desktop, you should see the Garmin tools available. Try asking:

> "What are my Garmin tools?"

Or:

> "How did I sleep last night?"

## Available Tools

The MCP server exposes these tools to Claude:

- `get_sleep_data` - Sleep hours, stages, scores
- `get_body_battery` - Recovery metric (0-100)
- `get_hrv_data` - Heart rate variability trends
- `get_heart_rate` - Resting, max, min heart rate
- `get_activities` - Workouts and exercise data
- `get_stress_levels` - All-day stress tracking
- `get_summary` - Combined health overview
- `get_user_profile` - Account and device info
- `generate_chart` - Create interactive HTML visualizations

## Troubleshooting

### "MCP server not found"
- Check the path in `claude_desktop_config.json` is absolute (starts with `/` or `C:\`)
- Verify the `index.js` file exists at that path
- Make sure you ran `npm install` in the repo directory

### "Authentication failed"
- Run `npm run auth` in the repo directory to refresh tokens
- Check your email/password in the `.env` file
- Try logging into Garmin Connect website to verify credentials

### "Tools not appearing"
- Completely quit Claude Desktop (not just close the window)
- Check Console (macOS) or Event Viewer (Windows) for MCP errors
- Verify Node.js is accessible: `node --version`

### "Missing Python dependencies"
- Run `pip3 install garminconnect fitparse gpxpy` again
- On some systems you need `pip3 install --user ...`
- Or use a virtual environment (see Python docs)

## Using Both: Clawdbot Skill + MCP Server

You can use both setups simultaneously:

- **Clawdbot**: Great for automation, scheduling, proactive health check-ins
- **Standard Claude**: Great for ad-hoc queries in the desktop app

They share the same authentication tokens (stored in `~/.clawdbot/garmin-tokens.json` or `~/.garmin-tokens.json`).

## Repository Structure

The MCP server repo should have:

```
garmin-health-mcp-server/
├── index.js              # MCP server entry point
├── package.json          # Node.js dependencies
├── src/
│   ├── garmin.js        # Garmin Connect API wrapper
│   ├── tools.js         # MCP tool definitions
│   └── auth.js          # Authentication logic
├── scripts/
│   └── auth.js          # CLI auth helper
├── .env.example         # Template for credentials
└── README.md            # Server-specific docs
```

## Security Note

- Never commit `.env` or credential files to git
- Session tokens are stored locally and auto-refresh
- The MCP server only communicates with Garmin's official API
- Claude Desktop runs the server locally (no cloud access)

## Updates

To update the MCP server:

```bash
cd ~/Projects/garmin-health-mcp-server
git pull
npm install
```

Then restart Claude Desktop.

---

**Need help?** File an issue on the [GitHub repo](https://github.com/eversonl/garmin-health-mcp-server).
