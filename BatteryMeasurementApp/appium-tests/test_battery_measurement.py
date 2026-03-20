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

Appium Test Script for Battery Measurement App
Supports both Android (UIAutomator2) and iOS (XCUITest)
"""

import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BatteryMeasurementTest:
    BUTTON_ID = "start_measurement_button"
    RESULT_LABEL_ID = "result_label"
    
    def __init__(self, platform: str = "android"):
        self.platform = platform.lower()
        self.driver = None
        
    def setup_android(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "Android Emulator"
        options.app = "/path/to/androidApp/build/outputs/apk/debug/androidApp-debug.apk"
        options.automation_name = "UiAutomator2"
        options.no_reset = True
        return options
    
    def setup_ios(self):
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.device_name = "iPhone 15"
        options.platform_version = "17.0"
        options.app = "/path/to/iosApp/build/Debug-iphonesimulator/iosApp.app"
        options.automation_name = "XCUITest"
        options.no_reset = True
        return options
    
    def start_driver(self, appium_server_url: str = "http://127.0.0.1:4723"):
        if self.platform == "android":
            options = self.setup_android()
        else:
            options = self.setup_ios()
        
        self.driver = webdriver.Remote(appium_server_url, options=options)
        self.driver.implicitly_wait(10)
        print(f"Driver started for {self.platform}")
        
    def find_element_by_accessibility_id(self, accessibility_id: str):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, accessibility_id)
    
    def run_test(self) -> bool:
        try:
            print("\n=== Starting Battery Measurement Test ===\n")
            
            print("Step 1: Finding the 'Start Measurement' button...")
            button = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.BUTTON_ID))
            )
            print(f"  ✓ Button found: {button}")
            
            print("\nStep 2: Verifying result label is initially empty...")
            result_label = self.find_element_by_accessibility_id(self.RESULT_LABEL_ID)
            initial_text = result_label.text if result_label.text else ""
            print(f"  ✓ Initial label text: '{initial_text}'")
            
            print("\nStep 3: Clicking the button...")
            button.click()
            print("  ✓ Button clicked")
            
            time.sleep(1)
            
            print("\nStep 4: Verifying result label contains measurement...")
            result_label = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.RESULT_LABEL_ID))
            )
            result_text = result_label.text
            print(f"  ✓ Result text: '{result_text}'")
            
            print("\nStep 5: Validating result format...")
            if result_text and "Battery consumption:" in result_text and "%" in result_text:
                print("  ✓ Result format is correct")
                
                percentage_str = result_text.split(":")[1].strip().replace("%", "")
                percentage = int(percentage_str)
                
                if 50 <= percentage <= 100:
                    print(f"  ✓ Battery value ({percentage}%) is within expected range [50-100]")
                    return True
                else:
                    print(f"  ✗ Battery value ({percentage}%) is outside expected range [50-100]")
                    return False
            else:
                print(f"  ✗ Result format is incorrect: '{result_text}'")
                return False
                
        except Exception as e:
            print(f"\n  ✗ Test failed with error: {e}")
            return False
    
    def cleanup(self):
        if self.driver:
            self.driver.quit()
            print("\nDriver closed")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Appium tests for Battery Measurement App")
    parser.add_argument(
        "--platform",
        choices=["android", "ios"],
        default="android",
        help="Target platform (default: android)"
    )
    parser.add_argument(
        "--appium-url",
        default="http://127.0.0.1:4723",
        help="Appium server URL (default: http://127.0.0.1:4723)"
    )
    parser.add_argument(
        "--app-path",
        help="Path to the app file (.apk for Android, .app for iOS)"
    )
    
    args = parser.parse_args()
    
    test = BatteryMeasurementTest(platform=args.platform)
    
    try:
        if args.platform == "android":
            options = UiAutomator2Options()
            options.platform_name = "Android"
            options.device_name = "Android Emulator"
            options.automation_name = "UiAutomator2"
            options.no_reset = True
            
            if args.app_path:
                options.app = args.app_path
            else:
                options.app = "./androidApp/build/outputs/apk/debug/androidApp-debug.apk"
        else:
            options = XCUITestOptions()
            options.platform_name = "iOS"
            options.device_name = "iPhone 15"
            options.platform_version = "17.0"
            options.automation_name = "XCUITest"
            options.no_reset = True
            
            if args.app_path:
                options.app = args.app_path
            else:
                options.app = "./iosApp/build/Debug-iphonesimulator/iosApp.app"
        
        test.driver = webdriver.Remote(args.appium_url, options=options)
        test.driver.implicitly_wait(10)
        print(f"Connected to Appium server at {args.appium_url}")
        
        result = test.run_test()
        
        print("\n" + "=" * 50)
        if result:
            print("✅ TEST PASSED")
        else:
            print("❌ TEST FAILED")
        print("=" * 50)
        
        return 0 if result else 1
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
        
    finally:
        test.cleanup()


if __name__ == "__main__":
    exit(main())
