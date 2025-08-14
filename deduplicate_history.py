#!/usr/bin/env python3
"""
History Deduplication Script for Ansible Jinja2 Playground

This script removes duplicate entries from the history file while preserving
the most recent occurrence of each unique entry.
"""

import json
import base64
import os
import sys
import argparse
from datetime import datetime
import shutil


def decode_base64_field(encoded_data):
    """Decode base64 field safely"""
    try:
        return base64.b64decode(encoded_data).decode('utf-8')
    except Exception:
        return encoded_data  # Return as-is if decoding fails


def create_entry_signature(entry):
    """Create a unique signature for a history entry"""
    # Decode the base64 fields to compare actual content
    input_content = decode_base64_field(entry.get('input', ''))
    expr_content = decode_base64_field(entry.get('expr', ''))

    # Create signature based on content and loop settings
    signature = {
        'input': input_content.strip(),
        'expr': expr_content.strip(),
        'enable_loop': entry.get('enable_loop', False),
        'loop_variable': entry.get('loop_variable', '').strip()
    }

    # Convert to string for hashing
    return str(sorted(signature.items()))


def parse_datetime(datetime_str):
    """Parse datetime string safely"""
    try:
        # Handle different datetime formats
        if datetime_str.endswith('Z'):
            return datetime.fromisoformat(datetime_str[:-1])
        else:
            return datetime.fromisoformat(datetime_str)
    except Exception:
        return datetime.min


def deduplicate_history(history_data, keep_strategy='newest'):
    """
    Remove duplicate entries from history

    Args:
        history_data: List of history entries
        keep_strategy: 'newest' or 'oldest' - which duplicate to keep

    Returns:
        Deduplicated history list
    """
    seen_signatures = {}
    unique_entries = []

    print(f"📊 Processing {len(history_data)} history entries...")

    for entry in history_data:
        signature = create_entry_signature(entry)
        entry_datetime = parse_datetime(entry.get('datetime', ''))

        if signature not in seen_signatures:
            # First time seeing this signature
            seen_signatures[signature] = {
                'entry': entry,
                'datetime': entry_datetime,
                'index': len(unique_entries)
            }
            unique_entries.append(entry)
        else:
            # Duplicate found - decide which to keep
            existing = seen_signatures[signature]
            existing_datetime = existing['datetime']

            should_replace = False
            if keep_strategy == 'newest' and entry_datetime > existing_datetime:
                should_replace = True
            elif keep_strategy == 'oldest' and entry_datetime < existing_datetime:
                should_replace = True

            if should_replace:
                # Replace the existing entry
                unique_entries[existing['index']] = entry
                seen_signatures[signature] = {
                    'entry': entry,
                    'datetime': entry_datetime,
                    'index': existing['index']
                }

    duplicates_removed = len(history_data) - len(unique_entries)
    print(f"🗑️  Removed {duplicates_removed} duplicate entries")
    print(f"✅ Final history contains {len(unique_entries)} unique entries")

    return unique_entries


def backup_history_file(file_path):
    """Create a backup of the history file"""
    if not os.path.exists(file_path):
        return None

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{file_path}.backup_{timestamp}"

    try:
        shutil.copy2(file_path, backup_path)
        print(f"📁 Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"⚠️  Failed to create backup: {e}")
        return None


def validate_history_structure(history_data):
    """Validate the structure of history entries"""
    required_fields = ['datetime', 'input', 'expr']
    issues = []

    for i, entry in enumerate(history_data):
        if not isinstance(entry, dict):
            issues.append(f"Entry {i}: Not a dictionary")
            continue

        for field in required_fields:
            if field not in entry:
                issues.append(f"Entry {i}: Missing required field '{field}'")

        # Check datetime format
        try:
            parse_datetime(entry.get('datetime', ''))
        except Exception:
            issues.append(f"Entry {i}: Invalid datetime format")

    return issues


def main():
    parser = argparse.ArgumentParser(
        description='Remove duplicate entries from Ansible Jinja2 Playground history'
    )
    parser.add_argument(
        'history_file',
        nargs='?',
        default='conf/ansible_jinja2_playground_history.json',
        help='Path to history JSON file (default: conf/ansible_jinja2_playground_history.json)'
    )
    parser.add_argument(
        '--keep',
        choices=['newest', 'oldest'],
        default='newest',
        help='Which duplicate to keep: newest or oldest (default: newest)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip creating backup file'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate file structure without deduplication'
    )

    args = parser.parse_args()

    # Ensure we have the full path
    if not os.path.isabs(args.history_file):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        args.history_file = os.path.join(script_dir, args.history_file)

    print("🧹 History Deduplication Tool")
    print("=" * 40)
    print(f"📂 Target file: {args.history_file}")

    # Check if file exists
    if not os.path.exists(args.history_file):
        print(f"❌ Error: History file not found: {args.history_file}")
        return 1

    # Load history data
    try:
        with open(args.history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in history file: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: Failed to read history file: {e}")
        return 1

    if not isinstance(history_data, list):
        print("❌ Error: History file should contain a JSON array")
        return 1

    # Validate structure
    print(f"\n🔍 Validating {len(history_data)} entries...")
    validation_issues = validate_history_structure(history_data)

    if validation_issues:
        print("⚠️  Validation issues found:")
        for issue in validation_issues:
            print(f"   - {issue}")

        if args.validate_only:
            return 1

        response = input("\nContinue despite validation issues? (y/N): ")
        if response.lower() != 'y':
            return 1
    else:
        print("✅ File structure is valid")

    if args.validate_only:
        return 0

    # Deduplicate
    deduplicated_history = deduplicate_history(history_data, args.keep)

    if len(deduplicated_history) == len(history_data):
        print("🎉 No duplicates found - file is already clean!")
        return 0

    if args.dry_run:
        print("\n🔍 DRY RUN - No changes made")
        print(f"Would remove {len(history_data) - len(deduplicated_history)} duplicates")
        return 0

    # Create backup unless disabled
    if not args.no_backup:
        backup_path = backup_history_file(args.history_file)
        if not backup_path:
            response = input("Failed to create backup. Continue anyway? (y/N): ")
            if response.lower() != 'y':
                return 1

    # Write deduplicated history
    try:
        with open(args.history_file, 'w', encoding='utf-8') as f:
            json.dump(deduplicated_history, f, indent=2, ensure_ascii=False)

        print("\n✅ Successfully deduplicated history file")
        print(f"📊 Original entries: {len(history_data)}")
        print(f"📊 Final entries: {len(deduplicated_history)}")
        print(f"🗑️  Removed: {len(history_data) - len(deduplicated_history)} duplicates")

    except Exception as e:
        print(f"❌ Error: Failed to write deduplicated history: {e}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
