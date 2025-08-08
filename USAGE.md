# Usage Guide - Ansible Jinja2 Playground

This document provides detailed instructions for using both the frontend interface and backend API of the Ansible Jinja2 Playground.

## Frontend Usage

### Getting Started

1. **Start the Server**
   ```bash
   source /home/acarlos/Dropbox/RedHat/Ansible/venvs/python3.9-ansible2.14/bin/activate
   cd ansible_jinja2_playground
   python run.py
   ```

2. **Access the Interface**
   - Open Firefox (recommended) or Chrome
   - Navigate to: `http://localhost:8000`

### Interface Overview

#### 📝 **Input Data Section**
- **Format Selection**: Choose between JSON and YAML
- **Data Entry**: Enter your test data in the left editor
- **File Upload**: Use "Load File" button for local files
- **Auto-Loading**: Select from "Load from Input Files" dropdown

#### 🔧 **Template Section**
- **Jinja2 Templates**: Write your templates in the middle editor
- **Syntax Highlighting**: Automatic syntax highlighting
- **Real-time Validation**: Immediate error feedback

#### 📊 **Results Section**
- **Output Format**: Select JSON, YAML, or Plain Text
- **Real-time Rendering**: See results as you type
- **Error Display**: Detailed error messages when issues occur

#### 🔄 **Loop Controls**
- **Enable Loop**: Checkbox to activate loop functionality
- **Loop Variable**: Define custom variable name (e.g., "item", "server")
- **Auto-processing**: Automatically applies loop logic to data

#### 📚 **History Management**
- **Auto-save**: All interactions saved automatically
- **History Selection**: Dropdown with recent entries
- **Reverse Order**: Newest entries appear first
- **Auto-refresh**: History updates automatically

#### 🧹 **History Cleanup**
The project includes a dedicated script for cleaning duplicate history entries:

**Basic Usage:**
```bash
# Clean duplicates from history file
python3 deduplicate_history.py

# Preview changes without making modifications
python3 deduplicate_history.py --dry-run
```

**Advanced Options:**
```bash
# Keep oldest duplicates instead of newest
python3 deduplicate_history.py --keep oldest

# Skip creating backup file
python3 deduplicate_history.py --no-backup

# Only validate file structure
python3 deduplicate_history.py --validate-only

# Clean specific history file
python3 deduplicate_history.py path/to/history.json
```

**Features:**
- **Smart Detection**: Compares decoded base64 content for accurate duplicate identification
- **Automatic Backup**: Creates timestamped backups before making changes
- **Safe Operation**: Validates file structure and handles errors gracefully
- **Flexible Strategy**: Choose to keep newest or oldest duplicate entries
- **Detailed Reporting**: Shows exactly what was removed and what remains

**Example Output:**
```
🧹 History Deduplication Tool
========================================
📂 Target file: conf/ansible_jinja2_playground_history.json

🔍 Validating 78 entries...
✅ File structure is valid
📊 Processing 78 history entries...
🗑️  Removed 58 duplicate entries
✅ Final history contains 20 unique entries
📁 Backup created: conf/ansible_jinja2_playground_history.json.backup_20250808_120127

✅ Successfully deduplicated history file
📊 Original entries: 78
📊 Final entries: 20
🗑️  Removed: 58 duplicates
```

**When to Use:**
- Regular maintenance to prevent history file bloat
- Before sharing or backing up the project
- When history dropdown becomes cluttered with duplicates
- As part of automated cleanup workflows

For complete documentation, see `HISTORY_CLEANUP.md`.

### Working with Data

#### JSON Input Example
```json
{
  "servers": [
    {"name": "web01", "ip": "192.168.1.10"},
    {"name": "web02", "ip": "192.168.1.11"}
  ],
  "environment": "production"
}
```

#### YAML Input Example
```yaml
servers:
  - name: web01
    ip: 192.168.1.10
  - name: web02
    ip: 192.168.1.11
environment: production
```

### Template Examples

#### Basic Template
```jinja2
Environment: {{ environment }}
Server Count: {{ servers | length }}
```

#### With Ansible Filters
```jinja2
{% for server in servers %}
Server: {{ server.name | upper }}
IP: {{ server.ip | ipaddr('address') }}
{% endfor %}
```

#### Using Loop Functionality
1. Enable "Enable Loop" checkbox
2. Set loop variable to "server"
3. Template will process each server individually:
```jinja2
Current Server: {{ server.name }}
IP Address: {{ server.ip }}
```

### File Management

#### Input Files
- Place files in the `inputs/` directory
- Supported formats: JSON, YAML, TXT
- Files appear in "Load from Input Files" dropdown
- Auto-loading when selected (no "Load File" button needed)

#### File Upload
- Use "Load File" button for external files
- Drag-and-drop supported
- Automatic format detection

### Theme and Settings

#### Theme Selection
- **Dark Theme**: Default, eye-friendly
- **Light Theme**: Traditional light background
- **Eclipse Theme**: Alternative dark theme

#### Editor Configuration
- **Height Adjustment**: Resize editor panels
- **Auto-refresh Intervals**: Configure update frequency
- **Font Size**: Adjustable text size

## Backend API Usage

