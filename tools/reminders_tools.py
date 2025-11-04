# tools/reminders_tools.py
from langchain.tools import tool
import json
from pathlib import Path
from typing import Any, Dict

REMINDERS_FILE = Path("data/reminders.json")

def _load_reminders() -> Dict[str, Any]:
    """Load reminders from the JSON file."""
    if not REMINDERS_FILE.exists():
        return {}
    with open(REMINDERS_FILE, "r") as f:
        return json.load(f)

def _save_reminders(reminders: Dict[str, Any]):
    """Save reminders to the JSON file."""
    REMINDERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

@tool
def add_reminder(reminder_name: str, time: str, note: str = "") -> str:
    """
    Add a reminder for a given time.
    
    Args:
        reminder_name: Unique name for the reminder
        time: Time for the reminder (e.g., '2025-10-16 12:00')
        note: Optional note for the reminder
    """
    reminders = _load_reminders()
    reminders[reminder_name] = {"time": time, "note": note}
    _save_reminders(reminders)
    return f"Reminder '{reminder_name}' set for {time}."

@tool
def get_reminder(reminder_name: str) -> str:
    """Retrieve a reminder by its name."""
    reminders = _load_reminders()
    reminder = reminders.get(reminder_name)
    if reminder:
        return f"{reminder_name}: {reminder}"
    return "Reminder not found."

@tool
def delete_reminder(reminder_name: str) -> str:
    """Delete a reminder by its name."""
    reminders = _load_reminders()
    if reminder_name in reminders:
        del reminders[reminder_name]
        _save_reminders(reminders)
        return f"Reminder '{reminder_name}' deleted."
    return "Reminder not found."

@tool
def list_reminders() -> str:
    """List all active reminders."""
    reminders = _load_reminders()
    if not reminders:
        return "No reminders found."
    return json.dumps(reminders, indent=2)