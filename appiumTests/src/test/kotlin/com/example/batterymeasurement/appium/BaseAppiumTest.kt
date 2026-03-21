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

import io.appium.java_client.AppiumBy
import io.appium.java_client.AppiumDriver
import io.appium.java_client.android.AndroidDriver
import io.appium.java_client.android.options.UiAutomator2Options
import io.appium.java_client.ios.IOSDriver
import io.appium.java_client.ios.options.XCUITestOptions
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assumptions.assumeTrue
import org.junit.jupiter.api.BeforeEach
import org.openqa.selenium.WebElement
import java.io.File
import java.net.InetSocketAddress
import java.net.Socket
import java.net.URL
import java.time.Duration

abstract class BaseAppiumTest {
    companion object {
        const val APPIUM_HOST = "localhost"
        const val APPIUM_PORT = 4723

        fun isAppiumRunning(): Boolean {
            return try {
                Socket().use { socket ->
                    socket.connect(InetSocketAddress(APPIUM_HOST, APPIUM_PORT), 2000)
                    true
                }
            } catch (e: Exception) {
                false
            }
        }

        fun findLatestApk(): String? {
            val apkDir = File("../build/test-apks")
            if (!apkDir.exists()) {
                val defaultApk = File("../androidApp/build/outputs/apk/debug/androidApp-debug.apk")
                return if (defaultApk.exists()) defaultApk.absolutePath else null
            }

            val apkFiles = apkDir.listFiles { file -> file.extension == "apk" }
            return apkFiles?.maxByOrNull { it.lastModified() }?.absolutePath
        }
        
        fun findIosApp(): String? {
            // Check the iOS build location you provided
            val iosAppPath = File("../build/ios-derived-data/Build/Products/Debug-iphonesimulator/iosApp.app")
            return if (iosAppPath.exists()) iosAppPath.absolutePath else null
        }
    }

    protected lateinit var driver: AppiumDriver
    protected abstract val platform: String

    protected abstract val deviceName: String
    protected val androidApkPath: String = findLatestApk() ?: ""
    protected val iosAppPath: String = findIosApp() ?: ""

    @BeforeEach
    open fun setUp() {
        assumeTrue(isAppiumRunning()) {
            "Appium server not running on $APPIUM_HOST:$APPIUM_PORT. Start it with: appium"
        }

        driver = when (platform) {
            "android" -> createAndroidDriver()
            "ios" -> createIosDriver()
            else -> throw IllegalArgumentException("Unsupported platform: $platform")
        }

        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10))
        println("Appium session started successfully for platform: $platform")
    }

    private fun createAndroidDriver(): AndroidDriver {
        val options = UiAutomator2Options()
            .setPlatformName("Android")
            .setAutomationName("UiAutomator2")
            .setDeviceName(deviceName)

        val apkPath = androidApkPath
        if (apkPath.isEmpty()) {
            options.setApp(apkPath)
            println("Using APK: $apkPath")
        } else {
            println("Warning: No APK found, using already installed app")
            println("Note: APK should be in: ../build/test-apks/ (latest .apk file)")
            println("Or at: ../androidApp/build/outputs/apk/debug/androidApp-debug.apk")
        }

        options.setNoReset(true)
        options.setFullReset(false)
        options.setCapability("appium:dontStopAppOnReset", true)

        return AndroidDriver(URL("http://$APPIUM_HOST:$APPIUM_PORT"), options)
    }

    private fun createIosDriver(): IOSDriver {
        val options = XCUITestOptions()
            .setPlatformName("iOS")
            .setAutomationName("XCUITest")
            .setDeviceName(deviceName)

        options.setApp(iosAppPath)
        options.setBundleId("com.adouani.batterymeasurement.iosApp")

        options.setNoReset(true)
        options.setFullReset(false)

        return IOSDriver(URL("http://$APPIUM_HOST:$APPIUM_PORT"), options)
    }

    @AfterEach
    open fun tearDown() {
        if (::driver.isInitialized) {
            driver.quit()
            println("Appium session closed")
        }
    }

    protected fun findByTag(tag: String): WebElement {
        return when (platform) {
            "android" -> driver.findElement(
                AppiumBy.androidUIAutomator("new UiSelector().resourceIdMatches(\".*$tag.*\")")
            )
            "ios" -> driver.findElement(AppiumBy.accessibilityId(tag))
            else -> throw IllegalStateException("Unsupported platform: $platform")
        }
    }

    protected fun sleep(seconds: Long) {
        Thread.sleep(seconds * 1000)
    }
}
