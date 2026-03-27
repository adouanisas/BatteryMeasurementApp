plugins {
    alias(libs.plugins.androidApplication) apply false
    alias(libs.plugins.androidLibrary) apply false
    alias(libs.plugins.kotlinMultiplatform) apply false

    alias(libs.plugins.kotlinAndroid) apply false

    alias(libs.plugins.composeMultiplatform) apply false
    alias(libs.plugins.composeCompiler) apply false

    alias(libs.plugins.detekt) apply false
}

subprojects {
    apply(plugin = "io.gitlab.arturbosch.detekt")

    configure<io.gitlab.arturbosch.detekt.extensions.DetektExtension> {
        config.setFrom("${rootProject.projectDir}/detekt.yml")
        buildUponDefaultConfig = true
        ignoredBuildTypes = listOf("release")
    }
}
