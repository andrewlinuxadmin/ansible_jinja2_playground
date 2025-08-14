#!/usr/bin/env python3
"""
Script to check compliance with .copilotrc rules
"""

import os
import re
import yaml
import sys

def load_copilotrc():
  """Loads .copilotrc rules"""
  try:
    with open('.copilotrc', 'r') as f:
      return yaml.safe_load(f)
  except Exception as e:
    print(f"❌ Error reading .copilotrc: {e}")
    return None

def check_coding_style():
  """Checks if coding style is being followed"""
  print("🎨 Checking coding style...")

  issues = []

  # Check Python files
  for root, dirs, files in os.walk('.'):
    # Ignore specific directories
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]

    for file in files:
      if file.endswith('.py'):
        file_path = os.path.join(root, file)

        with open(file_path, 'r', encoding='utf-8') as f:
          lines = f.readlines()

        for i, line in enumerate(lines, 1):
          # Check trailing whitespace (line cannot end with spaces or tabs)
          if line.endswith(' ') or line.endswith('\t'):
            issues.append(f"   ⚠️  {file_path}:{i} - Trailing whitespace")

          # Check indentation (must be multiple of 2)
          leading_spaces = len(line) - len(line.lstrip(' '))
          if leading_spaces > 0 and leading_spaces % 2 != 0:
            issues.append(f"   ⚠️  {file_path}:{i} - Incorrect indentation (not multiple of 2)")

  if issues:
    print("   ❌ Problems found:")
    for issue in issues[:10]:  # Show only first 10
      print(issue)
    if len(issues) > 10:
      print(f"   ... and {len(issues) - 10} more problems")
  else:
    print("   ✅ Coding style OK")

  return len(issues) == 0

def check_test_structure():
  """Checks if test structure is correct"""
  print("🧪 Checking test structure...")

  if not os.path.exists('tests'):
    print("   ❌ Tests directory not found")
    return False

  test_files = [f for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')]

  if len(test_files) == 0:
    print("   ❌ No test files found")
    return False

  print(f"   ✅ Found {len(test_files)} test files:")
  for test_file in test_files:
    print(f"      📄 {test_file}")

  return True

def check_documentation():
  """Checks if documentation is present"""
  print("📚 Checking documentation...")

  required_docs = ['README.md', 'USAGE.md', 'INSTALL.md', 'LOOP_USAGE.md']
  missing_docs = []

  for doc in required_docs:
    if not os.path.exists(doc):
      missing_docs.append(doc)

  if missing_docs:
    print("   ❌ Missing documentation:")
    for doc in missing_docs:
      print(f"      📄 {doc}")
    return False
  else:
    print("   ✅ Complete documentation")
    return True

def main():
  print("🔍 Checking compliance with .copilotrc")
  print("=" * 50)

  # Load configurations
  config = load_copilotrc()
  if not config:
    sys.exit(1)

  print("✅ .copilotrc file loaded successfully")
  print()

  # Run checks
  results = []
  results.append(check_coding_style())
  results.append(check_test_structure())
  results.append(check_documentation())

  print()
  print("=" * 50)

  if all(results):
    print("🎉 ALL CHECKS PASSED!")
    print("✅ Project is compliant with .copilotrc")
    sys.exit(0)
  else:
    print("⚠️  SOME CHECKS FAILED")
    print("❌ Project needs adjustments for compliance")
    sys.exit(1)

if __name__ == "__main__":
  main()
