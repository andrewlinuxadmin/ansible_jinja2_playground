# Loop Usage Guide - Ansible Jinja2 Playground

This document explains the loop functionality in the Ansible Jinja2 Playground, which allows you to process array data elements individually through templates.

## Overview

The loop functionality enables you to:

- Process each element of an array separately
- Define custom loop variable names
- Test templates against individual data items
- Simulate Ansible task iteration behavior

## How Loop Processing Works

### Standard Processing vs Loop Processing

#### Without Loop (Standard)

- Template receives the entire data structure
- You must write explicit loops in Jinja2
- Data passed as-is to template engine

#### With Loop Enabled

- Each array element is processed individually
- Template runs once per array item
- Loop variable contains current item
- Results are concatenated

## Enabling Loop Functionality

### Frontend Interface

1. **Checkbox Control**: Check "Enable Loop" checkbox
2. **Variable Name**: Enter custom loop variable name (default: "item")
3. **Auto-processing**: Template automatically processes each array element

### Backend API

```http
POST /render
Content-Type: application/x-www-form-urlencoded

json=[{"name":"server1"},{"name":"server2"}]&expr=Server: {{ item.name }}&enable_loop=true&loop_variable=item
```

## Data Structure Requirements

### Supported Input Formats

#### JSON Array

```json
[
  {"name": "web01", "ip": "192.168.1.10"},
  {"name": "web02", "ip": "192.168.1.11"},
  {"name": "db01", "ip": "192.168.1.20"}
]
```

#### YAML Array

```yaml
- name: web01
  ip: 192.168.1.10
- name: web02
  ip: 192.168.1.11
- name: db01
  ip: 192.168.1.20
```

#### Nested Array Data

```json
{
  "servers": [
    {"name": "web01", "role": "webserver"},
    {"name": "db01", "role": "database"}
  ],
  "environment": "production"
}
```

### Loop Variable Access

#### With Array Root Data

```jinja2
# Loop Variable: item
# Template processes each server individually
Server Name: {{ item.name }}
Server IP: {{ item.ip }}
Role: {{ item.role | default('unknown') }}
```

#### With Nested Array Data

```jinja2
# Loop Variable: server
# Template accesses: servers array + environment
Environment: {{ environment }}
Current Server: {{ server.name }}
Server Role: {{ server.role }}
```

## Practical Examples

### Example 1: Basic Server Configuration

#### Input Data

```json
[
  {"hostname": "web01", "ip": "10.0.1.10", "role": "web"},
  {"hostname": "web02", "ip": "10.0.1.11", "role": "web"},
  {"hostname": "db01", "ip": "10.0.1.20", "role": "database"}
]
```

#### Template

```jinja2
Host: {{ item.hostname }}
IP Address: {{ item.ip }}
Role: {{ item.role | upper }}
FQDN: {{ item.hostname }}.example.com
```

#### Settings

- **Enable Loop**: ✓ Checked
- **Loop Variable**: `item`

#### Output

```
Host: web01
IP Address: 10.0.1.10
Role: WEB
FQDN: web01.example.com

Host: web02
IP Address: 10.0.1.11
Role: WEB
FQDN: web02.example.com

Host: db01
IP Address: 10.0.1.20
Role: DATABASE
FQDN: db01.example.com
```

### Example 2: User Account Generation

#### Input Data

```json
[
  {"username": "alice", "uid": 1001, "groups": ["users", "developers"]},
  {"username": "bob", "uid": 1002, "groups": ["users", "admins"]},
  {"username": "charlie", "uid": 1003, "groups": ["users"]}
]
```

#### Template

```jinja2
# User: {{ user.username }}
useradd -u {{ user.uid }} -G {{ user.groups | join(',') }} {{ user.username }}
echo "User {{ user.username }} created with UID {{ user.uid }}"
```

#### Settings

- **Enable Loop**: ✓ Checked
- **Loop Variable**: `user`

#### Output

```bash
# User: alice
useradd -u 1001 -G users,developers alice
echo "User alice created with UID 1001"

# User: bob
useradd -u 1002 -G users,admins bob
echo "User bob created with UID 1002"

# User: charlie
useradd -u 1003 -G users charlie
echo "User charlie created with UID 1003"
```

### Example 3: Configuration Files with Context

#### Input Data

```json
{
  "domain": "example.com",
  "environments": [
    {"name": "development", "port": 8080, "debug": true},
    {"name": "staging", "port": 8081, "debug": false},
    {"name": "production", "port": 80, "debug": false}
  ]
}
```

#### Template

```jinja2
# {{ env.name | upper }} Environment Configuration
server {
    listen {{ env.port }};
    server_name {{ env.name }}.{{ domain }};

    {% if env.debug %}
    error_log /var/log/nginx/{{ env.name }}_debug.log debug;
    {% else %}
    error_log /var/log/nginx/{{ env.name }}.log warn;
    {% endif %}

    location / {
        proxy_pass http://{{ env.name }}-backend:{{ env.port }};
    }
}
```

