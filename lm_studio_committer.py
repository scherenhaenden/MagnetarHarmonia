import requests
import json
from git_changes import get_git_diff


def commit_file_to_lm_studio(file_data, api_url, api_token):
    """
    Commits a single file to the LM Studio server using the API.
    Returns the extracted commit message (JSON) or None on failure.
    """
    if not api_token:
        print("Error: API token is missing.")
        return None

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    git_diff = get_git_diff(file_data['path'])
    if not git_diff:
        print(f"No diff available for {file_data['path']}. Skipping file.")
        return None

    prompt = (
        f"I need you to analyze the changes shown in this Git diff and generate a commit message. "
        f"The commit message must be returned exclusively in JSON format as shown in the example below. "
        f"Do not add anything else to your response.\n\n"
        f"Example JSON format:\n\n"
        f"{{\n"
        f"  \"commit\": {{\n"
        f"    \"title\": \"Your title here\",\n"
        f"    \"body\": \"Your body here.\"\n"
        f"  }}\n"
        f"}}\n\n"
        f"Here the actual Git diff:\n\n{git_diff}\n\n"
        f"Ensure the response includes:\n"
        f"- A title summarizing the changes (max 60 characters).\n"
        f"- A body explaining the changes, with a blank line after the title and lines limited to 75 characters."
    )

    payload = {
        "prompt": prompt,
        "model": "unsloth",
        "filename": file_data['path'],
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            # Extract and parse the JSON response
            response_data = response.json()
            choices = response_data.get("choices", [])
            if choices:
                raw_text = choices[0].get("text", "").strip()
                # Parse the JSON structure from the response text
                try:
                    commit_json = json.loads(raw_text)
                    print(f"Extracted Commit JSON: {commit_json}")
                    return commit_json
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from response text: {raw_text}")
                    return None
            else:
                print("No choices found in the response.")
                return None
        else:
            print(f"Failed to commit file: {file_data['path']}. Status: {response.status_code}")
            print(response.text)
            return None
    except requests.RequestException as e:
        print(f"Error committing file {file_data['path']}: {e}")
        return None


def commit_files_to_lm_studio(files, api_url, api_token):
    """
    Commits multiple files to the LM Studio server.

    :param files: A list of dictionaries with file 'path' and 'content'.
    :param api_url: The LM Studio API endpoint for committing files.
    :param api_token: The API token for authentication.
    :return: A list of extracted commit messages (JSON).
    """
    if not api_token:
        print("Error: API token is missing.")
        return []

    results = []
    for file_data in files:
        commit_message = commit_file_to_lm_studio(file_data, api_url, api_token)
        if commit_message is None:
            print(f"Skipping file: {file_data['path']}")
        results.append(commit_message)
    return results


if __name__ == "__main__":
    # Example usage
    api_url = "http://localhost:1234/v1/completions"  # Replace with the actual endpoint
    api_token = "your_api_token_here"

    if api_token == "your_api_token_here":
        print("Error: Replace 'your_api_token_here' with a valid API token.")
        exit(1)

    # Example file data
    files = [
        {"path": "example1.txt", "content": "Example content for file 1"},
        {"path": "example2.txt", "content": "Example content for file 2"},
    ]

    responses = commit_files_to_lm_studio(files, api_url, api_token)
    for resp in responses:
        print(f"Commit message JSON: {json.dumps(resp, indent=4)}")
