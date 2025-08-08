# Configuration Directory

This directory contains configuration files for the Ansible Jinja2 Playground application.

## Files Overview

### ansible_jinja2_playground.conf
Main configuration file containing application settings organized in sections:

- **[user]**: User interface preferences (theme, editor heights)
- **[system]**: System-level settings (history limits, debug mode)
- **[server]**: Server configuration (port, host, security settings)

### ansible_jinja2_playground_history.json
History storage file containing all user interactions in reverse chronological order (newest first).

### ansible_jinja2_playground_history_examples.json
Example history entries for reference and testing purposes.

## Configuration File Format

### Settings Structure
```ini
[user]
theme = dark
height-inputcode = 100
height-jinjaexpr = 200
height-resultview = 1000

[system]
history_max_size = 1000
auto_save = true
debug_mode = false

[server]
port = 8000
host = localhost
```

### History File Structure
```json
[
  {
    "input": "JSON or YAML input data (base64 encoded)",
    "expr": "Jinja2 template expression (base64 encoded)",
    "enable_loop": true,
    "loop_variable": "item",
    "timestamp": "2025-01-07T23:30:00"
  }
]
```

## Data Format Standards

### Loop Fields (Native Format)
- **enable_loop**: Boolean value (`true`/`false`)
- **loop_variable**: Plain text string

### Preserved Base64 Fields
- **input**: User data (JSON/YAML) - base64 encoded for safety
- **expr**: Jinja2 template content - base64 encoded for safety

### Timestamp Format
ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`

## File Permissions

Recommended permissions for security:
```bash
chmod 750 conf/
chmod 640 conf/*.conf
chmod 644 conf/*.json
```

## Backup and Maintenance

### Regular Backups
```bash
# Create timestamped backup
cp conf/ansible_jinja2_playground_history.json \
   conf/history_backup_$(date +%Y%m%d_%H%M%S).json
```

### History Cleanup
The application automatically manages history size based on `history_max_size` setting.

Manual cleanup:
```bash
# Keep only last 100 entries
python -c "
import json
with open('conf/ansible_jinja2_playground_history.json', 'r') as f:
    data = json.load(f)
with open('conf/ansible_jinja2_playground_history.json', 'w') as f:
    json.dump(data[:100], f, indent=2)
"
```

## Security Considerations

- Configuration files may contain sensitive information
- Restrict access to configuration directory
- Regular backup of history data
- Monitor file size growth for history files
