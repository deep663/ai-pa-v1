# tools/file_tools.py
from langchain.tools import tool
from pathlib import Path
import os
import PyPDF2

@tool
def list_files(directory: str = ".") -> str:
    """List files in a directory."""
    p = Path(directory)
    if not p.exists() or not p.is_dir():
        return f"Directory not found: {p.resolve()}"
    files = [str(x.name) for x in sorted(p.iterdir())]
    return "\n".join(files)

@tool
def read_any_file(file_path: str, max_chars: int = 5000) -> str:
    """
    Read and return the content of any file from any location.
    Handles text files and PDFs.
    
    Args:
        file_path: The absolute or relative path to the file.
        max_chars: Optional limit on number of characters to return (default 5000).
    
    Returns:
        File content as string or a message if file is too large or not readable.
    """
    try:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            return f"File not found: {path}"
        if path.is_dir():
            return f"'{path}' is a directory, not a file."

        if path.suffix.lower() == '.pdf':
            try:
                with open(path, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text_output = ""
                    for page in pdf_reader.pages:
                        text_output += page.extract_text() + "\n"
                    
                    if len(text_output) > max_chars:
                        return f"(Preview of first {max_chars} chars)\n\n{text_output[:max_chars]}\n\n... [truncated]"
                    return text_output
            except Exception as e:
                return f"Error reading PDF file '{file_path}': {str(e)}"

        # Try different encodings for text files
        encodings = ["utf-8", "utf-16", "latin-1"]
        content = None
        for enc in encodings:
            try:
                with open(path, "r", encoding=enc, errors="ignore") as f:
                    content = f.read()
                break
            except Exception:
                continue

        if content is None:
            return f"Unable to read file: {path}"

        # Limit large files
        if len(content) > max_chars:
            preview = content[:max_chars]
            return f"(Preview of first {max_chars} chars)\n\n{preview}\n\n... [truncated]"
        
        return content

    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

@tool
def find_files(start_path: str = ".", name_pattern: str = "*") -> str:
    """
    Find files recursively in a directory that match a name pattern.
    
    Args:
        start_path: The directory to start the search from.
        name_pattern: A glob pattern to match filenames (e.g., '*.py', 'data_*.csv').
        
    Returns:
        A list of matching file paths.
    """
    try:
        path = Path(start_path).expanduser().resolve()
        if not path.is_dir():
            return f"Invalid directory: {path}"
        
        files = [str(p) for p in path.rglob(name_pattern)]
        return "\n".join(files)
    except Exception as e:
        return f"Error finding files: {str(e)}"

from rich.console import Console
from rich.prompt import Confirm

@tool
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        file_path: The absolute or relative path to the file.
        content: The content to write to the file.
        
    Returns:
        A confirmation message.
    """
    console = Console()
    path = Path(file_path).expanduser().resolve()
    if path.exists():
        if not Confirm.ask(f"Are you sure you want to overwrite the file '{file_path}'?"):
            return "Operation cancelled."
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File written successfully to {path}"
    except Exception as e:
        return f"Error writing file '{file_path}': {str(e)}"