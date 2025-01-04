import subprocess
import os
import sys

def get_git_changes(repo_path):
    """
    Fetches a list of changed, new, and deleted files in the specified Git repository.
    Returns a dictionary with keys: 'modified', 'untracked', and 'deleted'.
    """
    try:
        # Ensure the provided path is a valid Git repository
        if not os.path.isdir(repo_path):
            raise ValueError(f"Invalid repository path: {repo_path}")
        os.chdir(repo_path)

        # Get modified files
        modified_files = subprocess.check_output(
            ['git', 'diff', '--name-only']
        ).decode('utf-8').splitlines()

        # Get untracked files
        untracked_files = subprocess.check_output(
            ['git', 'ls-files', '--others', '--exclude-standard']
        ).decode('utf-8').splitlines()

        # Get deleted files
        deleted_files = subprocess.check_output(
            ['git', 'diff', '--name-only', '--diff-filter=D']
        ).decode('utf-8').splitlines()

        return {
            'modified': modified_files,
            'untracked': untracked_files,
            'deleted': deleted_files,
        }
    except subprocess.CalledProcessError as e:
        print(f"Error while fetching git changes: {e}")
        return {
            'modified': [],
            'untracked': [],
            'deleted': [],
        }
    except ValueError as e:
        print(e)
        return {
            'modified': [],
            'untracked': [],
            'deleted': [],
        }

def get_git_diff(file_path):
    """
    Retrieves the `git diff` for a specific file.
    """
    try:
        diff_output = subprocess.check_output(['git', 'diff', file_path]).decode('utf-8')
        return diff_output
    except subprocess.CalledProcessError as e:
        print(f"Error fetching git diff for {file_path}: {e}")
        return None

if __name__ == "__main__":
    # Expect the repository path as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python get_changes.py <path_to_git_repo> [file_to_diff]")
        sys.exit(1)

    repo_path = sys.argv[1]

    # If a file path is provided, fetch its diff
    if len(sys.argv) == 3:
        file_path = sys.argv[2]
        diff = get_git_diff(file_path)
        if diff:
            print(f"Git diff for {file_path}:\n{diff}")
        else:
            print(f"No diff available for {file_path}")
    else:
        changes = get_git_changes(repo_path)
        print("Git changes detected:")
        print(f"Modified files: {changes['modified']}")
        print(f"Untracked files: {changes['untracked']}")
        print(f"Deleted files: {changes['deleted']}")
