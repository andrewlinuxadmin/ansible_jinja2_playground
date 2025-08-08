import unittest
import json
import os
import sys

# Add the app directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from test_utils import HTTPTestCase


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
    """Test GET /input-file-content with encoded path traversal"""
    response = self.make_request('/input-file-content?filename=..%2F..%2F..%2Fetc%2Fpasswd')
    self.assertEqual(response['status_code'], 403)

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
