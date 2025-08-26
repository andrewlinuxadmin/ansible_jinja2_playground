#!/usr/bin/env python3
"""
Ansible Jinja2 Playground - Runner Script
Entry point script to run the application.

Configuration:
- Server settings (host, port) can be modified in conf/ansible_jinja2_playground.conf
- Default port: 8000
- Default host: 127.0.0.1

Usage:
  python ansible-jinja2-playground/run.py

Note: Activate the virtual environment before running.
"""

import os
import sys
from http.server import HTTPServer

# Set up paths - we're already in the ansible-jinja2-playground directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
  # Import and run the main application
  from ansible_jinja2_playground import JinjaHandler, CONF_PATH, HOST, PORT

  if __name__ == '__main__':
    print(f"Server started at http://{HOST}:{PORT}")
    print(f"Application directory: {current_dir}")
    print(f"Configuration: {CONF_PATH}")
    print("")
    print("💡 To change the server port:")
    print(f"   Edit the 'port' value in the [server] section of: {CONF_PATH}")
    print("   Example: port = 8080")
    print("")
    HTTPServer((HOST, PORT), JinjaHandler).serve_forever()

except Exception as e:
  print(f"Error starting server: {e}")
  sys.exit(1)
