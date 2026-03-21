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

Automated License Compliance Checker for EUPL Projects
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# tomllib is available in Python 3.11+, fallback to tomli for older versions
try:
    import tomllib
except ImportError:
    import tomli as tomllib

# EUPL compatible licenses (from EUPL-1.2 Appendix)
EUPL_COMPATIBLE_LICENSES = {
    # Apache licenses
    "Apache-2.0", "Apache 2.0", "Apache License 2.0", "Apache License, Version 2.0",
    
    # MIT licenses
    "MIT", "MIT License", "Expat",
    
    # BSD licenses
    "BSD-2-Clause", "BSD-3-Clause", "BSD License", "BSD-style",
    
    # GPL licenses (with copyleft)
    "GPL-2.0", "GPL-2.0-only", "GPL-2.0-or-later",
    "GPL-3.0", "GPL-3.0-only", "GPL-3.0-or-later",
    
    # LGPL licenses
    "LGPL-2.1", "LGPL-2.1-only", "LGPL-2.1-or-later",
    "LGPL-3.0", "LGPL-3.0-only", "LGPL-3.0-or-later",
    
    # AGPL
    "AGPL-3.0", "AGPL-3.0-only", "AGPL-3.0-or-later",
    
    # MPL
    "MPL-2.0",
    
    # EPL
    "EPL-1.0", "EPL-2.0",
    
    # CeCILL
    "CeCILL-2.0", "CeCILL-2.1",
    
    # Creative Commons (for non-software)
    "CC-BY-SA-3.0",
    
    # Other EUPL versions
    "EUPL-1.1", "EUPL-1.2",
    
    # Québec licenses
    "LiLiQ-R", "LiLiQ-R+",
}

# Known license patterns for common dependencies
KNOWN_LICENSE_MAPPINGS = {
    # Kotlin/Compose ecosystem
    "org.jetbrains.kotlin": "Apache-2.0",
    "org.jetbrains.compose": "Apache-2.0",
    "androidx": "Apache-2.0",
    "com.android": "Apache-2.0",
    "com.google.android": "Apache-2.0",
    
    # Python ecosystem
    "appium": "Apache-2.0",
    "selenium": "Apache-2.0",
    "requests": "Apache-2.0",
    "urllib3": "MIT",
    
    # Common patterns
    ".*apache.*": "Apache-2.0",
    ".*mit.*": "MIT",
    ".*bsd.*": "BSD-3-Clause",
}


