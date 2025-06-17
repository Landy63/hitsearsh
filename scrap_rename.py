import os
import re
import requests
from pathlib import Path
try:
    from PyPDF2 import PdfReader
except ImportError:
    print("PyPDF2 n'est pas installé. Utilisez: pip install PyPDF2")
    exit(1)

# Chemin vers le fichier PDF contenant les liens
LINKS_PDF_PATH = Path(__file__).parent / "VS_links.pdf"
DEST_DIR = Path(__file__).parent / "pdf"
DEST_DIR.mkdir(exist_ok=True)

# Extraire les liens depuis le fichier PDF
def extract_urls_from_pdf(pdf_path):
    print(f"Lecture du fichier PDF : {pdf_path}")
    
    if not pdf_path.exists():
        print(f"Erreur : Le fichier {pdf_path} n'existe pas")
        return []
    
    try:
        reader = PdfReader(pdf_path)
        print(f"Nombre de pages trouvées : {len(reader.pages)}")
        
        urls = []
        for i, page in enumerate(reader.pages):
            print(f"Traitement de la page {i+1}...")
            text = page.extract_text()
            if text:
                print(f"Texte extrait (première ligne) : {text[:100]}...")
                # Recherche des liens pokecardex
                found = re.findall(r'https://www\.pokecardex\.com/checklist/jp/([A-Z0-9]+)', text)
                # Recherche alternative au cas où le format serait différent
                if not found:
                    found = re.findall(r'pokecardex\.com/checklist/jp/([A-Z0-9]+)', text)
                # Recherche encore plus large
                if not found:
                    found = re.findall(r'/jp/([A-Z0-9]+)', text)
                
                print(f"Codes trouvés sur cette page : {found}")
                urls.extend(found)
        
        print(f"Total des codes trouvés : {len(urls)}")
        print(f"Codes : {urls}")
        return urls
        
    except Exception as e:
        print(f"Erreur lors de la lecture du PDF : {e}")
        return []

# Télécharger les fichiers PDF depuis les URL
def download_checklist_pdfs(series_codes):
    if not series_codes:
        print("Aucun code de série trouvé à télécharger")
        return
        
    for code in series_codes:
        url = f"https://www.pokecardex.com/checklist/jp/{code}"
        print(f"Tentative de téléchargement : {url}")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                output_path = DEST_DIR / f"{code}.pdf"
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✓ Téléchargé : {code} ({len(response.content)} bytes)")
            else:
                print(f"✗ Erreur pour {code} (status {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"✗ Erreur réseau pour {code} : {e}")
        except Exception as e:
            print(f"✗ Erreur pour {code} : {e}")

if __name__ == "__main__":
    print("=== Extraction des URLs depuis le PDF ===")
    codes = extract_urls_from_pdf(LINKS_PDF_PATH)
    
    if codes:
        print(f"\n=== Téléchargement de {len(codes)} fichiers ===")
        download_checklist_pdfs(codes)
    else:
        print("Aucun code trouvé dans le PDF. Vérifiez le contenu du fichier.")
