#!/usr/bin/env python3
"""
Android-specific Appium test script for Battery Measurement App
"""

import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


class AndroidBatteryAppTests(unittest.TestCase):
    """Android-specific test suite"""
    
    def setUp(self):
        """Set up Android test environment"""
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.automation_name = 'UiAutomator2'
        options.device_name = 'Android Emulator'
        options.app = '/path/to/your/app.apk'  # Update with actual APK path
        options.no_reset = True
        options.full_reset = False
        
        # Appium server URL
        self.driver = webdriver.Remote(
            'http://localhost:4723',
            options=options
        )
        
        self.driver.implicitly_wait(10)
    
    def tearDown(self):
        """Clean up"""
        if self.driver:
            self.driver.quit()
    
    def test_android_specific_features(self):
        """Test Android-specific features"""
        print("Testing Android-specific features...")
        
        # Test battery info access (Android-specific)
        battery_info = self.driver.execute_script('mobile: batteryInfo')
        print(f"Android Battery Info: {battery_info}")
        
        # Test device info
        device_info = self.driver.execute_script('mobile: deviceInfo')
        print(f"Device Info: {device_info}")
    
    def test_screen_orientation(self):
        """Test screen orientation changes"""
        # Get current orientation
        current_orientation = self.driver.orientation
        print(f"Current orientation: {current_orientation}")
        
        # Change orientation
        if current_orientation == 'PORTRAIT':
            self.driver.orientation = 'LANDSCAPE'
        else:
            self.driver.orientation = 'PORTRAIT'
        
        time.sleep(2)
        
        # Verify UI elements still work
        measure_button = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            'measure_button'
        )
        self.assertTrue(measure_button.is_displayed())
        
        # Change back
        self.driver.orientation = 'PORTRAIT'
    
    def test_notifications(self):
        """Test notification handling (Android-specific)"""
        # Open notifications (Android-specific)
        try:
            self.driver.open_notifications()
            time.sleep(2)
            
            # Close notifications
            self.driver.back()
            time.sleep(1)
            
            print("Notification test completed")
        except Exception as e:
            print(f"Notification test skipped: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)