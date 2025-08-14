# 🧪 Test Suite - Ansible Jinja2 Playground

This directory contains a complete unit test suite for all API endpoints of the
Ansible Jinja2 Playground.

## 📋 Overview

The test suite covers **10 endpoints** with **63 tests** in total following
strict coding style guidelines.

### 🎯 Tested Endpoints

| Endpoint | Method | Tests | File |
|----------|--------|---------|---------|
| `/` | GET | 3 | `test_main_page.py` |
| `/history/*` | GET/POST | 9 | `test_history_endpoints.py` |
| `/settings` | GET/POST | 14 | `test_settings_endpoints.py` |
| `/input-files/*` | GET | 11 | `test_input_files_endpoints.py` |
| `/render` | POST | 21 | `test_render.py` |
| **404/Invalid** | GET/POST | 5 | `test_404.py` |

### ✨ Tested Features

- ✅ **HTTP Response Validation** - Status codes, headers, content-type
- ✅ **JSON/YAML Processing** - Parsing, validation, data structure
- ✅ **Security** - Path validation, input sanitization
- ✅ **Jinja2 Functionality** - Templates, Ansible filters, loops
- ✅ **History Management** - Persistence, cleanup, entry limits
- ✅ **Dynamic Configuration** - Reading/writing configurations
- ✅ **Input Files** - Listing, reading, security validation
- ✅ **UTF-8 Encoding** - Special characters, emojis
- ✅ **Error Handling** - Invalid inputs, undefined variables

## 🚀 How to Run

### Run All Tests

```bash
cd tests/
python run_all_tests.py
```

### Run Specific Test

```bash
cd tests/
python test_main_page.py
python test_render.py
# etc...
```

### Run with Unittest

```bash
cd tests/
python -m unittest test_render.TestRenderEndpoint.test_post_render_simple_json -v
```

## 📊 Logs and Reports

Tests generate detailed logs in two formats:

### 📝 Text Log

- **Location**: `tests/logs/test_results_YYYYMMDD_HHMMSS.log`
- **Content**: Detailed output of each test, failures, errors
- **Format**: Plain text, easy to read

### 📊 JSON Log

- **Location**: `tests/logs/test_results_YYYYMMDD_HHMMSS.json`
- **Content**: Structured data for programmatic analysis
- **Format**: JSON with metrics, statistics, details

### Example Output

```text
🚀 Starting test execution at 2025-08-08 11:35:52
📋 Log files will be saved to:
   - Text log: tests/logs/test_results_20250808_113552.log
   - JSON log: tests/logs/test_results_20250808_113552.json

🧪 Testing module: test_render
   ✅ Passed: 17
   ❌ Failed: 0
   💥 Errors: 0

📊 FINAL TEST SUMMARY
🏁 Total tests executed: 63
✅ Passed: 63
⏱️  Total duration: 3.88 seconds
📈 Success rate: 100.0%

🎉 ALL TESTS PASSED! 🎉
```

## 🏗️ Test Structure

### Base Class: `HTTPTestCase`

- **File**: `test_utils.py`
- **Functionality**:
  - HTTP server setup/teardown
  - Helper methods for HTTP requests
  - Temporary configuration management
  - Automatic cleanup of temporary files

### Test Pattern

Each test file follows the coding style guidelines:

```python
class TestEndpointName(HTTPTestCase):
  def test_basic_functionality(self):
    response = self.make_request('/endpoint')
    self.assertEqual(response['status_code'], 200)

  def test_error_conditions(self):
    # Test error conditions

  def test_edge_cases(self):
    # Test edge cases
```

## 🎨 Coding Style Guidelines

The test suite follows strict coding style guidelines:

- ✅ **2 spaces indentation** (not 4 spaces)
- ✅ **Descriptive names in English**
- ✅ **No trailing whitespace**
- ✅ **Clean empty lines** (no spaces in empty lines)
- ✅ **Consistent formatting** throughout all test files

## 🔧 Test Configuration

### Test Server

- **Host**: `127.0.0.1`
- **Port**: `8000`
- **Configuration**: Temporary, isolated from main environment
- **Data**: Temporary directories for history and configurations

### Environment Variables

Tests create an isolated environment with:

- Temporary configuration in `/tmp/`
- Temporary history
- Temporary input files
- Automatic cleanup after each test

## 🧹 Cleanup and Maintenance

### Manual Cleanup

```bash
cd tests/
python cleanup_tests.py
```

### Automatic Cleanup

- Temporary files are cleaned automatically after each test
- Old logs can be manually removed from the `logs/` directory

## 📈 Coverage Metrics

### Current Coverage: **100%**

- ✅ All endpoints tested
- ✅ Success and error cases
- ✅ Security validation
- ✅ Data processing
- ✅ Complete integration

### Test Types

- **Functional**: 45 tests (61%)
- **Validation**: 15 tests (20%)
- **Security**: 8 tests (11%)
- **Error/Edge Cases**: 6 tests (8%)

## 🛠️ Troubleshooting

### Common Issues

#### Error: "Address already in use"

```bash
# Wait a few seconds between executions or
# Check if main server is running
ps aux | grep python | grep 8000
```

#### Import Failure

```bash
# Ensure you're in the correct directory
cd tests/
export PYTHONPATH=.
```

#### File Permissions

```bash
# Ensure correct permissions
chmod +x run_all_tests.py
chmod 644 *.py
```

## 📚 Additional Resources

- **API Documentation**: `../README.md`
- **Configuration**: `../conf/README.md`
- **Usage**: `../USAGE.md`
- **Loops**: `../LOOP_USAGE.md`
