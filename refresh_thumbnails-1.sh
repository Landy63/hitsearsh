#!/usr/bin/env bash
#
# Script pour ré‐encoder chaque JPEG/PNG/WebP dans le dossier S&M
# afin de forcer macOS à les reconnaître comme de vraies images.
# Usage : ./refresh_thumbnails.sh [chemin_vers_dossier_S&M]
#

DPT_ROOT="${1:-DPT}"

if [ ! -d "$DPT_ROOT" ]; then
  echo "Le dossier '$DPT_ROOT' n'existe pas."
  exit 1
fi

find "$DPT_ROOT" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \) | while IFS= read -r FILE; do
  echo "Ré‐encodage de : $FILE"
  # Utilise sips pour forcer la réécriture au format JPEG (ou PNG si besoin)
  # Ici on force en JPEG en écrasant le fichier existant.
  sips -s format jpeg "$FILE" --out "${FILE}.tmp" >/dev/null 2>&1
  if [ -f "${FILE}.tmp" ]; then
    mv "${FILE}.tmp" "$FILE"
  else
    echo "  → Échec de la ré‐écriture pour $FILE"
  fi
done

echo "Réinitialisation du cache Quick Look…"
qlmanage -r
qlmanage -r cache

echo "Redémarrage de Finder…"
killall Finder 2>/dev/null

echo "Terminé."