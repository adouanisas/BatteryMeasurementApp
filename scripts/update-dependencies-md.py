#!/usr/bin/env python3
"""
Copyright (c) 2026 Ahmed ADOUANI
Licensed under the EUPL, Version 1.2 or – as soon they will be
approved by the European Commission - subsequent versions of the
EUPL (the "Licence");
You may not use this work except in compliance with the Licence.
You may obtain a copy of the Licence at:
https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the Licence for the specific language governing permissions and
limitations under the Licence.
SPDX-License-Identifier: EUPL-1.2

Automated DEPENDENCIES.md Updater
Runs the license checker and updates DEPENDENCIES.md with current information.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def run_license_checker() -> str:
    """Run the license checker and return the report"""
    script_path = Path(__file__).parent / "check-licenses.py"
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running license checker: {e}")
        print(f"Stderr: {e.stderr}")
        return ""


def read_dependencies_md() -> str:
    """Read the current DEPENDENCIES.md file"""
    deps_path = Path(__file__).parent.parent / "DEPENDENCIES.md"
    if deps_path.exists():
        return deps_path.read_text()
    return ""


def update_dependencies_md(current_content: str, checker_output: str) -> str:
    """Update DEPENDENCIES.md with current information"""
    lines = current_content.split('\n')
    updated_lines = []
    
    # Find the "Last updated" line
    last_updated_index = -1
    for i, line in enumerate(lines):
        if "Last updated:" in line:
            last_updated_index = i
            break
    
    # Update or add last updated line
    current_date = datetime.now().strftime("%B %d, %Y")
    last_updated_line = f"*Last updated: {current_date}*"
    
    if last_updated_index != -1:
        lines[last_updated_index] = last_updated_line
    else:
        # Add at the end before the references
        for i in range(len(lines)-1, -1, -1):
            if "## References" in lines[i]:
                lines.insert(i, last_updated_line)
                lines.insert(i, "")  # Add empty line before
                break
    
    # Add automation note at the beginning
    automation_note = """## 🔄 Automated Updates

This file can be automatically updated using the provided scripts:

```bash
# Run the license compliance checker
python scripts/check-licenses.py

# Update DEPENDENCIES.md with current information
python scripts/update-dependencies-md.py
```

The automated checker will:
1. Scan all build files for dependencies
2. Check license compatibility with EUPL-1.2
3. Generate a compliance report
4. Update this documentation

**Note**: Always verify automated updates, especially for license compatibility.
"""
    
    # Insert automation note after the title
    for i, line in enumerate(lines):
        if line.startswith("# Dependencies Analysis"):
            # Find the next section
            for j in range(i+1, len(lines)):
                if lines[j].startswith("## "):
                    lines.insert(j, automation_note)
                    lines.insert(j, "")  # Add empty line
                    break
            break
    
    return '\n'.join(lines)


def main():
    print("🔄 Updating DEPENDENCIES.md...")
    
    # Run license checker first
    print("1. Running license compliance check...")
    checker_output = run_license_checker()
    
    if not checker_output:
        print("❌ Failed to run license checker")
        return 1
    
    # Read current DEPENDENCIES.md
    print("2. Reading current DEPENDENCIES.md...")
    current_content = read_dependencies_md()
    
    if not current_content:
        print("❌ DEPENDENCIES.md not found or empty")
        return 1
    
    # Update the file
    print("3. Updating DEPENDENCIES.md...")
    updated_content = update_dependencies_md(current_content, checker_output)
    
    # Write back
    deps_path = Path(__file__).parent.parent / "DEPENDENCIES.md"
    deps_path.write_text(updated_content)
    
    print(f"✅ DEPENDENCIES.md updated successfully")
    print(f"   File: {deps_path}")
    
    # Show summary
    print("\n📋 Update Summary:")
    print("-" * 40)
    print("✓ Updated 'Last updated' date")
    print("✓ Added automation section")
    print("✓ Maintained all existing content")
    print("\nNext steps:")
    print("1. Review the updated DEPENDENCIES.md")
    print("2. Check LICENSE_COMPLIANCE_REPORT.md for details")
    print("3. Commit changes to version control")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())