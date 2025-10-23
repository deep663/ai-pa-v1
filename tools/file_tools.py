# tools/file_reader_tool.py
from langchain.tools import tool
from pathlib import Path
import os

@tool
def list_files(directory: str = ".") -> str:
    """List files in directory."""
    p = Path(directory)
    if not p.exists() or not p.is_dir():
        return f"Directory not found: {p.resolve()}"
    files = [str(x.name) for x in sorted(p.iterdir())]
    return "\n".join(files)

@tool
def read_any_file(file_path: str, max_chars: int = 5000) -> str:
    """
    Read and return the content of any file from any location.
    
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

        # Try different encodings
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
