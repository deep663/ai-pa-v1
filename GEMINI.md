# GEMINI.md

## Project Overview

This project is a command-line interface (CLI) based AI personal assistant named EVA. It utilizes the Langchain library to provide a conversational interface with long and short-term memory. The assistant is equipped with a variety of tools to interact with the local system, including file system operations, project management, reminders, and web search.

**Key Technologies:**

*   Python
*   Langchain
*   Langgraph
*   Pandas
*   OpenPyXL
*   python-dotenv

**Architecture:**

The application is structured around a central agent (`agent/agent.py`) that processes user input. The agent is configured with a set of tools and a system prompt to define its capabilities and personality. The `main.py` file serves as the entry point for the CLI application, creating a read-eval-print loop (REPL) for user interaction.

## Building and Running

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**
    ```bash
    python main.py
    ```

## Development Conventions

*   **Tool-based Architecture:** The agent's functionality is extended through a set of tools located in the `tools/` directory. Each tool is a Python function that performs a specific task.
*   **State Management:** The agent maintains a state using the `CustomAgentState` class, which includes user ID and preferences.
*   **Memory:** The agent uses a combination of in-memory and SQLite-based storage for long-term and short-term memory.
*   **System Prompt:** The `agent/system_prompt.py` file contains the system prompt that defines the agent's persona and instructions.
