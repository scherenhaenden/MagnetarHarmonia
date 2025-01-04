import unittest
from unittest.mock import patch, MagicMock
import subprocess
from git_changes import get_git_changes, get_git_diff


class TestGitChanges(unittest.TestCase):

    @patch('os.path.isdir', return_value=True)
    @patch('os.chdir')
    @patch('subprocess.check_output')
    def test_get_git_changes_valid_repo(self, mock_check_output, mock_chdir, mock_isdir):
        """
        Test get_git_changes with a valid Git repository path.
        """
        # Mock the outputs for git commands
        mock_check_output.side_effect = [
            b"file1.txt\nfile2.txt\n",  # Modified files
            b"new_file.txt\n",          # Untracked files
            b"deleted_file.txt\n"       # Deleted files
        ]

        repo_path = "/path/to/git/repo"
        changes = get_git_changes(repo_path)

        # Validate results
        self.assertEqual(changes['modified'], ["file1.txt", "file2.txt"])
        self.assertEqual(changes['untracked'], ["new_file.txt"])
        self.assertEqual(changes['deleted'], ["deleted_file.txt"])

    @patch('os.path.isdir', return_value=True)
    @patch('os.chdir')
    @patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'git'))
    def test_get_git_changes_subprocess_error(self, mock_check_output, mock_chdir, mock_isdir):
        """
        Test get_git_changes when a Git command fails.
        """
        repo_path = "/path/to/git/repo"
        changes = get_git_changes(repo_path)

        # Validate results: all should be empty due to the error
        self.assertEqual(changes['modified'], [])
        self.assertEqual(changes['untracked'], [])
        self.assertEqual(changes['deleted'], [])

    @patch('os.path.isdir', return_value=False)
    def test_get_git_changes_invalid_repo_path(self, mock_isdir):
        """
        Test get_git_changes with an invalid repository path.
        """
        invalid_path = "/invalid/path"
        changes = get_git_changes(invalid_path)

        # Validate results: all should be empty due to the invalid path
        self.assertEqual(changes['modified'], [])
        self.assertEqual(changes['untracked'], [])
        self.assertEqual(changes['deleted'], [])

    @patch('os.path.isdir', return_value=True)
    @patch('os.chdir')
    @patch('subprocess.check_output', side_effect=[
        b"file1.txt\n",  # Modified
        b"new_file.txt\n",  # Untracked
        b""  # Deleted
    ])
    def test_get_git_changes_partial_results(self, mock_check_output, mock_chdir, mock_isdir):
        """
        Test get_git_changes with partial results (some categories empty).
        """
        repo_path = "/path/to/git/repo"
        changes = get_git_changes(repo_path)

        # Validate results
        self.assertEqual(changes['modified'], ["file1.txt"])
        self.assertEqual(changes['untracked'], ["new_file.txt"])
        self.assertEqual(changes['deleted'], [])  # No deleted files

    @patch('subprocess.check_output')
    def test_get_git_diff_valid_file(self, mock_check_output):
        """
        Test get_git_diff with a valid file path.
        """
        mock_check_output.return_value = (
            b"diff --git a/file1.txt b/file1.txt\n"
            b"index abc123..def456 100644\n"
            b"--- a/file1.txt\n"
            b"+++ b/file1.txt\n"
            b"@@ -1,2 +1,3 @@\n"
            b" Line 1\n"
            b"+New line\n"
            b" Line 2\n"
        )

        file_path = "file1.txt"
        diff = get_git_diff(file_path)

        # Validate the diff output
        self.assertIn("diff --git", diff)
        self.assertIn("New line", diff)

    @patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'git'))
    def test_get_git_diff_error(self, mock_check_output):
        """
        Test get_git_diff when git diff command fails.
        """
        file_path = "file1.txt"
        diff = get_git_diff(file_path)

        # Validate that no diff is returned
        self.assertIsNone(diff)

if __name__ == '__main__':
    unittest.main()
