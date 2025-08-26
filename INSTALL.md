# Installation Guide - Ansible Jinja2 Playground

Quick installation guide for the Ansible Jinja2 Playground - an interactive web application for testing Jinja2
templates with Ansible compatibility.

## Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **Git** for repository cloning
- **Virtual environment** (venv or conda)

## Quick Start

### Local Installation

All project dependencies and configuration are self-contained within the `ansible-jinja2-playground` directory.

```bash
# 1. Clone repository
git clone https://github.com/andrewlinuxadmin/ansible_jinja2_playground.git
cd ansible_jinja2_playground

# Everything you need is inside ansible-jinja2-playground/
# 2. Activate virtual environment (required)
# Create and activate your preferred virtual environment

# 3. Install dependencies
pip install -r ansible-jinja2-playground/requirements.txt

# 4. Run application
python ansible-jinja2-playground/run.py
```

Access at: `http://localhost:8000`

### Container Installation

All project files are self-contained - the container includes everything needed to run the playground.

```bash
# Using Podman
git clone https://github.com/andrewlinuxadmin/ansible_jinja2_playground.git
cd ansible_jinja2_playground
podman build -t ansible-jinja2-playground .
podman run -p 8000:8000 ansible-jinja2-playground

# Using Docker Compose
podman-compose up --build
```

## Configuration

### Basic Settings

Configuration file: `ansible-jinja2-playground/conf/ansible_jinja2_playground.conf`

```ini
[server]
host = 0.0.0.0
port = 8000

[user]
theme = dark
loop_variable_name = item
```

### Environment Variables

```bash
export AJP_PORT=8080
export AJP_DEBUG=true
python run.py
```

## Directory Structure

After installation, everything is self-contained within the project directory:

```text
ansible_jinja2_playground/
├── ansible-jinja2-playground/    # Main application (all code and config)
│   ├── run.py                    # Entry point
│   ├── requirements.txt          # Dependencies
│   ├── requirements-dev.txt      # Development dependencies
│   ├── ansible_jinja2_playground.py
│   ├── conf/                     # Configuration files
│   └── ...
├── tests/                        # Test suite
└── *.md                          # Documentation
```

## Development Setup

```bash
# Install development dependencies
pip install -r ansible-jinja2-playground/requirements-dev.txt

# Run tests
python tests/run_all_tests.py

# Check compliance
python check_compliance.py
```

## Verification

### Test Installation

```bash
# Health check
curl http://localhost:8000/

# Test rendering
curl -X POST http://localhost:8000/render \
  -d "input=$(echo 'Hello {{ name }}' | base64)" \
  -d "expr=$(echo 'name: World' | base64)"
```

### Feature Verification

1. **Web Interface**: Access `http://localhost:8000`
2. **Template Rendering**: Test with simple templates
3. **Loop Mode**: Enable loop with array data
4. **Input Files**: Place files in `inputs/` directory
5. **History**: Verify template history persistence

## Troubleshooting

### Common Issues

**Port in use:**
```bash
lsof -i :8000
export AJP_PORT=8080
python ansible-jinja2-playground/run.py
```

**Import errors:**
```bash
# Verify virtual environment
which python
pip install --force-reinstall -r ansible-jinja2-playground/requirements.txt
```

**Permission errors:**
```bash
chmod +x run.py
chmod -R 755 ansible-jinja2-playground/conf/
```

### Debug Mode

```bash
export AJP_DEBUG=true
python ansible-jinja2-playground/run.py
```

## Container Volumes

For persistent data with containers:

```bash
podman run -p 8000:8000 \
  -v $(pwd)/ansible-jinja2-playground/conf:$(pwd)/ansible-jinja2-playground/ansible-jinja2-playground/conf \
  ansible-jinja2-playground
```

## Security Notes

### Production Deployment

- Use reverse proxy (nginx/Apache)
- Enable HTTPS/TLS
- Implement access controls
- Regular security updates

### Built-in Security

- Jinja2 SandboxedEnvironment prevents code injection
- Input validation and sanitization
- Restricted file system access

## Performance

### Optimization Tips

- Monitor memory with large templates
- Adjust history retention in config
- Use simple templates for large datasets
- Regular cleanup of history files

### Resource Monitoring

```bash
# Check application health
curl http://localhost:8000/

# Monitor resources
htop
df -h
```

## Updates

```bash
# Update application
git pull origin main
pip install --upgrade -r ansible-jinja2-playground/requirements.txt

# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz ansible-jinja2-playground/conf/
```

## Next Steps

1. **Read Documentation**: Review `USAGE.md` and `LOOP_USAGE.md`
2. **Try Examples**: Test with sample templates
3. **Configure Preferences**: Customize theme and editor settings
4. **Explore API**: Test programmatic access
5. **Integrate Workflow**: Use with Ansible development

## Support

- **Documentation**: `USAGE.md`, `LOOP_USAGE.md`
- **Issues**: GitHub repository issues
- **Tests**: Run `python tests/run_all_tests.py`
- **Compliance**: Run `python check_compliance.py`

The playground is now ready for developing and testing Ansible-compatible Jinja2 templates.
