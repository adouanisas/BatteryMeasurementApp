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

package com.adouani.eei

/**
 * Business logic layer for battery level access.
 * Depends on [BatteryDataSource] — injected so it can be replaced with a fake in tests.
 */
class BatteryService(private val dataSource: BatteryDataSource) {

    /**
     * Returns the battery level (0–100) or -1 when unavailable.
     * Clamps out-of-range values from the platform API.
     */
    fun getBatteryLevel(): Int {
        val raw = dataSource.getLevel()
        return when {
            raw < 0 -> -1
            raw > 100 -> 100
            else -> raw
        }
    }

    /** Returns true if the battery level can be read on this device/platform. */
    fun isAvailable(): Boolean = getBatteryLevel() >= 0
}
