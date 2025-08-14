# Requirements Files

This project uses two separate requirements files to manage dependencies:

## Production Dependencies (`requirements.txt`)

Contains only the essential packages needed to run the application:

- `jmespath` - JSON path expressions
- `ansible-core` - Ansible core functionality (version 2.14.18)
- `jinja2` - Template engine
- `httpx` - HTTP client for testing endpoints
- `PyYAML` - YAML parser

**Installation:**

```bash
pip install -r requirements.txt
```

## Development Dependencies (`requirements-dev.txt`)

Contains tools and packages needed for development, testing, and code quality:

- `flake8` - Code linting
- `autopep8` - Code formatting
- `ansible-lint` - Ansible-specific linting
- `pytest` - Testing framework
- `pytest-cov` - Test coverage
- `black` - Code formatter
- `isort` - Import sorting
- `sphinx` - Documentation generation

**Installation:**

```bash
pip install -r requirements-dev.txt
```

## Quick Setup

For a complete development environment:

```bash
# Install production dependencies first
pip install -r requirements.txt

# Then install development tools
pip install -r requirements-dev.txt
```

## VS Code Tasks

You can also use the VS Code tasks:

- `📦 Install Dependencies` - Installs production requirements
- `🛠️ Install Dev Dependencies` - Installs development requirements

Access these through `Ctrl+Shift+P` → `Tasks: Run Task`
