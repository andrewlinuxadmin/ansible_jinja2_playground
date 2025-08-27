import json
import os
import configparser
import datetime
import base64
import yaml
import uuid
import ast

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from jinja2.sandbox import SandboxedEnvironment as Environment
from jinja2 import StrictUndefined
from ansible.plugins.filter.core import FilterModule as CoreFilters
from ansible.plugins.filter.mathstuff import FilterModule as MathFilters
from ansible.plugins.filter.urls import FilterModule as UrlFilters
from ansible.plugins.filter.urlsplit import FilterModule as UrlSplitFilters
from ansible.plugins.filter.encryption import FilterModule as EncryptionFilters
from ansible.plugins.test.core import TestModule as CoreTests
from ansible.plugins.test.files import TestModule as FileTests
from ansible.plugins.test.mathstuff import TestModule as MathTests
from ansible.plugins.test.uri import TestModule as UriTests

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
SCRIPT_BASE = os.path.splitext(os.path.basename(__file__))[0]
HTML_FILE_PATH = os.path.join(CURRENT_DIR, SCRIPT_BASE + '.html')
CONF_PATH = os.path.join(CURRENT_DIR, 'conf', SCRIPT_BASE + '.conf')
JSON_HISTORY_PATH = os.path.join(CURRENT_DIR, 'conf', SCRIPT_BASE + '_history.json')

# Load or create configuration
config = configparser.ConfigParser()

# Default configuration values
default_config = {
    'server': {
        'host': '0.0.0.0',
        'port': '8000'
    },
    'history': {'max_entries': '1000'},
    'input_files': {
        'directory': 'inputs',
        'refresh_interval': '30'
    },
    'listener': {
        'refresh_interval': '5'
    },
    'user': {
        'theme': 'dark',
        'height-inputcode': '100',
        'height-jinjaexpr': '200',
        'height-resultview': '1000',
        'api-listener-enabled': 'false'
    }
}


def entries_are_identical(entry1, entry2):
  """
  Compare two history entries excluding datetime field.
  Returns True if entries are identical in content.
  """
  if not entry1 or not entry2:
    return False

  # Compare all fields except datetime
  fields_to_compare = ['input', 'expr', 'enable_loop', 'loop_variable']

  for field in fields_to_compare:
    if entry1.get(field) != entry2.get(field):
      return False

  return True


def validate_input_directory(directory):
  """
  Validate that input directory is safe and within application structure.
  Returns sanitized directory path or raises ValueError for unsafe paths.
  """
  if not directory:
    return 'inputs'  # Default safe directory

  # Remove any dangerous characters and normalize
  directory = directory.strip()

  # Convert to absolute path for validation
  if os.path.isabs(directory):
    abs_dir = os.path.abspath(directory)
  else:
    abs_dir = os.path.abspath(os.path.join(PROJECT_ROOT, directory))

  # Get the real paths to avoid symlink attacks
  try:
    real_project_root = os.path.realpath(PROJECT_ROOT)
    real_abs_dir = os.path.realpath(abs_dir)
  except Exception:
    raise ValueError("Invalid directory path")

  # Security check: directory must be within project root
  if not real_abs_dir.startswith(real_project_root + os.sep) and real_abs_dir != real_project_root:
    raise ValueError(f"Security violation: Input directory must be within project structure ({PROJECT_ROOT})")

  # Additional security checks for dangerous system directories
  dangerous_paths = [
      '/etc', '/root', '/usr', '/var', '/bin', '/sbin', '/boot',
      '/dev', '/proc', '/sys', '/tmp', '/opt', '/lib', '/lib64'
  ]

  for dangerous in dangerous_paths:
    if real_abs_dir.startswith(dangerous + os.sep) or real_abs_dir == dangerous:
      raise ValueError(f"Security violation: Access to system directory '{dangerous}' is forbidden")

  # Convert back to relative path if it was originally relative
  if not os.path.isabs(directory):
    try:
      return os.path.relpath(real_abs_dir, real_project_root)
    except ValueError:
      # If relative path calculation fails, use absolute path validation
      pass

  return directory


