# tools/project_tools.py
from langchain.tools import tool
from pathlib import Path
import pandas as pd
import os
from typing import Optional

DEFAULT_PATH = os.getenv("PROJECT_DATA_PATH", "./data/projects.xlsx")

def _ensure_projects_file(path: str = DEFAULT_PATH):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        df = pd.DataFrame(columns=["id", "title", "description", "status", "deadline", "owner"])
        df.to_excel(p, index=False)

@tool
def create_project(title: str, description: str = "", status: str = "todo", deadline: str = "", owner: str = "", file_path: Optional[str] = None) -> str:
    """Create a new project row in projects Excel file. Returns assigned id."""
    path = file_path or DEFAULT_PATH
    _ensure_projects_file(path)
    p = Path(path)
    df = pd.read_excel(p)
    next_id = 1 if df.empty else int(df["id"].max()) + 1
    row = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": status,
        "deadline": deadline,
        "owner": owner
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(p, index=False)
    return f"Created project id={next_id} title='{title}' in {p.resolve()}"

@tool
def list_projects(file_path: Optional[str] = None, status: Optional[str] = None) -> str:
    """List projects (optionally filter by status), returns markdown table."""
    path = file_path or DEFAULT_PATH
    p = Path(path)
    if not p.exists():
        return f"No projects file found at {p.resolve()}"
    df = pd.read_excel(p)
    if status:
        df = df[df["status"].astype(str).str.lower() == status.lower()]
    if df.empty:
        return "No projects found"
    return df.to_markdown(index=False)

@tool
def update_project_status(project_id: int, new_status: str, file_path: Optional[str] = None) -> str:
    """Update project status by id."""
    path = file_path or DEFAULT_PATH
    p = Path(path)
    if not p.exists():
        return f"No projects file found at {p.resolve()}"
    df = pd.read_excel(p)
    mask = df["id"] == project_id
    if not mask.any():
        return f"Project id {project_id} not found"
    df.loc[mask, "status"] = new_status
    df.to_excel(p, index=False)
    return f"Updated project id {project_id} status -> {new_status}"

@tool
def delete_project(project_id: int, file_path: Optional[str] = None) -> str:
    """Delete project by id."""
    path = file_path or DEFAULT_PATH
    p = Path(path)
    if not p.exists():
        return f"No projects file found at {p.resolve()}"
    df = pd.read_excel(p)
    if project_id not in df["id"].values:
        return f"Project id {project_id} not found"
    removed = df[df["id"] == project_id].to_dict(orient="records")
    df = df[df["id"] != project_id].reset_index(drop=True)
    df.to_excel(p, index=False)
    return f"Deleted project id {project_id}. Removed row: {removed}"
