# CLAUDE.md

## Project Overview

**EEI (Energy Efficiency Index) measurement tool** built with Kotlin Multiplatform (Compose Multiplatform), following **EU Regulation 2023/1669**. Open source under EUPL-1.2.

The app measures battery consumption during a standardized "Day of Use" scenario and calculates the EEI to assess device energy efficiency per the EU regulation.

**Current status:** Basic UI (button + label), Appium tests configured, EUPL compliance script in place. Core features (battery measurement, Day of Use scenario, EEI calculation, reporting) are pending implementation.

**License:** EUPL-1.2 (European Union Public License). Every source file must include the EUPL license header.

## Goals & Standards

- Clean, documented code
- Semantic versioning — `CHANGELOG.md` (keepachangelog format) + version tags
- **Conventional commits** for clear history (`feat:`, `fix:`, `chore:`, etc.)
- Comprehensive README with setup, usage, and contribution guidelines
- Automated license compliance (Gradle script + GitHub Actions)
- CI/CD with GitHub Actions (build, test, lint)
- Issue templates for bug reports and feature requests

## Roadmap (Core Features to Implement)

1. Battery measurement (platform-specific `expect`/`actual`)
2. Day of Use scenario (standardized usage sequence per EU Reg. 2023/1669)
3. EEI calculation engine
4. Reporting (export results)

---

## Architecture

### Modules

| Module | Purpose |
|---|---|
| `composeApp` | Shared Kotlin Multiplatform code — UI (Compose), business logic, `expect`/`actual` platform bridges |
| `androidApp` | Android application wrapper (thin shell over composeApp) |
| `iosApp` | Xcode project consuming the compiled `ComposeApp.framework` |
| `appiumTests` | Kotlin/JUnit 5 Appium E2E tests for both platforms |
| `sharedTestTags` | KMP library exposing test tag constants (used by app + tests) |

### Platform Bridging

`expect`/`actual` pattern is used for platform-specific implementations (e.g., logging). Android uses `Log.d()`, iOS uses `NSLog`.

### Test Tags

Test tags are defined in `sharedTestTags` as a shared KMP object to avoid duplication between app and test code:
- `START_MEASUREMENT_BUTTON` = `"start_measurement_button"`
- `RESULT_LABEL` = `"result_label"`

Android uses `testTagsAsResourceId = true`; iOS uses accessibility IDs natively.

---

## Tech Stack

- **Kotlin:** 2.3.20
- **Compose Multiplatform:** 1.10.3
- **Android:** Min SDK 30, Target/Compile SDK 35/36, JVM 17
- **iOS:** Deployment target 15.0
- **Build:** Gradle 8.14.4, AGP 8.13.2
- **Testing:** JUnit 5 + Appium Java Client 9.0.0
- **CI:** GitHub Actions (`.github/workflows/`)
- **Python:** 3.8+ (scripts only)

All dependency versions are centralized in `gradle/libs.versions.toml`.

---

## Build Commands

```bash
# Android APK
./gradlew clean :androidApp:assembleDebug

# iOS framework (for Xcode consumption)
./gradlew :composeApp:embedAndSignAppleFrameworkForXcode

# Both platforms via script
./scripts/build_apps.sh --all
./scripts/build_apps.sh --android
./scripts/build_apps.sh --ios
./scripts/build_apps.sh --clean-ios  # clean then build iOS
```

APK output: `androidApp/build/outputs/apk/debug/` or `build/test-apks/`

---

## Running Tests

Tests require an Appium server running on `localhost:4723`.

```bash
# Android tests only
./gradlew :appiumTests:androidTest

# iOS tests only
./gradlew :appiumTests:iosTest

# All tests
./gradlew :appiumTests:allAppiumTests
```

Pass system properties to override APK path or device:
```bash
./gradlew :appiumTests:androidTest -DapkPath=/path/to/app.apk
```

See `appiumTests/README.md` and `appiumTests/ANDROID_STUDIO_SETUP.md` for IDE setup.

---

## CI/CD

Two GitHub Actions workflows:

| Workflow | Trigger | Purpose |
|---|---|---|
| `build-apps.yml` | push/PR to main, weekly (Tue 9 AM) | Build Android APK + iOS framework, upload artifacts |
| `license-compliance.yml` | push/PR to main, weekly (Mon 9 AM) | Run license compliance check, generate report, auto-PR on schedule |

Cache: Gradle dependencies are cached with hash-based keys.

---

## License Compliance

This project enforces EUPL-1.2 compliance on all dependencies.

```bash
# Check license compliance
python scripts/check-licenses.py

# Update DEPENDENCIES.md
python scripts/update-dependencies-md.py
```

Rules:
- All new dependencies must be EUPL-1.2 compatible
- Every source file must include the EUPL-1.2 license header
- `DEPENDENCIES.md` must be kept up to date with SPDX identifiers

---

## Key Files

| File | Purpose |
|---|---|
| `composeApp/src/commonMain/kotlin/App.kt` | Main shared Compose UI |
| `gradle/libs.versions.toml` | Centralized dependency versions |
| `scripts/build_apps.sh` | Cross-platform build script |
| `scripts/check-licenses.py` | License compliance checker |
| `appiumTests/src/test/kotlin/BaseAppiumTest.kt` | Appium test base class |
| `DEPENDENCIES.md` | Full dependency list with license info |
| `CONTRIBUTING.md` | Development process and coding standards |
