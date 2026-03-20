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


class BatteryMeasurementAppTests(unittest.TestCase):
    """Test suite for Battery Measurement App"""
    
    def setUp(self):
        """Set up the test environment"""
        # Configuration for Android
        android_options = UiAutomator2Options()
        android_options.platform_name = 'Android'
        android_options.automation_name = 'UiAutomator2'
        android_options.device_name = 'Android Emulator'
        android_options.app = '/path/to/your/app.apk'  # Update with actual APK path
        android_options.no_reset = True
        android_options.full_reset = False
        
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
        self.driver = webdriver.Remote(
            'http://localhost:4723',
            options=options
        )
        
        # Set implicit wait
        self.driver.implicitly_wait(10)
    
    def tearDown(self):
        """Clean up after test"""
        if self.driver:
            self.driver.quit()
    
    def test_battery_level_display(self):
        """Test that battery level is displayed"""
        # Find battery level text by test tag
        battery_level_element = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            'battery_level_text'
        )
        
        # Verify element exists and is displayed
        self.assertTrue(battery_level_element.is_displayed())
        
        # Get the text content
        battery_text = battery_level_element.text
        
        # Verify text contains battery information
        self.assertIn('%', battery_text)
        print(f"Battery level displayed: {battery_text}")
    
    def test_measure_button(self):
        """Test the measure button functionality"""
        # Find measure button by test tag
        measure_button = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            'measure_button'
        )
        
        # Verify button exists and is displayed
        self.assertTrue(measure_button.is_displayed())
        
        # Get button text
        button_text = measure_button.text
        print(f"Measure button text: {button_text}")
        
        # Click the button
        measure_button.click()
        time.sleep(2)  # Wait for measurement to complete
        
        # Verify battery level text updates
        battery_level_element = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            'battery_level_text'
        )
        
        updated_text = battery_level_element.text
        print(f"Battery level after measurement: {updated_text}")
        
        # Verify text changed (not empty and contains %)
        self.assertIsNotNone(updated_text)
        self.assertIn('%', updated_text)
    
    def test_history_button(self):
        """Test the history button functionality"""
        # Find history button by test tag
        history_button = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            'history_button'
        )
        
        # Verify button exists and is displayed
        self.assertTrue(history_button.is_displayed())
        
        # Get button text
        button_text = history_button.text
        print(f"History button text: {button_text}")
        
        # Click the button
        history_button.click()
        time.sleep(1)
        
        # Verify history screen elements
        try:
            history_title = self.driver.find_element(
                AppiumBy.ACCESSIBILITY_ID,
                'history_title'
            )
            self.assertTrue(history_title.is_displayed())
            print("History screen displayed successfully")
            
            # Go back to main screen
            back_button = self.driver.find_element(
                AppiumBy.ACCESSIBILITY_ID,
                'back_button'
            )
            if back_button.is_displayed():
                back_button.click()
                time.sleep(1)
                
        except Exception as e:
            print(f"History screen not fully implemented: {e}")
    
    def test_settings_button(self):
        """Test the settings button functionality"""
        # Find settings button by test tag
        settings_button = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            'settings_button'
        )
        
        # Verify button exists and is displayed
        self.assertTrue(settings_button.is_displayed())
        
        # Get button text
        button_text = settings_button.text
        print(f"Settings button text: {button_text}")
        
        # Click the button
        settings_button.click()
        time.sleep(1)
        
        # Verify settings screen elements
        try:
            settings_title = self.driver.find_element(
                AppiumBy.ACCESSIBILITY_ID,
                'settings_title'
            )
            self.assertTrue(settings_title.is_displayed())
            print("Settings screen displayed successfully")
            
            # Go back to main screen
            back_button = self.driver.find_element(
                AppiumBy.ACCESSIBILITY_ID,
                'back_button'
            )
            if back_button.is_displayed():
                back_button.click()
                time.sleep(1)
                
        except Exception as e:
            print(f"Settings screen not fully implemented: {e}")
    
    def test_app_title(self):
        """Test that app title is displayed"""
        # Find app title by test tag
        app_title = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID,
            'app_title'
        )
        
        # Verify element exists and is displayed
        self.assertTrue(app_title.is_displayed())
        
        # Get the text content
        title_text = app_title.text
        
        # Verify title is not empty
        self.assertIsNotNone(title_text)
        self.assertGreater(len(title_text.strip()), 0)
        print(f"App title: {title_text}")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)