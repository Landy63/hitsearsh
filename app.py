from flask import Flask, render_template, request, url_for
import os
import re

# Ordre de sortie des SÉRIES (seulement les codes, en majuscule)
SERIES_ORDER = [
    "S1H",
    "S1W",
    "S1A",
    "S2",
    "S2A",
    "S3",
    "S3A",
    "S4",
    "S4A",
    "S5R",
    "S5I",
    "S5A",
    "S6K",
    "S6H",
    "S6A",
    "S7R",
    "S7D",
    "S8",
    "S8A",
    "S8B",
    "S9",
    "S9A",
    "S10P",
    "S10D",
    "S10A",
    "S10B",
    "S11",
    "S11A",
    "S12",
    "S12A"
]

# Ordre de sortie des DECKS (seulement les codes, en majuscule)
DECK_ORDER = [
    "SA1",
    "SA2",
    "SA3",
    "SA4",
    "SA5",
    "SB",
    "SP1",
    "SC-C",
    "SC-G",
    "SD",
    "SP2",
    "SC2",
    "SEF",
    "SEK",
    "SF",
    "SP3",
    "SP4",
    "SGG",
    "SGI",
    "SH",
    "SP5",
    "SJ",
    "S8A-G",
    "SI",
    "CDCH",
    "SK",
    "SLD",
    "SLL",
    "SN",
    "SPD",
    "SPZ",
    "SP6",
    "SPO"
]

# Regroupement des séries par ères (inclut codes de séries, decks et promos)
ERA_TO_SERIES = {
    "SWORD_AND_SHIELD": SERIES_ORDER + DECK_ORDER,
    # À compléter plus tard pour d’autres ères, ex.:
    # "SUN_AND_MOON": ["SM1", "SM2", ...],
}

# Correspondance entre clé d'ère et nom de dossier
ERA_TO_FOLDER = {
    "SWORD_AND_SHIELD": "S&S",
    # ajouter d'autres ères ultérieurement si nécessaire
}


# Ordre de sortie des RARETÉS (en majuscule)
RARITY_ORDER = ["AR", "CHR", "CSR", "A", "K", "S", "DECK", "HR", "PROMO", "RR", "RRR", "SAR", "SR", "SSR", "UR"]

app = Flask(__name__)

# Racine de toutes les séries : dans static/cards/, chaque sous-dossier est une série (S&S, B&W, etc.)
CARDS_ROOT = os.path.join(app.static_folder, 'cards')

def lister_toutes_les_cartes():
    """
    Parcourt récursivement CARDS_ROOT et retourne la liste
    des chemins relatifs (par rapport à static/) vers chaque image.
    Ex : "cards/S&S/UR/Trainrs/card1.jpeg"
    """
    cartes = []
    for root, dirs, files in os.walk(CARDS_ROOT):
        for fn in files:
            if fn.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(root, fn)
                # Calcul du chemin relatif par rapport à static/
                rel_path = os.path.relpath(full_path, app.static_folder).replace('\\', '/')
                cartes.append(rel_path.upper())
    return cartes

