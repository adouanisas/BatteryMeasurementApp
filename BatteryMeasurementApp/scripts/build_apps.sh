#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_gradle_wrapper() {
    if [ ! -f "$PROJECT_DIR/gradle/wrapper/gradle-wrapper.jar" ]; then
        print_warning "Gradle wrapper not found. Regenerating..."
        cd "$PROJECT_DIR"
        if command -v gradle &> /dev/null; then
            gradle wrapper
        else
            print_error "Gradle not installed. Install with: brew install gradle"
            exit 1
        fi
    fi
}

build_android() {
    print_status "Building Android APK..."
    cd "$PROJECT_DIR"
    
    check_gradle_wrapper
    
    # Clean and build
    ./gradlew clean :androidApp:assembleDebug
    
    # Create dedicated directory for test APKs
    APK_DIR="$PROJECT_DIR/build/test-apks"
    mkdir -p "$APK_DIR"
    
    # Find all APK files
    APK_FILES=$(find "$PROJECT_DIR/androidApp/build" -name "*.apk" -type f 2>/dev/null)
    
    if [ -z "$APK_FILES" ]; then
        print_error "No APK files found after build"
        print_status "Checking build logs..."
        ./gradlew :androidApp:assembleDebug --stacktrace 2>&1 | tail -50
        exit 1
    fi
    
    # Copy the first APK found to dedicated directory
    FIRST_APK=$(echo "$APK_FILES" | head -1)
    APK_NAME="androidApp-debug-$(date +%Y%m%d-%H%M%S).apk"
    APK_PATH="$APK_DIR/$APK_NAME"
    
    cp "$FIRST_APK" "$APK_PATH"
    
    if [ -f "$APK_PATH" ]; then
        print_status "Android APK built successfully!"
        echo -e "APK Path: ${GREEN}$APK_PATH${NC}"
        echo -e "Original APK: ${YELLOW}$FIRST_APK${NC}"
        echo -e "APK Size: $(du -h "$APK_PATH" | cut -f1)"
        export ANDROID_APK_PATH="$APK_PATH"
    else
        print_error "Failed to copy APK to dedicated directory"
        exit 1
    fi
}

build_ios() {
    print_status "Building iOS App..."
    cd "$PROJECT_DIR"
    
    if [[ "$(uname)" != "Darwin" ]]; then
        print_error "iOS build requires macOS"
        exit 1
    fi
    
    if ! command -v xcodebuild &> /dev/null; then
        print_error "Xcode not installed"
        exit 1
    fi
    
    check_gradle_wrapper
    
    ./gradlew :composeApp:linkDebugFrameworkIosSimulatorArm64 || ./gradlew :composeApp:linkDebugFrameworkIosX64
    
    DERIVED_DATA="$PROJECT_DIR/build/ios-derived-data"
    mkdir -p "$DERIVED_DATA"
    
    if [ -d "$PROJECT_DIR/iosApp/iosApp.xcodeproj" ]; then
        xcodebuild -project "$PROJECT_DIR/iosApp/iosApp.xcodeproj" \
            -scheme "iosApp" \
            -configuration Debug \
            -sdk iphonesimulator \
            -derivedDataPath "$DERIVED_DATA" \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            build
    elif [ -d "$PROJECT_DIR/iosApp/iosApp.xcworkspace" ]; then
        xcodebuild -workspace "$PROJECT_DIR/iosApp/iosApp.xcworkspace" \
            -scheme "iosApp" \
            -configuration Debug \
            -sdk iphonesimulator \
            -derivedDataPath "$DERIVED_DATA" \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            build
    else
        print_warning "No Xcode project found. Generating with xcodegen or creating manually..."
        
        if command -v xcodegen &> /dev/null; then
            cd "$PROJECT_DIR/iosApp"
            xcodegen generate
            xcodebuild -project "$PROJECT_DIR/iosApp/iosApp.xcodeproj" \
                -scheme "iosApp" \
                -configuration Debug \
                -sdk iphonesimulator \
                -derivedDataPath "$DERIVED_DATA" \
                -destination 'platform=iOS Simulator,name=iPhone 15' \
                build
        else
            print_error "No Xcode project found and xcodegen not installed."
            print_status "Install xcodegen: brew install xcodegen"
            print_status "Or open the project in Xcode to generate the project files."
            exit 1
        fi
    fi
    
    APP_PATH=$(find "$DERIVED_DATA" -name "*.app" -type d | head -1)
    
    if [ -n "$APP_PATH" ] && [ -d "$APP_PATH" ]; then
        print_status "iOS App built successfully!"
        echo -e "App Path: ${GREEN}$APP_PATH${NC}"
        export IOS_APP_PATH="$APP_PATH"
    else
        print_error "iOS App not found after build"
        exit 1
    fi
}

run_appium_tests() {
    print_status "Running Appium tests..."
    cd "$PROJECT_DIR/tests"
    
    if [ -n "$ANDROID_APK_PATH" ]; then
        print_status "Running Android tests..."
        python run_tests.py --platform android --app "$ANDROID_APK_PATH"
    fi
    
    if [ -n "$IOS_APP_PATH" ]; then
        print_status "Running iOS tests..."
        python run_tests.py --platform ios --app "$IOS_APP_PATH"
    fi
}

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --android       Build Android APK only"
    echo "  --ios           Build iOS App only"
    echo "  --all           Build both Android and iOS (default)"
    echo "  --test          Run Appium tests after build"
    echo "  --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --android              # Build Android APK"
    echo "  $0 --ios                  # Build iOS App"
    echo "  $0 --all                  # Build both"
    echo "  $0 --android --test       # Build Android and run tests"
}

BUILD_ANDROID=false
BUILD_IOS=false
RUN_TESTS=false

if [ $# -eq 0 ]; then
    BUILD_ANDROID=true
    BUILD_IOS=true
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        --android)
            BUILD_ANDROID=true
            shift
            ;;
        --ios)
            BUILD_IOS=true
            shift
            ;;
        --all)
            BUILD_ANDROID=true
            BUILD_IOS=true
            shift
            ;;
        --test)
            RUN_TESTS=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

echo "=========================================="
echo "  Battery Measurement App Builder"
echo "=========================================="

if [ "$BUILD_ANDROID" = true ]; then
    build_android
fi

if [ "$BUILD_IOS" = true ]; then
    build_ios
fi

if [ "$RUN_TESTS" = true ]; then
    run_appium_tests
fi

print_status "Build completed!"

echo ""
echo "=========================================="
echo "  Build Summary"
echo "=========================================="
if [ -n "$ANDROID_APK_PATH" ]; then
    echo -e "Android APK: ${GREEN}$ANDROID_APK_PATH${NC}"
fi
if [ -n "$IOS_APP_PATH" ]; then
    echo -e "iOS App: ${GREEN}$IOS_APP_PATH${NC}"
fi
echo ""
echo "To run Appium tests manually:"
if [ -n "$ANDROID_APK_PATH" ]; then
    echo "  python tests/run_tests.py --platform android --app \"$ANDROID_APK_PATH\""
fi
if [ -n "$IOS_APP_PATH" ]; then
    echo "  python tests/run_tests.py --platform ios --app \"$IOS_APP_PATH\""
fi
