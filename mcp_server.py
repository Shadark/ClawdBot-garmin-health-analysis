#!/usr/bin/env python3
"""
Garmin Health Analysis MCP Server
Makes Garmin data accessible to Claude Desktop, Claude Code, and other MCP clients.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("MCP library not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

from garmin_auth import get_client
import garmin_data
import garmin_data_extended
import garmin_query
import garmin_activity_files

# Initialize MCP server
app = Server("garmin-health-analysis")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Garmin tools."""
    return [
        Tool(
            name="get_sleep_data",
            description="Get sleep data (duration, stages, scores) for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "number", "description": "Number of days (default: 7)"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                }
            }
        ),
        Tool(
            name="get_body_battery",
            description="Get Body Battery recovery metric (0-100) for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "number", "description": "Number of days (default: 7)"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                }
            }
        ),
        Tool(
            name="get_hrv_data",
            description="Get heart rate variability (HRV) data for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "number", "description": "Number of days (default: 7)"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                }
            }
        ),
        Tool(
            name="get_activities",
            description="Get activities/workouts (runs, rides, etc.) for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "number", "description": "Number of days (default: 7)"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                }
            }
        ),
        Tool(
            name="get_heart_rate",
            description="Get heart rate data (resting, max, min) for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "number", "description": "Number of days (default: 7)"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                }
            }
        ),
        Tool(
            name="get_health_summary",
            description="Get comprehensive health summary with all key metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "number", "description": "Number of days (default: 7)"}
                }
            }
        ),
        Tool(
            name="query_heart_rate_at_time",
            description="Get heart rate at a specific time (e.g., '3:00 PM', '15:30')",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {"type": "string", "description": "Time (e.g., '3:00 PM', '15:30')"},
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD), defaults to today"}
                },
                "required": ["time"]
            }
        ),
        Tool(
            name="query_stress_at_time",
            description="Get stress level at a specific time",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {"type": "string", "description": "Time (e.g., '10:30 AM')"},
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD), defaults to today"}
                },
                "required": ["time"]
            }
        ),
        Tool(
            name="query_body_battery_at_time",
            description="Get Body Battery level at a specific time",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {"type": "string", "description": "Time (e.g., 'noon', '12:00')"},
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD), defaults to today"}
                },
                "required": ["time"]
            }
        ),
        Tool(
            name="get_training_readiness",
            description="Get daily training readiness score",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD), defaults to today"}
                }
            }
        ),
        Tool(
            name="get_body_composition",
            description="Get body composition (weight, body fat %, muscle mass, BMI)",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD), defaults to today"}
                }
            }
        ),
        Tool(
            name="get_spo2",
            description="Get blood oxygen (SPO2) data",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD), defaults to today"}
                }
            }
        ),
        Tool(
            name="download_activity_file",
            description="Download FIT or GPX file for an activity (for detailed route/elevation analysis)",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_id": {"type": "number", "description": "Activity ID from Garmin Connect"},
                    "format": {"type": "string", "enum": ["fit", "gpx", "tcx"], "description": "File format (default: fit)"}
                },
                "required": ["activity_id"]
            }
        ),
        Tool(
            name="analyze_activity_file",
            description="Analyze a downloaded FIT/GPX file (get stats, max speed, elevation, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to FIT or GPX file"}
                },
                "required": ["file_path"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    client = get_client()
    if not client:
        return [TextContent(
            type="text",
            text=json.dumps({"error": "Not authenticated. Set GARMIN_EMAIL and GARMIN_PASSWORD environment variables."})
        )]
    
    try:
        if name == "get_sleep_data":
            result = garmin_data.fetch_sleep(
                client, 
                days=arguments.get("days", 7),
                start=arguments.get("start_date"),
                end=arguments.get("end_date")
            )
        
        elif name == "get_body_battery":
            result = garmin_data.fetch_body_battery(
                client,
                days=arguments.get("days", 7),
                start=arguments.get("start_date"),
                end=arguments.get("end_date")
            )
        
        elif name == "get_hrv_data":
            result = garmin_data.fetch_hrv(
                client,
                days=arguments.get("days", 7),
                start=arguments.get("start_date"),
                end=arguments.get("end_date")
            )
        
        elif name == "get_activities":
            result = garmin_data.fetch_activities(
                client,
                days=arguments.get("days", 7),
                start=arguments.get("start_date"),
                end=arguments.get("end_date")
            )
        
        elif name == "get_heart_rate":
            result = garmin_data.fetch_heart_rate(
                client,
                days=arguments.get("days", 7),
                start=arguments.get("start_date"),
                end=arguments.get("end_date")
            )
        
        elif name == "get_health_summary":
            result = garmin_data.fetch_summary(
                client,
                days=arguments.get("days", 7)
            )
        
        elif name == "query_heart_rate_at_time":
            result = garmin_query.query_heart_rate_at_time(
                client,
                arguments["time"],
                arguments.get("date")
            )
        
        elif name == "query_stress_at_time":
            result = garmin_query.query_stress_at_time(
                client,
                arguments["time"],
                arguments.get("date")
            )
        
        elif name == "query_body_battery_at_time":
            result = garmin_query.query_body_battery_at_time(
                client,
                arguments["time"],
                arguments.get("date")
            )
        
        elif name == "get_training_readiness":
            result = garmin_data_extended.fetch_training_readiness(
                client,
                arguments.get("date")
            )
        
        elif name == "get_body_composition":
            result = garmin_data_extended.fetch_body_composition(
                client,
                arguments.get("date")
            )
        
        elif name == "get_spo2":
            result = garmin_data_extended.fetch_spo2(
                client,
                arguments.get("date")
            )
        
        elif name == "download_activity_file":
            result = garmin_activity_files.download_activity_file(
                client,
                arguments["activity_id"],
                arguments.get("format", "fit")
            )
        
        elif name == "analyze_activity_file":
            file_path = arguments["file_path"]
            if file_path.endswith('.fit'):
                data = garmin_activity_files.parse_fit_file(file_path)
            elif file_path.endswith('.gpx'):
                data = garmin_activity_files.parse_gpx_file(file_path)
            else:
                data = {"error": "Unsupported file type"}
            
            if "error" not in data:
                result = garmin_activity_files.analyze_activity(data)
            else:
                result = data
        
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str)
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)})
        )]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