def filter_cards(cartes, selected_rarities, selected_types, selected_styles, selected_substyles, selected_excluded_styles,
                 no_fullart=False, no_characters=False, no_trainers=False, no_gold_opt=False, no_shiny_opt=False,
                 no_alternative_opt=False, no_rainbow_opt=False, no_v_shiny=False, no_vmax_shiny=False,
                 no_holo_shiny=False, no_k_shiny=False, selected_eras=None, selected_series=None, selected_decks=None):
    """
    Applique la charte sur la liste de chemins relatifs (en MAJUSCULE pour simplifier).
    """
    def matches_rarity(path):
        return any(f"/{rar}/" in path for rar in selected_rarities)

    # Remplacement par matches_type_with_substyle
    def matches_type_with_substyle(name, types, substyles):
        for t in types:
            # CHARACTERS RARES: cards with CSR or CHR rarity
            if t == "CHARACTERS RARES":
                if "/CSR/" in name or "/CHR/" in name:
                    return True
            if t == "V":
                if re.search(r'_V(?=[_.])', name) and not any(x in name for x in ["_VMAX", "_VSTAR", "V-UNION"]):
                    return True
            elif t == "VMAX":
                if "_VMAX" in name:
                    return True
            elif t == "VSTAR":
                if "_VSTAR" in name:
                    return True
            elif t == "ALTERNATIVES RARES":
                if "/AR/" in name or "/CHR/" in name:
                    return True
            elif t == "V-UNION":
                if "V-UNION" in name:
                    return True
            elif t == "EX B&W":
                if "_EX_B&W" in name or "_EXB&W" in name:
                    return True
            elif t == "EX_PCG":
                if "EX_PCG" in name:
                    return True
            elif t == "EX XY":
                if "EX_XY" in name:
                    return True
            elif t == "GX":
                if "_GX" in name:
                    return True
            elif t == "TRAINERS":
                if "TRAINERS" in name:
                    return True
            elif t == "ENERGY":
                if "ENERGY" in name:
                    return True
        return False

    def matches_style_included(name, styles, substyles):
        # Si aucun style sélectionné, on accepte tout
        if not styles:
            return True

        # Vérifier si la carte correspond à au moins un style sélectionné
        for style in styles:
            # FULL ART
            if style == "FULL ART":
                if "_FA" in name or "_FULL" in name:
                    return True

            # ALTERNATIVE
            elif style == "ALTERNATIVE":
                if "_ALT" in name and any(x in name for x in ["_V", "_VMAX", "_VSTAR", "TRAINERS"]):
                    return True

            # RAINBOW
            elif style == "RAINBOW":
                if "_RB" in name and any(x in name for x in ["_V", "_VMAX", "_VSTAR", "TRAINERS"]):
                    return True

            # ESCOUADE (TAG_TEAM)
            elif style == "ESCOUADE":
                if "_TAG_TEAM" in name and "GX" in name:
                    return True

            # SHINY (inclut toutes les cartes contenant "_SHINY")
            elif style == "SHINY":
                if "_SHINY" in name:
                    return True

            # GOLD
            elif style == "GOLD":
                # Si sous-catégories GOLD définies
                subs = substyles.get("GOLD", [])
                # Gold Metal
                if "GOLD METAL" in subs:
                    if "_GOLD_METAL" in name:
                        return True
                # Pokémon (exclude Trainers and Energies)
                if "POKEMON" in subs:
                    if "_GOLD" in name and not any(x in name for x in ["TRAINERS", "ENERGY"]):
                        return True
                if subs:
                    if "BASE" in subs:
                        if "_GOLD" in name and not any(x in name for x in ["_BLACK", "_ALT", "_SHINY", "_RB", "_TAG_TEAM", "_GOLD_METAL"]):
                            return True
                    if "ALTERNATIVE" in subs:
                        if "_GOLD" in name and "_ALT" in name:
                            return True
                    if "BLACK GOLD" in subs:
                        if "_BLACK_GOLD" in name or "_GOLD_BLACK" in name:
                            return True
                else:
                    if "_GOLD" in name:
                        return True

        # Si aucun style ne correspond, on exclut la carte
        return False

    def matches_style_excluded(name, excluded_styles):
        # Si aucun style à exclure, rien à filtrer
        if not excluded_styles:
            return False

        # On rejette toute carte correspondant à un style exclu
        for style in excluded_styles:
            if style == "GOLD" and "GOLD" in name:
                return True
            if style == "BASE" and ("_V" in name or "_VSTAR" in name):
                return True
            if style == "FULL ART" and (("FA" in name or "_FULL" in name) and "_V" in name):
                return True
            if style == "ALTERNATIVE" and "ALT" in name and any(x in name for x in ["_V", "_VMAX", "_VSTAR", "TRAINERS"]):
                return True
            if style == "RAINBOW" and "RB" in name and any(x in name for x in ["_V", "_VMAX", "_VSTAR", "TRAINERS"]):
                return True
            if style == "ESCOUADE" and "TAG_TEAM" in name and "GX" in name:
                return True
            if style == "SHINY" and "SHINY" in name and any(x in name for x in ["_V", "_VMAX"]):
                return True
        return False

    résultats = []
    for chemin in cartes:
        name = os.path.basename(chemin).upper()
        path_upper = chemin.upper()

        # Si l'utilisateur a coché une ou plusieurs séries ou decks
        if selected_series or selected_decks:
            match_series = any(name.startswith(f"{ser}_") for ser in selected_series) if selected_series else False
            match_deck = any(name.startswith(f"{deck}_") for deck in selected_decks) if selected_decks else False
            if not (match_series or match_deck):
                continue

        # Filtrer par ère si spécifié (vérifier dossier associé à l'ère)
        if selected_eras:
            if not any(f"/{ERA_TO_FOLDER.get(era, era)}/".upper() in path_upper for era in selected_eras):
                continue

        # Replacer name pour les filtres suivants
        name = chemin.upper()

        # Filtrage spécifique V / VMAX / VSTAR
        # Détecter si c'est une carte V (pas VMAX ni VSTAR)
        is_v = re.search(r'_V(?=[_.])', name) and not any(x in name for x in ["_VMAX", "_VSTAR", "V-UNION"])
        if "V" in selected_types and is_v:
            if no_fullart and ("_FA" in name or "_FULL" in name):
                continue
            if no_v_shiny and "_SHINY" in name:
                continue
            if no_shiny_opt and "_SHINY" in name:
                continue
            if no_gold_opt and "_GOLD" in name:
                continue
            if no_alternative_opt and "_ALT" in name:
                continue

        # Détecter si c'est une carte VMAX
        is_vmax = "_VMAX" in name
        if "VMAX" in selected_types and is_vmax:
            if no_vmax_shiny and "_SHINY" in name:
                continue
            if no_shiny_opt and "_SHINY" in name:
                continue
            if no_gold_opt and "_GOLD" in name:
                continue
            # Pour VMAX, exclure Rainbow ou Alternative si demandé
            if no_rainbow_opt and "_RB" in name:
                continue
            if no_alternative_opt and "_ALT" in name:
                continue

        # Détecter si c'est une carte VSTAR
        is_vstar = "_VSTAR" in name
        if "VSTAR" in selected_types and is_vstar:
            if no_gold_opt and "_GOLD" in name:
                continue
            # Pour VSTAR, exclure Rainbow ou Alternative si demandé
            if no_rainbow_opt and "_RB" in name:
                continue
            if no_alternative_opt and "_ALT" in name:
                continue

        # Exclure cartes holo/shiny "S" (simple shiny) si demandé
        if no_holo_shiny and "/S/" in name:
            continue
        # Exclure cartes "K" (Kagayaku) si demandé
        if no_k_shiny and "/K/" in name:
            continue

        # Nouveaux filtres "Options supplémentaires"
        if no_characters and ("/CSR/" in name or "/CHR/" in name):
            continue
        if no_trainers and "TRAINERS" in name:
            continue
        if no_gold_opt and "_GOLD" in name:
            continue
        if no_shiny_opt and "_SHINY" in name:
            continue
        # Vérification exclusion de style
        if matches_style_excluded(name, selected_excluded_styles):
            continue
        # Vérification rareté
        if selected_rarities and not matches_rarity(chemin):
            continue
        # Vérification type + sous-catégorie BASE
        if selected_types and not matches_type_with_substyle(name, selected_types, selected_substyles):
            continue
        # Vérification des autres styles (Gold, Rainbow, etc.)
        if selected_styles and not matches_style_included(name, selected_styles, selected_substyles):
            continue
        résultats.append(chemin)
    return résultats

