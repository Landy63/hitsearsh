#!/usr/bin/env python3
"""
Script pour renommer toutes les images dans un dossier racine donné, afin que chaque fichier
prenne comme préfixe le nom de son sous-dossier.

Ex. : XY/MMBP/001.jpeg → XY/MMBP/MMBP_001.jpeg
"""

import os
import sys

def rename_images_in_root(root_dir):
    """
    Parcourt chaque sous-dossier de 'root_dir' et renomme les fichiers image pour préfixer
    avec le nom de leur dossier parent.
    """
    if not os.path.isdir(root_dir):
        print(f"Le dossier '{root_dir}' n'existe pas.")
        return

    # Parcours des sous-dossiers de root_dir
    for series_code in os.listdir(root_dir):
        series_folder = os.path.join(root_dir, series_code)
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
    import sys
    # Racines à traiter : arguments passés ou par défaut ['S&S']
    roots = sys.argv[1:] if len(sys.argv) > 1 else ['ADV']
    for root in roots:
        rename_images_in_root(root)