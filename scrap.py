

import os
import re
import requests

def download_xy_images(txt_file_path, output_root="XY"):
    """
    Lit le fichier txt contenant des URLs de pages de la série XY,
    extrait tous les liens d'images HD pour chaque sous-série, et télécharge
    les images dans le dossier local 'XY/<series_code>/' avec des noms 'NNN.jpeg'.
    """
    # Expression régulière pour extraire les liens d'images HD, et capturer le code de série + numéro
    img_pattern = re.compile(
        r"https://pokecardex\.b-cdn\.net/assets/images/sets_jp/([^/]+)/HD/(\d+)\.jpg\?class=hd"
    )

    # S'assurer que le dossier racine existe
    if not os.path.exists(output_root):
        os.makedirs(output_root)

    # Lire chaque URL depuis le fichier texte
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        page_urls = [line.strip() for line in f if line.strip()]

    for page_url in page_urls:
        print(f"Traitement de la page : {page_url}")
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"  Erreur lors de la récupération de {page_url}: {e}")
            continue

        # Chercher toutes les correspondances dans le HTML
        matches = img_pattern.findall(html)
        if not matches:
            print("  Aucun lien d'image HD trouvé sur cette page.")
            continue

        for series_code, number_str in matches:
            # Dossier local pour cette sous-série
            series_folder = os.path.join(output_root, series_code)
            if not os.path.exists(series_folder):
                os.makedirs(series_folder)

            # Construction de l'URL complète (pour être sûr)
            img_url = f"https://pokecardex.b-cdn.net/assets/images/sets_jp/{series_code}/HD/{number_str}.jpg?class=hd"

            # Définir le nom de fichier local, numéroté sur 3 chiffres
            try:
                num_int = int(number_str)
                local_name = f"{num_int:03d}.jpeg"
            except ValueError:
                local_name = f"{number_str}.jpeg"

            local_path = os.path.join(series_folder, local_name)

            # Si le fichier existe déjà, on passe
            if os.path.exists(local_path):
                continue

            # Téléchargement de l'image
            try:
                img_resp = requests.get(img_url, stream=True)
                img_resp.raise_for_status()
                with open(local_path, 'wb') as img_file:
                    for chunk in img_resp.iter_content(1024):
                        img_file.write(chunk)
                print(f"  Téléchargé : {series_code}/{local_name}")
            except Exception as e:
                print(f"  Échec téléchargement {img_url}: {e}")
    print("Terminé.")
 
if __name__ == "__main__":
    # Chemin vers le fichier XY.txt contenant les URLs de pages à scraper
    txt_path = os.path.join(os.getcwd(), "XY.txt")
    download_xy_images(txt_path)