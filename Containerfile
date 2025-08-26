# Containerfile for Ansible Jinja2 Playground
# Optimized single-stage build using UBI9 Python 3.9

FROM registry.access.redhat.com/ubi9/python-39:latest

# Switch to root for system configuration
USER root

# Copy only requirements file first (for better layer caching)
COPY ansible-jinja2-playground/requirements.txt /tmp/requirements.txt

# Install system dependencies and Python packages in single layer
RUN dnf update -y && \
  dnf install -y curl --allowerasing && \
  dnf clean all && \
  rm -rf /var/cache/dnf && \
  useradd -m -u 1000 playground && \
  python3.9 -m pip install --no-cache-dir --upgrade pip && \
  python3.9 -m pip install --no-cache-dir -r /tmp/requirements.txt && \
  rm -f /tmp/requirements.txt

# Copy application files
COPY . /home/playground/ansible-jinja2-playground

# Configure application, run tests, and cleanup in single layer
RUN chown -R playground:playground /home/playground/ansible-jinja2-playground && \
  sed -i 's/host = 127.0.0.1/host = 0.0.0.0/' /home/playground/ansible-jinja2-playground/ansible-jinja2-playground/conf/ansible_jinja2_playground.conf && \
  echo '[]' > /home/playground/ansible-jinja2-playground/ansible-jinja2-playground/conf/ansible_jinja2_playground_history.json && \
  mkdir -p /tmp/ansible && \
  chmod 755 /tmp/ansible && \
  cd /home/playground/ansible-jinja2-playground && \
  echo "🧪 Running unit tests..." && \
  python3.9 tests/run_all_tests.py && \
  echo "✅ Tests passed! Cleaning up test files..." && \
  python3.9 tests/cleanup_tests.py --temp-only && \
  rm -rf tests/ && \
  echo "🗑️ Test directory removed from production image" && \
  find . -name "*.pyc" -delete && \
  find . -name "__pycache__" -type d -exec rm -rf {} + || true

# Switch to application user and set working directory
USER playground
WORKDIR /home/playground/ansible-jinja2-playground

# Runtime environment configuration
ENV ANSIBLE_HOST_KEY_CHECKING=false \
  ANSIBLE_LOCAL_TEMP=/tmp/ansible \
  ANSIBLE_REMOTE_TEMP=/tmp/ansible \
  PATH="/home/playground/.local/bin:$PATH" \
  PYTHONPATH="/home/playground/ansible-jinja2-playground"

# Expose the default port
EXPOSE 8000

# Default command to run the application
CMD ["python3.9", "ansible-jinja2-playground/run.py"]

# Metadata labels (consolidated)
LABEL maintainer="Ansible Jinja2 Playground Team" \
  description="A web-based playground for testing Ansible Jinja2 templates" \
  version="2.2.0" \
  org.opencontainers.image.title="Ansible Jinja2 Playground" \
  org.opencontainers.image.description="Interactive web interface for testing and developing Ansible Jinja2 templates" \
  org.opencontainers.image.source="https://github.com/andrewlinuxadmin/ansible_jinja2_playground" \
  org.opencontainers.image.licenses="GPL-3.0"