### Authentication
No authentication required for local development.

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Render Template
```http
POST /render
Content-Type: application/x-www-form-urlencoded

json={"name": "test"}&expr={{ name | upper }}&enable_loop=false&loop_variable=
```

**Response:**
```json
{
  "result": "TEST",
  "success": true,
  "input_format": "JSON"
}
```

#### 2. Get History
```http
GET /history
```

**Response:**
```json
[
  {
    "input": "{\"name\": \"test\"}",
    "expr": "{{ name | upper }}",
    "enable_loop": false,
    "loop_variable": "",
    "timestamp": "2025-08-07T23:30:00"
  }
]
```

#### 3. Get Input Files
```http
GET /input-files
```

**Response:**
```json
["sample.json", "sample.yaml", "loop_example.json"]
```

#### 4. Get File Content
```http
GET /input-file-content?filename=sample.json
```

**Response:**
```json
{
  "users": ["alice", "bob"],
  "environment": "development"
}
```

#### 5. Configuration Management
```http
GET /settings?section=user
```

**Response:**
```json
{
  "theme": "dark",
  "height-inputcode": "100",
  "height-jinjaexpr": "200",
  "height-resultview": "1000"
}
```

#### 6. Update Settings
```http
POST /settings
Content-Type: application/x-www-form-urlencoded

section=user&theme=light&height-inputcode=150
```

#### 7. Clear History
```http
POST /history/clear
Content-Type: application/x-www-form-urlencoded

count=10
```

### Error Handling

#### Common Error Codes
- **400**: Bad Request (invalid parameters)
- **403**: Forbidden (security violation)
- **404**: Not Found (endpoint/file not found)
- **500**: Internal Server Error

#### Error Response Format
```json
{
  "error": "Template syntax error",
  "details": "Unexpected token at line 1",
  "success": false
}
```

### Security Considerations

#### File Access
- Input files must be within `inputs/` directory
- Path traversal attacks prevented
- Filename validation enforced

#### Template Execution
- Sandboxed Jinja2 environment
- Limited access to system functions
- Safe execution of user templates

## Advanced Usage

### History Maintenance

#### Automated Cleanup
The `deduplicate_history.py` script can be integrated into maintenance workflows:

```bash
# Weekly automated cleanup
0 2 * * 0 /path/to/deduplicate_history.py

# Before application startup with validation
./deduplicate_history.py --dry-run && python run.py

# Cleanup with custom retention strategy
./deduplicate_history.py --keep oldest --no-backup
```

#### Manual Maintenance
```bash
# Check for duplicates without changes
python3 deduplicate_history.py --dry-run

# Clean duplicates and create backup
python3 deduplicate_history.py

# Validate history file structure only
python3 deduplicate_history.py --validate-only
```

### Custom Ansible Filters

The playground includes these Ansible filter modules:
- **Core Filters**: `default`, `map`, `select`, `reject`, etc.
- **Math Filters**: `abs`, `round`, `random`, etc.
- **URL Filters**: `urlsplit`, `urljoin`, etc.

### Loop Processing

When loop is enabled:
1. Input data is treated as an array
2. Each item is processed individually
3. Loop variable contains current item
4. Results are concatenated

### Integration with External Tools

#### curl Examples
```bash
# Render a template
curl -X POST http://localhost:8000/render \
  -d "json={\"name\":\"world\"}" \
  -d "expr=Hello {{ name }}!"

# Get current settings
curl http://localhost:8000/settings?section=user

# Clear history (remove last 10 entries)
curl -X POST http://localhost:8000/history/clear \
  -d "count=10"

# Check history file for maintenance
python3 deduplicate_history.py --dry-run
```

#### Python Integration
```python
import requests

# Render template
response = requests.post('http://localhost:8000/render', data={
    'json': '{"items": [1,2,3]}',
    'expr': '{% for item in items %}{{ item }}{% endfor %}',
    'enable_loop': 'false'
})

result = response.json()
print(result['result'])
```

## Troubleshooting

### Common Issues

1. **Server Won't Start**
   - Check virtual environment is activated
   - Verify Python 3.9+ is installed
   - Check port 8000 is available

2. **Templates Not Rendering**
   - Verify JSON/YAML syntax
   - Check Jinja2 template syntax
   - Review error messages in results panel

3. **Files Not Loading**
   - Ensure files are in `inputs/` directory
   - Check file permissions
   - Verify file format (JSON/YAML)

4. **History Not Saving**
   - Check `conf/` directory exists
   - Verify write permissions
   - Check disk space

5. **History File Issues**
   - Use `deduplicate_history.py --validate-only` to check file structure
   - Run `deduplicate_history.py --dry-run` to identify duplicates
   - Create backup before cleanup with `deduplicate_history.py`

### Debug Mode

Enable debug output by modifying the server:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tips

1. **Large Data Sets**
   - Use smaller sample data for testing
   - Consider loop functionality for repetitive data

2. **Complex Templates**
   - Break down into smaller parts
   - Test incrementally
   - Use history to track working versions

3. **Browser Performance**
   - Use Firefox for best compatibility
   - Clear browser cache if issues occur
   - Disable browser extensions that may interfere

For additional help, refer to the project documentation or check the browser console for JavaScript errors.
