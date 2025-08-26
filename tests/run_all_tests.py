#!/usr/bin/env python3
"""
Test runner script for all API endpoints
Executes all unit tests and generates detailed logs
"""

import unittest
import sys
import os
import time
import datetime
import json
from io import StringIO


def discover_and_run_tests():
  """Discover and run all tests, generating detailed logs"""

  # Set up paths
  test_dir = os.path.dirname(os.path.abspath(__file__))

  # Create logs directory
  logs_dir = os.path.join(test_dir, 'logs')
  os.makedirs(logs_dir, exist_ok=True)

  # Generate log filename with timestamp
  timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
  log_file = os.path.join(logs_dir, f'test_results_{timestamp}.log')
  json_log_file = os.path.join(logs_dir, f'test_results_{timestamp}.json')

  print(f"🚀 Starting test execution at {datetime.datetime.now()}")
  print("📋 Log files will be saved to:")
  print(f"   - Text log: {log_file}")
  print(f"   - JSON log: {json_log_file}")
  print("=" * 70)

  # Discover all test modules
  test_modules = [
      'test_main_page',
      'test_history_endpoints',
      'test_settings_endpoints',
      'test_input_files_endpoints',
      'test_render',
      'test_404'
  ]

  # Results tracking
  results = {
      'timestamp': datetime.datetime.now().isoformat(),
      'total_tests': 0,
      'passed': 0,
      'failed': 0,
      'errors': 0,
      'modules': {},
      'duration': 0
  }

  start_time = time.time()

  # Capture output for logging
  log_content = []
  log_content.append(f"Test Execution Report - {results['timestamp']}")
  log_content.append("=" * 70)

  # Execute tests module by module
  for module_name in test_modules:
    print(f"\n🧪 Testing module: {module_name}")
    log_content.append(f"\n📦 Module: {module_name}")
    log_content.append("-" * 40)

    try:
      # Import and run the test module
      module = __import__(module_name)
      loader = unittest.TestLoader()
      suite = loader.loadTestsFromModule(module)

      # Create a test runner with detailed output
      stream = StringIO()
      runner = unittest.TextTestRunner(
          stream=stream,
          verbosity=2,
          buffer=True
      )

      # Run the tests
      result = runner.run(suite)

      # Process results for this module
      module_results = {
          'tests_run': result.testsRun,
          'failures': len(result.failures),
          'errors': len(result.errors),
          'passed': result.testsRun - len(result.failures) - len(result.errors),
          'details': {
              'failures': [{'test': str(test), 'error': error} for test, error in result.failures],
              'errors': [{'test': str(test), 'error': error} for test, error in result.errors]
          }
      }

      # Update overall results
      results['total_tests'] += module_results['tests_run']
      results['passed'] += module_results['passed']
      results['failed'] += module_results['failures']
      results['errors'] += module_results['errors']
      results['modules'][module_name] = module_results

      # Display module results
      print(f"   ✅ Passed: {module_results['passed']}")
      print(f"   ❌ Failed: {module_results['failures']}")
      print(f"   💥 Errors: {module_results['errors']}")

      # Log module results
      log_content.append(f"Tests run: {module_results['tests_run']}")
      log_content.append(f"Passed: {module_results['passed']}")
      log_content.append(f"Failed: {module_results['failures']}")
      log_content.append(f"Errors: {module_results['errors']}")

      # Add test output to log
      test_output = stream.getvalue()
      if test_output:
        log_content.append("\nDetailed output:")
        log_content.append(test_output)

      # Show failures and errors
      if result.failures:
        print("   💔 Failures:")
        for test, error in result.failures:
          print(f"      - {test}")
          log_content.append(f"\nFAILURE: {test}")
          log_content.append(error)

      if result.errors:
        print("   💥 Errors:")
        for test, error in result.errors:
          print(f"      - {test}")
          log_content.append(f"\nERROR: {test}")
          log_content.append(error)

    except Exception as e:
      print(f"   💥 Failed to load/run module: {e}")
      log_content.append(f"CRITICAL ERROR loading module: {e}")
      results['errors'] += 1

  # Calculate duration
  end_time = time.time()
  results['duration'] = round(end_time - start_time, 2)

  # Final summary
  print("\n" + "=" * 70)
  print("📊 FINAL TEST SUMMARY")
  print("=" * 70)
  print(f"🏁 Total tests executed: {results['total_tests']}")
  print(f"✅ Passed: {results['passed']}")
  print(f"❌ Failed: {results['failed']}")
  print(f"💥 Errors: {results['errors']}")
  print(f"⏱️  Total duration: {results['duration']} seconds")

  success_rate = (results['passed'] / results['total_tests'] * 100) if results['total_tests'] > 0 else 0
  print(f"📈 Success rate: {success_rate:.1f}%")

  if results['failed'] == 0 and results['errors'] == 0:
    print("\n🎉 ALL TESTS PASSED! 🎉")
    exit_code = 0
  else:
    print("\n⚠️  SOME TESTS FAILED OR HAD ERRORS")
    exit_code = 1

  # Generate text log
  log_content.append("\n" + "=" * 70)
  log_content.append("FINAL SUMMARY")
  log_content.append("=" * 70)
  log_content.append(f"Total tests: {results['total_tests']}")
  log_content.append(f"Passed: {results['passed']}")
  log_content.append(f"Failed: {results['failed']}")
  log_content.append(f"Errors: {results['errors']}")
  log_content.append(f"Duration: {results['duration']} seconds")
  log_content.append(f"Success rate: {success_rate:.1f}%")

  # Write text log
  with open(log_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_content))

  # Write JSON log
  with open(json_log_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

  print("\n📝 Detailed logs saved to:")
  print(f"   - {log_file}")
  print(f"   - {json_log_file}")

  return exit_code


if __name__ == '__main__':
  exit_code = discover_and_run_tests()
  sys.exit(exit_code)
