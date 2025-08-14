#!/usr/bin/env python3
"""
Ansible Jinja2 Playground - Runner Script
Entry point script to run the application from the project root.

Configuration:
- Server settings (host, port) can be modified in conf/ansible_jinja2_playground.conf
- Default port: 8000
- Default host: 127.0.0.1

Usage:
  python run.py

Note: Make sure to activate the virtual environment before running:
  source /home/acarlos/Dropbox/RedHat/Ansible/venvs/python3.9-ansible2.14/bin/activate
"""

import os
import sys
from http.server import HTTPServer

# Add the app directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, 'app')
sys.path.insert(0, app_dir)

# Change to app directory to maintain relative imports
original_cwd = os.getcwd()
os.chdir(app_dir)

try:
    # Import and run the main application
    from ansible_jinja2_playground import JinjaHandler, CONF_PATH, HOST, PORT

    if __name__ == '__main__':
        print(f"Server started at http://{HOST}:{PORT}")
        print(f"Project root: {current_dir}")
        print(f"Configuration: {CONF_PATH}")
        print(f"Input files: {os.path.join(current_dir, 'inputs')}")
        print("")
        print("💡 To change the server port:")
        print(f"   Edit the 'port' value in the [server] section of: {CONF_PATH}")
        print("   Example: port = 8080")
        print("")
        HTTPServer((HOST, PORT), JinjaHandler).serve_forever()

except Exception as e:
    print(f"Error starting server: {e}")
    os.chdir(original_cwd)
    sys.exit(1)
