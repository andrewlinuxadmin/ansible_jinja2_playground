# Loop Usage Guide - Ansible Jinja2 Playground

This document explains the loop functionality for processing array data elements individually through templates.

> **Note**: All loop configuration and examples are self-contained within the `ansible-jinja2-playground/` directory
> structure.

## Overview

Loop mode allows you to process array data in an Ansible-style loop where each array element becomes accessible
through a loop variable (default: `item`).

## Basic Loop Usage

### 1. Enable Loop Mode
- Check the "Enable Loop" checkbox in the web interface
- Or set `enable_loop=true` when using the API

### 2. Structure Your Data
Provide data as an array in YAML or JSON format:

```yaml
# Simple array
- web01
- web02
- db01
```

```yaml
# Array of objects
- name: web01
  ip: 10.0.1.10
  role: webserver
- name: web02
  ip: 10.0.1.11
  role: webserver
- name: db01
  ip: 10.0.1.20
  role: database
```

### 3. Write Template
Access each array element using the loop variable:

```jinja2
Server: {{ item.name }}
IP: {{ item.ip }}
Role: {{ item.role | upper }}
```

## Loop Examples

### Simple Host List
**Template:**
```jinja2
Processing host: {{ item }}
```

**Data:**
```yaml
- web01.example.com
- web02.example.com
- db01.example.com
```

**Output:**
```text
Processing host: web01.example.com

Processing host: web02.example.com

Processing host: db01.example.com
```

### Server Configuration
**Template:**
```jinja2
# {{ item.name }} Configuration
Host: {{ item.name }}
IP Address: {{ item.ip }}
Role: {{ item.role | upper }}
Services:
{% for service in item.services %}
  - {{ service }}
{% endfor %}
```

**Data:**
```yaml
- name: web01
  ip: 10.0.1.10
  role: webserver
  services:
    - nginx
    - php-fpm
- name: db01
  ip: 10.0.1.20
  role: database
  services:
    - mysql
    - redis
```

**Output:**
```text
# web01 Configuration
Host: web01
IP Address: 10.0.1.10
Role: WEBSERVER
Services:
  - nginx
  - php-fpm

# db01 Configuration
Host: db01
IP Address: 10.0.1.20
Role: DATABASE
Services:
  - mysql
  - redis
```

### Conditional Processing
**Template:**
```jinja2
Host: {{ item.hostname }}
{% if item.role == 'web' %}
Configuration: Web Server
  - Document Root: html/
  - Port: 80, 443
{% elif item.role == 'db' %}
Configuration: Database Server
  - Data Directory: data/mysql/
  - Port: 3306
{% endif %}
Status: {{ item.status | default('Unknown') }}
```

## Advanced Features

### Custom Loop Variable

Change the loop variable name in settings:

1. **Web Interface:** Settings → User Preferences → Loop Variable Name
2. **Configuration File:** Edit `loop_variable_name` in `[user]` section

```ini
[user]
loop_variable_name = host
```

**Template with custom variable:**
```jinja2
Hostname: {{ host.name }}
IP: {{ host.ip }}
```

### Mixed Data Types
**Template:**
```jinja2
{% if item is string %}
Simple value: {{ item }}
{% else %}
Complex object:
  Name: {{ item.name }}
  Type: {{ item.type }}
{% endif %}
```

**Data:**
```yaml
- "simple_string"
- name: complex_object
  type: server
```

### Nested Loops
**Template:**
```jinja2
Datacenter: {{ item.name }}
Racks:
{% for rack in item.racks %}
  Rack {{ rack.id }}:
  {% for server in rack.servers %}
    - {{ server.hostname }} ({{ server.ip }})
  {% endfor %}
{% endfor %}
```

**Data:**
```yaml
- name: DC1
  racks:
    - id: 1
      servers:
        - hostname: web01
          ip: 10.0.1.10
        - hostname: web02
          ip: 10.0.1.11
    - id: 2
      servers:
        - hostname: db01
          ip: 10.0.1.20
```

## Loop with Filters

### Using Ansible Filters
**Template:**
```jinja2
Server: {{ item.hostname | upper }}
Network: {{ item.ip | ipaddr('network') }}
Subnet: {{ item.ip | ipaddr('netmask') }}
Config Hash: {{ item | to_json | hash('md5') }}
```

### Data Transformation
**Template:**
```jinja2
{% set server_info = {
  'name': item.hostname,
  'network': item.ip | ipaddr('network'),
  'domain': item.hostname.split('.')[1:]|join('.')
} %}
{{ server_info | to_yaml }}
```

