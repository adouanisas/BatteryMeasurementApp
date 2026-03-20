# Battery Measurement App - Compose Multiplatform POC

A simple Compose Multiplatform app demonstrating battery measurement simulation with Appium testing support.

## Project Structure

```
BatteryMeasurementApp/
├── composeApp/                 # Shared Compose Multiplatform code
│   └── src/
│       ├── commonMain/         # Common UI code
│       ├── androidMain/        # Android-specific implementations
│       └── iosMain/            # iOS-specific implementations
├── androidApp/                 # Android application module
├── iosApp/                     # iOS application (Xcode project)
├── appium-tests/               # Appium test scripts
│   ├── test_battery_measurement.py
│   └── requirements.txt
└── gradle/                     # Gradle wrapper
```

## Prerequisites

### For Building
- **JDK 17+**
- **Android Studio** (Arctic Fox or later) with:
  - Android SDK 34
  - Android Emulator
- **Xcode 15+** (for iOS, macOS only)
- **Kotlin Multiplatform Mobile plugin** (install via Android Studio plugins)

### For Testing
- **Python 3.8+**
- **Node.js 16+** (for Appium)
- **Appium 2.x**

## Building the App

### Android

1. Open the project in Android Studio
2. Sync Gradle files
3. Build the debug APK:

```bash
cd BatteryMeasurementApp
./gradlew :androidApp:assembleDebug
```

The APK will be at: `androidApp/build/outputs/apk/debug/androidApp-debug.apk`

### iOS

1. Generate the iOS framework:

```bash
cd BatteryMeasurementApp
./gradlew :composeApp:linkDebugFrameworkIosSimulatorArm64
```

2. Open `iosApp/iosApp.xcodeproj` in Xcode
3. Add the ComposeApp framework:
   - Go to project settings → General → Frameworks, Libraries
   - Add the framework from `composeApp/build/bin/iosSimulatorArm64/debugFramework/`
4. Build and run on simulator

## Running the App

### Android

```bash
# Start an emulator first
emulator -avd <your_avd_name>

# Install and run
./gradlew :androidApp:installDebug
adb shell am start -n com.example.batterymeasurement.android/.MainActivity
```

### iOS

Run from Xcode on a simulator or device.

## Appium Testing

### 1. Install Appium

```bash
# Install Appium globally
npm install -g appium

# Install drivers
appium driver install uiautomator2  # For Android
appium driver install xcuitest      # For iOS
```

### 2. Install Python Dependencies

```bash
cd appium-tests
pip install -r requirements.txt
```

### 3. Start Appium Server

```bash
appium
```

The server will start at `http://127.0.0.1:4723`

### 4. Run Tests

#### Android Test

```bash
# Make sure an emulator is running and the app is installed
cd appium-tests
python test_battery_measurement.py --platform android --app-path ../androidApp/build/outputs/apk/debug/androidApp-debug.apk
```

#### iOS Test

```bash
# Make sure a simulator is running
cd appium-tests
python test_battery_measurement.py --platform ios --app-path ../iosApp/build/Debug-iphonesimulator/iosApp.app
```

### Test Script Options

```
--platform      Target platform: android or ios (default: android)
--appium-url    Appium server URL (default: http://127.0.0.1:4723)
--app-path      Path to the app file (.apk or .app)
```

## Accessibility Identifiers (Test Tags)

The following test tags are used for Appium testing:

| Element | Test Tag / Accessibility ID |
|---------|----------------------------|
| Start Measurement Button | `start_measurement_button` |
| Result Label | `result_label` |

## App Features

- **Start Measurement Button**: Simulates a battery measurement
- **Result Label**: Displays "Battery consumption: X%" where X is 50-100
- **Logging**: Each measurement is logged with a timestamp

## Troubleshooting

### Android
- Ensure `ANDROID_HOME` is set correctly
- Make sure USB debugging is enabled for physical devices
- Check that the emulator is running: `adb devices`

### iOS
- Ensure Xcode command line tools are installed: `xcode-select --install`
- For simulators, use: `xcrun simctl list devices`

### Appium
- Verify Appium is running: `curl http://127.0.0.1:4723/status`
- Check driver installation: `appium driver list --installed`

## Open Source Compliance

This project is developed for European Commission projects and follows strict open source compliance requirements.

### License
- **Primary License**: EUPL-1.2 (European Union Public Licence)
- **SPDX Identifier**: `EUPL-1.2`
- **Copyright**: © 2026 Ahmed ADOUANI

### License Files
- `LICENSE` - Full EUPL-1.2 text
- `DEPENDENCIES.md` - License analysis of all dependencies
- All source files contain EUPL license headers

### Compliance Status
✅ **All dependencies are EUPL-compatible**  
✅ **All source files have proper license headers**  
✅ **No hard-coded secrets in the codebase**  
✅ **Complete dependency documentation**  
✅ **Automated compliance checking**

### Automated Compliance Checking
This project includes automated tools for EUPL compliance:

```bash
# Run the license compliance checker
python scripts/check-licenses.py

# Update dependency documentation
python scripts/update-dependencies-md.py
```

The automated checker will:
- Scan all build files for dependencies
- Check license compatibility with EUPL-1.2
- Generate compliance reports
- Update documentation

### CI/CD Integration
GitHub Actions workflow (`.github/workflows/license-compliance.yml`):
- Runs on every push and pull request
- Weekly scheduled checks
- Automatic PR creation for documentation updates
- PR comments with compliance status

### Building for EU Projects
When building for European Commission projects:
1. Ensure all contributors accept the EUPL terms
2. Maintain the license headers in all new files
3. Verify new dependencies are EUPL-compatible
4. Run automated compliance checks before releases
5. Update documentation using automated tools

### References
- [EUPL-1.2 Official Text](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
- [EUPL Compatibility Guidelines](https://joinup.ec.europa.eu/collection/eupl/guidelines-eupl-licence)
- [SPDX License Identifiers](https://spdx.org/licenses/)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License

Copyright (c) 2026 Ahmed ADOUANI

Licensed under the EUPL, Version 1.2 or – as soon they will be approved by the European Commission - subsequent versions of the EUPL (the "Licence");
You may not use this work except in compliance with the Licence.
You may obtain a copy of the Licence at:
https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the Licence for the specific language governing permissions and limitations under the Licence.

SPDX-License-Identifier: EUPL-1.2
