# EEI Commission — Energy Efficiency Index Measurement Tool

A **Kotlin Multiplatform** (Compose Multiplatform) mobile application for measuring and calculating the **Energy Efficiency Index (EEI)** of mobile devices, following **EU Regulation 2023/1669**.

Open source under [EUPL-1.2](LICENSE).

---

## Overview

The EEI measures how energy-efficient a device is during a standardized "Day of Use" scenario defined by the EU regulation. This tool automates the measurement process across Android and iOS from a single shared codebase.

**Current status:** foundational structure in place — battery UI, Appium tests, EUPL compliance tooling. Core EEI features (battery measurement, Day of Use scenario, EEI calculation, reporting) are under active development.

---

## Project Structure

```
├── composeApp/          # Shared Compose Multiplatform UI + business logic
│   └── src/
│       ├── commonMain/  # Common code (UI, EEI logic)
│       ├── androidMain/ # Android-specific implementations
│       └── iosMain/     # iOS-specific implementations
├── androidApp/          # Android application module
├── iosApp/              # iOS application (Xcode project)
├── appiumTests/         # Appium E2E tests (Kotlin/JUnit 5)
├── sharedTestTags/      # Shared test tag constants (KMP)
├── scripts/             # Build and compliance scripts
└── gradle/              # Gradle wrapper and version catalog
```

---

## Prerequisites

### Build

- **JDK 17+**
- **Android Studio** (Hedgehog or later) with Android SDK 34+
- **Xcode 15+** (iOS, macOS only)
- **Kotlin Multiplatform Mobile plugin** (Android Studio)

```bash
# Install Gradle wrapper (already included)
./gradlew --version
```

### Testing

- **Node.js 16+**
- **Appium 2.x**

```bash
npm install -g appium
appium driver install uiautomator2   # Android
appium driver install xcuitest       # iOS
```

---

## Building

```bash
# Android APK
./scripts/build_apps.sh --android

# iOS simulator app
./scripts/build_apps.sh --ios

# Both platforms
./scripts/build_apps.sh --all
```

| Platform | Output path |
|---|---|
| Android | `androidApp/build/outputs/apk/debug/androidApp-debug.apk` |
| iOS | `build/ios-derived-data/Build/Products/Debug-iphonesimulator/` |

---

## Code Quality

Static analysis is enforced via **detekt**:

```bash
./gradlew detekt
```

Configuration: [`detekt.yml`](detekt.yml). Rules are applied to all modules. Compose Multiplatform generated sources are automatically excluded.

---

## Running Tests

Start Appium server first:

```bash
appium --port 4723 --address 127.0.0.1
```

Then run:

```bash
./gradlew :appiumTests:androidTest   # Android
./gradlew :appiumTests:iosTest       # iOS
./gradlew :appiumTests:allAppiumTests
```

Override APK path or device via system properties:

```bash
./gradlew :appiumTests:androidTest -DapkPath=/path/to/app.apk
```

See [`appiumTests/README.md`](appiumTests/README.md) and [`appiumTests/ANDROID_STUDIO_SETUP.md`](appiumTests/ANDROID_STUDIO_SETUP.md) for IDE setup.

### Test Tags (Accessibility IDs)

| Element | Tag |
|---|---|
| Start Measurement Button | `start_measurement_button` |
| Result Label | `result_label` |

---

## Troubleshooting

**Android**
- Verify `ANDROID_HOME` is set
- Check emulator is running: `adb devices`

**iOS**
- Install Xcode CLI tools: `xcode-select --install`
- List simulators: `xcrun simctl list devices`

**Appium**
- Check server status: `curl http://127.0.0.1:4723/status`
- List installed drivers: `appium driver list --installed`

---

## License Compliance

This project enforces **EUPL-1.2** compliance on all dependencies.

```bash
python scripts/check-licenses.py       # Check compliance
python scripts/update-dependencies-md.py  # Update DEPENDENCIES.md
```

All new dependencies must be EUPL-1.2 compatible. See [`DEPENDENCIES.md`](DEPENDENCIES.md) for the full analysis.

**Compliance status:**
- All dependencies are EUPL-compatible
- All source files carry EUPL-1.2 license headers
- Automated compliance checks run on every push (GitHub Actions)

References: [EUPL-1.2 text](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12) · [EUPL compatibility guidelines](https://joinup.ec.europa.eu/collection/eupl/guidelines-eupl-licence)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). This project uses **conventional commits** and **semantic versioning**. Changes are tracked in [CHANGELOG.md](CHANGELOG.md).

---

## License

Copyright © 2026 Ahmed ADOUANI

Licensed under the EUPL, Version 1.2. You may obtain a copy of the licence at:
https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

`SPDX-License-Identifier: EUPL-1.2`
