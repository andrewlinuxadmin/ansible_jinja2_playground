#!/usr/bin/env python3
"""
Tests for the main page endpoint (GET /)
"""

import unittest
from test_utils import HTTPTestCase


class TestMainPageEndpoint(HTTPTestCase):
  """Test cases for GET / endpoint"""

  def test_get_main_page_returns_html(self):
    """Test that GET / returns HTML page"""
    response = self.make_request('/')

    self.assertEqual(response['status_code'], 200)
    content_type = response['headers'].get('Content-type', '') or response['headers'].get('Content-Type', '')
    self.assertIn('text/html', content_type)
    self.assertIn('<html', response['content'].lower())
    self.assertIn('ansible jinja2 playground', response['content'].lower())

  def test_get_main_page_contains_required_elements(self):
    """Test that main page contains required HTML elements"""
    response = self.make_request('/')
    content = response['content'].lower()

    # Check for key elements that should be in the playground
    self.assertIn('<title>', content)
    self.assertIn('<body>', content)
    self.assertIn('<head>', content)

    # Check for form or interactive elements (common in web playgrounds)
    # This might need adjustment based on actual HTML content
    self.assertTrue(
      any(element in content for element in ['<form', '<textarea', '<input', '<button']),
      "Main page should contain interactive elements"
    )

  def test_get_main_page_encoding(self):
    """Test that main page is properly UTF-8 encoded"""
    response = self.make_request('/')

    self.assertEqual(response['status_code'], 200)
    # Should not raise encoding errors
    self.assertIsInstance(response['content'], str)

    # Test with non-ASCII characters if they exist in the page
    try:
      response['content'].encode('utf-8')
    except UnicodeEncodeError:
      self.fail("Main page content is not properly UTF-8 encoded")


if __name__ == '__main__':
  unittest.main()
