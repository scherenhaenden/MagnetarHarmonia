import os
import sys
import subprocess
from git_changes import get_git_changes
from file_processor import process_files
from lm_studio_committer import commit_file_to_lm_studio, commit_files_to_lm_studio

def install_and_import(package):
    """
    Installs a package if it's not already installed and then imports it.
    """
    try:
        __import__(package)
    except ImportError:
        print(f"Installing missing package: {package}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        globals()[package] = __import__(package)

def interactive_commit(repo_path, lm_studio_api_url, lm_studio_api_token):
    """
    Process files one by one in interactive mode.
    """
    # Fetch Git changes
    git_changes = get_git_changes(repo_path)
    changed_files = git_changes['modified'] + git_changes['untracked']

    if not changed_files:
        print("No changes detected.")
        return

    # Process files
    processed_files = process_files(changed_files, repo_path)
    if not processed_files:
        print("No valid files to process.")
        return

    # Interactive commit process
    for file_data in processed_files:
        print(f"\nProcessing file: {file_data['path']}")
        commit_message = commit_file_to_lm_studio(file_data, lm_studio_api_url, lm_studio_api_token)

        if not commit_message:
            print(f"Skipping file: {file_data['path']}")
            continue

        print("\nSuggested Commit Message:")
        print(f"Title: {commit_message['commit']['title']}")
        print(f"Body:\n{commit_message['commit']['body']}")

        user_input = input("\nDo you accept this commit? (yes/no): ").strip().lower()
        if user_input == 'yes':
            try:
                subprocess.run(['git', '-C', repo_path, 'add', file_data['path']], check=True)
                subprocess.run(
                    ['git', '-C', repo_path, 'commit', '-m', commit_message['commit']['title'], '-m', commit_message['commit']['body']],
                    check=True
                )
                print(f"Successfully committed: {file_data['path']}")
            except subprocess.CalledProcessError as e:
                print(f"Error during Git commit for {file_data['path']}: {e}")
        else:
            print(f"Commit skipped for: {file_data['path']}")

def main(repo_path, interactive_mode=False):
    # Configuration
    lm_studio_api_url = "http://localhost:1234/v1/completions"  # LM Studio API endpoint
    lm_studio_api_token = "your_api_token_here"  # Replace with your actual API token

    if interactive_mode:
        print("Starting interactive mode...")
        interactive_commit(repo_path, lm_studio_api_url, lm_studio_api_token)
    else:
        # Fetch Git changes
        print("Fetching Git changes...")
        git_changes = get_git_changes(repo_path)
        if not git_changes['modified'] and not git_changes['untracked']:
            print("No changes detected.")
            return

        # Process files
        print("Processing files...")
        changed_files = git_changes['modified'] + git_changes['untracked']
        processed_files = process_files(changed_files, repo_path)

        if not processed_files:
            print("No valid files to process.")
            return

        # Commit files
        print("Committing files to LM Studio...")
        responses = commit_files_to_lm_studio(processed_files, lm_studio_api_url, lm_studio_api_token)

        # Log results
        print("Commit results:")
        for response in responses:
            print(response)

if __name__ == "__main__":
    install_and_import("requests")

    if len(sys.argv) < 2:
        print("Usage: python main.py <repo_path> [--interactive]")
        sys.exit(1)

    repository_path = sys.argv[1]
    interactive_mode = '--interactive' in sys.argv

    if not os.path.exists(repository_path):
        print(f"Error: The specified path does not exist: {repository_path}")
        sys.exit(1)

    main(repository_path, interactive_mode)
