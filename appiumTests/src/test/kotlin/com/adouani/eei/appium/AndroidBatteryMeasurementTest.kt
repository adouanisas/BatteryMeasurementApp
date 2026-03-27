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
