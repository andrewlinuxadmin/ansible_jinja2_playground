from test_utils import HTTPTestCase
import unittest
import json
import os
import time
import sys

# Add the ansible-jinja2-playground directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ansible-jinja2-playground'))


class TestHistoryDuplicatePreventionIntegration(HTTPTestCase):
  """Integration test for preventing duplicate consecutive history entries"""

  def test_duplicate_entries_not_saved_consecutively(self):
    """Test that identical consecutive entries are not saved to history"""
    # Clear history first
    response = self.make_request('/history/clear', 'POST', {'count': '1000'})
    self.assertEqual(response['status_code'], 200)

    # First request with specific data
    test_data = {
        'json': '{"name": "test_duplicate"}',
        'expr': '{{ name | upper }}',
        'enable_loop': 'false',
        'loop_variable': ''
    }

    # Make first request
    response1 = self.make_request('/render', 'POST', test_data)
    self.assertEqual(response1['status_code'], 200)
    self.assertEqual(response1['content'].strip(), 'TEST_DUPLICATE')

    # Get history size after first request
    history_response1 = self.make_request('/history')
    self.assertEqual(history_response1['status_code'], 200)
    history1 = json.loads(history_response1['content'])
    initial_size = len(history1)

    # Wait a moment to ensure different timestamps
    time.sleep(0.1)

    # Make second identical request
    response2 = self.make_request('/render', 'POST', test_data)
    self.assertEqual(response2['status_code'], 200)
    self.assertEqual(response2['content'].strip(), 'TEST_DUPLICATE')

    # Get history size after second request
    history_response2 = self.make_request('/history')
    self.assertEqual(history_response2['status_code'], 200)
    history2 = json.loads(history_response2['content'])
    final_size = len(history2)

    # History size should be the same (duplicate not added)
    self.assertEqual(initial_size, final_size,
                     "Duplicate entry was incorrectly added to history")

  def test_different_entries_are_saved(self):
    """Test that different entries are properly saved to history"""
    # Clear history first
    response = self.make_request('/history/clear', 'POST', {'count': '1000'})
    self.assertEqual(response['status_code'], 200)

    # First request
    test_data1 = {
        'json': '{"name": "first"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    }

    response1 = self.make_request('/render', 'POST', test_data1)
    self.assertEqual(response1['status_code'], 200)

    # Get history size after first request
    history_response1 = self.make_request('/history')
    history1 = json.loads(history_response1['content'])
    size_after_first = len(history1)

    # Second request with different data
    test_data2 = {
        'json': '{"name": "second"}',  # Different input
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    }

    response2 = self.make_request('/render', 'POST', test_data2)
    self.assertEqual(response2['status_code'], 200)

    # Get history size after second request
    history_response2 = self.make_request('/history')
    history2 = json.loads(history_response2['content'])
    size_after_second = len(history2)

    # History size should increase (different entry added)
    self.assertEqual(size_after_second, size_after_first + 1,
                     "Different entry was not added to history")

  def test_duplicate_after_different_entry_is_saved(self):
    """Test that duplicate of a non-consecutive entry is saved"""
    # Clear history first
    response = self.make_request('/history/clear', 'POST', {'count': '1000'})
    self.assertEqual(response['status_code'], 200)

    # First request
    test_data1 = {
        'json': '{"name": "original"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    }

    response1 = self.make_request('/render', 'POST', test_data1)
    self.assertEqual(response1['status_code'], 200)

    # Second request with different data
    test_data2 = {
        'json': '{"name": "different"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    }

    response2 = self.make_request('/render', 'POST', test_data2)
    self.assertEqual(response2['status_code'], 200)

    # Get history size before third request
    history_response_before = self.make_request('/history')
    history_before = json.loads(history_response_before['content'])
    size_before_third = len(history_before)

    # Third request - same as first (should be saved since it's not consecutive)
    response3 = self.make_request('/render', 'POST', test_data1)
    self.assertEqual(response3['status_code'], 200)

    # Get history size after third request
    history_response_after = self.make_request('/history')
    history_after = json.loads(history_response_after['content'])
    size_after_third = len(history_after)

    # History size should increase (non-consecutive duplicate added)
    self.assertEqual(size_after_third, size_before_third + 1,
                     "Non-consecutive duplicate was not added to history")

  def test_different_loop_settings_create_different_entries(self):
    """Test that same data with different loop settings creates separate entries"""
    # Clear history first
    response = self.make_request('/history/clear', 'POST', {'count': '1000'})
    self.assertEqual(response['status_code'], 200)

    # First request without loop
    test_data1 = {
        'json': '{"name": "test"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    }

    response1 = self.make_request('/render', 'POST', test_data1)
    self.assertEqual(response1['status_code'], 200)

    # Get history size after first request
    history_response1 = self.make_request('/history')
    history1 = json.loads(history_response1['content'])
    size_after_first = len(history1)

    # Second request with different loop variable (same data, different settings)
    test_data2 = {
        'json': '{"name": "test"}',     # Same input
        'expr': '{{ name }}',           # Same expression
        'enable_loop': 'false',         # Same loop setting
        'loop_variable': 'item'         # Different loop variable
    }

    response2 = self.make_request('/render', 'POST', test_data2)
    self.assertEqual(response2['status_code'], 200)

    # Get history size after second request
    history_response2 = self.make_request('/history')
    history2 = json.loads(history_response2['content'])
    size_after_second = len(history2)

    # History size should increase (different loop variable makes it a different entry)
    self.assertEqual(size_after_second, size_after_first + 1,
                     "Entry with different loop variable was not added to history")


if __name__ == '__main__':
  unittest.main()
