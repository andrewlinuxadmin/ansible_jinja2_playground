import unittest
import json
import sys
import os

# Add the app directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from test_utils import HTTPTestCase


class TestSimpleDuplicatePrevention(HTTPTestCase):
    """Simple test for duplicate prevention"""

    def test_simple_duplicate_prevention(self):
        """Test basic duplicate prevention"""
        # Clear history first
        response = self.make_request('/history/clear', 'POST', {'count': '1000'})
        print(f"Clear response: {response}")

        # Make first request
        test_data = {
            'json': '{"name": "test"}',
            'expr': '{{ name }}',
            'enable_loop': 'false',
            'loop_variable': ''
        }

        response1 = self.make_request('/render', 'POST', test_data)
        print(f"First response: {response1}")

        if response1['status_code'] != 200:
            print(f"First request failed: {response1['content']}")
            return

        # Get history
        history_response1 = self.make_request('/history')
        history1 = json.loads(history_response1['content'])
        print(f"History after first: {len(history1)} entries")

        # Make identical second request
        response2 = self.make_request('/render', 'POST', test_data)
        print(f"Second response: {response2}")

        if response2['status_code'] != 200:
            print(f"Second request failed: {response2['content']}")
            return

        # Get history again
        history_response2 = self.make_request('/history')
        history2 = json.loads(history_response2['content'])
        print(f"History after second: {len(history2)} entries")

        # Check if duplicate was prevented
        print(f"Duplicate prevented: {len(history1) == len(history2)}")


if __name__ == '__main__':
    unittest.main()
