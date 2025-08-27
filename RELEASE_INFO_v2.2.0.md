# Ansible Jinja2 Playground v2.2.0 Release

## 📦 Release Package

**File**: `ansible-jinja2-playground-v2.2.0.tar.gz`
**Size**: Updated with enhanced loop functionality
**SHA256**: `$(cat ansible-jinja2-playground-v2.2.0.tar.gz.sha256 | cut -d' ' -f1)`

## 🆕 NEW IN v2.2.0: Enhanced Loop Functionality

### 🔄 Jinja2 Expression Support in Loops
Now supports **Jinja2 expressions** in the `loop_variable` field, bringing full Ansible compatibility:

```yaml
# NEW: Jinja2 expressions
loop_variable: "services.keys() | list"
loop_variable: "services.values() | list"
loop_variable: "range(5) | list"
loop_variable: "users | selectattr('active') | list"

# Still supported: Simple paths
loop_variable: "services"
loop_variable: "data.services"
```

### 🧠 Smart Auto-Detection
- **Expressions** (contains `|`, `(`, `[`) → Evaluated as Jinja2
- **Simple paths** → Navigation by dot notation
- **Full backward compatibility** maintained

## 📋 Package Contents

This release contains the enhanced application files from `ansible-jinja2-playground/`:

### Core Application
- `ansible_jinja2_playground.py` - **Enhanced** with Jinja2 expression support
- `ansible_jinja2_playground.html` - Web interface
- `run.py` - Application entry point

### Support Scripts
- `scan_ansible_filters.py` - Ansible compatibility scanner
- `deduplicate_history.py` - History cleanup utility
- `test_scan.json` - Filter/test discovery data

### Configuration
- `conf/` - Configuration directory
  - `ansible_jinja2_playground.conf` - Main configuration file
  - `ansible_jinja2_playground_history.json` - Command history
  - `README.md` - Configuration documentation

### Dependencies
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies

## 🚀 Quick Start

1. **Extract**: `tar -xzf ansible-jinja2-playground-v2.2.0.tar.gz`
2. **Install**: `pip install -r requirements.txt`
3. **Run**: `python run.py`
4. **Access**: `http://localhost:8000`

## ✅ Verification

```bash
# Verify package integrity
sha256sum -c ansible-jinja2-playground-v2.2.0.tar.gz.sha256
```

## 🎯 Enhanced Loop Examples

### Dictionary Keys/Values
```bash
# Input: {"services": {"web": "nginx", "api": "fastapi"}}
loop_variable: "services.keys() | list"    # → ["web", "api"]
loop_variable: "services.values() | list"  # → ["nginx", "fastapi"]
```

### Range Generation
```bash
# Generate number sequences
loop_variable: "range(5) | list"           # → [0, 1, 2, 3, 4]
```

### Complex Filters
```bash
# Filter active users
loop_variable: "users | selectattr('active') | list"
```

### Data Object Access
```bash
# Access via data object
loop_variable: "data.services.keys() | list"
```

## 🧪 Testing

- **8 new comprehensive tests** for Jinja2 expressions
- **86 total tests** with 100% pass rate
- **Comprehensive error handling** and validation
- **Backward compatibility** verified

## 🔗 What's New in v2.2.0

### 🆕 Enhanced Loop Functionality
- **Jinja2 Expression Support**: Full compatibility with Ansible loop syntax
- **Auto-Detection**: Smart detection of expressions vs simple paths
- **Error Handling**: Clear error messages for invalid expressions
- **Performance**: Efficient evaluation with proper context

### 🐳 Container Optimization (from v2.2.0 base)
- **54% Layer Reduction**: Optimized from 26 to 12 Docker layers
- **Enhanced Configuration**: New sections and dynamic settings
- **Development Tools**: VS Code integration and cleanup scripts
- **Build Improvements**: Comprehensive .dockerignore and optimized builds

### 📚 Documentation
- Complete configuration reference and updated guides
- Enhanced loop usage examples and best practices

See `RELEASE_NOTES_v2.2.md` for complete feature details.
