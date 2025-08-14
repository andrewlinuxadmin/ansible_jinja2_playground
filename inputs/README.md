# Input Files Directory

This directory contains sample input files for the Ansible Jinja2 Playground.
Files placed here are automatically detected and made available through the
"Load from Input Files" dropdown in the web interface.

## Supported File Formats

- **JSON** (`.json`): JavaScript Object Notation files
- **YAML** (`.yaml`, `.yml`): YAML Ain't Markup Language files
- **Text** (`.txt`): Plain text files

## File Loading Behavior

### Auto-detection

- Files are automatically scanned when the interface loads
- Dropdown menu is populated with available files
- File selection triggers immediate loading (no additional "Load File" button needed)

### File Validation

- JSON files are validated for proper syntax
- YAML files are parsed and validated
- Invalid files are skipped with console warnings

## Sample Files

### sample.json

Basic JSON structure for testing simple templates:

```json
{
  "users": ["alice", "bob", "charlie"],
  "environment": "development",
  "version": "1.0.0"
}
```

### sample.yaml

YAML equivalent of the JSON sample:

```yaml
users:
  - alice
  - bob
  - charlie
environment: development
version: 1.0.0
```

### loop_example.json

Example data structure designed for loop functionality testing:

```json
[
  {"name": "web01", "ip": "192.168.1.10", "role": "webserver"},
  {"name": "web02", "ip": "192.168.1.11", "role": "webserver"},
  {"name": "db01", "ip": "192.168.1.20", "role": "database"}
]
```

## Adding Custom Files

### File Naming

- Use descriptive names that indicate the file purpose
- Include appropriate file extensions (`.json`, `.yaml`, `.yml`, `.txt`)
- Avoid spaces and special characters in filenames

### Content Guidelines

- Ensure JSON files are properly formatted and valid
- Use consistent indentation in YAML files (2 or 4 spaces)
- Include comments in YAML files to explain complex structures
- Test files with the playground before sharing

### Example Custom Files

#### servers.json

```json
{
  "servers": [
    {
      "hostname": "web-01",
      "ip": "10.0.1.10",
      "services": ["nginx", "php-fpm"],
      "cpu_cores": 4,
      "memory_gb": 8
    },
    {
      "hostname": "db-01",
      "ip": "10.0.1.20",
      "services": ["mysql"],
      "cpu_cores": 8,
      "memory_gb": 16
    }
  ],
  "environment": "production",
  "domain": "example.com"
}
```

#### ansible_vars.yaml

```yaml
# Ansible playbook variables example
apache_packages:
  - apache2
  - apache2-utils
  - libapache2-mod-ssl

apache_vhosts:
  - name: "example.com"
    port: 80
    document_root: "/var/www/example"
  - name: "test.example.com"
    port: 8080
    document_root: "/var/www/test"

mysql_databases:
  - name: app_prod
    user: app_user
    password: "{{ vault_mysql_password }}"
    privileges: "ALL"
```

## Working with Loop Data

### Array Structure for Loops

When using the loop functionality, structure your data as arrays:

```json
[
  {"name": "item1", "value": "data1"},
  {"name": "item2", "value": "data2"},
  {"name": "item3", "value": "data3"}
]
```

### Nested Loop Data

For complex scenarios with global context:

```yaml
global_config:
  environment: production
  domain: example.com

servers:
  - name: web01
    ip: 192.168.1.10
  - name: web02
    ip: 192.168.1.11
```

## File Management

### Organization Tips

- Group related files by purpose (e.g., `web_servers.json`, `db_config.yaml`)
- Use version numbers for evolving datasets (`config_v1.json`, `config_v2.json`)
- Create backup copies before making major changes

### Cleanup

- Remove unused or outdated files regularly
- Keep file sizes reasonable for quick loading
- Document file purposes in comments (YAML) or descriptive names

### Security Considerations

- Avoid including sensitive data (passwords, API keys)
- Use placeholder values for confidential information
- Consider using Ansible Vault format for sensitive test data

## Troubleshooting

### File Not Appearing in Dropdown

1. Check file extension is supported (`.json`, `.yaml`, `.yml`, `.txt`)
2. Verify file is saved in the `inputs/` directory
3. Refresh the web page to re-scan files
4. Check browser console for parsing errors

### File Loading Errors

1. Validate JSON syntax using online validators
2. Check YAML indentation and structure
3. Ensure file encoding is UTF-8
4. Verify file permissions allow reading

### Large File Performance

- Keep input files under 1MB for optimal performance
- Use simplified datasets for testing complex templates
- Consider breaking large files into smaller, focused examples

## Best Practices

### Data Design

- Use realistic but simplified data structures
- Include edge cases (empty arrays, null values, optional fields)
- Provide both simple and complex examples
- Document expected template behavior

### File Documentation

- Use descriptive filenames
- Include comments explaining data structure purpose
- Provide example templates that work with the data
- Document any special loop or filtering requirements

### Version Control

- Track changes to input files
- Use meaningful commit messages for file updates
- Tag stable versions for reference
- Document breaking changes to data structures

This directory serves as your testing playground for various data structures
and scenarios, enabling thorough template testing before deployment in real
environments.
