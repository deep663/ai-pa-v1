# tools/excel_tools.py
from langchain.tools import tool
import pandas as pd
from pathlib import Path
from typing import Any

@tool
def create_excel(file_path: str) -> str:
    """Create a new Excel workbook (empty)."""
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame()
    df.to_excel(p, index=False)
    return f"Created new Excel file at {p.resolve()}"

@tool
def add_row(file_path: str, data: dict) -> str:
    """Append a row (given as a dict) to sheet. Create file if missing."""
    p = Path(file_path)
    if not isinstance(data, dict):
        return "Error: 'data' must be a dictionary with column-value pairs."
    
    if not p.exists():
        df = pd.DataFrame([data])
    else:
        df = pd.read_excel(p)
        # Ensure all keys exist as columns
        for key in data.keys():
            if key not in df.columns:
                df[key] = None
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    
    df.to_excel(p, index=False)
    return f"Added row to {p.resolve()}: {data}"

@tool
def read_excel(file_path: str, n: int = 10) -> str:
    """Return first n rows in markdown-format (string)"""
    p = Path(file_path)
    if not p.exists():
        return f"File not found: {p.resolve()}"
    df = pd.read_excel(p)
    if df.empty:
        return f"File {p.resolve()} is empty"
    # show first n rows
    return df.head(n).to_markdown(index=False)

@tool
def update_cell(file_path: str, row_index: int, column: str, value: Any) -> str:
    """Update a particular cell by row index (0-based) and column name."""
    p = Path(file_path)
    if not p.exists():
        return f"File not found: {p.resolve()}"
    df = pd.read_excel(p)
    if column not in df.columns:
        return f"Column '{column}' not found in {p.resolve()}"
    if row_index < 0 or row_index >= len(df):
        return f"Row index {row_index} out of bounds (0..{len(df)-1})"
    df.at[row_index, column] = value
    df.to_excel(p, index=False)
    return f"Updated {p.resolve()} row {row_index} column {column} -> {value}"

@tool
def delete_row(file_path: str, row_index: int) -> str:
    """Delete a particular row by row index (0-based)."""
    p = Path(file_path)
    if not p.exists():
        return f"File not found: {p.resolve()}"
    df = pd.read_excel(p)
    if row_index < 0 or row_index >= len(df):
        return f"Row index {row_index} out of bounds (0..{len(df)-1})"
    removed = df.iloc[row_index].to_dict()
    df = df.drop(df.index[row_index]).reset_index(drop=True)
    df.to_excel(p, index=False)
    return f"Deleted row {row_index} from {p.resolve()}. Removed data: {removed}"
