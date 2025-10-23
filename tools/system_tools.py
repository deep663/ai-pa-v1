# tools/system_tools.py
from datetime import datetime
from langchain.tools import tool
from pathlib import Path
import shutil
import os
import requests

@tool
def check_internet(url: str = "https://www.google.com") -> str:
    """
    Check if internet is available by pinging a website.
    
    Args:
        url: Website to check connectivity
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return "Internet is available."
        else:
            return f"Internet might be slow or restricted. Status code: {response.status_code}"
    except requests.ConnectionError:
        return "No internet connection."


@tool
def make_backup(file_path: str) -> str:
    """Make a backup of a file."""
    p = Path(file_path)
    if not p.exists():
        return f"File not found: {p.resolve()}"
    backup = p.with_suffix(p.suffix + ".bak")
    shutil.copy(p, backup)
    return f"Backup created at {backup.resolve()}"


@tool
def get_current_time() -> str:
    """Get the current time ."""
    now = datetime.now()
    return now.strftime("%H:%M:%S")

@tool
def get_today() -> str:
    """Get today's date"""
    today = datetime.today()
    return today.strftime("%Y-%m-%d")
