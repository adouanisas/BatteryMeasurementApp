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

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import kotlin.random.Random

@Composable
fun App() {
    MaterialTheme {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.background,
        ) {
            BatteryMeasurementScreen()
        }
    }
}

@Composable
fun BatteryMeasurementScreen() {
    var resultText by remember { mutableStateOf("") }

    Column(
        modifier =
            Modifier
                .fillMaxSize()
                .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Button(
            onClick = {
                val batteryValue = Random.nextInt(50, 101)
                resultText = "Battery consumption: $batteryValue%"
                logMeasurement(batteryValue)
            },
            modifier =
                Modifier
                    .testTag(TestTags.START_MEASUREMENT_BUTTON),
        ) {
            Text("Start Measurement")
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = resultText,
            style = MaterialTheme.typography.headlineSmall,
            modifier =
                Modifier
                    .testTag(TestTags.RESULT_LABEL),
// .semantics { contentDescription = "Measurement result" }
// Note: contentDescription is intentionally removed because:
// - On iOS, contentDescription overrides the actual text in the accessibility tree,
//   making element.text return the description instead of the real value.
// - On Android, contentDescription and text coexist without conflict.
// - When resultText is empty, the element won't appear in the accessibility tree.
//   Use a default value like "--" if the element must always be present.
        )
    }
}

expect fun logMeasurement(batteryValue: Int)
