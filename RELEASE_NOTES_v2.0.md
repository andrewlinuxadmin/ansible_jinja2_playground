# Ansible Jinja2 Playground v2.0 Release Notes

## 🚀 Major Release Features

This v2.0 release represents a significant milestone with enhanced functionality, improved code quality, and
professional development standards.

### ✨ **New Features**

- **Smart Duplicate Prevention**: Intelligent history management that prevents consecutive duplicate entries
- **Enhanced Loop Simulation**: Ansible-style loop functionality with custom variable names
- **Improved File Management**: Auto-loading input files with cross-browser compatibility
- **Professional Code Standards**: 2-space indentation and comprehensive coding style enforcement

### 🔧 **Technical Improvements**

- **100% Test Coverage**: Comprehensive test suite with 63/63 tests passing
- **Development Environment**: Complete VS Code workspace configuration
- **Code Quality**: Automated formatting and compliance checking
- **Container Support**: Full Docker/Podman containerization

### 🎯 **Core Functionality**

- Real-time Jinja2 template rendering with Ansible filters
- JSON/YAML input data processing
- Persistent history with duplicate prevention
- Configurable auto-refresh and UI themes
- Sandboxed execution environment

### 📦 **What's Included**

- Complete source code with professional structure
- Comprehensive test suite and compliance tools
- Container configuration for easy deployment
- Documentation and usage examples
- VS Code development environment setup

### 🛠 **Installation & Usage**

Extract the archive and follow the INSTALL.md instructions for setup options including virtual environment,
container, or direct execution.

## Technical Specifications

- **Python**: 3.9+ compatibility
- **Dependencies**: Flask, Jinja2, PyYAML, Ansible filters
- **Testing**: 100% pass rate with endpoint-specific test organization
- **Code Style**: 2-space indentation, automated formatting
- **Container**: Podman/Docker ready with compose configuration

## Release Assets

- **ansible-jinja2-playground-v2.0.tar.gz**: Complete source code archive (68.8 KB)

## Installation Instructions

### Method 1: Download and Extract

```bash
wget https://github.com/andrewlinuxadmin/ansible_jinja2_playground/releases/download/v2.0/ansible-jinja2-playground-v2.0.tar.gz
tar -xzf ansible-jinja2-playground-v2.0.tar.gz
cd ansible-jinja2-playground-v2.0
```

### Method 2: Git Clone

```bash
git clone https://github.com/andrewlinuxadmin/ansible_jinja2_playground.git
cd ansible_jinja2_playground
git checkout v2.0
```

### Setup and Run

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r pip-venv-requirements.txt

# Run application
python run.py
```

Visit <http://localhost:5000> to access the application.

## Changelog

### Added

- Smart duplicate prevention in history management
- Enhanced Ansible loop simulation capabilities
- Professional VS Code development environment configuration
- Comprehensive test suite with 100% coverage
- Automated code formatting and compliance checking
- Container support with Podman/Docker

### Improved

- Code style enforcement with 2-space indentation
- File management with auto-loading capabilities
- Error handling and validation
- Documentation and installation guides

### Technical Details

- Implemented `entries_are_identical()` function for intelligent duplicate detection
- Reorganized test structure following "1 arquivo de teste por endpoint" pattern
- Added complete VS Code workspace configuration
- Established clean Git history with professional version control

---

**Full Changelog**: This release includes duplicate prevention, enhanced testing, professional coding standards,
and comprehensive development environment setup.

For support and documentation, visit: <https://github.com/andrewlinuxadmin/ansible_jinja2_playground>
