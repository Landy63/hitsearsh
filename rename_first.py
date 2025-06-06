

#!/usr/bin/env python3
"""
Script pour renommer toutes les images dans le dossier 'XY', afin que chaque fichier
prenne comme préfixe le nom de son sous-dossier.

Ex. : XY/MMBP/001.jpeg → XY/MMBP/MMBP_001.jpeg
"""

import os
import sys

def rename_images_in_xy(xy_root="XY"):
    """
    Parcourt chaque sous-dossier de 'XY' et renomme les fichiers image pour préfixer
    avec le nom de leur dossier parent.
    """
    if not os.path.isdir(xy_root):
        print(f"Le dossier '{xy_root}' n'existe pas.")
        return

    # Parcours des sous-dossiers de XY
    for series_code in os.listdir(xy_root):
        series_folder = os.path.join(xy_root, series_code)
        if not os.path.isdir(series_folder):
            continue

        # Pour chaque fichier dans le sous-dossier
        for filename in os.listdir(series_folder):
            # Cibler uniquement les fichiers .jpg, .jpeg, .png ou .webp
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                continue

            # Déjà préfixé ? Sauter
            if filename.startswith(f"{series_code}_"):
                continue

            old_path = os.path.join(series_folder, filename)

            # Numéro + extension
            name_with_ext = os.path.basename(filename)
            prefix = f"{series_code}_"
            new_name = prefix + name_with_ext
            new_path = os.path.join(series_folder, new_name)

            try:
                os.rename(old_path, new_path)
                print(f"Renommé: {old_path} → {new_path}")
            except Exception as e:
                print(f"Erreur lors du renommage de {old_path}: {e}")

if __name__ == "__main__":
    # Si un argument est fourni, l'utiliser comme dossier racine
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "XY"
    rename_images_in_xy(root)