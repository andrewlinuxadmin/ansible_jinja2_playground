#!/usr/bin/env python3
"""
Tests for 404 endpoint (not found)
"""

from test_utils import HTTPTestCase
import unittest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))


class Test404Endpoint(HTTPTestCase):
  """Test cases for 404 (not found) endpoints"""

  def test_get_invalid_endpoint(self):
    """Test GET request to invalid endpoint returns 404"""
    response = self.make_request('/invalid-endpoint')

    self.assertEqual(response['status_code'], 404)

  def test_post_invalid_endpoint(self):
    """Test POST request to invalid endpoint returns 404"""
    response = self.make_request('/invalid-endpoint', method='POST', data={
        'test': 'data'
    })

    self.assertEqual(response['status_code'], 404)

  def test_get_root_with_trailing_slash(self):
    """Test GET request to root with trailing slash"""
    response = self.make_request('/')

    # Should return the main page (200), not 404
    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('Content-type'), 'text/html')

  def test_get_nonexistent_nested_path(self):
    """Test GET request to non-existent nested path"""
    response = self.make_request('/api/v1/nonexistent')

    self.assertEqual(response['status_code'], 404)

  def test_put_method_not_allowed(self):
    """Test PUT method (not implemented) to valid endpoint"""
    response = self.make_request('/history', method='PUT', data={})

    # Should return method not allowed, not implemented, or 404
    self.assertIn(response['status_code'], [404, 405, 501])


if __name__ == '__main__':
  unittest.main()
