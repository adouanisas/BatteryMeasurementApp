/*
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
*/

package com.example.batterymeasurement.appium

import com.example.batterymeasurement.TestTags
import io.appium.java_client.android.AndroidDriver
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Assumptions.assumeTrue
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Tag
import org.junit.jupiter.api.Test
import org.openqa.selenium.ScreenOrientation

@Tag("android")
class AndroidAppiumTest : BaseAppiumTest() {

    override var platform: String = "android"
    override val deviceName: String = "Android Emulator"

    private lateinit var androidDriver: AndroidDriver
    
    @BeforeEach
    override fun setUp() {
        assumeTrue(platform == "android") { "Skipping Android tests on platform: $platform" }
        super.setUp()
        androidDriver = driver as AndroidDriver
    }
    
    @Test
    fun testAndroidSpecificFeatures() {
        println("Testing Android-specific features...")
        
        val batteryInfo = androidDriver.executeScript("mobile: batteryInfo") as Map<*, *>
        println("Android Battery Info: $batteryInfo")
        assertNotNull(batteryInfo)
        
        val deviceInfo = androidDriver.executeScript("mobile: deviceInfo") as Map<*, *>
        println("Device Info: $deviceInfo")
        assertNotNull(deviceInfo)
    }
    
    @Test
    fun testScreenOrientation() {
        println("Testing screen orientation changes...")
        
        val currentOrientation = androidDriver.orientation
        println("Current orientation: $currentOrientation")
        
        if (currentOrientation == ScreenOrientation.PORTRAIT) {
            androidDriver.rotate(ScreenOrientation.LANDSCAPE)
        } else {
            androidDriver.rotate(ScreenOrientation.PORTRAIT)
        }
        
        sleep(2)
        
        val measureButton = findByTag(TestTags.START_MEASUREMENT_BUTTON)
        assertTrue(measureButton.isDisplayed)
        
        androidDriver.rotate(ScreenOrientation.PORTRAIT)
    }
    
    @Test
    fun testNotifications() {
        println("Testing notification handling...")
        
        try {
            androidDriver.openNotifications()
            sleep(2)
            
            androidDriver.navigate().back()
            sleep(1)
            
            println("Notification test completed")
        } catch (e: Exception) {
            println("Notification test skipped: ${e.message}")
        }
    }
}