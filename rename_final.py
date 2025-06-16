import os
import re
from pathlib import Path
from PyPDF2 import PdfReader

pdf_dir = Path(__file__).parent / "pdf"
cards_dir = Path(__file__).parent / "ADV"

# Crée un dictionnaire global : {"EGCS": {8: "Groudon ex", ...}, ...}
card_map = {}

# Nettoie et complète les noms tronqués
def clean_name(name):
    name = name.replace("..", "").strip()
    # Corrige toutes les occurrences de 'δ Delta Speci..' en 'δ Delta Species'
    name = re.sub(r'δ Delta Speci.*', 'δ Delta Species', name)
    # Ajoute 'Species' si 'δ Delta' n'est pas déjà suivi de 'Species'
    name = re.sub(r'δ Delta(?! Species)', 'δ Delta Species', name)
    return name

# Extraction des noms depuis les fichiers PDF
def parse_pdfs():
    for pdf_path in pdf_dir.glob("*.pdf"):
        code = pdf_path.stem
        print(f"Lecture du fichier PDF : {pdf_path.name}")
        reader = PdfReader(pdf_path)
        card_dict = {}
        for page in reader.pages:
            text = page.extract_text()
            if not text:
                continue
            matches = re.findall(r"(\d{3}) ([^\n]+)", text)
            for num_str, name in matches:
                try:
                    num = int(num_str)
                    card_dict[num] = clean_name(name)
                except ValueError:
                    continue
        card_map[code] = card_dict
        print(f"Cartes extraites pour {code} : {len(card_dict)} trouvées")

# Renommer les fichiers dans ADV/ (récursivement)
def rename_card_files():
    count = 0
    for filepath in cards_dir.rglob("*.jpeg"):
        match = re.match(r"([A-Z0-9]+)_(\d{3})_(.+)", filepath.name, re.IGNORECASE)
        if not match:
            print(f"Fichier ignoré (aucun match) : {filepath.name}")
            continue
        code, num_str, rest = match.groups()
        try:
            num = int(num_str)
            name = card_map.get(code.upper(), {}).get(num)
            print(f"{filepath.name} → code: {code}, num: {num}, rest: {rest}, name trouvé: {name}")
            if name:
                # Nettoyer le nom pour éviter les caractères problématiques
                safe_name = re.sub(r'[\\/*?:"<>|]', '_', name)
                parts = rest.split("_")
                new_name = f"{code}_{num_str}_{safe_name}_" + "_".join(parts)
                filepath.rename(filepath.with_name(new_name))
                print(f"Renommé : {filepath.name} → {new_name}")
                count += 1
        except Exception as e:
            print(f"Erreur avec {filepath.name} : {e}")
    print(f"{count} fichier(s) renommé(s).")

if __name__ == "__main__":
    parse_pdfs()
    rename_card_files()
