import unittest
import tempfile
import json
import os
import base64
import sys

# Add the app directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from ansible_jinja2_playground import entries_are_identical


class TestHistoryDuplicatePrevention(unittest.TestCase):
    """Test cases for preventing duplicate consecutive history entries"""

    def test_entries_are_identical_same_content(self):
        """Test that identical entries (excluding datetime) are detected"""
        entry1 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        entry2 = {
            'datetime': '2025-08-08T12:01:00Z',  # Different datetime
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        self.assertTrue(entries_are_identical(entry1, entry2))

    def test_entries_are_identical_different_content(self):
        """Test that different entries are not detected as identical"""
        entry1 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        entry2 = {
            'datetime': '2025-08-08T12:00:00Z',  # Same datetime
            'input': base64.b64encode('{"name": "different"}'.encode()).decode(),  # Different input
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        self.assertFalse(entries_are_identical(entry1, entry2))

    def test_entries_are_identical_different_expr(self):
        """Test that entries with different expressions are not identical"""
        entry1 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        entry2 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name | upper }}'.encode()).decode(),  # Different expression
            'enable_loop': False,
            'loop_variable': ''
        }

        self.assertFalse(entries_are_identical(entry1, entry2))

    def test_entries_are_identical_different_loop_settings(self):
        """Test that entries with different loop settings are not identical"""
        entry1 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        entry2 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': True,  # Different loop setting
            'loop_variable': 'item'  # Different loop variable
        }

        self.assertFalse(entries_are_identical(entry1, entry2))

    def test_entries_are_identical_with_empty_entries(self):
        """Test that function handles empty/None entries gracefully"""
        entry1 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        self.assertFalse(entries_are_identical(entry1, None))
        self.assertFalse(entries_are_identical(None, entry1))
        self.assertFalse(entries_are_identical(None, None))

    def test_entries_are_identical_missing_fields(self):
        """Test that entries with missing fields are handled correctly"""
        entry1 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        entry2 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode()
            # Missing other fields
        }

        self.assertFalse(entries_are_identical(entry1, entry2))

    def test_entries_datetime_ignored(self):
        """Test that datetime differences are properly ignored"""
        entry1 = {
            'datetime': '2025-08-08T12:00:00Z',
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        entry2 = {
            'datetime': '2025-08-08T15:30:45Z',  # Very different datetime
            'input': base64.b64encode('{"name": "test"}'.encode()).decode(),
            'expr': base64.b64encode('{{ name }}'.encode()).decode(),
            'enable_loop': False,
            'loop_variable': ''
        }

        self.assertTrue(entries_are_identical(entry1, entry2))


if __name__ == '__main__':
    unittest.main()
