import os
import shutil
from langchain.tools import tool

@tool
def create_directory(directory_path: str) -> str:
    """Create a new directory at the specified path."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return f"Directory created: {directory_path}"
    except Exception as e:
        return f"Error creating directory: {e}"

from rich.console import Console
from rich.prompt import Confirm

@tool
def delete_directory(directory_path: str) -> str:
    """Delete a directory at the specified path."""
    console = Console()
    if not Confirm.ask(f"Are you sure you want to delete the directory '{directory_path}'?"):
        return "Operation cancelled."
    try:
        shutil.rmtree(directory_path)
        return f"Directory deleted: {directory_path}"
    except Exception as e:
        return f"Error deleting directory: {e}"

@tool
def move_directory(source_path: str, destination_path: str) -> str:
    """Move or rename a directory."""
    console = Console()
    if not Confirm.ask(f"Are you sure you want to move the directory '{source_path}' to '{destination_path}'?"):
        return "Operation cancelled."
    try:
        shutil.move(source_path, destination_path)
        return f"Directory moved to: {destination_path}"
    except Exception as e:
        return f"Error moving directory: {e}"

@tool
def find_files_by_name(file_name: str, search_path: str = '.') -> list:
    """Find files by name in a specified directory."""
    result = []
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            result.append(os.path.join(root, file_name))
    return result

@tool
def read_directory(directory_path: str) -> str:
    """Read the content of a directory at the specified path."""
    try:
        if not os.path.isdir(directory_path):
            return f"Error: Path is not a directory: {directory_path}"
        
        items = os.listdir(directory_path)
        
        if not items:
            return f"The directory is empty: {directory_path}"
        
        return f"Directory content:\n" + "\n".join(items)
    except Exception as e:
        return f"Error reading directory: {e}"
