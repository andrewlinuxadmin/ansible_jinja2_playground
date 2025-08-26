# Release Notes v2.2.0

## Ansible Jinja2 Playground v2.2.0 - Container Optimization & Enhanced Configuration

**Release Date**: August 26, 2025

This v2.2.0 release focuses on **container optimization**, **enhanced configuration management**, and **development workflow improvements**. Major improvements include optimized Docker builds, comprehensive configuration documentation, and advanced development tools.

## 🎯 Major Features

### Container & Build Optimization
- **Optimized Containerfile**: Reduced from 26 to 12 layers (54% reduction)
- **Test Removal**: Unit tests executed during build and removed from production image
- **Layer Consolidation**: Combined RUN commands for better Docker practices
- **Build Context Optimization**: Added comprehensive .dockerignore
- **Automatic Configuration**: Container-ready with host binding and history cleanup

### Enhanced Configuration Management
- **New Configuration Sections**: Added `[listener]` section for real-time updates
- **Expanded Settings**: New `refresh_interval` and `api-listener-enabled` options
- **Environment-Specific Configs**: Support for development, production, and container configurations
- **Dynamic Updates**: Most settings apply without restart
- **Comprehensive Documentation**: Complete configuration reference in `conf/README.md`

### Development Workflow Improvements
- **VS Code Auto-Close**: Automatic tab closure for deleted files
- **Podman Cleanup Scripts**: Automated cleanup for dangling images and containers
- **Enhanced Linting**: Updated markdownlint rules and Python formatting
- **Project Structure**: Complete self-contained structure with all dependencies

## 🔧 Technical Improvements

### Container Optimization Details
```dockerfile
# Before: Multiple RUN commands, 26 layers
# After: Consolidated operations, 12 layers

RUN system_setup && \
    python_packages && \
    configuration && \
    test_execution && \
    cleanup_and_optimization
```

### Configuration Schema Updates
```ini
[listener]
refresh_interval = 5

[user]
api-listener-enabled = false
```

### Build Process Enhancement
- Tests execute during container build (79 tests, 100% pass rate)
- Automatic failure on test failures
- Complete test removal from production image
- Build context size reduction with .dockerignore

## 📋 Complete Feature List

### Container & Infrastructure
- ✅ **12-layer optimized Containerfile** (down from 26)
- ✅ **Automatic test execution and cleanup** during build
- ✅ **Container-ready configuration** (host = 0.0.0.0)
- ✅ **History file cleanup** in production images
- ✅ **Comprehensive .dockerignore** for build optimization

### Configuration Management
- ✅ **Enhanced configuration sections** with new options
- ✅ **Dynamic configuration updates** without restart
- ✅ **Environment-specific configurations** support
- ✅ **Complete configuration documentation** and examples
- ✅ **Configuration validation** tools

### Development Tools
- ✅ **VS Code workspace optimization** with auto-close tabs
- ✅ **Podman cleanup automation** scripts
- ✅ **Enhanced development tasks** in VS Code
- ✅ **Comprehensive linting rules** for code quality
- ✅ **Self-contained project structure**

### Quality & Testing
- ✅ **79 comprehensive unit tests** (100% pass rate)
- ✅ **Automated test execution** in container builds
- ✅ **Build failure on test failures** for CI/CD safety
- ✅ **Code quality enforcement** with linting
- ✅ **Documentation consistency** across all files

## 🛠️ Installation & Upgrade

### New Installation
```bash
# Clone repository
git clone https://github.com/andrewlinuxadmin/ansible_jinja2_playground.git
cd ansible_jinja2_playground

# Build optimized container
podman build -t ansible-jinja2-playground .

# Run container
podman run -p 8000:8000 ansible-jinja2-playground
```

### Container Usage
```bash
# Run with volume mounting for persistent configs
podman run -p 8000:8000 \
  -v ./inputs:/home/playground/inputs:ro \
  ansible-jinja2-playground
```

### Development Setup
```bash
# Install dependencies
pip install -r ansible-jinja2-playground/requirements.txt

# Run tests
python tests/run_all_tests.py

# Run application
python ansible-jinja2-playground/run.py
```

## 🔄 Migration from v2.1

### Configuration Updates
- Review new `[listener]` section options
- Update `api-listener-enabled` setting if needed
- Check `refresh_interval` settings for performance

### Container Users
- Rebuild containers with new optimized Containerfile
- Update docker-compose files if using custom configurations
- Clean up old dangling images with provided cleanup scripts

### Developers
- Update VS Code settings for enhanced development experience
- Use new Podman cleanup scripts for maintenance
- Review updated configuration documentation

## 🐛 Bug Fixes & Improvements

- **Container Build**: Fixed layer optimization and reduced image size
- **Configuration Management**: Improved validation and error handling
- **Development Workflow**: Enhanced VS Code integration and tooling
- **Documentation**: Updated all configuration references and examples
- **Testing**: Ensured 100% test coverage with container validation

## 📊 Performance Metrics

- **Container Size**: Maintained at ~1.09GB with enhanced functionality
- **Build Time**: Improved with better layer caching
- **Test Execution**: 79 tests in ~3.4 seconds
- **Memory Usage**: Optimized with cleanup and efficient layering

## 🔒 Security Enhancements

- **Production Images**: No test code in final containers
- **Configuration Security**: Enhanced file permission recommendations
- **Build Validation**: Mandatory test passing for image creation
- **Clean Runtime**: Minimal attack surface with optimized layers

## 📈 Development Statistics

- **Files Modified**: 15+ configuration and container files
- **New Scripts**: 2 Podman cleanup automation scripts
- **Documentation**: Complete rewrite of configuration guide
- **Test Coverage**: Maintained 79 tests with 100% pass rate
- **Container Optimization**: 54% layer reduction

---

**Full Changelog**: [v2.1...v2.2](https://github.com/andrewlinuxadmin/ansible_jinja2_playground/compare/v2.1...v2.2)

**Download**: [ansible-jinja2-playground-v2.2.0.tar.gz](https://github.com/andrewlinuxadmin/ansible_jinja2_playground/releases/download/v2.2.0/ansible-jinja2-playground-v2.2.0.tar.gz)
