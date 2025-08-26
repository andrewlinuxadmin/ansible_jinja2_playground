# Configuration Directory

This directory contains configuration files for the Ansible Jinja2 Playground application.

## Files Overview

### ansible_jinja2_playground.conf

Main configuration file containing application settings organized in sections:

- **[server]**: Server configuration (host, port)
- **[history]**: History management settings
- **[input_files]**: Input directory configuration and refresh settings
- **[listener]**: API listener configuration for real-time updates
- **[user]**: User interface preferences (theme, editor heights, API features)

### ansible_jinja2_playground_history.json

History storage file containing all user interactions in reverse chronological
order (newest first). Automatically managed by the application.

### ansible_jinja2_playground_history_examples.json

Example history entries for reference and testing purposes.

## Configuration File Format

### Complete Settings Structure

```ini
[server]
host = 127.0.0.1
port = 8000

[history]
max_entries = 1000

[input_files]
directory = inputs
refresh_interval = 30

[listener]
refresh_interval = 5

[user]
theme = dark
height-inputcode = 100
height-jinjaexpr = 100
height-resultview = 1000
api-listener-enabled = false
```

## Configuration Sections Explained

### [server] Section

Controls web server behavior:

- **host**: Server bind address
  - `127.0.0.1` for localhost only (default)
  - `0.0.0.0` for all interfaces (container mode)
- **port**: Server port number (default: 8000)

### [history] Section

Manages user interaction history:

- **max_entries**: Maximum number of history entries to retain (default: 1000)

### [input_files] Section

Controls input file handling:

- **directory**: Path to input files directory (default: `inputs`)
- **refresh_interval**: Seconds between input file list refreshes (default: 30)

### [listener] Section

Real-time update configuration:

- **refresh_interval**: Seconds between listener updates (default: 5)

### [user] Section

User interface customization:

- **theme**: UI color scheme (`dark` or `light`)
- **height-inputcode**: Input code editor height in pixels (default: 100)
- **height-jinjaexpr**: Jinja2 expression editor height in pixels (default: 100)
- **height-resultview**: Result view area height in pixels (default: 1000)
- **api-listener-enabled**: Enable real-time API updates (default: false)

## Common Configuration Changes

### Changing Server Port

To run the application on a different port:

1. Edit `ansible_jinja2_playground.conf`
2. Modify the `port` value in the `[server]` section:

   ```ini
   [server]
   host = 127.0.0.1
   port = 8080
   ```

3. Restart the application: `python ansible-jinja2-playground/run.py`

### Container Configuration

For container deployments, change host binding:

```ini
[server]
host = 0.0.0.0
port = 8000
```

### Performance Tuning

Adjust refresh intervals for better performance:

```ini
[input_files]
refresh_interval = 60  # Slower refresh for large input directories

[listener]
refresh_interval = 10  # Less frequent updates for lower resource usage
```

### UI Customization

Customize editor heights for your screen:

```ini
[user]
theme = light
height-inputcode = 150    # Larger input editor
height-jinjaexpr = 120    # Medium template editor
height-resultview = 600   # Compact result view
api-listener-enabled = true  # Enable real-time updates
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
chmod 750 ansible-jinja2-playground/conf/
chmod 640 ansible-jinja2-playground/conf/*.conf
chmod 644 ansible-jinja2-playground/conf/*.json
```

## Configuration Management

### Environment-Specific Configurations

Create different configurations for different environments:

```bash
# Development (default)
ansible_jinja2_playground.conf

# Production
ansible_jinja2_playground_prod.conf

# Container
ansible_jinja2_playground_container.conf
```

### Dynamic Configuration Updates

Most settings can be changed without restarting the application:

- **UI settings**: Applied immediately via API endpoints
- **Refresh intervals**: Take effect on next refresh cycle
- **Server settings**: Require application restart

## Backup and Maintenance

### Automated Backups

```bash
# Create timestamped backup
cp ansible-jinja2-playground/conf/ansible_jinja2_playground_history.json \
   ansible-jinja2-playground/conf/history_backup_$(date +%Y%m%d_%H%M%S).json
```

### History Management

The application automatically manages history size based on `max_entries` setting.

Manual cleanup using built-in utility:

```bash
# Use the built-in deduplication tool
python ansible-jinja2-playground/deduplicate_history.py

# Manual cleanup (keep only last 100 entries)
python -c "
import json
with open('ansible-jinja2-playground/conf/ansible_jinja2_playground_history.json', 'r') as f:
    data = json.load(f)
with open('ansible-jinja2-playground/conf/ansible_jinja2_playground_history.json', 'w') as f:
    json.dump(data[:100], f, indent=2)
"
```

### Configuration Validation

Validate configuration before applying:

```bash
# Check compliance with project standards
python check_compliance.py
```

## Troubleshooting

### Common Issues

1. **Server won't start on specified port**
   - Check if port is already in use: `netstat -tulpn | grep :8000`
   - Try a different port in configuration

2. **Input files not refreshing**
   - Check `input_files.directory` path exists
   - Verify `refresh_interval` is not too high
   - Ensure proper file permissions

3. **History not saving**
   - Check write permissions on history file
   - Verify `max_entries` is not set to 0
   - Check disk space availability

4. **UI settings not persisting**
   - Verify configuration file write permissions
   - Check for syntax errors in configuration file

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export FLASK_DEBUG=1
python ansible-jinja2-playground/run.py
```

## Security Considerations

- Configuration files may contain sensitive paths and settings
- Restrict access to configuration directory (chmod 750)
- Regular backup of configuration and history data
- Monitor file size growth for history files
- Use `0.0.0.0` host binding only in secure environments
- Consider using reverse proxy for production deployments
