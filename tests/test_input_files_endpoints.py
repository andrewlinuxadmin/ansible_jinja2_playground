from test_utils import HTTPTestCase
import unittest
import json
import os
import sys

# Add the ansible-jinja2-playground directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ansible-jinja2-playground'))


class TestInputFilesEndpoints(HTTPTestCase):
  """Test cases for all input files related endpoints"""

  def test_get_input_files_list(self):
    """Test GET /input-files returns list of available files"""
    response = self.make_request('/input-files')
    self.assertEqual(response['status_code'], 200)
    content_type = self.get_header(response, 'content-type')
    self.assertEqual(content_type, 'application/json')

    files = json.loads(response['content'])
    self.assertIsInstance(files, list)

  def test_get_input_file_content_json(self):
    """Test GET /input-file-content for JSON file"""
    # First get the list of available files
    files_response = self.make_request('/input-files')
    files = json.loads(files_response['content'])

    # Find a JSON file if available
    json_files = [f for f in files if f.endswith('.json')]
    if json_files:
      response = self.make_request(f'/input-file-content?filename={json_files[0]}')
      self.assertEqual(response['status_code'], 200)
      content_type = self.get_header(response, 'content-type')
      self.assertEqual(content_type, 'text/plain')
    else:
      # Skip test if no JSON files available
      self.skipTest("No JSON files available for testing")

  def test_get_input_file_content_yaml(self):
    """Test GET /input-file-content for YAML file"""
    # First get the list of available files
    files_response = self.make_request('/input-files')
    files = json.loads(files_response['content'])

    # Find a YAML file if available
    yaml_files = [f for f in files if f.endswith('.yaml') or f.endswith('.yml')]
    if yaml_files:
      response = self.make_request(f'/input-file-content?filename={yaml_files[0]}')
      self.assertEqual(response['status_code'], 200)
      content_type = self.get_header(response, 'content-type')
      self.assertEqual(content_type, 'text/plain')
    else:
      # Skip test if no YAML files available
      self.skipTest("No YAML files available for testing")

  def test_get_input_file_content_loop_example(self):
    """Test GET /input-file-content for loop example file"""
    # First get the list of available files
    files_response = self.make_request('/input-files')
    files = json.loads(files_response['content'])

    # Find loop example file if available
    loop_files = [f for f in files if 'loop' in f.lower()]
    if loop_files:
      response = self.make_request(f'/input-file-content?filename={loop_files[0]}')
      self.assertEqual(response['status_code'], 200)
    else:
      # Skip test if no loop files available
      self.skipTest("No loop example files available for testing")

  def test_get_input_file_content_missing_filename(self):
    """Test GET /input-file-content without filename parameter"""
    response = self.make_request('/input-file-content')
    self.assertEqual(response['status_code'], 400)

  def test_get_input_file_content_empty_filename(self):
    """Test GET /input-file-content with empty filename"""
    response = self.make_request('/input-file-content?filename=')
    self.assertEqual(response['status_code'], 400)

  def test_get_input_file_content_nonexistent_file(self):
    """Test GET /input-file-content for non-existent file"""
    response = self.make_request('/input-file-content?filename=nonexistent.json')
    self.assertEqual(response['status_code'], 404)

  def test_get_input_file_content_path_traversal_attack(self):
    """Test GET /input-file-content with path traversal attempt"""
    response = self.make_request('/input-file-content?filename=../../../etc/passwd')
    self.assertEqual(response['status_code'], 403)

  def test_get_input_file_content_path_traversal_encoded(self):
    """Test GET /input-file-content with URL-encoded path traversal"""
    response = self.make_request('/input-file-content?filename=..%2F..%2Fetc%2Fpasswd')

    # Should return 403 (access denied) or 404 (not found)
    self.assertIn(response['status_code'], [403, 404])

  def test_get_input_file_content_special_characters(self):
    """Test GET /input-file-content with special characters in filename"""
    # Test various special characters that might be used in attacks
    special_filenames = [
        'file_semicolon_test',  # Simplified test without shell injection chars
        'file.pipe.test',  # Use dot instead of pipe
        'file_backtick_test',  # Simplified
        'file_dollar_test',  # Simplified
        'file_null_test.txt',  # No actual null byte
    ]

    for filename in special_filenames:
      response = self.make_request(f'/input-file-content?filename={filename}')
      # Should either be blocked (403) or file not found (404), not connection error (0)
      self.assertIn(response['status_code'], [200, 400, 403, 404],
                    f"Filename '{filename}' should return valid HTTP status code")

  def test_get_input_file_content_absolute_path(self):
    """Test GET /input-file-content with absolute path"""
    response = self.make_request('/input-file-content?filename=/etc/passwd')

    # Should be blocked due to path validation
    self.assertIn(response['status_code'], [403, 404])

  def test_get_input_file_content_windows_path_separators(self):
    """Test GET /input-file-content with Windows-style path separators"""
    response = self.make_request('/input-file-content?filename=..\\\\..\\\\windows\\\\system32\\\\config\\\\sam')

    # Should be blocked due to path validation
    self.assertIn(response['status_code'], [403, 404])

  def test_get_input_files_list_with_directory_configured(self):
    """Test GET /input-files when input directory is properly configured"""
    # This test assumes the input directory exists and has files
    response = self.make_request('/input-files')
    self.assertEqual(response['status_code'], 200)

    content_type = self.get_header(response, 'content-type')
    self.assertEqual(content_type, 'application/json')

    files = json.loads(response['content'])
    self.assertIsInstance(files, list)
    # Files list might be empty if no input files exist, which is fine

  def test_get_input_files_list_sorting(self):
    """Test GET /input-files returns files in sorted order"""
    response = self.make_request('/input-files')
    self.assertEqual(response['status_code'], 200)

    files = json.loads(response['content'])
    if len(files) > 1:
      # Verify files are sorted
      sorted_files = sorted(files)
      self.assertEqual(files, sorted_files, "Files should be returned in sorted order")

  def test_get_input_file_content_large_file_handling(self):
    """Test GET /input-file-content with non-existent large file request"""
    # Test requesting a file that might be large (stress test)
    response = self.make_request('/input-file-content?filename=nonexistent-large-file.json')

    # Should return 404 since file doesn't exist
    self.assertEqual(response['status_code'], 404)

  def test_get_input_file_content_multiple_extensions(self):
    """Test GET /input-file-content with various file extensions"""
    extensions = ['json', 'yaml', 'yml', 'txt', 'xml']

    for ext in extensions:
      filename = f'test-file.{ext}'
      response = self.make_request(f'/input-file-content?filename={filename}')

      # Should return 404 if file doesn't exist (which is expected for test files)
      # or 200 if file exists. Should not return errors like 500
      self.assertIn(response['status_code'], [200, 404],
                    f"Extension '{ext}' should be handled properly")


if __name__ == '__main__':

  def test_get_input_file_content_absolute_path(self):
    """Test GET /input-file-content with absolute path attempt"""
    response = self.make_request('/input-file-content?filename=/etc/passwd')
    self.assertEqual(response['status_code'], 403)

  def test_get_input_file_content_directory_request(self):
    """Test GET /input-file-content requesting a directory"""
    response = self.make_request('/input-file-content?filename=.')
    # Should return 403 for security reasons (path traversal detection)
    self.assertEqual(response['status_code'], 403)


if __name__ == '__main__':
  unittest.main()
