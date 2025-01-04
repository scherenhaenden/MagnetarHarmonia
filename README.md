Here’s a well-structured README for your program:

---

# Git-to-LM Studio Commit Message Generator

This program automates the generation of commit messages by leveraging the **LM Studio API**. It analyzes changes in a Git repository (via `git diff`), sends them to the LM Studio model, and retrieves commit messages that follow a structured format.

---

## Features

- **Automated Commit Message Generation**: Analyze Git diffs and generate structured commit messages.
- **Supports Multiple Files**: Process changes across multiple files in a repository.
- **Flexible API Integration**: Uses LM Studio's API for natural language processing.
- **Mocked or Real API Testing**: Includes tests with support for mocking or using the real LM Studio server.

---

## Requirements

- **Python**: Version 3.8 or higher.
- **Git**: Installed and available in the system's PATH.
- **LM Studio**: Running locally with an accessible API endpoint.
- **Python Libraries**:
  - `requests`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo-folder
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Run the Main Script

1. Ensure you have a running LM Studio server (default port: `1234`).

2. Run the program with your Git repository path:
   ```bash
   python main.py /path/to/your/git/repository
   ```

3. Example output:
   ```plaintext
   Fetching Git changes...
   Processing files...
   Committing files to LM Studio...
   Commit message: Update test.txt file contents and remove typo
   ```

---

## API Configuration

The program communicates with the LM Studio API. The configuration is in the `main.py` file:

- **API URL**: Default is `http://localhost:1234/v1/completions`.
- **API Token**: Replace `"your_api_token_here"` with a valid token if required.

---

## File Descriptions

### Core Scripts

1. **`main.py`**:
   - Entry point of the program.
   - Fetches Git changes, processes files, and communicates with LM Studio.

2. **`git_changes.py`**:
   - Extracts modified, untracked, and deleted files using Git commands.
   - Provides Git diffs for analysis.

3. **`lm_studio_committer.py`**:
   - Handles the communication with the LM Studio API.
   - Sends prompts and retrieves structured commit messages.

4. **`file_processor.py`**:
   - Reads and encodes file content (text or binary).

### Tests

1. **`test_file_processor.py`**:
   - Unit tests for file content processing.
   
2. **`test_git_changes.py`**:
   - Unit tests for Git change detection and diff generation.

3. **`test_lm_studio_committer.py`**:
   - Unit tests for API communication, with support for mocked and real API responses.

---

## Running Tests

1. Run all tests:
   ```bash
   python -m unittest discover
   ```

2. Run a specific test file:
   ```bash
   python -m unittest test_lm_studio_committer.py
   ```

3. Run real API tests:
   ```bash
   python test_lm_studio_committer.py --real-api
   ```

---

## Example Output

### Generated Commit Message
```plaintext
Title: Update test.txt file contents and remove typo

Body:
Fixed a typo in the original filename and added a new line of content
to the file. Updated existing lines with corrected text, including
removing unnecessary whitespace.
```

---

## Troubleshooting

1. **API Not Responding**:
   - Ensure the LM Studio server is running locally (`http://localhost:1234`).
   - Verify the API token if required.

2. **Git Not Found**:
   - Ensure Git is installed and available in your system's PATH.

3. **Tests Fail**:
   - Run with a clean Python environment and ensure all dependencies are installed.

---

## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue to discuss your ideas.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Let me know if you'd like me to adjust any part of this README! 🚀