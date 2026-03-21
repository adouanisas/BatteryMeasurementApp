package com.example.batterymeasurement.appium

import org.junit.jupiter.api.Tag

/**
 * Android-specific test launcher.
 * Extends the shared test logic and sets platform to Android.
 */
@Tag("android")
class AndroidBatteryMeasurementTest : BatteryMeasurementTest() {

    override var platform: String = "android"
    override val deviceName: String = "Android Emulator"
}