if not os.path.exists(CONF_PATH):
  # Create new configuration with default values
  for section, options in default_config.items():
    config[section] = options
  # Create conf directory if it doesn't exist
  os.makedirs(os.path.dirname(CONF_PATH), exist_ok=True)
  with open(CONF_PATH, 'w', encoding='utf-8') as conf_file:
    config.write(conf_file)
else:
  # Load existing configuration
  config.read(CONF_PATH)

  # Check for missing sections/options and add them with defaults
  config_updated = False
  for section, options in default_config.items():
    if not config.has_section(section):
      config.add_section(section)
      config_updated = True
    for option, value in options.items():
      if not config.has_option(section, option):
        config.set(section, option, value)
        config_updated = True

  # Validate and sanitize input directory for security
  if config.has_section('input_files') and config.has_option('input_files', 'directory'):
    current_dir = config.get('input_files', 'directory')
    try:
      safe_dir = validate_input_directory(current_dir)
      if safe_dir != current_dir:
        print(f"WARNING: Input directory '{current_dir}' is unsafe. Resetting to safe default: '{safe_dir}'")
        config.set('input_files', 'directory', safe_dir)
        config_updated = True
    except ValueError as e:
      print(f"SECURITY WARNING: {e}")
      print("Resetting input directory to safe default: 'inputs'")
      config.set('input_files', 'directory', 'inputs')
      config_updated = True

  # Save updated configuration if anything was added or changed
  if config_updated:
    with open(CONF_PATH, 'w', encoding='utf-8') as conf_file:
      config.write(conf_file)

# Initial max entries
MAX_ENTRIES = int(config.get('history', 'max_entries', fallback='1000'))

# Server configuration
HOST = config.get('server', 'host', fallback='0.0.0.0')
PORT = int(config.get('server', 'port', fallback='8000'))

with open(HTML_FILE_PATH, 'r', encoding='utf-8') as f:
  HTML_PAGE = f.read()

env = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=StrictUndefined
)
env.filters.update(CoreFilters().filters())
env.filters.update(MathFilters().filters())
env.filters.update(UrlFilters().filters())
env.filters.update(UrlSplitFilters().filters())
env.filters.update(EncryptionFilters().filters())

# Adiciona todos os testes extras do Ansible-core
env.tests.update(CoreTests().tests())
env.tests.update(FileTests().tests())
env.tests.update(MathTests().tests())
env.tests.update(UriTests().tests())


