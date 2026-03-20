#!/usr/bin/env python3
"""
Script d'installation d'Appium pour les tests automatisés de l'application BatteryMeasurementApp.
Ce script installe Appium Server, Appium Doctor, et configure l'environnement pour les tests.

Licence: EUPL v1.2
Copyright (c) 2025 EEIComission
"""

import subprocess
import sys
import os
import platform
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Exécute une commande shell et affiche le résultat."""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"Commande: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Succès: {description}")
        if result.stdout:
            print(f"Sortie: {result.stdout[:500]}...")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Échec: {description}")
        print(f"Code d'erreur: {e.returncode}")
        if e.stdout:
            print(f"Sortie: {e.stdout}")
        if e.stderr:
            print(f"Erreur: {e.stderr}")
        return False

def check_node_installed():
    """Vérifie si Node.js est installé."""
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        print("✅ Node.js est installé")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js n'est pas installé")
        print("Veuillez installer Node.js depuis: https://nodejs.org/")
        return False

def check_npm_installed():
    """Vérifie si npm est installé."""
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ npm est installé")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm n'est pas installé")
        return False

def install_appium_server():
    """Installe Appium Server globalement."""
    print("\n📡 Installation d'Appium Server...")
    
    # Vérifier si Appium est déjà installé
    try:
        subprocess.run(["appium", "--version"], check=True, capture_output=True)
        print("✅ Appium est déjà installé")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Installer Appium
    commands = [
        ("npm install -g appium", "Installation d'Appium globalement"),
        ("npm install -g appium-doctor", "Installation d'Appium Doctor"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    return True

def install_appium_python_client():
    """Installe le client Python pour Appium."""
    print("\n🐍 Installation du client Python pour Appium...")
    
    # Vérifier si pip est disponible
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip n'est pas disponible")
        return False
    
    # Installer les dépendances Python
    requirements = [
        "Appium-Python-Client>=4.0.0",
        "selenium>=4.0.0",
        "pytest>=7.0.0",
        "pytest-html>=3.0.0",
        "pytest-xdist>=3.0.0",
        "allure-pytest>=2.0.0",
        "webdriver-manager>=4.0.0",
    ]
    
    for package in requirements:
        cmd = f"{sys.executable} -m pip install {package}"
        if not run_command(cmd, f"Installation de {package}"):
            return False
    
    return True

def setup_venv():
    """Configure un environnement virtuel Python."""
    print("\n🐍 Configuration de l'environnement virtuel Python...")
    
    venv_dir = Path("venv")
    
    if venv_dir.exists():
        print(f"✅ L'environnement virtuel existe déjà: {venv_dir}")
        return True
    
    # Créer l'environnement virtuel
    if not run_command(f"{sys.executable} -m venv venv", "Création de l'environnement virtuel"):
        return False
    
    # Déterminer le chemin d'activation selon l'OS
    system = platform.system()
    if system == "Windows":
        activate_script = "venv\\Scripts\\activate"
        pip_path = "venv\\Scripts\\pip"
    else:
        activate_script = "venv/bin/activate"
        pip_path = "venv/bin/pip"
    
    print(f"\n📝 Pour activer l'environnement virtuel:")
    print(f"  Sur Windows: {activate_script}")
    print(f"  Sur macOS/Linux: source {activate_script}")
    
    # Mettre à jour pip dans le venv
    if not run_command(f"{pip_path} install --upgrade pip", "Mise à jour de pip dans le venv"):
        return False
    
    return True

def generate_requirements():
    """Génère un fichier requirements.txt à partir des packages installés."""
    print("\n📄 Génération du fichier requirements.txt...")
    
    try:
        # Utiliser pip freeze pour générer requirements.txt
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            check=True,
            capture_output=True,
            text=True
        )
        
        with open("requirements.txt", "w") as f:
            f.write(result.stdout)
        
        print("✅ Fichier requirements.txt généré avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Échec de la génération de requirements.txt: {e}")
        return False

def check_system_requirements():
    """Vérifie les prérequis système."""
    print("🔍 Vérification des prérequis système...")
    
    system = platform.system()
    print(f"Système d'exploitation: {system}")
    print(f"Version Python: {sys.version}")
    
    # Vérifier Node.js et npm
    node_ok = check_node_installed()
    npm_ok = check_npm_installed()
    
    if not node_ok or not npm_ok:
        print("\n⚠️  Node.js et npm sont requis pour Appium.")
        print("Veuillez les installer depuis: https://nodejs.org/")
        return False
    
    return True

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Script d'installation d'Appium pour BatteryMeasurementApp")
    parser.add_argument("--venv-only", action="store_true", help="Configurer uniquement l'environnement virtuel")
    parser.add_argument("--appium-only", action="store_true", help="Installer uniquement Appium")
    parser.add_argument("--python-only", action="store_true", help="Installer uniquement les dépendances Python")
    parser.add_argument("--generate-reqs", action="store_true", help="Générer uniquement requirements.txt")
    
    args = parser.parse_args()
    
    print("🚀 Script d'installation d'Appium pour BatteryMeasurementApp")
    print("=" * 60)
    
    # Changer de répertoire pour être dans le projet
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    print(f"📁 Répertoire de travail: {project_root}")
    
    success = True
    
    if args.venv_only:
        success = setup_venv()
    elif args.appium_only:
        success = check_system_requirements() and install_appium_server()
    elif args.python_only:
        success = install_appium_python_client()
    elif args.generate_reqs:
        success = generate_requirements()
    else:
        # Installation complète
        if not check_system_requirements():
            sys.exit(1)
        
        if not setup_venv():
            success = False
        
        if not install_appium_server():
            success = False
        
        if not install_appium_python_client():
            success = False
        
        if not generate_requirements():
            success = False
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Installation terminée avec succès!")
        print("\n📋 Prochaines étapes:")
        print("1. Activer l'environnement virtuel:")
        print("   - Windows: venv\\Scripts\\activate")
        print("   - macOS/Linux: source venv/bin/activate")
        print("\n2. Démarrer Appium Server:")
        print("   appium")
        print("\n3. Exécuter les tests:")
        print("   pytest tests/")
        print("\n4. Vérifier la configuration avec Appium Doctor:")
        print("   appium-doctor")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ L'installation a échoué. Veuillez vérifier les erreurs ci-dessus.")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()