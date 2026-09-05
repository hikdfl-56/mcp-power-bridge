# MCP Power Bridge

A centralized, persistent Model Context Protocol (MCP) server designed to bridge local system automation, background daemon monitoring, and SQLite database interactions directly with AI clients like Antigravity.

## Features

* **Persistent Background Daemon:** Runs an independent background thread (`background_file_automation`) that continuously polls a designated folder every 5 seconds to track state changes and log newly created files in-memory.
* **Direct SQLite Integration:** Exposes a robust `query_database` tool that lets your AI client securely run custom SQL queries against local database files (`api_records.db`) with real-time feedback.
* **Structured State Reporting:** Features the `get_automation_status` tool to provide immediate visibility into daemon health, last-checked timestamps, and session-specific file detection logs.

## Project Structure

```text
D:\my-first-mcp-server\
│
├── server.py              # Main MCP server containing daemon threads and tools
├── api_records.db         # Local SQLite database for query operations
└── watched_folder\        # Target directory monitored by the background file daemon

## Setup & Installation

1. Ensure Python 3.10+ is installed on your system.
2. Install the required dependencies (pinned to stable compatibility versions):
   ```bash
   pip install "mcp<2"
3. Run the server locally
   python server.py
