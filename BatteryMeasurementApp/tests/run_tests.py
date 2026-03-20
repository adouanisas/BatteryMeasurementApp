#!/usr/bin/env python3
"""
Test runner script for Battery Measurement App
Run all Appium tests with configuration options
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_tests(test_file, platform='android', device_name=None, app_path=None):
    """
    Run specific test file with configuration
    
    Args:
        test_file: Path to test file
        platform: 'android' or 'ios'
        device_name: Device/simulator name
        app_path: Path to app file (.apk or .app)
    """
    print(f"\n{'='*60}")
    print(f"Running tests: {test_file}")
    print(f"Platform: {platform}")
    print(f"Device: {device_name}")
    print(f"App: {app_path}")
    print(f"{'='*60}\n")
    
    # Set environment variables for tests
    env = os.environ.copy()
    env['APPIUM_PLATFORM'] = platform
    
    if device_name:
        env['APPIUM_DEVICE_NAME'] = device_name
    
    if app_path:
        env['APPIUM_APP_PATH'] = app_path
    
    # Run the test
    result = subprocess.run(
        [sys.executable, '-m', 'unittest', test_file],
        env=env,
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_all_tests():
    """Run all test suites"""
    test_files = [
        'test_appium.py',
        'test_appium_android.py',
        'test_appium_ios.py'
    ]
    
    results = []
    
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_tests(test_file)
            results.append((test_file, success))
        else:
            print(f"Test file not found: {test_file}")
            results.append((test_file, False))
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    all_passed = True
    for test_file, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_file:30} {status}")
        if not success:
            all_passed = False
    
    print(f"{'='*60}")
    print(f"OVERALL: {'PASS' if all_passed else 'FAIL'}")
    print(f"{'='*60}")
    
    return all_passed


def check_appium_server():
    """Check if Appium server is running"""
    try:
        import requests
        response = requests.get('http://localhost:4723/wd/hub/status', timeout=5)
        if response.status_code == 200:
            print("Appium server is running")
            return True
    except Exception as e:
        print(f"Appium server not running: {e}")
        print("\nTo start Appium server:")
        print("1. Install Appium: npm install -g appium")
        print("2. Start server: appium")
        print("3. Or use Appium Desktop GUI")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run Appium tests for Battery Measurement App')
    parser.add_argument('--test', help='Specific test file to run')
    parser.add_argument('--platform', choices=['android', 'ios'], default='android',
                       help='Platform to test (default: android)')
    parser.add_argument('--device', help='Device/simulator name')
    parser.add_argument('--app', help='Path to app file (.apk or .app)')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--check-server', action='store_true', help='Check Appium server status')
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check Appium server if requested
    if args.check_server:
        check_appium_server()
        return
    
    # Check Appium server before running tests
    if not check_appium_server():
        print("\nWARNING: Appium server may not be running!")
        print("Tests may fail. Start Appium server first.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Run tests
    if args.all:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    elif args.test:
        success = run_tests(args.test, args.platform, args.device, args.app)
        sys.exit(0 if success else 1)
    else:
        # Default: run main test
        success = run_tests('test_appium.py', args.platform, args.device, args.app)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()