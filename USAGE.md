# Usage Guide - Ansible Jinja2 Playground

Interactive web-based tool for testing Jinja2 templates with full Ansible 2.14 compatibility.

> **Note**: All configuration, templates, and data files are self-contained within the `ansible-jinja2-playground/`
> directory structure.

## Quick Start

1. **Start the server:**
   ```bash
   python ansible-jinja2-playground/run.py
   ```

2. **Open browser:** <http://localhost:8000>

3. **Test templates:** Enter Jinja2 template and data, click "Render"

## Web Interface

### Template Editor
- **Template field:** Enter your Jinja2 template
- **Data field:** Enter YAML/JSON test data
- **Loop mode:** Enable to process array elements individually
- **Render button:** Process template with data

### Features
- **Auto-refresh:** History and input files update automatically
- **Dark/Light themes:** Toggle in settings
- **History browsing:** View and reuse previous templates
- **Input file loading:** Load sample data files
- **Error display:** Clear error messages for debugging

## Loop Functionality

### Basic Loop
Enable "Loop Mode" to process array data:

**Template:**
```jinja2
Host: {{ item.name }}
IP: {{ item.ip }}
```

**Data:**
```yaml
- name: web01
  ip: 10.0.1.10
- name: web02
  ip: 10.0.1.11
```

**Output:**
```text
Host: web01
IP: 10.0.1.10

Host: web02
IP: 10.0.1.11
```

### Custom Loop Variable
Change loop variable name in settings (default: `item`).

## History Management

### Automatic Deduplication
- Prevents consecutive duplicate entries
- Keeps history clean and relevant
- Preserves unique templates and data combinations

### Manual Cleanup
```bash
python ansible-jinja2-playground/deduplicate_history.py
```

## Ansible Filters & Tests

### Available Filters (68 total)
- **Text:** `upper`, `lower`, `regex_replace`, `split`
- **Data:** `to_json`, `to_yaml`, `from_json`, `from_yaml`
- **Lists:** `first`, `last`, `unique`, `flatten`
- **Math:** `abs`, `round`, `max`, `min`
- **Path:** `basename`, `dirname`, `expanduser`
- **Network:** `ipaddr`, `network`, `netmask`
- **Encoding:** `b64encode`, `b64decode`, `urlsplit`

### Available Tests (47 total)
- **Type:** `string`, `number`, `boolean`
- **Comparison:** `equalto`, `greaterthan`, `lessthan`
- **Pattern:** `match`, `search`, `regex`
- **Network:** `ip`, `ipv4`, `ipv6`
- **File:** `exists`, `directory`, `file`

### Discovery Tool
```bash
python ansible-jinja2-playground/scan_ansible_filters.py
```

## API Usage

### Render Endpoint
```http
POST /render
Content-Type: application/x-www-form-urlencoded

input=SGVsbG8gV29ybGQ%3D&expr=SGVsbG8gV29ybGQ%3D&enable_loop=false
```

- **input:** Base64-encoded template
- **expr:** Base64-encoded data
- **enable_loop:** Boolean for loop mode

### Other Endpoints
- `GET /` - Main interface
- `GET /history` - History data (JSON)
- `GET /input-files` - Available input files
- `GET /settings` - Configuration settings

## Configuration

### Server Settings
Edit `ansible-jinja2-playground/conf/ansible_jinja2_playground.conf`:

```ini
[server]
port = 8000
host = 127.0.0.1

[user]
theme = dark
editor_height = 300
```

### Input Files
Place sample data files in `inputs/` directory. Supported formats: JSON, YAML.

## Troubleshooting

### Common Issues

**Server won't start:**
- Check if port is available
- Verify Python virtual environment is activated
- Ensure all dependencies are installed

**Template errors:**
- Check Jinja2 syntax
- Verify data format (YAML/JSON)
- Review error messages in web interface

**Missing filters:**
- Ensure Ansible 2.14+ is installed
- Check filter availability with scan tool
- Verify filter name spelling

**Debug mode:**
```bash
export AJP_DEBUG=true
python ansible-jinja2-playground/run.py
```

## Container Usage

### Build and Run
```bash
podman build -t ansible-jinja2-playground .
podman run -p 8000:8000 ansible-jinja2-playground
```

### With Persistent Data
```bash
podman run -p 8000:8000 \
  -v ./inputs:/home/playground/inputs:ro \
  -v ./ansible-jinja2-playground/conf:/home/playground/ansible-jinja2-playground/conf \
  ansible-jinja2-playground
```

## Best Practices

### Template Development
1. **Start simple:** Test basic templates first
2. **Use loop mode:** For array data processing
3. **Check history:** Learn from previous templates
4. **Test incrementally:** Add complexity gradually

### Data Preparation
1. **Valid format:** Ensure YAML/JSON is well-formed
2. **Sample data:** Use representative test data
3. **Edge cases:** Test with empty/null values
4. **Array structure:** Consistent item format for loops

### Performance
1. **Limit data size:** Large datasets may slow rendering
2. **Simple templates:** Complex logic may timeout
3. **Browser limits:** Very large outputs may not display fully

## Support

- **Documentation:** Check other .md files in project root
- **Issues:** Review error messages and logs
- **Testing:** Use included test suite for validation
- **Community:** GitHub repository for questions and contributions
