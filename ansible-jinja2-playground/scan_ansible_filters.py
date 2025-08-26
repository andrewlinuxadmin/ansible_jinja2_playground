#!/usr/bin/env python3
"""
Script to automatically scan all Ansible filters and tests
and verify their compatibility with ansible_jinja2_playground.

This script:
1. Discovers all available filters and tests in the installed Ansible
2. Tests each one via HTTP endpoint
3. Generates detailed compatibility report
4. Useful for verifying compatibility when changing Ansible versions

Author: ansible_jinja2_playground
Date: 2025-08-14
"""

import json
import requests
import sys
import importlib
from typing import Dict, List, Any, Tuple
import ansible


class AnsibleFilterScanner:
  """Scanner for Ansible filters and tests with compatibility testing."""

  def __init__(self, base_url: str = "http://localhost:8000"):
    self.base_url = base_url
    self.results = {
        'ansible_version': ansible.__version__,
        'discovered_filters': {},
        'discovered_tests': {},
        'compatibility_results': {},
        'summary': {}
    }

  def discover_filter_modules(self) -> List[str]:
    """Discovers all Ansible filter modules."""
    filter_modules = []

    # Known modules
    known_modules = [
        'core', 'mathstuff', 'urls', 'urlsplit',
        'encryption', 'json_query', 'network'
    ]

    for module_name in known_modules:
      try:
        module_path = f'ansible.plugins.filter.{module_name}'
        module = importlib.import_module(module_path)
        if hasattr(module, 'FilterModule'):
          filter_modules.append(module_name)
          print(f"✅ Discovered filter module: {module_name}")
      except ImportError as e:
        print(f"❌ Filter module not found: {module_name} - {e}")

    return filter_modules

  def discover_test_modules(self) -> List[str]:
    """Discovers all Ansible test modules."""
    test_modules = []

    # Known modules
    known_modules = [
        'core', 'files', 'mathstuff', 'uri'
    ]

    for module_name in known_modules:
      try:
        module_path = f'ansible.plugins.test.{module_name}'
        module = importlib.import_module(module_path)
        if hasattr(module, 'TestModule'):
          test_modules.append(module_name)
          print(f"✅ Discovered test module: {module_name}")
      except ImportError as e:
        print(f"❌ Test module not found: {module_name} - {e}")

    return test_modules

  def extract_filters_from_module(self, module_name: str) -> Dict[str, Any]:
    """Extracts all filters from a specific module."""
    try:
      module_path = f'ansible.plugins.filter.{module_name}'
      module = importlib.import_module(module_path)
      filter_module = module.FilterModule()
      filters = filter_module.filters()

      print(f"📦 Module {module_name}: {len(filters)} filters found")
      return filters

    except Exception as e:
      print(f"❌ Error extracting filters from {module_name}: {e}")
      return {}

  def extract_tests_from_module(self, module_name: str) -> Dict[str, Any]:
    """Extracts all tests from a specific module."""
    try:
      module_path = f'ansible.plugins.test.{module_name}'
      module = importlib.import_module(module_path)
      test_module = module.TestModule()
      tests = test_module.tests()

      print(f"🧪 Module {module_name}: {len(tests)} tests found")
      return tests

    except Exception as e:
      print(f"❌ Error extracting tests from {module_name}: {e}")
      return {}

  def discover_all_filters(self) -> Dict[str, Dict[str, Any]]:
    """Discovers all available filters in Ansible."""
    print("\\n🔍 DISCOVERING ANSIBLE FILTERS...")

    filter_modules = self.discover_filter_modules()
    all_filters = {}

    for module_name in filter_modules:
      module_filters = self.extract_filters_from_module(module_name)
      all_filters[module_name] = module_filters
      filter_names = list(module_filters.keys())
      self.results['discovered_filters'][module_name] = filter_names

    total_modules = len(filter_modules)
    total_filters = sum(len(filters) for filters in all_filters.values())
    print(f"\\n📊 Total filter modules: {total_modules}")
    print(f"📊 Total filters discovered: {total_filters}")

    return all_filters

  def discover_all_tests(self) -> Dict[str, Dict[str, Any]]:
    """Discovers all available tests in Ansible."""
    print("\\n🔍 DISCOVERING ANSIBLE TESTS...")

    test_modules = self.discover_test_modules()
    all_tests = {}

    for module_name in test_modules:
      module_tests = self.extract_tests_from_module(module_name)
      all_tests[module_name] = module_tests
      test_names = list(module_tests.keys())
      self.results['discovered_tests'][module_name] = test_names

    total_modules = len(test_modules)
    total_tests = sum(len(tests) for tests in all_tests.values())
    print(f"\\n📊 Total test modules: {total_modules}")
    print(f"📊 Total tests discovered: {total_tests}")

    return all_tests

  def generate_test_cases(self) -> Dict[str, str]:
    """Generates test cases for common filters and tests."""
    test_cases = {
        # String filters
        'regex_search': '{{ "foobar" | regex_search("o+") }}',
        'regex_replace': '{{ "foo" | regex_replace("o", "a") }}',
        'regex_findall': '{{ "foo bar" | regex_findall("[a-z]+") }}',
        'regex_escape': '{{ "^f.*o(.*)" | regex_escape }}',

        # Conversion filters
        'from_yaml': '{{ "a: 1\\nb: 2" | from_yaml }}',
        'from_json': '{{ \'{"a": 1, "b": 2}\' | from_json }}',
        'to_yaml': '{{ ["a", "b"] | to_yaml }}',
        'to_json': '{{ ["a", "b"] | to_json }}',

        # List/dict filters
        'dict2items': '{{ {"a": 1, "b": 2} | dict2items }}',
        'items2dict': '{{ [{"key": "a", "value": 1}] | items2dict }}',
        'flatten': '{{ [[1, 2], [3, 4]] | flatten }}',
        'unique': '{{ ["a", "b", "a", "c", "b"] | unique }}',
        'intersect': '{{ ["a", "b", "c"] | intersect(["a", "b"]) }}',
        'difference': '{{ ["a", "b", "c"] | difference(["a"]) }}',
        'combine': '{{ {"a": 1} | combine({"b": 2}) }}',
        'zip': '{{ [1, 2] | zip([3, 4]) }}',
        'zip_longest': '{{ [1, 2] | zip_longest([3, 4, 5], fillvalue=0) }}',
        'symmetric_difference': '{{ [1, 2, 3] | symmetric_difference([2, 3, 4]) }}',

        # Encoding filters
        'b64encode': '{{ "foo" | b64encode }}',
        'b64decode': '{{ "Zm9v" | b64decode }}',
        'md5': '{{ "foo" | md5 }}',
        'sha1': '{{ "foo" | sha1 }}',
        'hash': '{{ "foo" | hash("sha256") }}',
        'password_hash': '{{ "foo" | password_hash("sha256_crypt", "salt") }}',

        # Math filters
        'log': '{{ 100 | log }}',
        'pow': '{{ 2 | pow(3) }}',
        'root': '{{ 8 | root(3) }}',
        'abs': '{{ -5 | abs }}',

        # Path filters
        'expanduser': '{{ "~/foo" | expanduser }}',
        'expandvars': '{{ "$HOME/foo" | expandvars }}',
        'basename': '{{ "/foo/bar.txt" | basename }}',
        'dirname': '{{ "/foo/bar.txt" | dirname }}',
        'splitext': '{{ "/foo/bar.txt" | splitext }}',
        'normpath': '{{ "/foo/../bar" | normpath }}',

        # URL filters
        'urlsplit': '{{ "http://example.com/path?q=1" | urlsplit }}',
        'urljoin': '{{ "http://example.com" | urljoin("/path") }}',

        # File tests
        'is_file': '{{ "/tmp/test" is is_file }}',
        'is_dir': '{{ "/tmp" is is_dir }}',
        'exists': '{{ "/tmp" is exists }}',
        'is_abs': '{{ "/tmp/test" is is_abs }}',

        # Math tests
        'issubset': '{{ [1, 2] is issubset([1, 2, 3]) }}',
        'issuperset': '{{ [1, 2, 3] is issuperset([1, 2]) }}',
        'contains': '{{ [1, 2, 3] is contains(2) }}',
        'isnan': '{{ "nan"|float is isnan }}',
        'isinf': '{{ "inf"|float is isinf }}',

        # URI tests
        'uri': '{{ "http://example.com" is uri }}',
        'url': '{{ "http://example.com" is url }}',

        # String tests
        'match': '{{ "foo123" is match("foo.*") }}',
        'search': '{{ "foo123" is search("\\d+") }}',
        'regex': '{{ "foo123" is regex("foo.*") }}',

        # Type tests
        'string': '{{ "foo" is string }}',
        'number': '{{ 123 is number }}',
        'integer': '{{ 123 is integer }}',
        'float': '{{ 1.23 is float }}',
        'boolean': '{{ true is boolean }}',
        'list': '{{ [] is list }}',
        'dict': '{{ {} is dict }}',
        'mapping': '{{ {} is mapping }}',
        'sequence': '{{ [] is sequence }}',
        'iterable': '{{ [] is iterable }}',
    }

    return test_cases

  def test_filter_via_endpoint(self, filter_name: str,
                               test_expression: str) -> Tuple[bool, str]:
    """Tests a specific filter via HTTP endpoint."""
    try:
      # ansible_jinja2_playground expects form data, not JSON
      payload = {
          'expr': test_expression,
          'json': '{}'  # Empty data in JSON
      }

      response = requests.post(f"{self.base_url}/render",
                               data=payload, timeout=5)

      if response.status_code == 200:
        # Response is text/plain with the result
        response_text = response.text.strip()
        return True, f"SUCCESS: {response_text}"
      else:
        return False, f"ERROR: {response.status_code} - {response.text}"

    except Exception as e:
      return False, f"EXCEPTION: {str(e)}"

  def test_all_compatibility(self) -> Dict[str, Any]:
    """Tests compatibility of all discovered filters."""
    print("\\n🧪 TESTING COMPATIBILITY VIA ENDPOINT...")

    test_cases = self.generate_test_cases()
    all_filters = self.discover_all_filters()
    all_tests = self.discover_all_tests()

    # Collect all filter and test names
    all_filter_names = set()
    for module_filters in all_filters.values():
      all_filter_names.update(module_filters.keys())

    all_test_names = set()
    for module_tests in all_tests.values():
      all_test_names.update(module_tests.keys())

    print(f"🎯 Testing {len(all_filter_names)} filters and "
          f"{len(all_test_names)} tests...")

    results = {}
    success_count = 0
    total_count = 0

    # Test filters with known test cases
    for name in all_filter_names:
      if name in test_cases:
        total_count += 1
        success, message = self.test_filter_via_endpoint(name,
                                                         test_cases[name])
        results[name] = {
            'type': 'filter',
            'tested': True,
            'success': success,
            'message': message,
            'test_case': test_cases[name]
        }
        if success:
          success_count += 1
          print(f"✅ {name}: {message[:50]}...")
        else:
          print(f"❌ {name}: {message[:50]}...")
      else:
        results[name] = {
            'type': 'filter',
            'tested': False,
            'success': None,
            'message': 'No test case available',
            'test_case': None
        }
        print(f"⚠️  {name}: Not tested (no test case)")

    # Test tests with known test cases
    for name in all_test_names:
      if name in test_cases:
        total_count += 1
        success, message = self.test_filter_via_endpoint(name,
                                                         test_cases[name])
        results[name] = {
            'type': 'test',
            'tested': True,
            'success': success,
            'message': message,
            'test_case': test_cases[name]
        }
        if success:
          success_count += 1
          print(f"✅ {name}: {message[:50]}...")
        else:
          print(f"❌ {name}: {message[:50]}...")
      else:
        results[name] = {
            'type': 'test',
            'tested': False,
            'success': None,
            'message': 'No test case available',
            'test_case': None
        }
        print(f"⚠️  {name}: Not tested (no test case)")

    self.results['compatibility_results'] = results

    # Calculate summary
    total_discovered = len(all_filter_names) + len(all_test_names)
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0

    self.results['summary'] = {
        'total_discovered': total_discovered,
        'total_tested': total_count,
        'total_success': success_count,
        'success_rate': success_rate,
        'filters_discovered': len(all_filter_names),
        'tests_discovered': len(all_test_names)
    }

    return results

  def generate_report(self) -> str:
    """Generates detailed compatibility report."""
    summary = self.results.get('summary', {})

    # Calculate totals if not in summary
    if not summary:
      filters = self.results.get('discovered_filters', {})
      tests = self.results.get('discovered_tests', {})
      total_filters = sum(len(f) for f in filters.values())
      total_tests = sum(len(t) for t in tests.values())
      summary = {
          'total_discovered': total_filters + total_tests,
          'total_tested': 0,
          'total_success': 0,
          'success_rate': 0,
          'filters_discovered': total_filters,
          'tests_discovered': total_tests
      }

    report = f"""
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                        ANSIBLE COMPATIBILITY REPORT                                 ║
║                            ansible_jinja2_playground                                 ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

📊 EXECUTIVE SUMMARY:
├─ Ansible Version: {self.results['ansible_version']}
├─ Total Discovered: {summary['total_discovered']} (filters + tests)
├─ Total Tested: {summary['total_tested']}
├─ Total Working: {summary['total_success']}
├─ Success Rate: {summary['success_rate']:.1f}%
├─ Filters Discovered: {summary['filters_discovered']}
└─ Tests Discovered: {summary['tests_discovered']}

🎯 WORKING FILTERS AND TESTS:
"""

    working_items = []
    failing_items = []
    untested_items = []

    results = self.results.get('compatibility_results', {})
    for name, result in results.items():
      if result['tested']:
        if result['success']:
          working_items.append(f"✅ {name} ({result['type']})")
        else:
          msg = result['message'][:60] + "..."
          failing_items.append(f"❌ {name} ({result['type']}): {msg}")
      else:
        msg = result['message']
        untested_items.append(f"⚠️  {name} ({result['type']}): {msg}")

    report += "\\n".join(working_items)

    if failing_items:
      count = len(failing_items)
      report += f"\\n\\n❌ FILTERS/TESTS WITH PROBLEMS ({count}):\\n"
      report += "\\n".join(failing_items)

    if untested_items:
      count = len(untested_items)
      report += f"\\n\\n⚠️  FILTERS/TESTS NOT TESTED ({count}):\\n"
      # Limit display to prevent very long output
      report += "\\n".join(untested_items[:10])
      if len(untested_items) > 10:
        remaining = len(untested_items) - 10
        report += f"\\n... and {remaining} more items"

    report += "\\n\\n🔧 DISCOVERED MODULES:\\n\\n📦 Filter Modules:\\n"

    filters = self.results.get('discovered_filters', {})
    for module, filter_list in filters.items():
      report += f"├─ {module}: {len(filter_list)} filters\\n"

    report += "\\n🧪 Test Modules:\\n"
    tests = self.results.get('discovered_tests', {})
    for module, test_list in tests.items():
      report += f"├─ {module}: {len(test_list)} tests\\n"

    report += """
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║ This report was generated automatically by scan_ansible_filters.py                  ║
║ To verify compatibility when changing Ansible versions, run again                   ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
"""

    return report

  def save_results(self, filename: str = "ansible_compatibility_scan.json"):
    """Saves complete results to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
      json.dump(self.results, f, indent=2, ensure_ascii=False,
                default=str)
    print(f"💾 Results saved to: {filename}")

  def run_full_scan(self):
    """Runs complete scan and generates report."""
    print("🚀 STARTING COMPLETE ANSIBLE COMPATIBILITY SCAN")
    print("=" * 80)

    # Discover and test everything
    self.test_all_compatibility()

    # Generate and display report
    report = self.generate_report()
    print(report)

    # Save results
    self.save_results()

    return self.results


def main():
  """Main function of the script."""
  import argparse

  parser = argparse.ArgumentParser(
      description='Ansible compatibility scanner')
  parser.add_argument('--url', default='http://localhost:8000',
                      help='Base URL for ansible_jinja2_playground '
                      '(default: http://localhost:8000)')
  parser.add_argument('--output', default='ansible_compatibility_scan.json',
                      help='JSON output file '
                      '(default: ansible_compatibility_scan.json)')
  parser.add_argument('--report-only', action='store_true',
                      help='Only generate report without testing endpoints')

  args = parser.parse_args()

  try:
    scanner = AnsibleFilterScanner(base_url=args.url)

    if args.report_only:
      # Only discover without testing
      scanner.discover_all_filters()
      scanner.discover_all_tests()
      print(scanner.generate_report())
    else:
      # Complete scan with tests
      scanner.run_full_scan()

    scanner.save_results(args.output)

  except KeyboardInterrupt:
    print("\\n\\n⚠️  Scan interrupted by user")
    sys.exit(1)
  except Exception as e:
    print(f"\\n\\n❌ Error during scan: {e}")
    sys.exit(1)


if __name__ == "__main__":
  main()