## Common Patterns

### Inventory Generation
**Template:**
```jinja2
[{{ item.group }}]
{% for host in item.hosts %}
{{ host.name }} ansible_host={{ host.ip }}
{% endfor %}
```

**Data:**
```yaml
- group: webservers
  hosts:
    - name: web01
      ip: 10.0.1.10
    - name: web02
      ip: 10.0.1.11
- group: databases
  hosts:
    - name: db01
      ip: 10.0.1.20
```

### Configuration Files
**Template:**
```jinja2
# {{ item.service }} configuration
server {
    listen {{ item.port }};
    server_name {{ item.server_name }};
    root {{ item.document_root }};

    {% if item.ssl_enabled %}
    ssl_certificate {{ item.ssl_cert }};
    ssl_certificate_key {{ item.ssl_key }};
    {% endif %}
}
```

### Report Generation
**Template:**
```jinja2
## Server Report: {{ item.hostname }}

**Status:** {{ item.status | title }}
**Last Check:** {{ item.last_check }}
**Uptime:** {{ item.uptime_days }} days

### Resource Usage
- CPU: {{ item.cpu_usage }}%
- Memory: {{ item.memory_usage }}%
- Disk: {{ item.disk_usage }}%

{% if item.alerts %}
### Alerts
{% for alert in item.alerts %}
- ⚠️  {{ alert }}
{% endfor %}
{% endif %}
```

## Error Handling

### Common Issues

**No output generated:**
- Ensure data is properly formatted as an array
- Check that loop mode is enabled
- Verify template syntax

**Template errors:**
- Check loop variable name matches settings
- Ensure proper indentation in YAML data
- Validate JSON syntax if using JSON format

**Missing data fields:**
- Use `default` filter for optional fields: `{{ item.field | default('N/A') }}`
- Check for typos in field names
- Use conditional statements for optional data

### Debugging Tips

**Check data structure:**
```jinja2
Debug: {{ item | to_json }}
```

**Validate array elements:**
```jinja2
Item type: {{ item | type_debug }}
Item keys: {{ item.keys() | list }}
```

**Test with simple template:**
```jinja2
Processing item: {{ item }}
```

## Performance Considerations

### Large Arrays
- Limit array size for better performance (< 1000 items recommended)
- Use simple templates for large datasets
- Consider pagination for very large arrays

### Complex Templates
- Break complex logic into smaller templates
- Use variables to store computed values
- Avoid nested loops when possible

### Memory Usage
- Large objects in arrays consume more memory
- Monitor browser performance with large outputs
- Use simpler data structures when possible

## Best Practices

### Data Design
1. **Consistent structure:** Keep array elements uniform
2. **Required fields:** Ensure essential fields are present in all items
3. **Flat structure:** Avoid deeply nested objects when possible
4. **Meaningful names:** Use descriptive field names

### Template Design
1. **Error handling:** Use `default` filters for optional fields
2. **Clear formatting:** Add appropriate spacing and headers
3. **Conditional logic:** Handle different item types gracefully
4. **Documentation:** Comment complex template logic

### Testing Strategy
1. **Start small:** Test with 2-3 array items first
2. **Edge cases:** Test with empty arrays and missing fields
3. **Data validation:** Verify all required fields are present
4. **Output review:** Check formatting and completeness

## Integration Examples

### Ansible Playbook Integration
Use the playground to develop templates for Ansible tasks:

```yaml
- name: Generate server configs
  template:
    src: server.j2
    dest: "configs/{{ item.name }}"
  loop: "{{ servers }}"
```

### Dynamic Documentation
Generate documentation from infrastructure data:

```jinja2
# Infrastructure Overview

{% for item in servers %}
## {{ item.name }}
- **IP:** {{ item.ip }}
- **Role:** {{ item.role }}
- **Status:** {{ item.status }}
{% endfor %}
```

## API Usage with Loops

### Enable Loop via API
```bash
curl -X POST http://localhost:8000/render \
  -d "input=$(echo 'Host: {{ item.name }}' | base64)" \
  -d "expr=$(echo '[{name: web01}, {name: web02}]' | base64)" \
  -d "enable_loop=true"
```

### Response Format
Loop mode returns concatenated output from all array elements:

```json
{
  "status": "success",
  "result": "Host: web01\n\nHost: web02\n\n",
  "loop_processed": true,
  "items_count": 2
}
```

This loop functionality makes the Ansible Jinja2 Playground ideal for developing and testing templates that
will be used with Ansible's native loop constructs.
