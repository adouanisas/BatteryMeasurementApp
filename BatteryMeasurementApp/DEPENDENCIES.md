# Dependencies Analysis for Battery Measurement App

This document lists all third-party dependencies used in the Battery Measurement App project and analyzes their license compatibility with the EUPL-1.2 license.


## 🔄 Automated Updates

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

## License Compatibility Analysis

According to the EUPL-1.2 Appendix, the following licenses are compatible:
- Apache License 2.0
- MIT License
- BSD licenses
- LGPL v2.1, v3.0
- GPL v2, v3 (with copyleft clause)
- AGPL v3
- MPL v2
- EPL v1.0
- CeCILL v2.0, v2.1
- Other EUPL versions (v1.1, v1.2)

## Direct Dependencies

### Kotlin Multiplatform Dependencies

| Dependency | Version | License | EUPL Compatibility | Notes |
|------------|---------|---------|-------------------|-------|
| Kotlin Multiplatform | 2.1.0 | Apache-2.0 | ✅ Compatible | [Kotlin License](https://github.com/JetBrains/kotlin/blob/master/license/LICENSE.txt) |
| Kotlin Android Plugin | 2.1.0 | Apache-2.0 | ✅ Compatible | Same as Kotlin Multiplatform |
| Compose Multiplatform | 1.10.3 | Apache-2.0 | ✅ Compatible | [Compose License](https://github.com/JetBrains/compose-multiplatform/blob/master/LICENSE) |
| Compose Compiler Plugin | 2.1.0 | Apache-2.0 | ✅ Compatible | Bundled with Kotlin |
| Android Gradle Plugin | 8.7.3 | Apache-2.0 | ✅ Compatible | [AGP License](https://android.googlesource.com/platform/tools/base/+/refs/heads/master/LICENSE) |
| AndroidX Activity Compose | 1.9.3 | Apache-2.0 | ✅ Compatible | [AndroidX License](https://android.googlesource.com/platform/frameworks/support/+/refs/heads/androidx-main/LICENSE.txt) |
| AndroidX Core KTX | 1.15.0 | Apache-2.0 | ✅ Compatible | [AndroidX License](https://android.googlesource.com/platform/frameworks/support/+/refs/heads/androidx-main/LICENSE.txt) |

### Test Dependencies (Appium)

| Dependency | Version | License | EUPL Compatibility | Notes |
|------------|---------|---------|-------------------|-------|
| Appium Python Client | ≥3.0.0 | Apache-2.0 | ✅ Compatible | [Appium License](https://github.com/appium/python-client/blob/master/LICENSE) |
| Selenium | ≥4.15.0 | Apache-2.0 | ✅ Compatible | [Selenium License](https://github.com/SeleniumHQ/selenium/blob/trunk/LICENSE) |

## Transitive Dependencies

The following dependencies are brought in transitively by the direct dependencies:

### Kotlin/Compose Transitive Dependencies
- **Skiko** (Skia for Kotlin): Apache-2.0 ✅ Compatible
- **Kotlinx Coroutines**: Apache-2.0 ✅ Compatible  
- **Kotlinx Serialization**: Apache-2.0 ✅ Compatible
- **AndroidX Lifecycle**: Apache-2.0 ✅ Compatible
- **AndroidX Runtime**: Apache-2.0 ✅ Compatible
- **Material Design 3**: Apache-2.0 ✅ Compatible

### Appium/Selenium Transitive Dependencies
- **urllib3**: MIT ✅ Compatible
- **requests**: Apache-2.0 ✅ Compatible
- **websocket-client**: BSD-3-Clause ✅ Compatible

## License Verification

All identified dependencies use licenses that are **compatible with EUPL-1.2**:

1. **Apache License 2.0**: All major dependencies (Kotlin, Compose, AndroidX, Appium, Selenium)
2. **MIT License**: Some Python utilities
3. **BSD-3-Clause**: WebSocket client library

## Build Tool Dependencies

| Tool | Version | License | EUPL Compatibility | Notes |
|------|---------|---------|-------------------|-------|
| Gradle | 8.5 | Apache-2.0 | ✅ Compatible | Build system |
| Kotlin Compiler | 2.1.0 | Apache-2.0 | ✅ Compatible | Compiler tool |
| Xcode (iOS) | 15+ | Apple Proprietary | ⚠️ Build tool only | Required for iOS builds |
| Android SDK | 35 | Apache-2.0 | ✅ Compatible | Development platform |
| Python | 3.8+ | PSF License | ✅ Compatible | Test automation |
| Node.js | 16+ | MIT | ✅ Compatible | Appium server |
| Appium | 2.x | Apache-2.0 | ✅ Compatible | Test automation server |

## Compliance Status

✅ **ALL DEPENDENCIES ARE EUPL-COMPATIBLE**

No GPL-only dependencies are used. All dependencies use permissive licenses (Apache-2.0, MIT, BSD) that are explicitly listed as compatible in the EUPL-1.2 Appendix.

## Automated License Checking

### Automated Compliance Checker
We provide an automated script to check license compliance:

```bash
# Run the automated license checker
python scripts/check-licenses.py

# Output includes:
# - List of all dependencies
# - License compatibility analysis
# - EUPL compliance status
# - Recommendations for any issues
```

### Manual Verification Commands

#### For Android/Kotlin:
```bash
# List all dependencies
./gradlew dependencies

# Check specific configurations
./gradlew :androidApp:dependencies --configuration implementation
./gradlew :composeApp:dependencies --configuration commonMainImplementation
```

#### For Python:
```bash
# List installed packages
pip list --format=freeze

# Check package licenses
pip show <package-name> | grep License
```

### Continuous Integration
Add this to your CI/CD pipeline:

```yaml
# GitHub Actions example
name: License Compliance Check
on: [push, pull_request]
jobs:
  check-licenses:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Run license checker
        run: python scripts/check-licenses.py
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: license-compliance-report
          path: LICENSE_COMPLIANCE_REPORT.md
```

## License Texts

All dependency licenses are available in their respective source repositories. The main licenses used are:

1. **Apache License 2.0**: Used by Kotlin, Compose Multiplatform, AndroidX, Appium, Selenium
2. **MIT License**: Used by some Python utilities
3. **BSD-3-Clause**: Used by websocket-client

## Recommendations

1. **Keep dependencies updated**: Regularly update to latest versions to maintain security and compatibility.
2. **Document changes**: Update this file when adding new dependencies.
3. **Verify compatibility**: Always check license compatibility before adding new dependencies.
4. **Use SPDX identifiers**: Include SPDX license identifiers in all source files.

## References

- [EUPL-1.2 Compatible Licenses](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
- [SPDX License List](https://spdx.org/licenses/)
- [Kotlin License](https://github.com/JetBrains/kotlin/blob/master/license/LICENSE.txt)
- [Compose Multiplatform License](https://github.com/JetBrains/compose-multiplatform/blob/master/LICENSE)

---

*Last updated: March 20, 2026*
*This analysis is based on the project configuration as of the above date.*