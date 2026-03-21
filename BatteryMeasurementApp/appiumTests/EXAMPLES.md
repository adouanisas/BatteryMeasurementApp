# Exemples d'exécution des tests Appium

## Configuration de base

### 1. Démarrer le serveur Appium
```bash
appium
```

### 2. Exécuter les tests Android (par défaut)
```bash
./gradlew :appiumTests:androidTest
```

### 3. Exécuter les tests iOS
```bash
./gradlew :appiumTests:iosTest
```

## Exemples avec paramètres personnalisés

### Android avec APK spécifique
```bash
./gradlew :appiumTests:androidTest \
  -Dappium.android.apk=/chemin/vers/app-debug.apk
```

### Android avec émulateur spécifique
```bash
./gradlew :appiumTests:androidTest \
  -Dappium.device.name="Pixel_6_Pro_API_35"
```

### iOS avec application spécifique
```bash
./gradlew :appiumTests:iosTest \
  -Dappium.ios.app="/chemin/vers/BatteryMeasurement.app" \
  -Dappium.device.name="iPhone 17"
```

### Tous les tests (Android par défaut)
```bash
./gradlew :appiumTests:allAppiumTests
```

## Exécution en mode debug

### Afficher les logs détaillés
```bash
./gradlew :appiumTests:androidTest --info
```

### Exécuter un test spécifique
```bash
./gradlew :appiumTests:androidTest --tests "*testMeasureButton"
```

### Exécuter avec stacktrace en cas d'erreur
```bash
./gradlew :appiumTests:androidTest --stacktrace
```

## Intégration avec CI/CD

### GitHub Actions (exemple)
```yaml
name: Appium Tests

on: [push, pull_request]

jobs:
  appium-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          java-version: '17'
      - name: Start Appium
        run: |
          npm install -g appium
          appium &
          sleep 10
      - name: Build APK
        run: ./gradlew :androidApp:assembleDebug
      - name: Run Android Appium Tests
        run: ./gradlew :appiumTests:androidTest
```

### Script shell pour exécution locale
```bash
#!/bin/bash
# run-appium-tests.sh

echo "Starting Appium server..."
appium &
APPIUM_PID=$!

echo "Waiting for Appium to start..."
sleep 10

echo "Building APK..."
./gradlew :androidApp:assembleDebug

echo "Running Appium tests..."
./gradlew :appiumTests:androidTest

echo "Stopping Appium server..."
kill $APPIUM_PID
```

## Dépannage

### Erreur : Appium server not running
```bash
# Vérifier que Appium est en cours d'exécution
appium --version
appium &  # Démarrer en arrière-plan
```

### Erreur : No APK found
```bash
# Construire l'APK d'abord
./gradlew :androidApp:assembleDebug

# Ou spécifier le chemin manuellement
./gradlew :appiumTests:androidTest \
  -Dappium.android.apk="androidApp/build/outputs/apk/debug/androidApp-debug.apk"
```

### Erreur : Device not found
```bash
# Lister les appareils disponibles
adb devices  # Android
xcrun simctl list devices  # iOS

# Utiliser un nom d'appareil valide
./gradlew :appiumTests:androidTest \
  -Dappium.device.name="emulator-5554"
```

## Variables d'environnement alternatives

```bash
# Utiliser des variables d'environnement au lieu de propriétés système
export APPIUM_PLATFORM=android
export APPIUM_DEVICE_NAME="Android Emulator"
./gradlew :appiumTests:androidTest
```

## Notes
- Les tests iOS nécessitent un Mac avec Xcode
- L'auto-détection d'APK cherche dans `build/test-apks/` puis dans `androidApp/build/outputs/apk/debug/`
- Les tests skip automatiquement si le serveur Appium n'est pas disponible