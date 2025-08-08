#!/usr/bin/env python3
"""
Ansible Jinja2 Playground - Runner Script
Entry point script to run the application from the project root.
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
    import ansible_jinja2_playground
    from ansible_jinja2_playground import JinjaHandler, HTML_FILE_PATH, CONF_PATH, HOST, PORT

    if __name__ == '__main__':
        print(f"Server started at http://{HOST}:{PORT}")
        print(f"Project root: {current_dir}")
        print(f"Configuration: {CONF_PATH}")
        print(f"Input files: {os.path.join(current_dir, 'inputs')}")
        HTTPServer((HOST, PORT), JinjaHandler).serve_forever()

except Exception as e:
    print(f"Error starting server: {e}")
    os.chdir(original_cwd)
    sys.exit(1)
