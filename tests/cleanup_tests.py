#!/usr/bin/env python3
"""
Cleanup script for test environment
Removes temporary files, old logs, and cleans up test artifacts
"""

import os
import shutil
import glob
import datetime
import argparse


def cleanup_temp_files():
    """Remove temporary test files"""
    print("🧹 Cleaning temporary test files...")

    temp_patterns = [
        '/tmp/ansible_jinja2_playground_test_*',
        '/tmp/test_*'
    ]

    removed_count = 0
    for pattern in temp_patterns:
        for file_path in glob.glob(pattern):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    removed_count += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    removed_count += 1
            except Exception as e:
                print(f"   ⚠️  Failed to remove {file_path}: {e}")

    print(f"   ✅ Removed {removed_count} temporary files/directories")


def cleanup_old_logs(days=7):
    """Remove log files older than specified days"""
    print(f"🗂️  Cleaning log files older than {days} days...")

    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(logs_dir):
        print("   ℹ️  No logs directory found")
        return

    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
    removed_count = 0

    for filename in os.listdir(logs_dir):
        file_path = os.path.join(logs_dir, filename)
        if os.path.isfile(file_path):
            try:
                # Get file modification time
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

                if file_time < cutoff_date:
                    os.remove(file_path)
                    removed_count += 1
                    print(f"   🗑️  Removed old log: {filename}")
            except Exception as e:
                print(f"   ⚠️  Failed to remove {filename}: {e}")

    print(f"   ✅ Removed {removed_count} old log files")


def cleanup_pycache():
    """Remove Python cache directories"""
    print("🐍 Cleaning Python cache files...")

    test_dir = os.path.dirname(__file__)
    removed_count = 0

    # Find all __pycache__ directories
    for root, dirs, files in os.walk(test_dir):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                removed_count += 1
                print(f"   🗑️  Removed: {pycache_path}")
            except Exception as e:
                print(f"   ⚠️  Failed to remove {pycache_path}: {e}")

    # Remove .pyc files
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    removed_count += 1
                except Exception as e:
                    print(f"   ⚠️  Failed to remove {pyc_path}: {e}")

    print(f"   ✅ Removed {removed_count} cache files/directories")


def reset_test_environment():
    """Reset test environment to clean state"""
    print("🔄 Resetting test environment...")

    # Remove any test configuration files
    test_conf_patterns = [
        os.path.join(os.path.dirname(__file__), 'test_*.conf'),
        os.path.join(os.path.dirname(__file__), 'test_*.json'),
    ]

    removed_count = 0
    for pattern in test_conf_patterns:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                removed_count += 1
                print(f"   🗑️  Removed test file: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"   ⚠️  Failed to remove {file_path}: {e}")

    print(f"   ✅ Reset complete - removed {removed_count} test files")


def display_disk_usage():
    """Display disk usage information for test directory"""
    print("💾 Disk usage information:")

    test_dir = os.path.dirname(__file__)
    total_size = 0
    file_count = 0

    for root, dirs, files in os.walk(test_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_size += size
                file_count += 1
            except Exception:
                pass

    # Convert bytes to human readable format
    def format_bytes(bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"

    print(f"   📁 Test directory: {test_dir}")
    print(f"   📊 Total files: {file_count}")
    print(f"   💿 Total size: {format_bytes(total_size)}")

    # Show logs directory size if it exists
    logs_dir = os.path.join(test_dir, 'logs')
    if os.path.exists(logs_dir):
        logs_size = 0
        logs_count = 0
        for file in os.listdir(logs_dir):
            file_path = os.path.join(logs_dir, file)
            if os.path.isfile(file_path):
                logs_size += os.path.getsize(file_path)
                logs_count += 1

        print(f"   📝 Log files: {logs_count}")
        print(f"   📊 Logs size: {format_bytes(logs_size)}")


def main():
  parser = argparse.ArgumentParser(description='Cleanup test environment')
  parser.add_argument('--logs-days', type=int, default=7,
                      help='Remove log files older than N days (default: 7)')
  parser.add_argument('--temp-only', action='store_true',
                      help='Only clean temporary files')
  parser.add_argument('--logs-only', action='store_true',
                      help='Only clean log files')
  parser.add_argument('--reset', action='store_true',
                      help='Reset entire test environment')
  parser.add_argument('--usage', action='store_true',
                      help='Show disk usage information')

  args = parser.parse_args()

  print("🧹 Test Environment Cleanup Tool")
  print("=" * 40)

  if args.usage:
    display_disk_usage()
    return

  if args.temp_only:
    cleanup_temp_files()
  elif args.logs_only:
    cleanup_old_logs(args.logs_days)
  elif args.reset:
    cleanup_temp_files()
    cleanup_old_logs(0)  # Remove all logs
    cleanup_pycache()
    reset_test_environment()
  else:
    # Default: clean everything with sensible defaults
    cleanup_temp_files()
    cleanup_old_logs(args.logs_days)
    cleanup_pycache()

  print("\n" + "=" * 40)
  print("✨ Cleanup completed!")

  # Show final disk usage
  display_disk_usage()


if __name__ == '__main__':
  main()
