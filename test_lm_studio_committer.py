import unittest
import requests
import sys
from unittest.mock import patch
from lm_studio_committer import commit_file_to_lm_studio


class TestLMStudioPrompt(unittest.TestCase):

    def setUp(self):
        """
        Set up common variables for the tests.
        """
        self.api_url = "http://localhost:1234/v1/completions"
        self.api_token = "your_api_token_here"  # Replace with a valid token
        self.git_diff = """diff --git a/test.txt b/test.txt
index 83db48f..f4c3f2b 100644
--- a/test.txt
+++ b/test.txt
@@ -1,2 +1,3 @@
This is the first line of the file.
+This is a new line added to the file.
This is the last line of the file."""
        self.run_real_api_tests = False  # Default to mocked tests

    @patch('requests.post')
    def test_prompt_generation_mock(self, mock_post):
        """
        Test the prompt generation and response via a mocked API.
        """
        # Mock the response from LM Studio
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"choices": [{"text": "Title of commit\\n\\nDetailed explanation of the changes."}]}'
        mock_post.return_value = mock_response

        # Simulate the API payload
        payload = {
            "prompt": (
                f"I need you to analyze the changes shown in this Git diff and generate a commit message. "
                f"The commit message should include:\n"
                f"- A title of max 60 characters summarizing the changes.\n"
                f"- A body explaining the changes, formatted with a blank line after the title and lines of max 75 characters.\n"
                f"- Use UK-English.\n"
                f"Respond ONLY with the commit message. Do not include any other comments or explanations.\n\n"
                f"Here is the Git diff:\n\n{self.git_diff}"
            ),
            "model": "unsloth",
            "filename": "test.txt",
        }

        # Call the function
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        # prinft payload
        print(payload)

        response = requests.post(self.api_url, headers=headers, json=payload)

        # Validate the response
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn("choices", response.json())
        self.assertIn("text", response.json()["choices"][0])

    def test_prompt_real_api(self):
        """
        Test the prompt with the real LM Studio API.
        """
        payload = {
            "prompt": (
                f"I need you to analyze the changes shown in this Git diff and generate a commit message. "
                f"The commit message should include:\n"
                f"- A title of max 60 characters summarizing the changes.\n"
                f"- A body explaining the changes, formatted with a blank line after the title and lines of max 75 characters.\n"
                f"- Use UK-English.\n"
                f"Respond ONLY with the commit message. Do not include any other comments or explanations.\n\n"
                f"Here is the Git diff:\n\n{self.git_diff}"
            ),
            "model": "unsloth",
            "filename": "test.txt",
        }

        headers = {
            "Content-Type": "application/json",
        }

        # Include the token in headers only if it is set
        if self.api_token and self.api_token != "your_api_token_here":
            headers["Authorization"] = f"Bearer {self.api_token}"

        response = requests.post(self.api_url, headers=headers, json=payload)
        print(f"Real API response: {response.json()}")

        # Validate the real API response
        self.assertIsNotNone(response.json())
        self.assertIn("choices", response.json())
        self.assertIn("text", response.json()["choices"][0])


if __name__ == '__main__':
    # Handle custom arguments like `--real-api`
    if "--real-api" in sys.argv:
        TestLMStudioPrompt.run_real_api_tests = True
        sys.argv.remove("--real-api")

    unittest.main()
