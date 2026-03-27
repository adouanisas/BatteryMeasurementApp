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

package com.adouani.eei.appium

import com.adouani.eei.TestTags
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Tag
import org.junit.jupiter.api.Test

/**
 * Base test class with shared test logic.
 * This class should NOT be executed directly.
 * Use AndroidBatteryMeasurementTest or IosBatteryMeasurementTest instead.
 */
@Tag("shared")
abstract class BatteryMeasurementTest : BaseAppiumTest() {
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
