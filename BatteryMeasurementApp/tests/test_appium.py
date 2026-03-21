#!/usr/bin/env python3
"""
Appium test script for Battery Measurement App
Tests the UI components with test tags
"""

import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
import socket

# En dehors de la classe
def is_appium_running():
    try:
        sock = socket.create_connection(('localhost', 4723), timeout=2)
        sock.close()
        return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        return False
        
class BatteryMeasurementAppTests(unittest.TestCase):
    """Test suite for Battery Measurement App"""
    
    APPIUM_HOST = 'localhost'
    APPIUM_PORT = 4723

    
    def setUp(self):
        if not is_appium_running():
            self.skipTest("Appium server not running on localhost:4723. Start it with: appium")

        """Set up the test environment"""
        # Configuration for Android - Use UiAutomator2 with LocalComposeTestTagAsResourceId
        android_options = UiAutomator2Options()
        android_options.platform_name = 'Android'
        android_options.automation_name = 'UiAutomator2'
        android_options.device_name = 'Android Emulator'
        android_options.no_reset = True
        android_options.set_capability('appium:dontStopAppOnReset', True)

        # Find latest APK in test-apks directory
        import os, glob
        apk_dir = os.path.join(os.path.dirname(__file__), '..', 'build', 'test-apks')
        apk_files = glob.glob(os.path.join(apk_dir, '*.apk'))
        if apk_files:
            # Use the most recent APK
            apk_files.sort(key=os.path.getmtime, reverse=True)
            android_options.app = apk_files[0]
        else:
            # Fallback to default location
            android_options.app = os.path.join(os.path.dirname(__file__), '..', 'androidApp', 'build', 'outputs', 'apk', 'debug', 'androidApp-debug.apk')
        android_options.no_reset = True
        android_options.full_reset = False
        
        # No special capabilities needed - LocalComposeTestTagAsResourceId handles it in the app
        
        # Configuration for iOS
        ios_options = XCUITestOptions()
        ios_options.platform_name = 'iOS'
        ios_options.automation_name = 'XCUITest'
        ios_options.device_name = 'iPhone Simulator'
        ios_options.app = '/path/to/your/app.app'  # Update with actual app path
        ios_options.no_reset = True
        ios_options.full_reset = False
        
        # Choose platform (Android by default)
        self.platform = 'android'  # Change to 'ios' for iOS testing
        
        if self.platform == 'android':
            options = android_options
        else:
            options = ios_options
        
        # Start Appium session
        print(f"Appium URL: http://localhost:4723")
        print(f"Options: {options.to_capabilities()}")
        self.driver = webdriver.Remote(
            'http://localhost:4723',
            options=options
        )
        print("Appium session started successfully")
        
        # Set implicit wait
        self.driver.implicitly_wait(10)

    def find_by_tag(self, tag: str):
        """Find element by testTag, using ACCESSIBILITY_ID on both platforms"""
        if self.platform == 'android':
            return self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().resourceIdMatches(".*{tag}.*")'
            )
        else:
            return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, tag)
    
    def tearDown(self):
        """Clean up after test"""
        if self.driver:
            self.driver.quit()
    
    def test_battery_level_display(self):
        """Test that battery level is displayed"""
        time.sleep(3)
        
        # Click button first to generate a result
        button = self.find_by_tag('start_measurement_button')
        button.click()
        time.sleep(2)
        
        battery_level_element = self.find_by_tag('result_label')
        self.assertTrue(battery_level_element.is_displayed())
        battery_text = battery_level_element.text
        self.assertIn('%', battery_text)
        print(f"Battery level displayed: {battery_text}")
    
    def test_measure_button(self):
        """Test the measure button functionality"""
        # Find button by testTag using helper
        measure_button = self.find_by_tag('start_measurement_button')
        
        # Verify button exists and is displayed
        self.assertTrue(measure_button.is_displayed())
        
        # Get button text
        button_text = measure_button.text
        print(f"Measure button text: {button_text}")
        
        # Click the button
        measure_button.click()
        time.sleep(2)  # Wait for measurement to complete
        
        # Find updated battery level text by testTag
        battery_level_element = self.find_by_tag('result_label')
        
        updated_text = battery_level_element.text
        print(f"Updated battery level: {updated_text}")
        
        # Verify text contains percentage
        self.assertIn('%', updated_text)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)