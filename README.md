# Ansible Jinja2 Playground

Interactive web application for testing Jinja2 templates with 100+ Ansible filters and loop functionality.

![Version](https://img.shields.io/badge/version-2.2-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Ansible](https://img.shields.io/badge/ansible-2.14+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **🎯 Ansible Playbook Integration** - Receive variables directly from Ansible playbooks for easy debugging and
  Jinja2 expression development
- **Real-time template rendering** with Jinja2 and 100+ Ansible filters
- **Loop simulation** for processing arrays with custom variables
- **Web interface** with syntax highlighting and theme support
- **History management** for saving and reusing templates
- **Auto-refresh** for input files and settings
- **Sandboxed execution** for secure template processing

## Quick Start

All project dependencies and configuration are self-contained within the `ansible-jinja2-playground` directory.

```bash
# Clone and setup
git clone https://github.com/andrewlinuxadmin/ansible_jinja2_playground.git
cd ansible_jinja2_playground

# Activate virtual environment (required)
# Use your preferred virtual environment method

# Install dependencies
pip install -r ansible-jinja2-playground/requirements.txt

# Start server
python ansible-jinja2-playground/run.py
```

Access at: `http://localhost:8000`

## Container Deployment

```bash
# Using Podman
podman build -t ansible-jinja2-playground .
podman run -p 8000:8000 \
  -v $(pwd)/ansible-jinja2-playground/conf:$(pwd)/ansible-jinja2-playground/ansible-jinja2-playground/conf \
  ansible-jinja2-playground

# Using Compose
podman-compose up --build
```

## Project Structure

```text
ansible_jinja2_playground/
├── ansible-jinja2-playground/                # Main application
│   ├── run.py                                # Entry point
│   ├── requirements.txt                      # Dependencies
│   ├── requirements-dev.txt                  # Development dependencies
│   ├── ansible_jinja2_playground.py         # Backend server
│   ├── ansible_jinja2_playground.html       # Web interface
│   ├── scan_ansible_filters.py              # Filter scanner
│   ├── deduplicate_history.py               # History cleanup
│   └── conf/                                 # Configuration files
├── tests/                                    # Test suite
└── *.md                                      # Documentation
```

## Utilities

### Ansible Filter Scanner
```bash
python ansible-jinja2-playground/scan_ansible_filters.py
```

### History Cleanup
```bash
python ansible-jinja2-playground/deduplicate_history.py
```

### Test Suite
```bash
python tests/run_all_tests.py
```

## Documentation

- **[Installation Guide](INSTALL.md)** - Setup instructions
- **[Usage Guide](USAGE.md)** - Web interface and API
- **[Loop Guide](LOOP_USAGE.md)** - Array processing with loops

## Technology

- **Backend**: Python 3.9+ HTTP server
- **Frontend**: HTML5, Bootstrap 5, CodeMirror
- **Templates**: Jinja2 with Ansible 2.14 compatibility
- **Security**: Sandboxed environment with input validation

## Browser Support

Modern browsers with ES5+ support (Firefox, Chrome, Edge, Safari).

## License

See [LICENSE](LICENSE) file for details.
