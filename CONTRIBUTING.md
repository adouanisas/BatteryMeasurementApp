# Contributing to Battery Measurement App

Thank you for your interest in contributing to the Battery Measurement App! This project follows European Commission open source guidelines and uses the EUPL-1.2 license.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## Development Process

### 1. Fork and Clone
- Fork the repository on GitHub
- Clone your fork locally
- Set up the development environment as described in README.md

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 3. Make Changes
Follow the coding standards and ensure compliance with EUPL requirements.

### 4. Test Your Changes
- Run the app on Android and/or iOS
- Execute Appium tests: `cd appium-tests && python test_battery_measurement.py`
- Ensure all tests pass

### 5. Commit Your Changes
Use conventional commit messages:
```
feat: add dark mode support
fix: resolve crash on measurement start
docs: update README with build instructions
chore: update dependencies
```

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub.

## EUPL Compliance Requirements

### License Headers
**Every source file must include the EUPL license header:**

```kotlin
/*
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
*/
```

### File Types Requiring Headers
- Kotlin files (`.kt`)
- Swift files (`.swift`)
- Python files (`.py`)
- Gradle files (`.gradle.kts`, `.gradle`)
- Shell scripts (`.sh`)
- Configuration files (`.xml`, `.properties`)

### Dependencies
**Before adding a new dependency:**
1. Check its license compatibility with EUPL-1.2
2. Update `DEPENDENCIES.md` with the new dependency
3. Ensure the license is in the compatible list:
   - Apache-2.0 ✅
   - MIT ✅
   - BSD ✅
   - LGPL ✅
   - GPL (with copyleft) ✅
   - MPL-2.0 ✅

**Incompatible licenses:**
- Proprietary licenses ❌
- GPL-only without linking exception ❌

### No Secrets in Code
- Never commit API keys, passwords, or credentials
- Use environment variables or configuration files excluded from git
- Add `.env` or similar files to `.gitignore`

## Coding Standards

### Kotlin/Compose
- Follow Kotlin coding conventions
- Use meaningful variable and function names
- Add `testTag` modifiers for UI elements that need testing
- Use `expect`/`actual` for platform-specific code

### Swift/iOS
- Follow Swift API Design Guidelines
- Use SwiftUI best practices
- Maintain compatibility with Compose Multiplatform

### Python
- Follow PEP 8 style guide
- Add type hints where appropriate
- Write docstrings for public functions

### Git Practices
- Keep commits focused and atomic
- Write clear commit messages
- Rebase instead of merge when updating branches
- Squash commits when appropriate

## Testing Requirements

### Unit Tests
- Write tests for new functionality
- Maintain existing test coverage
- Use descriptive test names

### UI Tests (Appium)
- Add `testTag` modifiers to new UI elements
- Update Appium tests when UI changes
- Test on both Android and iOS when possible

### Manual Testing
- Test on physical devices when possible
- Verify accessibility features work
- Check performance on different device types

## Documentation

### Update Documentation When:
- Adding new features
- Changing APIs
- Adding dependencies
- Changing build process

### Documentation Files:
- `README.md` - Main project documentation
- `DEPENDENCIES.md` - License analysis
- `CONTRIBUTING.md` - This file
- Code comments for complex logic

## Review Process

1. **Automated Checks**: GitHub Actions will run:
   - Build verification
   - License header check
   - Dependency license check

2. **Manual Review**: Maintainers will review:
   - Code quality and standards
   - EUPL compliance
   - Test coverage
   - Documentation updates

3. **Approval**: At least one maintainer must approve before merge.

## Questions?

- Open an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Join discussions in existing issues/PRs

## Acknowledgments

Thank you for contributing to open source software for European Commission projects. Your contributions help create reusable, compliant software for public benefit.

---

*This contributing guide is based on European Commission open source guidelines and best practices for EUPL-licensed projects.*