package com.example.batterymeasurement.appium

import com.example.batterymeasurement.TestTags
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Tag
import org.junit.jupiter.api.Test
import java.io.File

/**
 * Base test class with shared test logic.
 * This class should NOT be executed directly.
 * Use AndroidBatteryMeasurementTest or IosBatteryMeasurementTest instead.
 */
@Tag("shared")
abstract class BatteryMeasurementTest : BaseAppiumTest() {

    @Test
    fun testDebugPageSource() {
        sleep(3)

        // Click button first to have content
        /*val button = findByTag(TestTags.START_MEASUREMENT_BUTTON)
        button.click()
        sleep(2)*/

        val source = driver.pageSource
        File("page_source_ios.xml").writeText(source)
        println(source)
    }

    @Test
    fun testBatteryLevelDisplay() {
        println("Testing battery level display on $platform...")
        sleep(3)
        
        val button = findByTag(TestTags.START_MEASUREMENT_BUTTON)
        button.click()
        sleep(2)
        
        val batteryLevelElement = findByTag(TestTags.RESULT_LABEL)
        assertTrue(batteryLevelElement.isDisplayed)
        val batteryText = batteryLevelElement.text
        assertTrue(batteryText.contains("%"))
        println("Battery level displayed on $platform: $batteryText")
    }
    
    @Test
    fun testMeasureButton() {
        println("Testing measure button on $platform...")
        
        val measureButton = findByTag(TestTags.START_MEASUREMENT_BUTTON)
        assertTrue(measureButton.isDisplayed)
        
        val buttonText = measureButton.text
        println("Measure button text on $platform: $buttonText")
        
        measureButton.click()
        sleep(2)
        
        val batteryLevelElement = findByTag(TestTags.RESULT_LABEL)
        val updatedText = batteryLevelElement.text
        println("Updated battery level on $platform: $updatedText")
        assertTrue(updatedText.contains("%"))
    }
}