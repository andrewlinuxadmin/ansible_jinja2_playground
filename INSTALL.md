# Installation Guide - Ansible Jinja2 Playground v2.1

This guide provides step-by-step instructions for setting up the Ansible Jinja2 Playground on your system.

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu/Debian, CentOS/RHEL, Fedora), macOS, or Windows WSL2
- **Python**: Version 3.9 or higher
- **Ansible**: Version 2.14+ (for full compatibility)
- **Memory**: Minimum 512MB RAM
- **Storage**: 150MB free disk space
- **Network**: Internet connection for package downloads

### Required Software

- Python 3.9+
- pip (Python package manager)
- virtualenv or venv
- git (for cloning repository)
- Ansible 2.14+ (automatically installed with requirements)

## Installation Methods

### Method 1: Container Deployment (Recommended)

#### Prerequisites

- **Podman** or **Docker** installed
- **Git** for cloning repository
- **curl** (for health checks)

#### Quick Container Setup

```bash
# Clone repository
git clone <repository-url>
cd ansible_jinja2_playground

# Option A: Using helper script (recommended)
./container.sh run

# Option B: Using Podman directly
podman build -t ansible-jinja2-playground -f Containerfile .
podman run -d --name playground -p 8000:8000 \
  -v "$(pwd)/conf:/home/playground/app/conf" \
  -v "$(pwd)/inputs:/home/playground/app/inputs:ro" \
  ansible-jinja2-playground

# Option C: Using Podman Compose
podman-compose up -d
```

#### Container Benefits

- **Isolated Environment**: No system dependency conflicts
- **Consistent Setup**: Works across different operating systems
- **Easy Deployment**: Single command installation
- **Security**: Non-root execution and read-only filesystem
- **Persistence**: Configuration and data preserved in volumes

### Method 2: Virtual Environment Setup (Traditional)

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd ansible_jinja2_playground
```

#### 2. Create Virtual Environment

```bash
# Using venv (Python 3.9+)
python3.9 -m venv /path/to/venvs/python3.9-ansible2.14

# Or using virtualenv
virtualenv -p python3.9 /path/to/venvs/python3.9-ansible2.14
```

#### 3. Activate Virtual Environment

```bash
# Linux/macOS
source /path/to/venvs/python3.9-ansible2.14/bin/activate

# Windows (if using WSL2)
source /path/to/venvs/python3.9-ansible2.14/bin/activate
```

#### 4. Install Dependencies

```bash
pip install -r pip-venv-requirements.txt
```

#### 5. Verify Installation

```bash
python run.py --version
```

#### 6. Test New Features (v2.1)

Test the Ansible compatibility scanner:

```bash
# Start the server in background
python run.py &

# Run compatibility scan
python scan_ansible_filters.py --report-only

# Kill background server
pkill -f "python run.py"
```

Test the history cleanup utility:

```bash
# Check for duplicate entries
python deduplicate_history.py --dry-run

# View help for all options
python deduplicate_history.py --help
```

### Method 2: System-wide Installation

⚠️ **Warning**: System-wide installation is not recommended as it may cause conflicts with other Python projects.

```bash
# Install dependencies globally
pip3 install -r pip-venv-requirements.txt

