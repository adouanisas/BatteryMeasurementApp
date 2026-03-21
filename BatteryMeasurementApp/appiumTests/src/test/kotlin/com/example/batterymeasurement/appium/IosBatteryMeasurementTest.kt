package com.example.batterymeasurement.appium

import org.junit.jupiter.api.Assumptions.assumeTrue
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Tag

/**
 * iOS-specific test launcher.
 * Extends the shared test logic and sets platform to iOS.
 */
@Tag("ios")
class IosBatteryMeasurementTest : BatteryMeasurementTest() {
    override var platform: String = "ios"
    override val deviceName: String = "iPhone 17"
}