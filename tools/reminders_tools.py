from langchain.tools import tool
from langgraph.runtime import get_runtime
from typing import Any

# Add reminder
@tool
def add_reminder(reminder_name: str, time: str, note: str = "") -> str:
    """
    Add a reminder for a given time.
    
    Args:
        reminder_name: Unique name for the reminder
        time: Time for the reminder (e.g., '2025-10-16 12:00')
        note: Optional note for the reminder
    """
    store = get_runtime().store
    store.put(("reminders",), reminder_name, {"time": time, "note": note})
    return f"Reminder '{reminder_name}' set for {time}."

# Get reminder
@tool
def get_reminder(reminder_name: str) -> str:
    """Retrieve a reminder by its name."""
    store = get_runtime().store
    reminder = store.get(("reminders",), reminder_name)
    return f"{reminder_name}: {reminder.value}" if reminder else "Reminder not found."

# Delete reminder
@tool
def delete_reminder(reminder_name: str) -> str:
    """Delete a reminder by its name."""
    store = get_runtime().store
    store.delete(("reminders",), reminder_name)
    return f"Reminder '{reminder_name}' deleted."
