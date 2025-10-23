# EVA - AI personal Assistant

## Description

This project is an interactive web application that provides an AI personal assistant with long/short memory and various tools. The assistant is powered by the Langchain library and can perform tasks such as creating and managing projects, adding and deleting reminders, reading and writing files, and more.

## Installation

1. Clone the repository: `git clone https://github.com/your-username/your-repo.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Set up the environment variables:
   - `PROJECT_DATA_PATH`: Path to the directory where the project data will be stored (default: `./data/projects.xlsx`)
   - `DEFAULT_EXCEL_PATH`: Path to the default Excel file (default: `./data/projects.xlsx`)
   - `DEFAULT_PDF_PATH`: Path to the default PDF file (default: `./data/sample.pdf`)
   - `DEFAULT_FILE_PATH`: Path to the default file (default: `./data/sample.txt`)
   - `DEFAULT_WEB_SEARCH_ENGINE`: The search engine to use for web searches (default: `DuckDuckGoSearchResults`)
4. Start the server: `python server.py`

## Usage

1. Open the application in your web browser: `http://localhost:5000`
2. Use the web interface to interact with the assistant.
3. Type your query in the input field and press Enter to get a response from the assistant.

## Features

- AI personal assistant with long/short memory
- Create and manage projects
- Add and delete reminders
- Read and write files
- Perform web searches
- Read PDF files

## Technologies Used

- Flask
- HTML/CSS/JavaScript
- Langchain
- PyYAML
- SQLAlchemy
- Pandas
- OpenPyXL
- Requests
- PyPDF2

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

