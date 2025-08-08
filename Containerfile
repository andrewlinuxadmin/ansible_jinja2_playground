# Containerfile for Ansible Jinja2 Playground
# Single-stage build using UBI9 Python 3.9

FROM registry.access.redhat.com/ubi9/python-39:latest

# Switch to root for system configuration
USER root

# Install additional runtime dependencies
RUN dnf update -y && \
    dnf install -y curl --allowerasing && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# Create application user
RUN useradd -m -u 1000 playground || true

# Copy application files (as root first)
COPY . /home/playground/app
RUN chown -R playground:playground /home/playground/app

# Install Python dependencies as root
RUN python3.9 -m pip install --no-cache-dir --upgrade pip && \
    python3.9 -m pip install --no-cache-dir -r /home/playground/app/pip-venv-requirements.txt

# Set up application directory
USER playground
WORKDIR /home/playground/app

# Create necessary directories with proper permissions
RUN mkdir -p conf inputs && \
    chmod 755 conf inputs

# Configure Ansible environment for testing
ENV ANSIBLE_HOST_KEY_CHECKING=false
ENV ANSIBLE_LOCAL_TEMP=/tmp/ansible
ENV ANSIBLE_REMOTE_TEMP=/tmp/ansible
RUN mkdir -p /tmp/ansible && chmod 755 /tmp/ansible

# Run unit tests - build will fail if tests don't pass
WORKDIR /home/playground/app
RUN echo "🧪 Running unit tests before build completion..." && \
    ls -la tests/ && \
    python3.9 tests/run_all_tests.py && \
    echo "✅ All tests passed! Build can continue..." && \
    python3.9 tests/cleanup_tests.py --temp-only

# Ensure Python packages are in PATH
ENV PATH="/home/playground/.local/bin:$PATH"
ENV PYTHONPATH="/home/playground/app"

# Expose the default port
EXPOSE 8000

# Default command to run the application
CMD ["python3.9", "/home/playground/app/run.py"]

# Metadata labels
LABEL maintainer="Ansible Jinja2 Playground Team"
LABEL description="A web-based playground for testing Ansible Jinja2 templates"
LABEL version="1.0.0"
LABEL org.opencontainers.image.title="Ansible Jinja2 Playground"
LABEL org.opencontainers.image.description="Interactive web interface for testing and developing Ansible Jinja2 templates"
LABEL org.opencontainers.image.source="https://github.com/andrewlinuxadmin/ansible_jinja2_playground"
LABEL org.opencontainers.image.licenses="GPL-3.0"
