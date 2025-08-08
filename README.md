# Ansible Jinja2 Playground

An interactive web application for testing and experimenting with Jinja2 templates using Ansible filters and loop functionality.

![Version](https://img.shields.io/badge/version-1.2-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

The Ansible Jinja2 Playground provides a user-friendly interface to:

- **Test Jinja2 templates** with real-time rendering
- **Use Ansible filters** (core, math, URL filters)
- **Simulate Ansible loops** with custom variables
- **Load sample data** from JSON/YAML files
- **Save and manage history** of your experiments
- **Auto-refresh** input files and history

## Key Features

### 🎯 **Template Processing**
- Real-time Jinja2 template rendering
- Full Ansible filter support (core, math, URLs)
- JSON and YAML input data formats
- Syntax highlighting with multiple themes
- Sandboxed environment for secure execution

### 🔄 **Loop Simulation**
- Ansible-style loop functionality
- Custom loop variable names
- Boolean-based loop controls
- Integration with template rendering

### 📁 **File Management**
- Auto-loading from input files directory
- Cross-browser compatible file uploads
- Real-time file list updates
- Security-validated file access

### 📊 **History & Settings**
- Persistent interaction history
- Reverse chronological ordering
- Configurable auto-refresh intervals
- Theme and UI customization

## Quick Start

### Prerequisites
- Python 3.9+
- Virtual environment (recommended)
- Modern web browser (Firefox, Chrome, Edge)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd ansible_jinja2_playground

# Activate virtual environment
source /home/acarlos/Dropbox/RedHat/Ansible/venvs/python3.9-ansible2.14/bin/activate

# Install dependencies
pip install -r pip-venv-requirements.txt

# Start the server
python run.py
```

### Access
Open your browser and navigate to: `http://localhost:8000`

## Container Deployment

### Using Podman (Recommended)

#### Quick Start with Helper Script
```bash
# Build and run the container
./container.sh run

# Check status
./container.sh status

# View logs
./container.sh logs

# Stop the container
./container.sh stop
```

#### Manual Podman Commands
```bash
# Build the image
podman build -t ansible-jinja2-playground:latest -f Containerfile .

# Run the container
podman run -d \
  --name ansible-jinja2-playground \
  -p 8000:8000 \
  -v "$(pwd)/conf:/home/playground/app/conf" \
  -v "$(pwd)/inputs:/home/playground/app/inputs:ro" \
  ansible-jinja2-playground:latest

# Access the application
open http://localhost:8000
```

#### Using Podman Compose
```bash
# Start with compose
podman-compose up -d

# Stop with compose
podman-compose down

# View logs
podman-compose logs -f
```

### Container Features

- **Multi-stage build** for optimized image size
- **Non-root user** execution for security
- **Persistent volumes** for configuration and input files
- **Health checks** for reliability
- **Resource limits** for performance control
- **Read-only filesystem** for enhanced security

### Container Configuration

- **Base Image**: Fedora 39
- **Python Version**: 3.11
- **User**: playground (UID 1000)
- **Port**: 8000
- **Volumes**: `conf/` (persistent), `inputs/` (read-only)

## Project Structure

```
ansible_jinja2_playground/
├── README.md              # Main project documentation
├── INSTALL.md             # Installation instructions
├── USAGE.md               # Detailed usage guide
├── LOOP_USAGE.md          # Loop functionality guide
├── run.py                 # Server entry point
├── app/                   # Main application
│   ├── ansible_jinja2_playground.py    # Backend server
│   └── ansible_jinja2_playground.html  # Frontend interface
├── conf/                  # Configuration files
│   ├── README.md          # Configuration documentation
│   ├── *.conf             # Application settings
│   └── *_history.json     # Interaction history
├── inputs/                # Sample input files
│   ├── README.md          # Input files documentation
│   ├── sample.json        # Sample JSON data
│   ├── sample.yaml        # Sample YAML data
│   └── loop_example.json  # Loop demonstration data
└── tests/                 # Test files
```

## Technology Stack

- **Backend**: Python 3.9+ with HTTP server
- **Template Engine**: Jinja2 with Ansible filters
- **Frontend**: HTML5, Bootstrap 5, jQuery
- **Editors**: CodeMirror with syntax highlighting
- **Data Formats**: JSON, YAML support
- **Security**: Path traversal protection, input validation

## Browser Compatibility

- **Primary**: Firefox (fully tested)
- **Secondary**: Chrome, Edge, Safari
- **Features**: Cross-browser JavaScript compatibility
- **Requirements**: Modern browser with ES5+ support

## Contributing

1. Follow the `.copilotrc` coding standards
2. Use descriptive English variable names
3. Maintain 2-space indentation
4. Test on Firefox before submitting
5. Activate virtual environment for Python work

## License

See [LICENSE](LICENSE) file for details.

## Documentation

- [Installation Guide](INSTALL.md)
- [Usage Instructions](USAGE.md)
- [Loop Functionality](LOOP_USAGE.md)
- [Configuration Options](conf/README.md)
- [Input Files Guide](inputs/README.md)

## Version

Current version: v1.2
