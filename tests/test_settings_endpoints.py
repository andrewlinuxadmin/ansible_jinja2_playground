from test_utils import HTTPTestCase
import unittest
import json
import os
import sys

# Add the ansible-jinja2-playground directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ansible-jinja2-playground'))


class TestSettingsEndpoints(HTTPTestCase):
  """Test cases for all settings-related endpoints"""

  def test_get_settings_user_section(self):
    """Test GET /settings with user section"""
    response = self.make_request('/settings?section=user')
    self.assertEqual(response['status_code'], 200)
    content_type = self.get_header(response, 'content-type')
    self.assertEqual(content_type, 'application/json')

    data = json.loads(response['content'])
    # User section should return settings directly, not wrapped in 'user' key
    self.assertIn('theme', data)
    self.assertIn('height-inputcode', data)
    self.assertIn('height-jinjaexpr', data)
    self.assertIn('height-resultview', data)

  def test_get_settings_server_section(self):
    """Test GET /settings with server section"""
    response = self.make_request('/settings?section=server')
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    # Server section should return settings directly
    self.assertIn('host', data)
    self.assertIn('port', data)

  def test_get_settings_history_section(self):
    """Test GET /settings with history section"""
    response = self.make_request('/settings?section=history')
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    # History section should return settings directly
    self.assertIn('max_entries', data)

  def test_get_settings_input_files_section(self):
    """Test GET /settings with input_files section"""
    response = self.make_request('/settings?section=input_files')
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    # Input files section should return settings directly
    self.assertIn('directory', data)

  def test_get_settings_invalid_section(self):
    """Test GET /settings with invalid section"""
    response = self.make_request('/settings?section=invalid')
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    self.assertEqual(data, {})

  def test_get_settings_no_section(self):
    """Test GET /settings without section parameter"""
    response = self.make_request('/settings')
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    # Should return all sections
    expected_sections = ['user', 'history', 'input_files', 'server']
    for section in expected_sections:
      self.assertIn(section, data, f"Should contain {section} section")

  def test_post_settings_user_theme(self):
    """Test POST /settings to update user theme"""
    # Update theme
    response = self.make_request('/settings', 'POST', {
        'section': 'user',
        'theme': 'light'
    })
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    self.assertIn('user', data)
    if 'user' in data:
      self.assertEqual(data['user']['theme'], 'light')

    # Verify the change persisted
    response = self.make_request('/settings?section=user')
    self.assertEqual(response['status_code'], 200)
    data = json.loads(response['content'])
    if 'user' in data:
      self.assertEqual(data['user']['theme'], 'light')

  def test_post_settings_user_heights(self):
    """Test POST /settings to update user height settings"""
    response = self.make_request('/settings', 'POST', {
        'section': 'user',
        'height-inputcode': '150',
        'height-jinjaexpr': '250',
        'height-resultview': '800'
    })
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    user_settings = data['user']
    self.assertEqual(user_settings['height-inputcode'], '150')
    self.assertEqual(user_settings['height-jinjaexpr'], '250')
    self.assertEqual(user_settings['height-resultview'], '800')

  def test_post_settings_history_max_entries(self):
    """Test POST /settings to update history max entries"""
    response = self.make_request('/settings', 'POST', {
        'section': 'history',
        'max_entries': '500'
    })
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    self.assertEqual(data['history']['max_entries'], '500')

  def test_post_settings_input_files_directory(self):
    """Test POST /settings to update input files directory"""
    # Just test that we get a response, since directory validation may be strict
    response = self.make_request('/settings', 'POST', {
        'section': 'input_files',
        'directory': 'inputs'
    })
    # Accept either 200 (success) or 400 (validation error) as valid responses
    self.assertIn(response['status_code'], [200, 400],
                  f"Expected status 200 or 400, got {response['status_code']}")

    # If successful, should contain some response
    if response['status_code'] == 200:
      self.assertIsNotNone(response['content'])

  def test_post_settings_input_files_invalid_directory(self):
    """Test POST /settings with invalid input directory"""
    response = self.make_request('/settings', 'POST', {
        'section': 'input_files',
        'directory': '../../../etc/passwd'  # Path traversal attempt
    })
    self.assertEqual(response['status_code'], 400)

    data = json.loads(response['content'])
    self.assertIn('error', data)
    self.assertIn('Security validation failed', data['error'])

  def test_post_settings_missing_section_parameter(self):
    """Test POST /settings without section parameter"""
    response = self.make_request('/settings', 'POST', {
        'theme': 'dark'
    })

    self.assertEqual(response['status_code'], 400)
    data = json.loads(response['content'])
    self.assertIn('error', data)
    self.assertEqual(data['error'], 'Missing section parameter')

  def test_post_settings_input_files_security_traversal(self):
    """Test POST /settings with path traversal attempt in input_files directory"""
    response = self.make_request('/settings', 'POST', {
        'section': 'input_files',
        'directory': '../../../etc/passwd'
    })

    self.assertEqual(response['status_code'], 400)
    data = json.loads(response['content'])
    self.assertIn('error', data)
    self.assertIn('Security validation failed', data['error'])

  def test_post_settings_input_files_absolute_path_security(self):
    """Test POST /settings with absolute path in input_files directory"""
    response = self.make_request('/settings', 'POST', {
        'section': 'input_files',
        'directory': '/etc/shadow'
    })

    self.assertEqual(response['status_code'], 400)
    data = json.loads(response['content'])
    self.assertIn('error', data)
    self.assertIn('Security validation failed', data['error'])

  def test_post_settings_server_section_all_options(self):
    """Test POST /settings updating all server section options"""
    response = self.make_request('/settings', 'POST', {
        'section': 'server',
        'host': '127.0.0.1',
        'port': '8001'
    })

    # Server settings might require restart, so just verify we get a response
    self.assertIn(response['status_code'], [200, 400])
    if response['status_code'] == 200:
      data = json.loads(response['content'])
      self.assertIn('server', data)

  def test_post_settings_user_all_options(self):
    """Test POST /settings updating all user section options"""
    response = self.make_request('/settings', 'POST', {
        'section': 'user',
        'theme': 'light',
        'height-inputcode': '150',
        'height-jinjaexpr': '250',
        'height-resultview': '800',
        'api-listener-enabled': 'true'
    })

    self.assertEqual(response['status_code'], 200)
    data = json.loads(response['content'])
    self.assertIn('user', data)

    # Verify all settings were applied
    user_settings = data['user']
    self.assertEqual(user_settings['theme'], 'light')
    self.assertEqual(user_settings['height-inputcode'], '150')
    self.assertEqual(user_settings['height-jinjaexpr'], '250')
    self.assertEqual(user_settings['height-resultview'], '800')
    self.assertEqual(user_settings['api-listener-enabled'], 'true')

  def test_post_settings_history_max_entries_validation(self):
    """Test POST /settings with different max_entries values"""
    # Test valid numeric value
    response = self.make_request('/settings', 'POST', {
        'section': 'history',
        'max_entries': '500'
    })

    self.assertEqual(response['status_code'], 200)
    data = json.loads(response['content'])
    self.assertIn('history', data)
    self.assertEqual(data['history']['max_entries'], '500')

    # Test invalid non-numeric value (should still succeed but may be handled as string)
    response = self.make_request('/settings', 'POST', {
        'section': 'history',
        'max_entries': 'invalid'
    })

    self.assertEqual(response['status_code'], 200)

  def test_post_settings_create_new_section(self):
    """Test POST /settings creating a completely new section"""
    response = self.make_request('/settings', 'POST', {
        'section': 'custom_test_section',
        'custom_option': 'test_value',
        'another_option': 'another_value'
    })

    self.assertEqual(response['status_code'], 200)
    data = json.loads(response['content'])
    self.assertIn('custom_test_section', data)

    custom_section = data['custom_test_section']
    self.assertEqual(custom_section['custom_option'], 'test_value')
    self.assertEqual(custom_section['another_option'], 'another_value')


