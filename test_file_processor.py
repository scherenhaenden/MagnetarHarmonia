import unittest
import os
import tempfile
import base64
from file_processor import read_file_content, process_files


class TestFileProcessor(unittest.TestCase):

    def setUp(self):
        """
        Set up temporary files for testing.
        """
        self.test_dir = tempfile.TemporaryDirectory()
        self.text_file_path = os.path.join(self.test_dir.name, "test.txt")
        self.binary_file_path = os.path.join(self.test_dir.name, "test.bin")

        # Create a text file
        with open(self.text_file_path, 'w', encoding='utf-8') as f:
            f.write("This is a test file.")

        # Create a binary file
        with open(self.binary_file_path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01')

    def tearDown(self):
        """
        Clean up temporary files.
        """
        self.test_dir.cleanup()

    def test_read_file_content_text(self):
        """
        Test reading the content of a text file.
        """
        content = read_file_content(self.text_file_path)
        self.assertEqual(content, "This is a test file.")

    def test_read_file_content_binary(self):
        """
        Test reading the content of a binary file.
        """
        content = read_file_content(self.binary_file_path)
        expected_content = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01').decode('utf-8')
        self.assertEqual(content, expected_content)

    def test_read_file_content_nonexistent(self):
        """
        Test reading a nonexistent file.
        """
        content = read_file_content("nonexistent.txt")
        self.assertIsNone(content)

    def test_process_files(self):
        """
        Test processing a list of files.
        """
        file_list = ["test.txt", "test.bin"]
        processed = process_files(file_list, self.test_dir.name)

        # Validate the processed data
        self.assertEqual(len(processed), 2)

        # Check text file
        self.assertEqual(processed[0]['path'], "test.txt")
        self.assertEqual(processed[0]['content'], "This is a test file.")

        # Check binary file
        self.assertEqual(processed[1]['path'], "test.bin")
        expected_binary_content = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01').decode('utf-8')
        self.assertEqual(processed[1]['content'], expected_binary_content)


if __name__ == '__main__':
    unittest.main()
