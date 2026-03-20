# Appium Test Suite for Battery Measurement App

This directory contains Appium test scripts for the Battery Measurement App, a Compose Multiplatform application that runs on both Android and iOS.

## Test Structure

- `test_appium.py` - Main test suite with cross-platform tests
- `test_appium_android.py` - Android-specific tests
- `test_appium_ios.py` - iOS-specific tests
- `run_tests.py` - Test runner script
- `requirements.txt` - Python dependencies

## Prerequisites

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Appium
```bash
npm install -g appium
npm install -g appium-doctor
```

### 3. Set Up Test Environment

#### Android:
- Android SDK installed
- Android emulator or physical device
- App APK built from the project

#### iOS:
- Xcode installed
- iOS simulator or physical device
- App .app bundle built from the project

## Running Tests

### Basic Usage
```bash
# Run all tests
python run_tests.py --all

# Run specific test
python run_tests.py --test test_appium.py

# Run with platform specification
python run_tests.py --platform android
python run_tests.py --platform ios

# Check Appium server status
python run_tests.py --check-server
```

### With Custom Configuration
```bash
# Specify device and app path
python run_tests.py --test test_appium.py --platform android --device "Pixel 6" --app "/path/to/app.apk"
```

## Test Coverage

### Cross-Platform Tests (`test_appium.py`)
- Battery level display verification
- Measure button functionality
- History button navigation
- Settings button navigation
- App title display

### Android-Specific Tests (`test_appium_android.py`)
- Android battery info access
- Screen orientation changes
- Notification handling

### iOS-Specific Tests (`test_appium_ios.py`)
- iOS device info access
- iOS gestures (swipe)
- Permission handling

## Test Tags (Accessibility IDs)

The tests use these accessibility identifiers defined in the app:

| Element | Accessibility ID | Description |
|---------|-----------------|-------------|
| Battery Level Text | `battery_level_text` | Displays current battery percentage |
| Measure Button | `measure_button` | Button to start battery measurement |
| History Button | `history_button` | Button to navigate to history screen |
| Settings Button | `settings_button` | Button to navigate to settings screen |
| App Title | `app_title` | Main app title |
| History Title | `history_title` | Title on history screen |
| Settings Title | `settings_title` | Title on settings screen |
| Back Button | `back_button` | Navigation back button |

## Configuration

### Environment Variables
- `APPIUM_PLATFORM`: Set to 'android' or 'ios'
- `APPIUM_DEVICE_NAME`: Device/simulator name
- `APPIUM_APP_PATH`: Path to app file

### Command Line Arguments
See `python run_tests.py --help` for all options.

## Troubleshooting

### Appium Server Not Running
```bash
# Start Appium server
appium

# Or with specific port
appium --port 4723
```

### Device Not Found
- Ensure emulator/simulator is running
- Check device name in Android Studio/Xcode
- Verify USB debugging enabled (physical devices)

### Test Failures
- Update accessibility IDs in tests if app changes
- Check app path is correct
- Verify platform-specific capabilities

## Best Practices

1. **Run tests on both platforms** to ensure cross-platform compatibility
2. **Update test tags** when modifying UI components
3. **Check Appium server** before running tests
4. **Review test logs** for detailed failure information
5. **Maintain test dependencies** with requirements.txt

## Integration with CI/CD

Add to your CI pipeline:
```yaml
- name: Install dependencies
  run: pip install -r tests/requirements.txt

- name: Run Appium tests
  run: python tests/run_tests.py --all
```