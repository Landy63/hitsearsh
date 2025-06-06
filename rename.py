

#!/usr/bin/env python3
"""
Script pour renommer les images dans static/cards/XY en ajoutant le chemin des dossiers
parents comme suffixe au nom de fichier.

Exemple :
  Avant : static/cards/XY/PROMO/EX_MEGA-PRIMO/XYP_079.jpeg
  Après  : static/cards/XY/PROMO/EX_MEGA-PRIMO/XYP_079_PROMO_EX_MEGA-PRIMO.jpeg
"""

import os
import sys

def rename_xy_images(xy_root="static/cards/XY"):
    """
    Parcourt récursivement le dossier xy_root et renomme chaque fichier image en
    ajoutant le chemin relatif (depuis xy_root) comme suffixe au nom principal.
    """
    if not os.path.isdir(xy_root):
        print(f"Le dossier '{xy_root}' n'existe pas.")
        return

    for root, dirs, files in os.walk(xy_root):
        # Ignorer le dossier racine lui-même
        rel_dir = os.path.relpath(root, xy_root)
        if rel_dir == ".":
            continue

        # Construire la partie suffixe : on prend le chemin relatif, on remplace les séparateurs par underscore
        # Exemple : rel_dir = "PROMO/EX_MEGA-PRIMO" -> suffix = "PROMO_EX_MEGA-PRIMO"
        suffix = rel_dir.replace(os.sep, "_")

        for filename in files:
            # Cibler uniquement les fichiers image (jpg, jpeg, png, webp, etc.)
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                continue

            old_path = os.path.join(root, filename)
            name, ext = os.path.splitext(filename)

            # Si le nom contient déjà le suffixe, on saute
            if name.endswith(f"_{suffix}"):
                continue

            new_name = f"{name}_{suffix}{ext}"
            new_path = os.path.join(root, new_name)

            try:
                os.rename(old_path, new_path)
                print(f"Renommé : {old_path} → {new_path}")
            except Exception as e:
                print(f"Erreur lors du renommage de {old_path} : {e}")

if __name__ == "__main__":
    # Autoriser un argument en ligne de commande pour spécifier le dossier XY
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = "static/cards/XY"
    rename_xy_images(root_dir)