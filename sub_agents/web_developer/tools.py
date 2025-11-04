from langchain.tools import tool
import os

@tool
def create_html_file(file_name: str, content: str) -> str:
    """Creates an HTML file with the given name and content.

    Args:
        file_name (str): The name of the HTML file to create.
        content (str): The content to write to the HTML file.

    Returns:
        str: A message indicating whether the file was created successfully.
    """
    try:
        with open(file_name, "w") as f:
            f.write(content)
        return f"HTML file {file_name} created successfully."
    except Exception as e:
        return f"Error creating HTML file: {e}"

@tool
def create_css_file(file_name: str, content: str) -> str:
    """Creates a CSS file with the given name and content.

    Args:
        file_name (str): The name of the CSS file to create.
        content (str): The content to write to the CSS file.

    Returns:
        str: A message indicating whether the file was created successfully.
    """
    try:
        with open(file_name, "w") as f:
            f.write(content)
        return f"CSS file {file_name} created successfully."
    except Exception as e:
        return f"Error creating CSS file: {e}"

@tool
def create_js_file(file_name: str, content: str) -> str:
    """Creates a JavaScript file with the given name and content.

    Args:
        file_name (str): The name of the JavaScript file to create.
        content (str): The content to write to the JavaScript file.

    Returns:
        str: A message indicating whether the file was created successfully.
    """
    try:
        with open(file_name, "w") as f:
            f.write(content)
        return f"JavaScript file {file_name} created successfully."
    except Exception as e:
        return f"Error creating JavaScript file: {e}"

@tool
def append_to_file(file_name: str, content: str) -> str:
    """Appends content to a file.

    Args:
        file_name (str): The name of the file to append to.
        content (str): The content to append to the file.

    Returns:
        str: A message indicating whether the content was appended successfully.
    """
    try:
        with open(file_name, "a") as f:
            f.write(content)
        return f"Content appended to {file_name} successfully."
    except Exception as e:
        return f"Error appending to file: {e}"