# Run the application
python3 run.py
```

## Dependencies

### Core Dependencies

The `pip-venv-requirements.txt` file contains all required packages:

```
ansible>=2.14.0,<3.0.0
jinja2>=3.1.0
pyyaml>=6.0
markupsafe>=2.1.0
```

### Optional Dependencies

For development and testing:

```bash
pip install pytest>=7.0.0
pip install black>=22.0.0
pip install flake8>=4.0.0
```

## Configuration

### 1. Environment Setup

Create the necessary directory structure:

```bash
mkdir -p conf inputs
```

### 2. Configuration Files

The application will create default configuration files on first run:

- `conf/ansible_jinja2_playground.conf` - Main configuration
- `conf/ansible_jinja2_playground_history.json` - History storage

### 3. Input Directory

Place your test files in the `inputs/` directory:

```bash
# Example input files
cp examples/*.json inputs/
cp examples/*.yaml inputs/
```

### 4. Permissions

Ensure proper file permissions:

```bash
chmod 755 run.py
chmod 644 conf/*
chmod 644 inputs/*
```

## Platform-Specific Instructions

### Ubuntu/Debian

#### Install Prerequisites

```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip git
```

#### Create Virtual Environment

```bash
python3.9 -m venv ~/venvs/python3.9-ansible2.14
source ~/venvs/python3.9-ansible2.14/bin/activate
```

### CentOS/RHEL 8+

#### Install Prerequisites

```bash
sudo dnf install python39 python39-pip git
```

#### Create Virtual Environment

```bash
python3.9 -m venv ~/venvs/python3.9-ansible2.14
source ~/venvs/python3.9-ansible2.14/bin/activate
```

### Fedora

#### Install Prerequisites

```bash
sudo dnf install python3 python3-pip git python3-virtualenv
```

#### Create Virtual Environment

```bash
python3 -m venv ~/venvs/python3.9-ansible2.14
source ~/venvs/python3.9-ansible2.14/bin/activate
```

### macOS

#### Install Prerequisites (using Homebrew)

```bash
brew install python@3.9 git
```

#### Create Virtual Environment

```bash
python3.9 -m venv ~/venvs/python3.9-ansible2.14
source ~/venvs/python3.9-ansible2.14/bin/activate
```

### Windows (WSL2)

#### Install WSL2 and Ubuntu

1. Enable WSL2 in Windows Features
2. Install Ubuntu from Microsoft Store
3. Follow Ubuntu instructions above

## Verification

### 1. Test Server Startup

```bash
# Activate virtual environment
source /path/to/venvs/python3.9-ansible2.14/bin/activate

# Start the server
python run.py

# Expected output:
# Starting server on http://localhost:8000
# Press Ctrl+C to stop
```

### 2. Test Frontend Access

- Open browser to `http://localhost:8000`
- Verify interface loads correctly
- Test basic template rendering

### 3. Test Backend API

```bash
# Test render endpoint
curl -X POST http://localhost:8000/render \
  -d "json={\"name\":\"test\"}" \
  -d "expr=Hello {{ name }}!"

# Expected response:
# {"result":"Hello test!","success":true,"input_format":"JSON"}
```

## Troubleshooting

### Common Installation Issues

#### 1. Python Version Conflicts

```bash
# Check Python version
python --version
python3 --version
python3.9 --version

# Use specific version
python3.9 -m venv venv_name
```

#### 2. Permission Errors

```bash
# Fix file permissions
chmod +x run.py
sudo chown -R $USER:$USER .
```

#### 3. Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rm -rf /path/to/venvs/python3.9-ansible2.14
python3.9 -m venv /path/to/venvs/python3.9-ansible2.14
```

#### 4. Package Installation Failures

```bash
# Upgrade pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install with verbose output
pip install -v -r pip-venv-requirements.txt
```

#### 5. Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000
netstat -tulpn | grep 8000

# Kill process using port
sudo kill -9 <PID>

# Or use different port
python run.py --port 8080
```

### Network Issues

#### Firewall Configuration

```bash
# Ubuntu/Debian
sudo ufw allow 8000

# CentOS/RHEL
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

#### Proxy Settings

```bash
# Set proxy for pip
pip install --proxy http://proxy.example.com:8080 -r pip-venv-requirements.txt

# Set environment variables
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### Container Issues

#### 1. Container Build Failures

```bash
# Check Podman/Docker installation
podman --version

# Clear build cache
podman system prune -a

# Build with verbose output
podman build --no-cache -t ansible-jinja2-playground -f Containerfile .
```

#### 2. Container Runtime Issues

```bash
# Check container status
podman ps -a

# Check container logs
podman logs ansible-jinja2-playground

# Inspect container configuration
podman inspect ansible-jinja2-playground
```

#### 3. Volume Mount Problems

```bash
# Check volume permissions
ls -la conf/ inputs/

# Fix ownership if needed
sudo chown -R 1000:1000 conf/

# Verify volume mounts
podman inspect ansible-jinja2-playground | grep -A 10 "Mounts"
```

#### 4. Port Binding Issues

```bash
# Check port availability
ss -tlnp | grep 8000

# Use different port
podman run -p 8080:8000 ansible-jinja2-playground

# Check container networking
podman exec ansible-jinja2-playground netstat -tlnp
```

#### 5. Container Health Issues

```bash
# Check health status
podman inspect --format='{{.State.Health.Status}}' ansible-jinja2-playground

# Manual health check
curl -f http://localhost:8000/

# Debug container environment
podman exec -it ansible-jinja2-playground /bin/bash
```

## Performance Optimization

### 1. Virtual Environment Location

- Place virtual environment on fast storage (SSD)
- Avoid network drives for virtual environments

### 2. Python Optimization

```bash
# Use optimized Python compilation
export PYTHONOPTIMIZE=2

# Increase Python memory limits if needed
export PYTHONMALLOC=malloc
```

### 3. System Resources

- Ensure adequate RAM (minimum 512MB)
- Monitor disk space in `conf/` directory
- Regular cleanup of history files if needed

## Security Considerations

### 1. Virtual Environment Isolation

- Always use virtual environments in production
- Regularly update dependencies
- Monitor for security vulnerabilities

### 2. File System Permissions

```bash
# Secure configuration directory
chmod 750 conf/
chmod 640 conf/*.conf

# Secure input directory
chmod 755 inputs/
chmod 644 inputs/*
```

### 3. Network Security

- Use firewall rules to restrict access
- Consider reverse proxy for production
- Enable HTTPS for public deployments

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate environment
deactivate

# Remove virtual environment directory
rm -rf /path/to/venvs/python3.9-ansible2.14
```

### Remove Application Files

```bash
# Remove application directory
rm -rf ansible_jinja2_playground

# Remove any system-wide packages (if installed globally)
pip uninstall ansible jinja2 pyyaml markupsafe
```

## Next Steps

After successful installation:

1. **Read Usage Guide**: See `USAGE.md` for detailed usage instructions
2. **Explore Examples**: Check `inputs/` directory for sample files
3. **Review Configuration**: Understand settings in `conf/` directory
4. **Test Loop Functionality**: See `LOOP_USAGE.md` for advanced features

For additional support, consult the project documentation or community forums.
