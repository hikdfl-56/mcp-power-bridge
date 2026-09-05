import time
import threading
import sqlite3
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("mcp-power-bridge")

# Define paths
BASE_DIR = Path(r"D:\my-first-mcp-server")
WATCH_DIR = BASE_DIR / "watched_folder"
WATCH_DIR.mkdir(exist_ok=True)
DB_PATH = BASE_DIR / "api_records.db"

# Shared in-memory state for the background daemon
daemon_state = {
    "status": "STOPPED",
    "last_checked": None,
    "detected_files": []
}

def background_file_automation():
    """Persistent background daemon that watches a folder and tracks new files in memory."""
    global daemon_state
    daemon_state["status"] = "ACTIVE"
    print(f"[*] Persistent Daemon Started: Monitoring {WATCH_DIR}")
    
    try:
        known_files = set(p.name for p in WATCH_DIR.iterdir() if p.is_file())
    except Exception:
        known_files = set()
    
    while True:
        try:
            current_files = set(p.name for p in WATCH_DIR.iterdir() if p.is_file())
            new_files = current_files - known_files
            
            if new_files:
                for filename in new_files:
                    print(f"[AUTOMATION ALERT] New file found: {filename}")
                    daemon_state["detected_files"].append(filename)
            
            known_files = current_files
            daemon_state["last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(5)  # Polling interval
        except Exception as e:
            daemon_state["status"] = f"ERROR: {str(e)}"
            time.sleep(5)

# Start the background automation thread automatically when the server boots
automation_thread = threading.Thread(target=background_file_automation, daemon=True)
automation_thread.start()

@mcp.tool()
def get_automation_status() -> str:
    """Retrieves live state and activity logs from the persistent background automation daemon."""
    return (
        f"Daemon Status: {daemon_state['status']}\n"
        f"Watched Directory: {WATCH_DIR}\n"
        f"Last Checked: {daemon_state['last_checked']}\n"
        f"Files Detected This Session: {daemon_state['detected_files']}"
    )

@mcp.tool()
def query_database(query: str) -> str:
    """Executes a custom SQL query against the local SQLite database and returns results."""
    try:
        if not DB_PATH.exists():
            return f"Error: Database file not found at {DB_PATH}"
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            conn.close()
            return f"Headers: {headers}\nRows: {rows}"
        else:
            conn.commit()
            changes = conn.total_changes
            conn.close()
            return f"Query executed successfully. Total changes: {changes}"
    except Exception as e:
        return f"Database Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()