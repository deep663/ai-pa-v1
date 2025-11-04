import subprocess
import psutil
from langchain.tools import tool

@tool
def run_shell_command(command: str) -> str:
    """Run a shell command. 
    
    DANGER: This tool can be dangerous. Only run commands that you trust.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error running command: {e}"

@tool
def get_system_info() -> dict:
    """Get system information (CPU, memory)."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        return {
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": memory_info.percent,
            "available_memory_gb": round(memory_info.available / (1024**3), 2),
            "total_memory_gb": round(memory_info.total / (1024**3), 2),
        }
    except Exception as e:
        return {"error": str(e)}

@tool("open_application", description="Opens an application on the user's system.")
def open_application(application_name: str) -> str:
    """
    Opens an application on the user's system using the 'start' command.

    Args:
        application_name: The name of the application to open (e.g., 'notepad', 'calc', 'chrome').
    """
    try:
        # Use the 'start' command to open the application
        # This is a safe way to open applications on Windows
        # as it uses the default application for the file type or the application in the PATH
        result = subprocess.run(f"start {application_name}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Successfully started '{application_name}'."
        else:
            return f"Error starting '{application_name}': {result.stderr}"
    except Exception as e:
        return f"An error occurred while trying to open the application: {e}"