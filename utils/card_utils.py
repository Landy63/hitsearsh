import os
from flask import current_app

def lister_toutes_les_cartes():
    """
    Parcourt récursivement CARDS_ROOT et retourne la liste
    des chemins relatifs (par rapport à static/) vers chaque image.
    """
    app = current_app._get_current_object()
    CARDS_ROOT = os.path.join(app.static_folder, 'cards')
    cartes = []
    for root, dirs, files in os.walk(CARDS_ROOT):
        for fn in files:
            if fn.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(root, fn)
                rel_path = os.path.relpath(full_path, app.static_folder).replace('\\', '/')
                cartes.append(rel_path.upper())
    return cartes

def extract_card_name(filename):
    """
    Extrait le nom de la carte entre le 2e et le 3e underscore, nettoie les tirets et espaces.
    """
    name = os.path.splitext(filename)[0]
    parts = name.split('_')
    if len(parts) >= 4:
        card_name = parts[2]
    else:
        card_name = ''
    card_name = card_name.replace('-', ' ').strip()
    return card_name.upper()
