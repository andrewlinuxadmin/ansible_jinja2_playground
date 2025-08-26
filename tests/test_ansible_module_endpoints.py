#!/usr/bin/env python3
"""
Tests for Ansible module related endpoints
"""

from test_utils import HTTPTestCase
import unittest
import json
import os
import sys

# Add the ansible-jinja2-playground directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ansible-jinja2-playground'))


class TestAnsibleModuleEndpoints(HTTPTestCase):
  """Test cases for Ansible module related endpoints"""

  def test_post_load_ansible_vars_success(self):
    """Test POST /load_ansible_vars with valid JSON payload"""
    test_vars = {
        'ansible_hostname': 'test-server',
        'ansible_distribution': 'Ubuntu',
        'ansible_distribution_version': '22.04',
        'custom_var': 'test_value'
    }

    response = self.make_request('/load_ansible_vars', 'POST', test_vars)
    self.assertEqual(response['status_code'], 200)

    content_type = self.get_header(response, 'content-type')
    self.assertEqual(content_type, 'application/json')

  def test_post_load_ansible_vars_with_summary(self):
    """Test POST /load_ansible_vars with summary information"""
    import base64
    import json

    test_vars = {'ansible_hostname': 'test-server', 'custom_var': 'test_value'}
    variables_b64 = base64.b64encode(json.dumps(test_vars).encode()).decode()

    payload = {
        'variables_b64': variables_b64,
        'summary': {
            'total_variables': 2,
            'module': 'ansible.builtin.uri',
            'source': 'test_variables',
            'timestamp': '2025-08-26T12:00:00Z'
        }
    }

    response = self.make_request('/load_ansible_vars', 'POST', payload)
    self.assertEqual(response['status_code'], 200)

    data = json.loads(response['content'])
    self.assertEqual(data['status'], 'success')
    self.assertIn('variables_count', data)
    self.assertIn('summary', data)

  def test_post_load_ansible_vars_invalid_base64(self):
    """Test POST /load_ansible_vars with invalid base64 data"""
    payload = {
        'variables_b64': 'invalid-base64-data!!!',
        'summary': {'total_variables': 0}
    }

    response = self.make_request('/load_ansible_vars', 'POST', payload)
    self.assertEqual(response['status_code'], 500)

    data = json.loads(response['content'])
    self.assertEqual(data['status'], 'error')
    self.assertIn('Invalid base64 variables data', data['message'])

  def test_post_load_ansible_vars_listener_disabled(self):
    """Test POST /load_ansible_vars when API listener is disabled"""
    # First, disable the API listener
    self.make_request('/settings', 'POST', {
        'section': 'user',
        'api-listener-enabled': 'false'
    })

    test_vars = {'ansible_hostname': 'test-server'}
    response = self.make_request('/load_ansible_vars', 'POST', test_vars)

    self.assertEqual(response['status_code'], 200)
    data = json.loads(response['content'])
    self.assertEqual(data['status'], 'discarded')
    self.assertEqual(data['listener_enabled'], False)
    self.assertIn('API Listener is disabled', data['message'])

    # Re-enable for other tests
    self.make_request('/settings', 'POST', {
        'section': 'user',
        'api-listener-enabled': 'true'
    })

  def test_post_load_ansible_vars_empty_payload(self):
    """Test POST /load_ansible_vars with empty payload"""
    response = self.make_request('/load_ansible_vars', 'POST', {})
    self.assertEqual(response['status_code'], 200)

  def test_get_load_ansible_vars_method_not_allowed(self):
    """Test GET /load_ansible_vars should not be allowed"""
    response = self.make_request('/load_ansible_vars', 'GET')
    # Should return error (405 or 404)
    self.assertIn(response['status_code'], [404, 405])

  def test_post_history_mark_read_success(self):
    """Test POST /history/mark_read with valid entry ID"""
    # First create a history entry by rendering something
    render_response = self.make_request('/render', 'POST', {
        'json': '{"test": "value"}',
        'expr': '{{ test }}',
        'enable_loop': 'false',
        'loop_variable': ''
    })
    self.assertEqual(render_response['status_code'], 200)

    # Get history to find an entry ID
    history_response = self.make_request('/history')
    self.assertEqual(history_response['status_code'], 200)

    history = json.loads(history_response['content'])
    if history:
      entry_id = history[0].get('id')
      if entry_id:
        response = self.make_request('/history/mark_read', 'POST', {
            'id': entry_id
        })
        self.assertEqual(response['status_code'], 200)

        data = json.loads(response['content'])
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['id'], entry_id)

  def test_post_history_mark_read_missing_id(self):
    """Test POST /history/mark_read without id parameter"""
    response = self.make_request('/history/mark_read', 'POST', {})
    self.assertEqual(response['status_code'], 400)

    data = json.loads(response['content'])
    self.assertIn('error', data)
    self.assertIn('Missing id parameter', data['error'])

  def test_post_history_mark_read_invalid_id(self):
    """Test POST /history/mark_read with non-existent ID"""
    response = self.make_request('/history/mark_read', 'POST', {
        'id': 'non-existent-id-12345'
    })
    self.assertEqual(response['status_code'], 404)

    data = json.loads(response['content'])
    self.assertIn('error', data)
    self.assertIn('Entry not found', data['error'])

  def test_get_history_mark_read_method_not_allowed(self):
    """Test GET /history/mark_read should not be allowed"""
    response = self.make_request('/history/mark_read', 'GET')
    # Should return error (405 or 404)
    self.assertIn(response['status_code'], [404, 405])


if __name__ == '__main__':
  unittest.main()