#### Settings

- **Enable Loop**: ✓ Checked
- **Loop Variable**: `env`
- **Note**: Loop processes `environments` array, but `domain` is accessible globally

### Example 4: Ansible Task Simulation

#### Input Data

```yaml
- package: nginx
  state: present
  service: nginx
- package: mysql-server
  state: present
  service: mysql
- package: php-fpm
  state: present
  service: php-fpm
```

#### Template

```jinja2
- name: Install {{ task.package }}
  package:
    name: {{ task.package }}
    state: {{ task.state }}

- name: Start {{ task.service }}
  service:
    name: {{ task.service }}
    state: started
    enabled: yes
```

#### Settings

- **Enable Loop**: ✓ Checked
- **Loop Variable**: `task`

## Advanced Loop Patterns

### Pattern 1: Conditional Processing

```jinja2
{% if item.enabled | default(true) %}
Server: {{ item.name }} is ENABLED
Port: {{ item.port | default(80) }}
{% else %}
Server: {{ item.name }} is DISABLED
{% endif %}
```

### Pattern 2: Complex Data Structures

```jinja2
# Processing: {{ item.name }}
{% for interface in item.interfaces %}
Interface {{ interface.name }}: {{ interface.ip }}/{{ interface.netmask }}
{% endfor %}

{% for mount in item.mounts %}
Mount {{ mount.device }} on {{ mount.path }}
{% endfor %}
```

### Pattern 3: Environment Variables

```jinja2
export {{ item.name | upper }}_HOST="{{ item.hostname }}"
export {{ item.name | upper }}_PORT="{{ item.port }}"
export {{ item.name | upper }}_ENV="{{ item.environment }}"
```

## Best Practices

### 1. Variable Naming

- Use descriptive loop variable names
- Common patterns: `item`, `server`, `user`, `host`, `task`
- Match variable name to data context

### 2. Data Structure Design

- Keep array elements consistent in structure
- Use default filters for optional fields
- Validate data before processing

### 3. Template Organization

- Start with simple templates
- Test with small datasets first
- Use comments to document complex logic

### 4. Error Handling

```jinja2
{% if item.name is defined %}
Name: {{ item.name }}
{% else %}
Name: UNDEFINED
{% endif %}

# Or using default filter
Name: {{ item.name | default('UNKNOWN') }}
```

## Troubleshooting

### Common Issues

#### 1. Loop Not Processing

**Problem**: Template shows entire array instead of individual items

**Solutions**:

- Verify "Enable Loop" checkbox is checked
- Ensure input data is an array format
- Check loop variable name matches template usage

#### 2. Variable Not Found

**Problem**: Template error "variable not defined"

**Solutions**:

- Check loop variable name spelling
- Verify data structure contains expected fields
- Use `default` filter for optional fields

#### 3. Empty Results

**Problem**: No output when loop is enabled

**Solutions**:

- Verify input data is valid JSON/YAML array
- Check array is not empty
- Ensure template syntax is correct

#### 4. Global Variables Not Accessible

**Problem**: Variables outside array not available in template

**Solutions**:

- For nested objects, global variables remain accessible
- For root arrays, only current item is available
- Restructure data to include global context

### Debug Techniques

#### 1. Inspect Current Item

```jinja2
DEBUG: Current item structure
{{ item | to_json }}

DEBUG: Available variables
{% for key in item.keys() %}
- {{ key }}: {{ item[key] }}
{% endfor %}
```

#### 2. Test with Simple Template

```jinja2
Item: {{ item }}
Type: {{ item.__class__.__name__ }}
```

#### 3. Validate Data Format

- Use JSON/YAML validators
- Test with minimal data sets
- Check array structure

## Performance Considerations

### 1. Large Arrays

- Loop processing handles large arrays efficiently
- Each item processed separately reduces memory usage
- Consider pagination for very large datasets

### 2. Complex Templates

- Simple templates process faster
- Avoid deeply nested loops within templates
- Use filters instead of complex logic

### 3. Output Size

- Large arrays produce large output
- Consider output format selection
- Monitor result size for display limitations

## Integration with Ansible

### Simulating Ansible Loops

The loop functionality simulates Ansible's `loop` and `with_items` behaviors:

```yaml
# Ansible Task
- name: Configure servers
  template:
    src: server.conf.j2
    dest: "/etc/{{ item.name }}.conf"
  loop:
    - { name: web01, port: 80 }
    - { name: web02, port: 8080 }

# Playground Equivalent
# Input: [{"name": "web01", "port": 80}, {"name": "web02", "port": 8080}]
# Template: server.conf.j2 content
# Loop Variable: item
```

### Testing Ansible Templates

1. Copy Ansible template content to playground
2. Use same data structure as Ansible variables
3. Enable loop with appropriate variable name
4. Compare output with expected Ansible results

This loop functionality makes the playground an excellent tool for testing and developing Ansible templates before deployment.
