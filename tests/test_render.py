#!/usr/bin/env python3
"""
Tests for POST /render endpoint
"""

from test_utils import HTTPTestCase
import unittest
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))


class TestRenderEndpoint(HTTPTestCase):
  """Test cases for POST /render endpoint"""

  def test_post_render_simple_json(self):
    """Test POST /render with simple JSON input"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"name": "John", "age": 30}',
        'expr': 'Hello {{ name }}, you are {{ age }} years old!'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('Content-type'), 'text/plain')
    self.assertEqual(response['content'], 'Hello John, you are 30 years old!')

    # Check custom headers
    self.assertEqual(response['headers'].get('X-Result-Type'), 'string')
    self.assertEqual(response['headers'].get('X-Input-Format'), 'JSON')

  def test_post_render_yaml_input(self):
    """Test POST /render with YAML input"""
    response = self.make_request('/render', method='POST', data={
        'json': 'name: Jane\nage: 25\ncity: Paris',
        'expr': '{{ name }} lives in {{ city }} and is {{ age }} years old'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['content'], 'Jane lives in Paris and is 25 years old')
    self.assertEqual(response['headers'].get('X-Input-Format'), 'YAML')

  def test_post_render_json_output(self):
    """Test POST /render that produces JSON output"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"items": ["apple", "banana", "cherry"]}',
        'expr': '{"count": {{ items | length }}, "first": "{{ items[0] }}"}'
    })

    self.assertEqual(response['status_code'], 200)

    # Should detect JSON output and format it
    output = json.loads(response['content'])
    self.assertEqual(output['count'], 3)
    self.assertEqual(output['first'], 'apple')
    self.assertEqual(response['headers'].get('X-Result-Type'), 'json')

  def test_post_render_ansible_filters(self):
    """Test POST /render with Ansible filters"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"items": ["apple", "BANANA", "Cherry"]}',
        'expr': '{{ items | map("upper") | list | join(", ") }}'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['content'], 'APPLE, BANANA, CHERRY')

  def test_post_render_with_loop_enabled(self):
    """Test POST /render with loop functionality"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"users": [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]}',
        'expr': '{"name": "{{ item.name }}", "status": "active"}',
        'enable_loop': 'true',
        'loop_variable': 'users'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Loop-Enabled'), 'true')

    # Should return JSON array
    output = json.loads(response['content'])
    self.assertIsInstance(output, list)
    self.assertEqual(len(output), 2)
    self.assertEqual(output[0]['name'], 'John')
    self.assertEqual(output[1]['name'], 'Jane')

  def test_post_render_loop_with_data_prefix(self):
    """Test POST /render with loop using 'data.' prefix"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"my_items": ["a", "b", "c"]}',
        'expr': 'Item: {{ item }} (total: {{ data.my_items | length }})',
        'enable_loop': 'true',
        'loop_variable': 'my_items'  # Use a different name to avoid dict.items() conflict
    })

    self.assertEqual(response['status_code'], 200)

    output = json.loads(response['content'])
    self.assertIsInstance(output, list)
    self.assertEqual(len(output), 3)
    self.assertEqual(output[0], 'Item: a (total: 3)')
    self.assertEqual(output[1], 'Item: b (total: 3)')

  def test_post_render_invalid_json(self):
    """Test POST /render with invalid JSON input"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"invalid": json}',
        'expr': '{{ test }}'
    })

    self.assertEqual(response['status_code'], 400)
    # JSON is invalid but processed as YAML, then fails on undefined variable
    self.assertIn('jinja expression error', response['content'].lower())

  def test_post_render_invalid_yaml(self):
    """Test POST /render with invalid YAML input"""
    response = self.make_request('/render', method='POST', data={
        'json': 'invalid:\n  - yaml\n syntax: [',
        'expr': '{{ test }}'
    })

    self.assertEqual(response['status_code'], 400)
    self.assertIn('parsing error', response['content'].lower())

  def test_post_render_invalid_jinja_syntax(self):
    """Test POST /render with invalid Jinja2 syntax"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"test": "value"}',
        'expr': '{{ invalid | nonexistent_filter }}'
    })

    self.assertEqual(response['status_code'], 400)
    self.assertIn('jinja expression error', response['content'].lower())

  def test_post_render_undefined_variable(self):
    """Test POST /render with undefined variable"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"test": "value"}',
        'expr': '{{ undefined_variable }}'
    })

    self.assertEqual(response['status_code'], 400)
    self.assertIn('jinja expression error', response['content'].lower())

  def test_post_render_empty_input(self):
    """Test POST /render with empty input"""
    response = self.make_request('/render', method='POST', data={
        'json': '',
        'expr': 'Static text'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['content'], 'Static text')

  def test_post_render_saves_to_history(self):
    """Test POST /render saves entries to history"""
    # Clear history first
    self.make_request('/history/clear', method='POST', data={})

    # Make a render request
    response = self.make_request('/render', method='POST', data={
        'json': '{"test": "data"}',
        'expr': '{{ test }}'
    })

    self.assertEqual(response['status_code'], 200)

    # Check history was updated
    history_response = self.make_request('/history')
    history_data = json.loads(history_response['content'])

    self.assertEqual(len(history_data), 1)
    self.assertEqual(history_data[0]['input'], '{"test": "data"}')
    self.assertEqual(history_data[0]['expr'], '{{ test }}')

  def test_post_render_doesnt_save_empty_input_to_history(self):
    """Test POST /render doesn't save empty input to history"""
    # Clear history first
    self.make_request('/history/clear', method='POST', data={})

    # Make a render request with empty input
    response = self.make_request('/render', method='POST', data={
        'json': '   ',  # Only whitespace
        'expr': 'Static text'
    })

    self.assertEqual(response['status_code'], 200)

    # Check history wasn't updated
    history_response = self.make_request('/history')
    history_data = json.loads(history_response['content'])

    self.assertEqual(len(history_data), 0)

  def test_post_render_loop_invalid_variable(self):
    """Test POST /render with loop and invalid loop variable"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"items": ["a", "b"]}',
        'expr': '{{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'nonexistent'
    })

    self.assertEqual(response['status_code'], 400)
    self.assertIn('jinja expression error', response['content'].lower())

  def test_post_render_loop_non_array_variable(self):
    """Test POST /render with loop enabled but non-array variable"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"name": "John", "age": 30}',
        'expr': '{{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'name'
    })

    self.assertEqual(response['status_code'], 400)
    self.assertIn('must evaluate to an array/list', response['content'])

  def test_post_render_loop_nested_variable_path(self):
    """Test POST /render with loop on nested variable path"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"servers": {"web": [{"name": "web1"}, {"name": "web2"}]}}',
        'expr': 'Server: {{ item.name }}',
        'enable_loop': 'true',
        'loop_variable': 'servers.web'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Loop-Enabled'), 'true')

    # Should return JSON array of results
    result = json.loads(response['content'])
    self.assertIsInstance(result, list)
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0], 'Server: web1')
    self.assertEqual(result[1], 'Server: web2')

  def test_post_render_loop_with_data_prefix_nested(self):
    """Test POST /render with loop using data.prefix for nested access"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"config": {"servers": [{"id": 1}, {"id": 2}]}}',
        'expr': 'Server ID: {{ item.id }}, Total servers: {{ data.config.servers | length }}',
        'enable_loop': 'true',
        'loop_variable': 'config.servers'
    })

    self.assertEqual(response['status_code'], 200)
    result = json.loads(response['content'])
    self.assertIsInstance(result, list)
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0], 'Server ID: 1, Total servers: 2')
    self.assertEqual(result[1], 'Server ID: 2, Total servers: 2')

  def test_post_render_loop_json_output_parsing(self):
    """Test POST /render with loop that produces JSON objects"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"users": [{"name": "Alice", "role": "admin"}, {"name": "Bob", "role": "user"}]}',
        'expr': '{"user": "{{ item.name }}", "role": "{{ item.role }}", "active": true}',
        'enable_loop': 'true',
        'loop_variable': 'users'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Result-Type'), 'json')

    result = json.loads(response['content'])
    self.assertIsInstance(result, list)
    self.assertEqual(len(result), 2)

    # First item should be parsed as JSON object
    self.assertIsInstance(result[0], dict)
    self.assertEqual(result[0]['user'], 'Alice')
    self.assertEqual(result[0]['role'], 'admin')
    self.assertEqual(result[0]['active'], True)

  def test_post_render_empty_loop_variable_name(self):
    """Test POST /render with loop enabled but empty variable name"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"items": [1, 2, 3]}',
        'expr': '{{ item }}',
        'enable_loop': 'true',
        'loop_variable': ''
    })

    # Should return 400 because loop processing fails without proper variable
    self.assertEqual(response['status_code'], 400)
    self.assertIn("'item' is undefined", response['content'])

  def test_post_render_loop_with_jinja_expression_keys(self):
    """Test POST /render with loop using Jinja2 expression - services.keys() | list"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"services": {"web": "nginx", "api": "fastapi", "db": "postgres"}}',
        'expr': 'Service: {{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'services.keys() | list'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Loop-Enabled'), 'true')

    result = json.loads(response['content'])
    self.assertIsInstance(result, list)
    self.assertEqual(len(result), 3)

    # Should contain all service keys
    service_names = [item.replace('Service: ', '') for item in result]
    self.assertIn('web', service_names)
    self.assertIn('api', service_names)
    self.assertIn('db', service_names)

  def test_post_render_loop_with_jinja_expression_values(self):
    """Test POST /render with loop using Jinja2 expression - services.values() | list"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"services": {"web": "nginx", "api": "fastapi", "db": "postgres"}}',
        'expr': 'Technology: {{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'services.values() | list'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Loop-Enabled'), 'true')

    result = json.loads(response['content'])
    self.assertIsInstance(result, list)
    self.assertEqual(len(result), 3)

    # Should contain all service values
    technologies = [item.replace('Technology: ', '') for item in result]
    self.assertIn('nginx', technologies)
    self.assertIn('fastapi', technologies)
    self.assertIn('postgres', technologies)

  def test_post_render_loop_with_jinja_expression_range(self):
    """Test POST /render with loop using Jinja2 expression - range(5) | list"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"count": 5}',
        'expr': 'Number: {{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'range(5) | list'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Loop-Enabled'), 'true')

    result = json.loads(response['content'])
    self.assertIsInstance(result, list)
    self.assertEqual(len(result), 5)

    # Should contain numbers 0 through 4
    for i in range(5):
      self.assertEqual(result[i], f'Number: {i}')

  def test_post_render_loop_with_jinja_expression_data_access(self):
    """Test POST /render with loop using Jinja2 expression - data.services.keys() | list"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"services": {"web": "nginx", "api": "fastapi", "db": "postgres"}}',
        'expr': 'Service via data: {{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'data.services.keys() | list'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Loop-Enabled'), 'true')

    result = json.loads(response['content'])
    self.assertIsInstance(result, list)
    self.assertEqual(len(result), 3)

    # Should contain all service keys
    service_names = [item.replace('Service via data: ', '') for item in result]
    self.assertIn('web', service_names)
    self.assertIn('api', service_names)
    self.assertIn('db', service_names)

  def test_post_render_loop_with_jinja_expression_complex_filter(self):
    """Test POST /render with loop using complex Jinja2 expression with Ansible filters"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"users": [{"name": "Alice", "active": true}, {"name": "Bob", "active": false}, {"name": "Charlie", "active": true}]}',
        'expr': 'Active user: {{ item.name }}',
        'enable_loop': 'true',
        'loop_variable': 'users | selectattr("active") | list'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Loop-Enabled'), 'true')

    result = json.loads(response['content'])
    self.assertIsInstance(result, list)
    self.assertEqual(len(result), 2)  # Only active users

    # Should contain only active users
    active_users = [item.replace('Active user: ', '') for item in result]
    self.assertIn('Alice', active_users)
    self.assertIn('Charlie', active_users)
    self.assertNotIn('Bob', active_users)

  def test_post_render_loop_jinja_expression_invalid(self):
    """Test POST /render with loop using invalid Jinja2 expression"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"services": {"web": "nginx"}}',
        'expr': 'Service: {{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'nonexistent.keys() | list'
    })

    self.assertEqual(response['status_code'], 400)
    self.assertIn("Error evaluating loop variable", response['content'])

  def test_post_render_loop_jinja_expression_non_list_result(self):
    """Test POST /render with loop using Jinja2 expression that doesn't return a list"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"services": {"web": "nginx"}}',
        'expr': 'Service: {{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'services | length'  # Returns int, not list
    })

    self.assertEqual(response['status_code'], 400)
    self.assertIn("must evaluate to an array/list", response['content'])

  def test_post_render_with_custom_headers_validation(self):
    """Test POST /render validates all custom headers are present"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"test": "value"}',
        'expr': '{{ test | upper }}',
        'enable_loop': 'false',
        'loop_variable': ''
    })

    self.assertEqual(response['status_code'], 200)

    # Validate all expected custom headers
    self.assertIsNotNone(response['headers'].get('X-Result-Type'))
    self.assertIsNotNone(response['headers'].get('X-Input-Format'))
    self.assertIsNotNone(response['headers'].get('X-Actual-Type'))

    # X-Actual-Type should always be 'str' for Jinja2 output
    self.assertEqual(response['headers'].get('X-Actual-Type'), 'str')

  def test_post_render_yaml_input_with_headers(self):
    """Test POST /render with YAML input validates headers correctly"""
    response = self.make_request('/render', method='POST', data={
        'json': 'name: John\nage: 30\nactive: true',  # YAML format
        'expr': '{{ name }} is {{ age }} years old and {{ "active" if active else "inactive" }}',
        'enable_loop': 'false',
        'loop_variable': ''
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['headers'].get('X-Input-Format'), 'YAML')
    self.assertEqual(response['content'], 'John is 30 years old and active')

  def test_post_render_ansible_filter_with_headers(self):
    """Test POST /render with loop variable that's not an array"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"name": "John"}',
        'expr': '{{ item }}',
        'enable_loop': 'true',
        'loop_variable': 'name'
    })

    self.assertEqual(response['status_code'], 400)
    self.assertIn('jinja expression error', response['content'].lower())

  def test_post_render_complex_nested_data(self):
    """Test POST /render with complex nested data structures"""
    complex_data = {
        "company": {
            "name": "TechCorp",
            "employees": [
                {"name": "John", "department": "IT", "skills": ["Python", "Docker"]},
                {"name": "Jane", "department": "HR", "skills": ["Management"]}
            ]
        }
    }

    response = self.make_request('/render', method='POST', data={
        'json': json.dumps(complex_data),
        'expr': '{{ company.name }} has {{ company.employees | length }} employees'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['content'], 'TechCorp has 2 employees')

  def test_post_render_unicode_characters(self):
    """Test POST /render with Unicode characters"""
    response = self.make_request('/render', method='POST', data={
        'json': '{"message": "Hëllö Wörld! 🌍", "price": "€10"}',
        'expr': '{{ message }} - Price: {{ price }}'
    })

    self.assertEqual(response['status_code'], 200)
    self.assertEqual(response['content'], 'Hëllö Wörld! 🌍 - Price: €10')

  def test_render_duplicate_prevention_consecutive(self):
    """Test that consecutive identical render requests don't create duplicate history entries"""
    # Clear history first
    response = self.make_request('/history/clear', 'POST', {'count': '1000'})
    self.assertEqual(response['status_code'], 200)

    # First request
    test_data = {
        'json': '{"name": "duplicate_test"}',
        'expr': '{{ name | upper }}',
        'enable_loop': 'false',
        'loop_variable': ''
    }

    response1 = self.make_request('/render', 'POST', test_data)
    self.assertEqual(response1['status_code'], 200)
    self.assertEqual(response1['content'], 'DUPLICATE_TEST')

    # Get history size after first request
    history_response1 = self.make_request('/history')
    history1 = json.loads(history_response1['content'])
    initial_size = len(history1)

    # Second identical request
    response2 = self.make_request('/render', 'POST', test_data)
    self.assertEqual(response2['status_code'], 200)
    self.assertEqual(response2['content'], 'DUPLICATE_TEST')

    # Get history size after second request
    history_response2 = self.make_request('/history')
    history2 = json.loads(history_response2['content'])
    final_size = len(history2)

    # History size should be the same (duplicate not added)
    self.assertEqual(initial_size, final_size,
                     "Consecutive duplicate entry was incorrectly added to history")

  def test_render_duplicate_prevention_different_entries(self):
    """Test that different render requests create separate history entries"""
    # Clear history first
    self.make_request('/history/clear', 'POST', {'count': '1000'})

    # First request
    response1 = self.make_request('/render', 'POST', {
        'json': '{"name": "first"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    })
    self.assertEqual(response1['status_code'], 200)

    # Get history size
    history_response1 = self.make_request('/history')
    history1 = json.loads(history_response1['content'])
    size_after_first = len(history1)

    # Second request with different data
    response2 = self.make_request('/render', 'POST', {
        'json': '{"name": "second"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    })
    self.assertEqual(response2['status_code'], 200)

    # Get history size after second request
    history_response2 = self.make_request('/history')
    history2 = json.loads(history_response2['content'])
    size_after_second = len(history2)

    # History size should increase
    self.assertEqual(size_after_second, size_after_first + 1,
                     "Different entry was not added to history")

  def test_render_duplicate_prevention_non_consecutive(self):
    """Test that non-consecutive duplicate requests are saved"""
    # Clear history first
    self.make_request('/history/clear', 'POST', {'count': '1000'})

    # First request
    test_data1 = {
        'json': '{"name": "original"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    }
    response1 = self.make_request('/render', 'POST', test_data1)
    self.assertEqual(response1['status_code'], 200)

    # Different request in between
    response2 = self.make_request('/render', 'POST', {
        'json': '{"name": "different"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    })
    self.assertEqual(response2['status_code'], 200)

    # Get history size before repeating first request
    history_response_before = self.make_request('/history')
    history_before = json.loads(history_response_before['content'])
    size_before = len(history_before)

    # Repeat first request (non-consecutive duplicate)
    response3 = self.make_request('/render', 'POST', test_data1)
    self.assertEqual(response3['status_code'], 200)

    # Get history size after
    history_response_after = self.make_request('/history')
    history_after = json.loads(history_response_after['content'])
    size_after = len(history_after)

    # History size should increase (non-consecutive duplicate allowed)
    self.assertEqual(size_after, size_before + 1,
                     "Non-consecutive duplicate was not added to history")

  def test_render_duplicate_prevention_different_loop_settings(self):
    """Test that same data with different loop settings creates different entries"""
    # Clear history first
    self.make_request('/history/clear', 'POST', {'count': '1000'})

    # First request without loop
    response1 = self.make_request('/render', 'POST', {
        'json': '{"name": "test"}',
        'expr': '{{ name }}',
        'enable_loop': 'false',
        'loop_variable': ''
    })
    self.assertEqual(response1['status_code'], 200)

    # Get history size
    history_response1 = self.make_request('/history')
    history1 = json.loads(history_response1['content'])
    size_after_first = len(history1)

    # Second request with different loop variable
    response2 = self.make_request('/render', 'POST', {
        'json': '{"name": "test"}',     # Same input
        'expr': '{{ name }}',           # Same expression
        'enable_loop': 'false',         # Same loop setting
        'loop_variable': 'item'         # Different loop variable
    })
    self.assertEqual(response2['status_code'], 200)

    # Get history size after second request
    history_response2 = self.make_request('/history')
    history2 = json.loads(history_response2['content'])
    size_after_second = len(history2)

    # History size should increase (different loop variable makes it different)
    self.assertEqual(size_after_second, size_after_first + 1,
                     "Entry with different loop variable was not added to history")


if __name__ == '__main__':
  unittest.main()
