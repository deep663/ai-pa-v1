# EVA - A Command-Line AI Personal Assistant

## Description

This project is a command-line interface (CLI) based AI personal assistant named EVA. It utilizes the Langchain library to provide a conversational interface with long and short-term memory. The assistant is equipped with a variety of tools to interact with the local system, including file system operations, project management, reminders, and web search.

## Installation

1. Clone the repository: `git clone https://github.com/your-username/your-repo.git`
2. Install the dependencies: `pip install -r requirements.txt`

## Usage

The CLI has two modes of operation:

*   **Interactive Chat:** To start an interactive chat session, run:
    ```bash
    python main.py chat
    ```
*   **Direct Command:** To send a single message to the agent, run:
    ```bash
    python main.py chat "your message here"
    ```

## Features

- AI personal assistant with long/short memory
- Create and manage projects
- Add and delete reminders
- Read and write files
- Perform advanced web searches with content summarization
- Find job listings from Google Jobs
- Search and play YouTube videos
- Open applications on your system
- Read PDF files

## Technologies Used

- Python
- Langchain
- Langgraph
- Pandas
- OpenPyXL
- python-dotenv
- click
- rich
- pywhatkit

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.
