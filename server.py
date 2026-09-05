import os
import sqlite3
from mcp.server.fastmcp import FastMCP

# Initialize the server container
mcp = FastMCP("VanshCalculator")

@mcp.tool()
def calculate_cgpa(marks_obtained: float, total_marks: float) -> str:
    """Calculates percentage and gives a quick grade breakdown."""
    percentage = (marks_obtained / total_marks) * 100
    return f"The percentage is {percentage:.2f}%. Great job!"

@mcp.tool()
def query_database(db_path: str, query_sql: str) -> str:
    """Executes a read-only SQL query on a local SQLite database and returns the results."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query_sql)
        rows = cursor.fetchall()
        conn.close()
        return str(rows)
    except Exception as e:
        return f"Error executing query: {str(e)}"

@mcp.tool()
def find_sqlite_files(search_directory: str = "D:/") -> str:
    """Scans a directory for SQLite database files and returns their paths."""
    found_files = []
    try:
        for root, dirs, files in os.walk(search_directory):
            for file in files:
                if file.endswith(('.db', '.sqlite', '.sqlite3')):
                    found_files.append(os.path.join(root, file))
        if not found_files:
            return "No SQLite files found in the specified directory."
        return str(found_files)
    except Exception as e:
        return f"Error scanning directory: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")