class DependencyChecker:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.dependencies = []
        self.license_cache = {}
        
    def parse_gradle_dependencies(self) -> List[Dict]:
        """Parse Gradle dependencies from build files"""
        dependencies = []
        
        # Read libs.versions.toml
        toml_path = self.project_root / "gradle" / "libs.versions.toml"
        if toml_path.exists():
            with open(toml_path, 'rb') as f:
                data = tomllib.load(f)
                
                # Parse libraries
                if 'libraries' in data:
                    for lib_name, lib_info in data['libraries'].items():
                        module = lib_info.get('module', '')
                        version_ref = lib_info.get('version.ref', '')
                        
                        if module and version_ref:
                            # Get version from versions section
                            version = data['versions'].get(version_ref, 'unknown')
                            dependencies.append({
                                'name': module,
                                'version': version,
                                'type': 'library',
                                'source': 'gradle/libs.versions.toml'
                            })
        
        # Parse composeApp/build.gradle.kts
        compose_build = self.project_root / "composeApp" / "build.gradle.kts"
        if compose_build.exists():
            content = compose_build.read_text()
            
            # Find compose dependencies
            compose_patterns = [
                r'implementation\(compose\.(\w+)',
                r'implementation\(libs\.(\w+\.\w+)',
            ]
            
            for pattern in compose_patterns:
                for match in re.finditer(pattern, content):
                    dep_name = match.group(1)
                    if 'compose.' in dep_name:
                        dependencies.append({
                            'name': f'org.jetbrains.compose:{dep_name.replace("compose.", "")}',
                            'version': '1.10.3',  # From libs.versions.toml
                            'type': 'compose',
                            'source': 'composeApp/build.gradle.kts'
                        })
        
        # Parse androidApp/build.gradle.kts
        android_build = self.project_root / "androidApp" / "build.gradle.kts"
        if android_build.exists():
            content = android_build.read_text()
            
            # Find project dependencies
            if 'implementation(project(":composeApp"))' in content:
                dependencies.append({
                    'name': 'project:composeApp',
                    'version': 'local',
                    'type': 'project',
                    'source': 'androidApp/build.gradle.kts'
                })
        
        return dependencies
    
    def parse_python_dependencies(self) -> List[Dict]:
        """Parse Python dependencies from requirements.txt"""
        dependencies = []
        req_path = self.project_root / "appium-tests" / "requirements.txt"
        
        if req_path.exists():
            content = req_path.read_text()
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Parse package name and version
                    parts = re.split(r'[>=<~!]+', line, 1)
                    package = parts[0].strip()
                    version = parts[1].strip() if len(parts) > 1 else 'latest'
                    
                    dependencies.append({
                        'name': package,
                        'version': version,
                        'type': 'python',
                        'source': 'appium-tests/requirements.txt'
                    })
        
        return dependencies
    
    def guess_license(self, dependency_name: str) -> Tuple[str, str]:
        """Guess license based on dependency name patterns"""
        # Check cache first
        if dependency_name in self.license_cache:
            return self.license_cache[dependency_name]
        
        # Check known mappings
        for pattern, license_type in KNOWN_LICENSE_MAPPINGS.items():
            if re.match(pattern, dependency_name, re.IGNORECASE):
                self.license_cache[dependency_name] = (license_type, 'guessed from pattern')
                return license_type, 'guessed from pattern'
        
        # Default to unknown
        self.license_cache[dependency_name] = ('UNKNOWN', 'not found in mapping')
        return 'UNKNOWN', 'not found in mapping'
    
    def check_eupl_compatibility(self, license_type: str) -> Tuple[bool, str]:
        """Check if a license is EUPL compatible"""
        license_lower = license_type.lower()
        
        # Check exact matches
        if license_type in EUPL_COMPATIBLE_LICENSES:
            return True, f"Exact match: {license_type}"
        
        # Check partial matches
        for eupl_license in EUPL_COMPATIBLE_LICENSES:
            if eupl_license.lower() in license_lower or license_lower in eupl_license.lower():
                return True, f"Partial match: {license_type} -> {eupl_license}"
        
        # Check for GPL without linking exception
        if 'gpl' in license_lower and 'exception' not in license_lower:
            return False, "GPL without linking exception may not be compatible"
        
        return False, f"Not in EUPL compatible list: {license_type}"
    
    def generate_report(self, dependencies: List[Dict]) -> str:
        """Generate a compliance report"""
        report_lines = []
        report_lines.append("# Automated License Compliance Report")
        report_lines.append(f"Generated: {subprocess.check_output(['date']).decode().strip()}")
        report_lines.append(f"Project: {self.project_root.name}")
        report_lines.append("")
        
        # Summary statistics
        total = len(dependencies)
        compatible = 0
        incompatible = 0
        unknown = 0
        
        report_lines.append("## Summary")
        report_lines.append("")
        
        # Dependency table
        report_lines.append("## Dependencies Analysis")
        report_lines.append("")
        report_lines.append("| Dependency | Version | Type | License | EUPL Compatible | Notes |")
        report_lines.append("|------------|---------|------|---------|-----------------|-------|")
        
        for dep in dependencies:
            license_type, license_source = self.guess_license(dep['name'])
            is_compatible, compatibility_note = self.check_eupl_compatibility(license_type)
            
            # Update counters
            if license_type == 'UNKNOWN':
                unknown += 1
            elif is_compatible:
                compatible += 1
            else:
                incompatible += 1
            
            # Format table row
            compat_icon = "✅" if is_compatible else "❌" if license_type != 'UNKNOWN' else "❓"
            report_lines.append(
                f"| {dep['name']} | {dep['version']} | {dep['type']} | {license_type} | {compat_icon} | {compatibility_note} |"
            )
        
        report_lines.append("")
        
        # Summary
        report_lines.append("## Compliance Summary")
        report_lines.append("")
        report_lines.append(f"- **Total Dependencies**: {total}")
        report_lines.append(f"- **✅ EUPL Compatible**: {compatible}")
        report_lines.append(f"- **❌ Not Compatible**: {incompatible}")
        report_lines.append(f"- **❓ Unknown License**: {unknown}")
        report_lines.append("")
        
        if incompatible == 0 and unknown == 0:
            report_lines.append("**✅ ALL DEPENDENCIES ARE EUPL COMPATIBLE**")
        elif incompatible > 0:
            report_lines.append(f"**⚠️ WARNING**: {incompatible} dependencies may not be EUPL compatible")
        else:
            report_lines.append("**ℹ️ NOTE**: Some dependencies have unknown licenses")
        
        report_lines.append("")
        
        # Recommendations
        report_lines.append("## Recommendations")
        report_lines.append("")
        
        if unknown > 0:
            report_lines.append("1. **Verify unknown licenses**: Manually check licenses for:")
            for dep in dependencies:
                license_type, _ = self.guess_license(dep['name'])
                if license_type == 'UNKNOWN':
                    report_lines.append(f"   - {dep['name']}")
        
        if incompatible > 0:
            report_lines.append("2. **Replace incompatible dependencies**: Consider alternatives for:")
            for dep in dependencies:
                license_type, _ = self.guess_license(dep['name'])
                is_compatible, _ = self.check_eupl_compatibility(license_type)
                if not is_compatible and license_type != 'UNKNOWN':
                    report_lines.append(f"   - {dep['name']} ({license_type})")
        
        report_lines.append("3. **Update DEPENDENCIES.md**: Run this script regularly to keep documentation current")
        
        return '\n'.join(report_lines)
    
    def check_license_headers(self) -> Tuple[int, int]:
        """Check source files for EUPL license headers"""
        source_extensions = {'.kt', '.swift', '.py', '.java', '.gradle.kts', '.gradle'}
        
        total_files = 0
        files_with_headers = 0
        
        for ext in source_extensions:
            for file_path in self.project_root.rglob(f'*{ext}'):
                # Skip build directories
                if 'build' in str(file_path) or '.gradle' in str(file_path):
                    continue
                
                total_files += 1
                try:
                    content = file_path.read_text()
                    if 'EUPL' in content and 'Copyright' in content:
                        files_with_headers += 1
                except:
                    continue
        
        return total_files, files_with_headers
    
    def run_checks(self):
        """Run all compliance checks"""
        print("🔍 Running EUPL Compliance Checks...")
        print("=" * 60)
        
        # Check dependencies
        print("\n📦 Checking dependencies...")
        gradle_deps = self.parse_gradle_dependencies()
        python_deps = self.parse_python_dependencies()
        all_deps = gradle_deps + python_deps
        
        print(f"  Found {len(all_deps)} dependencies")
        
        # Generate report
        report = self.generate_report(all_deps)
        
        # Check license headers
        print("\n📄 Checking license headers...")
        total_files, files_with_headers = self.check_license_headers()
        header_coverage = (files_with_headers / total_files * 100) if total_files > 0 else 0
        
        print(f"  Files with EUPL headers: {files_with_headers}/{total_files} ({header_coverage:.1f}%)")
        
        # Save report
        report_path = self.project_root / "LICENSE_COMPLIANCE_REPORT.md"
        report_path.write_text(report)
        
        print(f"\n📊 Report saved to: {report_path}")
        print("\n" + "=" * 60)
        print("✅ Compliance check completed!")
        
        # Show quick summary
        print("\nQuick Summary:")
        print("-" * 40)
        for line in report.split('\n'):
            if 'Total Dependencies' in line or 'EUPL Compatible' in line or 'Not Compatible' in line:
                print(line.strip('- '))
        
        if header_coverage < 100:
            print(f"⚠️  License headers: {header_coverage:.1f}% coverage")
        else:
            print("✅ License headers: 100% coverage")


def main():
    project_root = Path(__file__).parent.parent
    checker = DependencyChecker(project_root)
    
    try:
        checker.run_checks()
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())