@app.route('/', methods=['GET'])
def index():
    toutes_les_cartes = lister_toutes_les_cartes()

    # Récupération des filtres depuis l'URL (case à cocher)
    selected_rarities = [r.upper() for r in request.args.getlist('rarity')]
    selected_types = [t.upper() for t in request.args.getlist('type')]
    selected_styles = [s.upper() for s in request.args.getlist('style')]
    selected_excluded_styles = [s.upper() for s in request.args.getlist('exclude_style')]

    # Sélection des ères de série
    selected_eras = [e.upper() for e in request.args.getlist('era')]
    # Sélection des codes de série
    selected_series = [s.upper() for s in request.args.getlist('series')]
    # Sélection des codes de decks
    selected_decks = [d.upper() for d in request.args.getlist('deck')]
    # Construire la liste des séries autorisées pour l’affichage de l’accordéon
    allowed_series = []
    for era in selected_eras:
        allowed_series.extend(ERA_TO_SERIES.get(era, []))

    # Options supplémentaires
    no_characters = 'no_characters' in request.args
    no_trainers = 'no_trainers' in request.args
    no_gold_opt = 'no_gold' in request.args
    no_shiny_opt = 'no_shiny' in request.args
    no_fullart = 'no_fullart' in request.args
    no_alternative_opt = 'no_alternative' in request.args
    no_rainbow_opt = 'no_rainbow' in request.args
    no_v_shiny = 'no_v_shiny' in request.args
    no_vmax_shiny = 'no_vmax_shiny' in request.args
    no_holo_shiny = 'no_holo_shiny' in request.args
    no_k_shiny = 'no_k_shiny' in request.args

    # Traitement des sous-cases "Base" pour V, VMAX et VSTAR
    selected_substyles = {}
    for t in ['V', 'VMAX', 'VSTAR']:
        key = f"sub_{t}"
        values = [v.upper() for v in request.args.getlist(key) if v]
        if values:
            selected_substyles[t] = values

    # Sous-catégorie Base pour FULL ART
    values_fa = [v.upper() for v in request.args.getlist('sub_FULL_ART') if v]
    if values_fa:
        selected_substyles["FULL ART"] = values_fa

    # Collecte des sous-styles GOLD à partir des cases à cocher sub_BASE, sub_ALTERNATIVE et sub_BLACK GOLD
    for sub in ["BASE", "ALTERNATIVE", "BLACK GOLD", "GOLD METAL", "POKEMON"]:
        key = f"sub_{sub}"
        values = [v.upper() for v in request.args.getlist(key) if v]
        if values:
            selected_substyles.setdefault("GOLD", []).extend(values)

    cartes_filtrees = filter_cards(
        toutes_les_cartes,
        selected_rarities,
        selected_types,
        selected_styles,
        selected_substyles,
        selected_excluded_styles,
        no_fullart,
        no_characters,
        no_trainers,
        no_gold_opt,
        no_shiny_opt,
        no_alternative_opt,
        no_rainbow_opt,
        no_v_shiny,
        no_vmax_shiny,
        no_holo_shiny,
        no_k_shiny,
        selected_eras,
        selected_series,
        selected_decks
    )

    def sort_key(path):
        # Exemple de path : "cards/S&S/RR/V/S7D_001_RR_V.JPEG"
        parts = path.split('/')
        # Extraire la partie filename
        filename = parts[-1]
        # Extraire numéro depuis le nom de fichier après le premier underscore
        m = re.search(r'_(\d+)', filename)
        num = int(m.group(1)) if m else 0
        # Extraire le code de série/deck avant le premier underscore dans le nom du fichier
        set_name = filename.split('_')[0].upper()

        # Série : priorité 0
        if set_name in SERIES_ORDER:
            series_idx = SERIES_ORDER.index(set_name)
            return (0, series_idx, num)

        # Deck : priorité 1
        if set_name in DECK_ORDER:
            deck_idx = DECK_ORDER.index(set_name)
            return (1, deck_idx, num)

        # Promo ou autre : priorité 2, tri uniquement par numéro
        return (2, num)

    cartes_filtrees.sort(key=sort_key)

    return render_template(
        'index.html',
        cartes=cartes_filtrees,
        rarities=["AR","CHR","CSR","A","K","S","DECK","HR","PROMO","RR","RRR","SAR","SR","SSR","UR"],
        types=["CHARACTERS RARES","ALTERNATIVES RARES","V","VMAX","VSTAR","V-UNION","EX B&W","EX_PCG","EX XY","GX","TRAINERS","ENERGY"],
        styles=["BASE","FULL ART","ALTERNATIVE","RAINBOW","ESCOUADE","SHINY","GOLD"],
        substyles={"GOLD": ["BASE","ALTERNATIVE","BLACK GOLD","GOLD METAL","POKEMON"], "FULL ART": ["BASE"]},
        selected_rarities=selected_rarities,
        selected_types=selected_types,
        selected_styles=selected_styles,
        selected_substyles=selected_substyles,
        eras=list(ERA_TO_SERIES.keys()),
        series=SERIES_ORDER,
        decks=DECK_ORDER,
        selected_eras=selected_eras,
        selected_series=selected_series,
        selected_decks=selected_decks,
        allowed_series=allowed_series
    )

if __name__ == '__main__':
    app.run(debug=True)