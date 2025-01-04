import os
import base64


def read_file_content(file_path):
    """
    Reads the content of a file.
    Returns the content as a string for text files or Base64 encoded for binary files.
    """
    if not os.path.isfile(file_path):
        print(f"File does not exist: {file_path}")
        return None

    try:
        # Attempt to read as text
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # If file is binary, read in binary mode and encode in Base64
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def process_files(file_list, repo_path):
    """
    Processes a list of file paths, reading their content and preparing for submission.
    Returns a list of dictionaries with file metadata and content.
    """
    processed_files = []

    for file_path in file_list:
        full_path = os.path.join(repo_path, file_path)
        content = read_file_content(full_path)
        if content is not None:
            processed_files.append({
                'path': file_path,
                'content': content,
            })

    return processed_files


if __name__ == "__main__":
    # Example usage
    example_files = ["file1.txt", "binary_file.dat"]
    repo_path = "/path/to/repo"

    processed = process_files(example_files, repo_path)
    for file_data in processed:
        print(f"File: {file_data['path']}")
        print(f"Content: {file_data['content'][:100]}...")  # Print first 100 chars for brevity