class JinjaHandler(BaseHTTPRequestHandler):
  def _send_headers(self, status=200, content_type='text/html', extra_headers=None):
    self.send_response(status)
    self.send_header('Content-type', content_type)
    self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
    self.send_header('Pragma', 'no-cache')
    self.send_header('Expires', '0')
    if extra_headers:
      for key, value in extra_headers.items():
        self.send_header(key, value)
    self.end_headers()

  def do_GET(self):
    parsed = urlparse(self.path)
    path = parsed.path
    params = parse_qs(parsed.query)

    if path == '/history':
      self._send_headers(200, 'application/json')
      try:
        with open(JSON_HISTORY_PATH, 'r', encoding='utf-8') as hist_file:
          raw_history = json.load(hist_file)
      except Exception:
        raw_history = []
      decoded = []
      for entry in raw_history:
        e = entry.copy()
        try:
          e['input'] = base64.b64decode(e.get('input', '')).decode('utf-8')
        except Exception:
          pass
        try:
          e['expr'] = base64.b64decode(e.get('expr', '')).decode('utf-8')
        except Exception:
          pass
        # Handle enable_loop as boolean (no base64 needed) - only if it exists
        if 'enable_loop' in e:
          e['enable_loop'] = e.get('enable_loop', False)
          if isinstance(e['enable_loop'], str):
            e['enable_loop'] = e['enable_loop'].lower() == 'true'
        # Keep loop_variable as plain text (no base64 encoding) - only if it exists
        if 'loop_variable' in e:
          e['loop_variable'] = e.get('loop_variable', '')
        decoded.append(e)
      self.wfile.write(json.dumps(decoded, indent=2).encode('utf-8'))
      return

    if path == '/history/size':
      self._send_headers(200, 'application/json')
      try:
        with open(JSON_HISTORY_PATH, 'r', encoding='utf-8') as f:
          hist = json.load(f)
      except Exception:
        hist = []
      self.wfile.write(json.dumps({'size': len(hist)}).encode('utf-8'))
      return

    if path == '/history/maxsize':
      self._send_headers(200, 'application/json')
      self.wfile.write(json.dumps({'max_size': MAX_ENTRIES}).encode('utf-8'))
      return

    if path == '/settings':
      self._send_headers(200, 'application/json')
      section = params.get('section', [None])[0]
      if section:
        data = dict(config[section]) if config.has_section(section) else {}
      else:
        data = {s: dict(config[s]) for s in config.sections()}
      self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
      return

    if path == '/input-files':
      self._send_headers(200, 'application/json')
      try:
        input_dir = config.get('input_files', 'directory', fallback='')
        if not input_dir:
          self.wfile.write(json.dumps([]).encode('utf-8'))
          return

        # Convert relative path to absolute if needed
        if not os.path.isabs(input_dir):
          input_dir = os.path.join(PROJECT_ROOT, input_dir)

        if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
          self.wfile.write(json.dumps([]).encode('utf-8'))
          return

        files = []
        for filename in os.listdir(input_dir):
          filepath = os.path.join(input_dir, filename)
          if os.path.isfile(filepath):
            files.append(filename)

        files.sort()
        self.wfile.write(json.dumps(files).encode('utf-8'))
      except Exception:
        self.wfile.write(json.dumps([]).encode('utf-8'))
      return

    if path == '/input-file-content':
      filename = params.get('filename', [None])[0]
      if not filename:
        self.send_error(400, 'Missing filename parameter')
        return

      try:
        input_dir = config.get('input_files', 'directory', fallback='')
        if not input_dir:
          self.send_error(404, 'Input directory not configured')
          return

        # Convert relative path to absolute if needed
        if not os.path.isabs(input_dir):
          input_dir = os.path.join(PROJECT_ROOT, input_dir)

        # Security check - prevent path traversal attacks
        # Remove any path separators and ensure filename is safe
        safe_filename = os.path.basename(filename)
        if safe_filename != filename or '..' in filename or '/' in filename or '\\' in filename:
          self.send_error(403, 'Access denied - invalid filename')
          return

        filepath = os.path.join(input_dir, safe_filename)

        # Additional security check - ensure resolved path is within directory
        try:
          real_input_dir = os.path.realpath(input_dir)
          real_filepath = os.path.realpath(filepath)
          if not real_filepath.startswith(real_input_dir + os.sep):
            self.send_error(403, 'Access denied - path traversal detected')
            return
        except Exception:
          self.send_error(403, 'Access denied - path resolution error')
          return

        if not os.path.exists(filepath) or not os.path.isfile(filepath):
          self.send_error(404, 'File not found')
          return

        with open(filepath, 'r', encoding='utf-8') as f:
          content = f.read()

        self._send_headers(200, 'text/plain')
        self.wfile.write(content.encode('utf-8'))
        self.wfile.flush()
      except Exception as e:
        self.send_error(500, f'Error reading file: {e}')
      return

    if path != '/':
      self.send_error(404, 'File not found')
      return

    self._send_headers()
    self.wfile.write(HTML_PAGE.encode('utf-8'))

  def do_POST(self):
    global MAX_ENTRIES
    parsed = urlparse(self.path)
    path = parsed.path

    # Handle load_ansible_vars separately to avoid consuming the stream
    if path == '/load_ansible_vars':
      self.handle_load_ansible_vars()
      return

    length = int(self.headers.get('Content-Length', 0))
    post_data = self.rfile.read(length)
    params = parse_qs(post_data.decode())

    if path == '/history/clear':
      count = params.get('count', [None])[0]
      try:
        with open(JSON_HISTORY_PATH, 'r', encoding='utf-8') as f:
          hist = json.load(f)
      except Exception:
        hist = []
      original = len(hist)
      if count is None:
        hist = []
        cleared = original
      else:
        try:
          n = int(count)
          cleared = min(n, original)
          hist = hist[cleared:]
        except Exception:
          hist = []
          cleared = original
      # Create conf directory if it doesn't exist
      os.makedirs(os.path.dirname(JSON_HISTORY_PATH), exist_ok=True)
      with open(JSON_HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(hist, f, indent=2)
      self._send_headers(200, 'application/json')
      self.wfile.write(json.dumps({'cleared': cleared, 'size': len(hist)}).encode('utf-8'))
      return

    if path == '/settings':
      section = params.get('section', [None])[0]
      if not section:
        self._send_headers(400, 'application/json')
        self.wfile.write(json.dumps({'error': 'Missing section parameter'}).encode('utf-8'))
        return
      if not config.has_section(section):
        config[section] = {}

      # Apply security validation for input_files directory changes
      for k, v in params.items():
        if k == 'section':
          continue

        # Security check for input directory
        if section == 'input_files' and k == 'directory':
          try:
            safe_directory = validate_input_directory(v[0])
            config[section][k] = safe_directory
            if safe_directory != v[0]:
              print(f"SECURITY: Input directory '{v[0]}' was sanitized to '{safe_directory}'")
          except ValueError as e:
            self._send_headers(400, 'application/json')
            self.wfile.write(json.dumps({
                'error': f'Security validation failed: {str(e)}',
                'rejected_value': v[0]
            }).encode('utf-8'))
            return
        else:
          config[section][k] = v[0]

      # Create conf directory if it doesn't exist
      os.makedirs(os.path.dirname(CONF_PATH), exist_ok=True)
      with open(CONF_PATH, 'w', encoding='utf-8') as cf:
        config.write(cf)
      # update max entries if history section changed
      if section == 'history' and 'max_entries' in config['history']:
        try:
          MAX_ENTRIES = int(config.get('history', 'max_entries'))
        except Exception:
          pass
      self._send_headers(200, 'application/json')
      self.wfile.write(json.dumps({section: dict(config[section])}, indent=2).encode('utf-8'))
      return

    if path == '/history/mark_read':
      entry_id = params.get('id', [None])[0]
      if not entry_id:
        self._send_headers(400, 'application/json')
        self.wfile.write(json.dumps({'error': 'Missing id parameter'}).encode('utf-8'))
        return

      try:
        with open(JSON_HISTORY_PATH, 'r', encoding='utf-8') as f:
          hist = json.load(f)
      except Exception:
        hist = []

      # Find entry by ID and remove listener source
      entry_found = False
      for entry in hist:
        if entry.get('id') == entry_id:
          if entry.get('source') == 'listener':
            entry['source'] = 'manual'  # Change to manual to indicate it was read
          entry_found = True
          break

      if not entry_found:
        self._send_headers(404, 'application/json')
        self.wfile.write(json.dumps({'error': 'Entry not found'}).encode('utf-8'))
        return

      # Save updated history
      os.makedirs(os.path.dirname(JSON_HISTORY_PATH), exist_ok=True)
      with open(JSON_HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(hist, f, indent=2)

      self._send_headers(200, 'application/json')
      self.wfile.write(json.dumps({'status': 'success', 'id': entry_id}).encode('utf-8'))
      return

    if path != '/render':
      self._send_headers(404)
      self.send_error(404, 'Endpoint not found')
      return

    json_text = params.get('input', [''])[0] or params.get('json', [''])[0]
    expr = params.get('expr', [''])[0]

    # Loop parameters
    enable_loop = params.get('enable_loop', [''])[0] == 'true'
    loop_variable = params.get('loop_variable', [''])[0]

    # Try to parse as JSON first, then YAML if JSON fails
    try:
      data = json.loads(json_text)
      input_format = 'JSON'
    except json.JSONDecodeError:
      try:
        data = yaml.safe_load(json_text)
        input_format = 'YAML'
        # If yaml.safe_load returns None for empty string, treat as empty dict
        if data is None:
          data = {}
      except yaml.YAMLError as e:
        self._send_headers(400, 'text/plain')
        self.wfile.write(f'Input parsing error (tried JSON and YAML): {e}'.encode())
        return
      except Exception as e:
        self._send_headers(400, 'text/plain')
        self.wfile.write(f'Input parsing error: {e}'.encode())
        return

    try:
      template = env.from_string(expr)

      # Handle loop simulation
      if enable_loop and loop_variable:
        # Try to evaluate loop_variable as a Jinja2 expression first
        try:
          # If loop_variable contains Jinja2 expressions (filters, etc.), evaluate it
          if '|' in loop_variable or '(' in loop_variable or '[' in loop_variable:
            # Create context for evaluating the loop variable expression
            # Include both individual variables and data object access
            context = data.copy()
            context['data'] = data

            # Evaluate as Jinja2 expression
            loop_template = env.from_string('{{ ' + loop_variable + ' }}')
            loop_result = loop_template.render(**context)

            # Try to parse the result as Python literal (for lists, dicts, etc.)
            try:
              loop_data = ast.literal_eval(loop_result)
            except (ValueError, SyntaxError):
              # If literal_eval fails, try JSON parsing
              try:
                loop_data = json.loads(loop_result)
              except json.JSONDecodeError:
                raise ValueError(f"Loop variable expression '{loop_variable}' did not evaluate to a valid list/array")
          else:
            # Navigate to the loop variable in the data (original behavior for simple paths)
            loop_data = data
            parts = loop_variable.split('.')

            # Handle special case where first part is 'data' (refers to root)
            if parts[0] == 'data':
              # Skip 'data' prefix and start from the actual data
              parts = parts[1:]

            # Navigate through the remaining path
            for part in parts:
              if isinstance(loop_data, dict) and part in loop_data:
                loop_data = loop_data[part]
              else:
                raise ValueError(f"Loop variable '{part}' not found in input data")

        except Exception as e:
          raise ValueError(f"Error evaluating loop variable '{loop_variable}': {str(e)}")

        if not isinstance(loop_data, list):
          raise ValueError(f"Loop variable '{loop_variable}' must evaluate to an array/list, got {type(loop_data).__name__}")

        # Process each item in the loop
        results = []
        for item in loop_data:
          # Create context with the original data plus the current item
          loop_context = data.copy()
          loop_context['item'] = item
          loop_context['data'] = data  # Also provide access to original data

          # Render template for this iteration
          iteration_output = template.render(**loop_context)

          # Try to parse as JSON, otherwise keep as string
          try:
            parsed_iteration = json.loads(iteration_output)
            results.append(parsed_iteration)
          except BaseException:
            results.append(iteration_output)

        # Format final output as JSON array
        output = json.dumps(results, indent=2)
        actual_type = type(results).__name__  # This will be 'list'
        headers = {
            'X-Result-Type': 'json',
            'X-Input-Format': input_format,
            'X-Loop-Enabled': 'true',
            'X-Actual-Type': actual_type}
      else:
        # Normal processing without loop - provide access to both individual vars and data object
        context = data.copy()
        context['data'] = data
        output = template.render(**context)

        # The actual type is always string for Jinja2 template output
        # But we detect the content type for formatting purposes
        actual_type = 'str'  # Jinja2 always returns strings

        # Try to parse and format as JSON if possible, otherwise keep as string
        try:
          parsed_out = json.loads(output)
          output = json.dumps(parsed_out, indent=2)
          headers = {'X-Result-Type': 'json', 'X-Input-Format': input_format, 'X-Actual-Type': actual_type}
        except BaseException:
          try:
            # Try to safely evaluate as Python literal (dict, list, etc.)
            python_obj = ast.literal_eval(output)
            output = json.dumps(python_obj, indent=2)
            headers = {'X-Result-Type': 'json', 'X-Input-Format': input_format, 'X-Actual-Type': actual_type}
          except BaseException:
            # If all parsing attempts fail, treat as string
            headers = {'X-Result-Type': 'string', 'X-Input-Format': input_format, 'X-Actual-Type': actual_type}

      # Record - only save to history if input is not empty and not identical to previous entry
      try:
        # Check if input is not empty (after stripping whitespace)
        if json_text.strip():
          ts = datetime.datetime.utcnow().isoformat() + 'Z'
          entry = {
              'datetime': ts,
              'input': base64.b64encode(json_text.encode('utf-8')).decode('ascii'),
              'expr': base64.b64encode(expr.encode('utf-8')).decode('ascii'),
              'enable_loop': enable_loop,
              'loop_variable': loop_variable
          }

          # Load existing history
          try:
            with open(JSON_HISTORY_PATH, 'r', encoding='utf-8') as hf:
              hist = json.load(hf)
          except Exception:
            hist = []

          # Check if this entry is identical to the last one (excluding datetime)
          should_save = True
          if hist:
            last_entry = hist[-1]
            if entries_are_identical(entry, last_entry):
              should_save = False

          # Only save if the entry is different from the previous one
          if should_save:
            hist.append(entry)
            hist = hist[-MAX_ENTRIES:]
            # Create conf directory if it doesn't exist
            os.makedirs(os.path.dirname(JSON_HISTORY_PATH), exist_ok=True)
            with open(JSON_HISTORY_PATH, 'w', encoding='utf-8') as hf:
              json.dump(hist, hf, indent=2)
      except Exception:
        pass

      self._send_headers(200, 'text/plain', headers)
      self.wfile.write(output.encode())
    except Exception as e:
      self._send_headers(400, 'text/plain')
      self.wfile.write(f'Jinja expression error: {e}'.encode())

  def handle_load_ansible_vars(self):
    """Handle loading variables from Ansible module."""
    try:
      if self.command != 'POST':
        self.send_error(405, "Method not allowed")
        return

      # Check if API listener is enabled
      listener_enabled = config.getboolean('user', 'api-listener-enabled', fallback=False)

      if not listener_enabled:
        # Listener is disabled - discard variables and return success without saving
        response = {
            'status': 'discarded',
            'message': 'API Listener is disabled - variables discarded',
            'variables_count': 0,
            'listener_enabled': False
        }
        self._send_headers(200, 'application/json')
        self.wfile.write(json.dumps(response, indent=2).encode())
        return

      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)
      data = json.loads(post_data.decode('utf-8'))

      # Extract base64 encoded variables from module
      variables_b64 = data.get('variables_b64', '')
      summary = data.get('summary', {})

      # Decode to verify it's valid
      try:
        variables_json = base64.b64decode(variables_b64).decode('utf-8')
        variables = json.loads(variables_json)
      except Exception as e:
        raise ValueError(f"Invalid base64 variables data: {e}")

      # Create history entry
      # Don't set default values for listener entries to preserve existing content
      entry = {
          'id': str(uuid.uuid4()),
          'datetime': datetime.datetime.now().isoformat() + 'Z',
          'input': variables_b64,
          'expr': base64.b64encode(''.encode()).decode(),  # Empty expr to preserve current content
          # Don't set enable_loop and loop_variable to preserve current loop settings
          'source': 'listener',
          'summary': summary
      }

      # Save to history
      try:
        with open(JSON_HISTORY_PATH, 'r', encoding='utf-8') as hf:
          hist = json.load(hf)
      except Exception:
        hist = []

      hist.append(entry)
      hist = hist[-MAX_ENTRIES:]

      os.makedirs(os.path.dirname(JSON_HISTORY_PATH), exist_ok=True)
      with open(JSON_HISTORY_PATH, 'w', encoding='utf-8') as hf:
        json.dump(hist, hf, indent=2)

      # Return success response
      response = {
          'status': 'success',
          'message': 'Variables loaded from Ansible module',
          'variables_count': len(variables),
          'summary': summary,
          'entry_id': len(hist) - 1,
          'listener_enabled': True
      }

      self._send_headers(200, 'application/json')
      self.wfile.write(json.dumps(response, indent=2).encode())

    except Exception as e:
      self._send_headers(500, 'application/json')
      error_response = {
          'status': 'error',
          'message': f'Error loading Ansible variables: {str(e)}'
      }
      self.wfile.write(json.dumps(error_response).encode())


if __name__ == '__main__':
  print(f"Server started at http://{HOST}:{PORT}")
  HTTPServer((HOST, PORT), JinjaHandler).serve_forever()
