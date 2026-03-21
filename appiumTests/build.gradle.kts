plugins {
    id("org.jetbrains.kotlin.jvm")
    id("java-library")
}

group = "com.example.batterymeasurement"
version = "1.0.0"

repositories {
    mavenCentral()
    google()
}

kotlin {
    compilerOptions {
        jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
    }
}

dependencies {
    // Kotlin
    implementation(kotlin("stdlib"))
    
    // Appium Java Client 9.0.0 (new API)
    implementation("io.appium:java-client:9.0.0")
    
    // JUnit 5
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testImplementation("org.junit.jupiter:junit-jupiter-params")
    
    // Kotlin test
    testImplementation(kotlin("test"))
    
    // Access to shared TestTags from sharedTestTags module
    implementation(project(":sharedTestTags"))
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "skipped", "failed")
    }
    systemProperty("appium.platform", System.getProperty("appium.platform", "android"))
    systemProperty("appium.device.name", System.getProperty("appium.device.name", "Android Emulator"))
    systemProperty("appium.android.apk", System.getProperty("appium.android.apk", ""))
    systemProperty("appium.ios.app", System.getProperty("appium.ios.app", ""))
}

tasks.register<Test>("androidTest") {
    group = "verification"
    description = "Run Android Appium tests"
    useJUnitPlatform()
    systemProperty("appium.platform", "android")
    useJUnitPlatform {
        includeTags("android")
    }
}

tasks.register<Test>("iosTest") {
    group = "verification"
    description = "Run iOS Appium tests"
    useJUnitPlatform()
    systemProperty("appium.platform", "ios")
    useJUnitPlatform {
        includeTags("ios")
    }
}

tasks.register<Test>("allAppiumTests") {
    group = "verification"
    description = "Run all Appium tests"
    useJUnitPlatform()
}