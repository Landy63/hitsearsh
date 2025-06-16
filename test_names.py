#!/usr/bin/env python3
"""
Test rapide pour vérifier le décodage des noms de cartes
"""

import sys
import urllib.parse
sys.path.append('.')

from utils.card_utils import extract_card_name

# Test avec différents types de noms
test_files = [
    "TEST_001_JOLTEON%20STAR_RR.jpeg",
    "TEST_002_PROFESSOR%20OAK_TRAINERS.jpeg", 
    "TEST_003_CHARIZARD-EX_SR.jpeg",
    "TEST_004_Normal-Name_RR.jpeg"
]

print("Test de décodage des noms de cartes:")
print("=" * 40)

for filename in test_files:
    extracted_name = extract_card_name(filename)
    print(f"Fichier: {filename}")
    print(f"Nom extrait: '{extracted_name}'")
    print("-" * 40)
