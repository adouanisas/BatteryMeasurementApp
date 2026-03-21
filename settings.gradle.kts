rootProject.name = "BatteryMeasurementApp"

pluginManagement {
    repositories {
        google()
        gradlePluginPortal()
        mavenCentral()
    }
}

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}

include(":composeApp")
include(":androidApp")
include(":appiumTests")
include(":sharedTestTags")
