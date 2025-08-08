#!/usr/bin/env python3
"""
Test utilities and base classes for Ansible Jinja2 Playground tests
"""

import os
import sys
import json
import tempfile
import shutil
import unittest
from http.server import HTTPServer
import threading
import time
import urllib.request
import urllib.parse
import urllib.error

# Add the app directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
app_dir = os.path.join(project_root, 'app')
sys.path.insert(0, app_dir)

# Import after path setup
import ansible_jinja2_playground


class BaseTestCase(unittest.TestCase):
  """Base test case with common setup and utilities"""

  @classmethod
  def setUpClass(cls):
    """Set up test environment with temporary directories"""
    cls.test_dir = tempfile.mkdtemp()
    cls.conf_dir = os.path.join(cls.test_dir, 'conf')
    cls.inputs_dir = os.path.join(cls.test_dir, 'inputs')

    # Create directories
    os.makedirs(cls.conf_dir, exist_ok=True)
    os.makedirs(cls.inputs_dir, exist_ok=True)

    # Create test configuration file
    cls.conf_file = os.path.join(cls.conf_dir, 'ansible_jinja2_playground.conf')
    cls.history_file = os.path.join(cls.conf_dir, 'ansible_jinja2_playground_history.json')

    # Create test config
    with open(cls.conf_file, 'w', encoding='utf-8') as f:
      f.write(f"""[server]
host = 127.0.0.1
port = 0

[history]
max_entries = 1000

[input_files]
directory = {cls.inputs_dir}

[user]
theme = dark
height-inputcode = 100
height-jinjaexpr = 200
height-resultview = 800
""")

    # Create test input files
    cls.create_test_input_files()

    # Patch the module paths
    cls.original_conf_path = ansible_jinja2_playground.CONF_PATH
    cls.original_json_history_path = ansible_jinja2_playground.JSON_HISTORY_PATH
    cls.original_project_root = ansible_jinja2_playground.PROJECT_ROOT

    ansible_jinja2_playground.CONF_PATH = cls.conf_file
    ansible_jinja2_playground.JSON_HISTORY_PATH = cls.history_file
    ansible_jinja2_playground.PROJECT_ROOT = cls.test_dir

    # Reload configuration
    ansible_jinja2_playground.config.clear()
    ansible_jinja2_playground.config.read(cls.conf_file)

    # Update global variables
    ansible_jinja2_playground.MAX_ENTRIES = int(ansible_jinja2_playground.config.get('history', 'max_entries', fallback='1000'))
    ansible_jinja2_playground.HOST = ansible_jinja2_playground.config.get('server', 'host', fallback='127.0.0.1')
    ansible_jinja2_playground.PORT = int(ansible_jinja2_playground.config.get('server', 'port', fallback='0'))

  @classmethod
  def create_test_input_files(cls):
    """Create test input files"""
    # JSON test file
    with open(os.path.join(cls.inputs_dir, 'test.json'), 'w', encoding='utf-8') as f:
      json.dump({
        "name": "John Doe",
        "age": 30,
        "items": ["apple", "banana", "cherry"]
      }, f, indent=2)

    # YAML test file
    with open(os.path.join(cls.inputs_dir, 'test.yaml'), 'w', encoding='utf-8') as f:
      f.write("""name: Jane Smith
age: 25
items:
  - orange
  - grape
  - kiwi
""")

  @classmethod
  def tearDownClass(cls):
    """Clean up test environment"""
    # Restore original paths
    ansible_jinja2_playground.CONF_PATH = cls.original_conf_path
    ansible_jinja2_playground.JSON_HISTORY_PATH = cls.original_json_history_path
    ansible_jinja2_playground.PROJECT_ROOT = cls.original_project_root

    # Clean up temporary directory
    if os.path.exists(cls.test_dir):
      shutil.rmtree(cls.test_dir)

  def setUp(self):
    """Set up each test"""
    # Clear history file before each test
    if os.path.exists(self.history_file):
      os.remove(self.history_file)

  def tearDown(self):
    """Clean up after each test"""
    # Clear history file after each test
    if os.path.exists(self.history_file):
      os.remove(self.history_file)


class HTTPTestCase(BaseTestCase):
  """Test case with HTTP server for integration tests"""

  @classmethod
  def setUpClass(cls):
    """Set up HTTP server for testing"""
    super().setUpClass()

    # Start HTTP server in background thread
    cls.server = HTTPServer(('127.0.0.1', 0), ansible_jinja2_playground.JinjaHandler)
    cls.server_thread = threading.Thread(target=cls.server.serve_forever)
    cls.server_thread.daemon = True
    cls.server_thread.start()

    # Get the actual port assigned
    cls.server_port = cls.server.server_address[1]
    cls.base_url = f"http://127.0.0.1:{cls.server_port}"

    # Wait for server to start
    time.sleep(0.1)

  @classmethod
  def tearDownClass(cls):
    """Shut down HTTP server"""
    cls.server.shutdown()
    cls.server.server_close()
    super().tearDownClass()

  def make_request(self, path, method='GET', data=None, headers=None):
    """Make HTTP request to test server"""
    url = f"{self.base_url}{path}"

    if headers is None:
      headers = {}

    if method == 'GET':
      req = urllib.request.Request(url, headers=headers)
    else:
      if isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode('utf-8')
      elif isinstance(data, str):
        data = data.encode('utf-8')
      req = urllib.request.Request(url, data=data, headers=headers)
      req.get_method = lambda: method

    try:
      with urllib.request.urlopen(req) as response:
        return {
          'status_code': response.status,
          'headers': dict(response.headers),
          'content': response.read().decode('utf-8')
        }
    except urllib.error.HTTPError as e:
      return {
        'status_code': e.code,
        'headers': dict(e.headers) if hasattr(e, 'headers') else {},
        'content': e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
      }
    except Exception as e:
      return {
        'status_code': 0,
        'headers': {},
        'content': str(e)
      }

  def get_header(self, response, header_name):
    """Get header value case-insensitively"""
    for key, value in response['headers'].items():
      if key.lower() == header_name.lower():
        return value
    return None
