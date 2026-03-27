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

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class BatteryServiceTest {

    private fun serviceWith(level: Int) = BatteryService(FakeBatteryDataSource(level))

    // --- getBatteryLevel ---

    @Test
    fun `returns level when battery is available`() {
        assertEquals(75, serviceWith(75).getBatteryLevel())
    }

    @Test
    fun `returns 0 at minimum charge`() {
        assertEquals(0, serviceWith(0).getBatteryLevel())
    }

    @Test
    fun `returns 100 at full charge`() {
        assertEquals(100, serviceWith(100).getBatteryLevel())
    }

    @Test
    fun `returns -1 when battery is unavailable`() {
        assertEquals(-1, serviceWith(-1).getBatteryLevel())
    }

    @Test
    fun `clamps out-of-range high values to 100`() {
        assertEquals(100, serviceWith(150).getBatteryLevel())
    }

    @Test
    fun `clamps any negative value to -1`() {
        assertEquals(-1, serviceWith(Int.MIN_VALUE).getBatteryLevel())
    }

    // --- isAvailable ---

    @Test
    fun `isAvailable returns true when level is 0`() {
        assertTrue(serviceWith(0).isAvailable())
    }

    @Test
    fun `isAvailable returns true when level is 50`() {
        assertTrue(serviceWith(50).isAvailable())
    }

    @Test
    fun `isAvailable returns true when level is 100`() {
        assertTrue(serviceWith(100).isAvailable())
    }

    @Test
    fun `isAvailable returns false when level is -1`() {
        assertFalse(serviceWith(-1).isAvailable())
    }

    @Test
    fun `isAvailable returns false when platform returns MIN_VALUE`() {
        assertFalse(serviceWith(Int.MIN_VALUE).isAvailable())
    }
}
