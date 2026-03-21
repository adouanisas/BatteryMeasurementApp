# Appium Tests for Battery Measurement App

Kotlin-based Appium tests for the Battery Measurement KMP application.

## Prerequisites

1. **Appium Server**: Install and start Appium server
   ```bash
   npm install -g appium
   appium
   ```

2. **Android/iOS Setup**:
   - Android: Android SDK, emulator or device
   - iOS: Xcode, simulator or device

## Test Structure

### Base Classes
- `BaseAppiumTest`: Common setup/teardown, driver creation, `findByTag` helper
- `BatteryMeasurementTest`: Shared UI tests (button click, battery display)
- `AndroidAppiumTest`: Android-specific tests (battery info, orientation, notifications)
- `IosAppiumTest`: iOS-specific tests (device info, gestures)

### Test Tags
Tests use `TestTags` from the shared KMP module:
- `START_MEASUREMENT_BUTTON`: "start_measurement_button"
- `RESULT_LABEL`: "result_label"

### Test Structure
See [TEST_STRUCTURE.md](TEST_STRUCTURE.md) for detailed architecture.

#### Shared Test Logic (abstract)
- `BatteryMeasurementTest`: `@Tag("shared")` - Base class with shared test logic

#### Platform Launchers (run these)
- `AndroidBatteryMeasurementTest`: `@Tag("android")` - Android launcher
- `IosBatteryMeasurementTest`: `@Tag("ios")` - iOS launcher

#### Platform-Specific Tests
- `AndroidAppiumTest`: `@Tag("android")` - Android-only tests
- `IosAppiumTest`: `@Tag("ios")` - iOS-only tests

## Running Tests

### Android Studio (Recommandé)
Des configurations d'exécution pré-définies sont disponibles :
- **Android Appium Tests** : Tests Android (tags: android, shared)
- **iOS Appium Tests** : Tests iOS (tags: ios, shared)
- **All Appium Tests** : Tous les tests
- **Run Single Appium Test** : Test spécifique

Voir [ANDROID_STUDIO_SETUP.md](ANDROID_STUDIO_SETUP.md) pour la configuration détaillée.

### Command Line
```bash
# Android tests (tags: android, shared)
./gradlew :appiumTests:androidTest

# iOS tests (tags: ios, shared) - requires iOS app
./gradlew :appiumTests:iosTest -Dappium.ios.app="/path/to/BatteryMeasurement.app"

# All tests
./gradlew :appiumTests:allAppiumTests

# Custom APK
./gradlew :appiumTests:androidTest -Dappium.android.apk=/path/to/app.apk

# Custom device
./gradlew :appiumTests:androidTest -Dappium.device.name="Pixel_6_Pro_API_35"

# Custom iOS app
./gradlew :appiumTests:iosTest -Dappium.ios.app=/path/to/app.app
```

## Configuration

### System Properties
- `appium.platform`: "android" or "ios" (default: "android")
- `appium.device.name`: Device/simulator name 
  - Android default: "Android Emulator"
  - iOS default: "iPhone 17"
- `appium.android.apk`: Path to APK file (auto-detects latest in build/test-apks)
- `appium.ios.app`: Path to iOS .app bundle (REQUIRED for iOS tests)

### APK Auto-detection
Tests automatically find the latest APK in:
1. `../build/test-apks/` (sorted by modification time)
2. `../androidApp/build/outputs/apk/debug/androidApp-debug.apk`

### App Detection Scripts

#### Find Android APK:
```bash
./appiumTests/find-android-apk.sh
```

#### Find iOS App Bundle:
```bash
./appiumTests/find-ios-app.sh
```

#### Build Apps:
```bash
# Build Android APK
./gradlew :androidApp:assembleDebug

# Build iOS app (requires Mac with Xcode)
./gradlew :iosApp:build
```

## Test Logic

### Element Location Strategy
- **Android**: Uses `resourceIdMatches(".*tag.*")` with `testTagsAsResourceId = true`
- **iOS**: Uses `accessibilityId(tag)` (native Compose Multiplatform behavior)

### Server Detection
Tests skip execution if Appium server is not running on `localhost:4723`

## Dependencies
- Appium Java Client 9.0.0
- JUnit 5
- Kotlin test

## Integration with CI
Example GitHub Actions workflow:
```yaml
jobs:
  appium-tests:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          java-version: '17'
      - name: Start Appium
        run: |
          npm install -g appium
          appium &
      - name: Build APK
        run: ./gradlew :androidApp:assembleDebug
      - name: Run Android Appium Tests
        run: ./gradlew :appiumTests:androidTest
        env:
          APPIUM_PLATFORM: android
```

## Notes
- Tests are written in Kotlin for better integration with KMP codebase
- Reuses `TestTags` from shared module (no string duplication)
- Follows same locator strategy as Python tests
- Uses JUnit 5 with proper assumptions for platform-specific tests