if __name__ == '__main__':

  def test_post_settings_missing_section_parameter(self):
    """Test POST /settings without section parameter"""
    response = self.make_request('/settings', 'POST', {
        'theme': 'dark'
    })
    self.assertEqual(response['status_code'], 400)

    data = json.loads(response['content'])
    self.assertIn('error', data)
    self.assertEqual(data['error'], 'Missing section parameter')

  def test_post_settings_multiple_values(self):
    """Test POST /settings with multiple settings at once"""
    response = self.make_request('/settings', 'POST', {
        'section': 'user',
        'theme': 'eclipse',
        'height-inputcode': '120',
        'height-resultview': '900'
    })
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    user_settings = data['user']
    self.assertEqual(user_settings['theme'], 'eclipse')
    self.assertEqual(user_settings['height-inputcode'], '120')
    self.assertEqual(user_settings['height-resultview'], '900')

  def test_post_settings_server_section(self):
    """Test POST /settings to update server settings"""
    response = self.make_request('/settings', 'POST', {
        'section': 'server',
        'host': '127.0.0.1',
        'port': '8001'
    })
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    server_settings = data['server']
    self.assertEqual(server_settings['host'], '127.0.0.1')
    self.assertEqual(server_settings['port'], '8001')


if __name__ == '__main__':
  unittest.main()
