import shutil
from langchain.tools import tool
import os

DOCUMENTS_DIR = "data/documents"

@tool
def attach_document(file_path: str) -> str:
    """Attach a document to the agent.

    Args:
        file_path (str): The path to the document to attach.

    Returns:
        str: A message indicating whether the document was attached successfully.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"

    try:
        shutil.copy(file_path, DOCUMENTS_DIR)
        return f"Document {os.path.basename(file_path)} attached successfully."
    except Exception as e:
        return f"Error attaching document: {e}"

@tool
def list_documents() -> list[str]:
    """List the attached documents.

    Returns:
        list[str]: A list of the attached documents.
    """
    return os.listdir(DOCUMENTS_DIR)

@tool
def read_document(file_name: str) -> str:
    """Read the content of an attached document.

    Args:
        file_name (str): The name of the document to read.

    Returns:
        str: The content of the document.
    """
    file_path = os.path.join(DOCUMENTS_DIR, file_name)
    if not os.path.exists(file_path):
        return f"Error: Document not found: {file_name}"

    with open(file_path, "r") as f:
        return f.read()

@tool
def delete_document(file_name: str) -> str:
    """Delete an attached document.

    Args:
        file_name (str): The name of the document to delete.

    Returns:
        str: A message indicating whether the document was deleted successfully.
    """
    file_path = os.path.join(DOCUMENTS_DIR, file_name)
    if not os.path.exists(file_path):
        return f"Error: Document not found: {file_name}"

    try:
        os.remove(file_path)
        return f"Document {file_name} deleted successfully."
    except Exception as e:
        return f"Error deleting document: {e}"