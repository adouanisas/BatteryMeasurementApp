# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CLAUDE.md with project architecture and development guide
- Open source structure: CHANGELOG, issue templates, CI workflow
- Static analysis with **detekt** (`detekt.yml`) — replaces ktlint
- CI workflow (`ci.yml`) with lint (detekt), unit tests, and Android build jobs
- Detekt report uploaded as CI artifact on every run

### Changed
- Replaced ktlint with detekt — resolves incompatibility with Compose Multiplatform generated sources
- CI lint job updated: `ktlintCheck` → `detekt`
- `@Composable` functions excluded from `FunctionNaming` rule in `detekt.yml`

### Fixed
- Import ordering and wildcard imports in Appium test files
- `throw IllegalStateException(...)` replaced with idiomatic `error(...)` in `BaseAppiumTest`

---

## [0.1.0] - 2026-03-27

### Added
- Initial Compose Multiplatform project structure (Android + iOS)
- Basic UI: start measurement button and result label
- Shared test tags library (`sharedTestTags` KMP module)
- Appium E2E tests (Kotlin/JUnit 5) for Android and iOS
- EUPL-1.2 license compliance tooling (Gradle script + GitHub Actions)
- CI/CD workflows: build apps, license compliance
- `CONTRIBUTING.md`, `DEPENDENCIES.md`, `NOTICE`

[Unreleased]: https://github.com/ahmedadouani/EEIComission/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ahmedadouani/EEIComission/releases/tag/v0.1.0
