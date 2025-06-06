from flask import Flask, render_template, request, url_for
import os
import re
import math

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

# Ordre de sortie des SÉRIES pour l'ère XY
XY_SERIES_ORDER = [
    "XY1B", "XY1R", "XY2", "XY3", "XY4", "XY5G", "XY5Y", "CP1", "XY6", "XY7", "CP2",
    "XY8B", "XY8R", "XY9", "CP3", "20TH", "XY10", "CP4", "XY11B", "XY11P", "CP5", "CP6",
    "HXY", "Y30", "X30", "XYA", "XYB", "XYC", "XYD", "XYE", "MMBP", "MMBS", "SNPN", "SNPR",
    "XYF", "XYG", "XYH"
]

# Ordre de sortie des DECKS pour l'ère XY
XY_DECK_ORDER = [
    "HXY", "Y30", "X30", "XYA", "XYB", "XYC", "XYD", "XYE",
    "MMBP", "MMBS", "SNPN", "SNPR", "XYF", "XYG", "XYH"
]

# Regroupement des séries par ères (inclut codes de séries, decks et promos)
ERA_TO_SERIES = {
    "XY": XY_SERIES_ORDER,
    "SWORD_AND_SHIELD": SERIES_ORDER + DECK_ORDER,
    # d'autres ères peuvent suivre…
}

# Correspondance entre clé d'ère et nom de dossier
ERA_TO_FOLDER = {
    "XY": "XY",
    "SWORD_AND_SHIELD": "S&S",
    # ...
}


# Ordre de sortie des RARETÉS (en majuscule)
RARITY_ORDER = ["AR", "CHR", "CSR", "A", "K", "S", "DECK", "HR", "PROMO", "RR", "RRR", "SAR", "SR", "SSR", "UR", "NORARITY"]

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
                 no_alternative_opt=False, no_rainbow_opt=False,
                 no_holo_shiny=False, no_k_shiny=False, no_mega_primo=False,
                 opt_fullart=False, opt_megaprimo=False, opt_bordergold=False, opt_gold=False,
                 opt_alternative=False, opt_alternative_gold=False, opt_blackgold=False, opt_characters=False,
                 opt_metal=False, opt_rainbow=False, opt_shiny=False, opt_trainers=False,
                 metal=False, no_metal=False, no_border_gold=False, no_blackgold=False, no_gold_metal=False,
                 selected_eras=None, selected_series=None, selected_decks=None):
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
            elif t == "ARSTYLE":
                if "/AR/" in name or "/ARSTYLE/" in name:
                    return True
            elif t == "V-UNION":
                if "V-UNION" in name:
                    return True
            elif t == "TURBO":
                if "_TURBO" in name:
                    return True
            elif t == "EX":
                # Cartes EX : contiennent "_EX" (par ex. EX_FA, EX_MEGA, EX_XY, etc.)
                if "_EX" in name:
                    return True
            elif t == "SEMI AR":
                if "_SEMI_AR" in name:
                    return True
            # REMOVED SECRET from here: now handled as style
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
        # Pour chaque style demandé, la carte doit correspondre à ce style (AND)
        for style in styles:
            if style == "FULL ART":
                if not ("_FA" in name or "_FULL" in name):
                    return False
            elif style == "ALTERNATIVE":
                if "_ALT" not in name:
                    return False
            elif style == "RAINBOW":
                if not ("_RB" in name and any(x in name for x in ["_V", "_VMAX", "_VSTAR", "TRAINERS"])):
                    return False
            elif style == "ESCOUADE":
                if not ("_TAG_TEAM" in name and "GX" in name):
                    return False
            elif style == "SHINY":
                if not ("_SHINY" in name):
                    return False
            elif style == "GOLD":
                subs = substyles.get("GOLD", [])
                if "GOLD METAL" in subs:
                    if not ("_GOLD_METAL" in name):
                        return False
                if "POKEMON" in subs:
                    if not ("_GOLD" in name and not any(x in name for x in ["TRAINERS", "ENERGY"])):
                        return False
                if subs:
                    if "BASE" in subs:
                        if not ("_GOLD" in name and not any(x in name for x in ["_BLACK", "_ALT", "_SHINY", "_RB", "_TAG_TEAM", "_GOLD_METAL"])):
                            return False
                    if "ALTERNATIVE" in subs:
                        if not ("_GOLD" in name and "_ALT" in name):
                            return False
                    if "BLACK GOLD" in subs:
                        if not ("_BLACK_GOLD" in name or "_GOLD_BLACK" in name):
                            return False
                else:
                    # GOLD simple (exclut BORDER GOLD)
                    if not ("_GOLD" in name and "_BORDER_GOLD" not in name):
                        return False
            elif style == "BORDER GOLD":
                if not ("_BORDER_GOLD" in name):
                    return False
            elif style == "MEGA-PRIMO":
                if not ("_MEGA-PRIMO" in name):
                    return False
            # Si le style ne correspond à aucun cas, on le considère comme non-matching
        # Si on est arrivé ici, la carte a satisfait tous les styles demandés
        return True

    def matches_style_or(name, styles, substyles):
        # Si aucun style sélectionné, on accepte tout
        if not styles:
            return True
        # Retourne True si la carte correspond à au moins un des styles
        for style in styles:
            if style == "FULL ART":
                if "_FA" in name or "_FULL" in name:
                    return True
            elif style == "ALTERNATIVE":
                if "_ALT" in name:
                    return True
            elif style == "RAINBOW":
                if "_RB" in name and any(x in name for x in ["_V", "_VMAX", "_VSTAR", "TRAINERS"]):
                    return True
            elif style == "ESCOUADE":
                if "_TAG_TEAM" in name and "GX" in name:
                    return True
            elif style == "SHINY":
                if "_SHINY" in name:
                    return True
            elif style == "GOLD":
                subs = substyles.get("GOLD", [])
                if "GOLD METAL" in subs and "_GOLD_METAL" in name:
                    return True
                if "POKEMON" in subs and ("_GOLD" in name and not any(x in name for x in ["TRAINERS", "ENERGY"])):
                    return True
                if subs:
                    if "BASE" in subs and ("_GOLD" in name and not any(x in name for x in ["_BLACK", "_ALT", "_SHINY", "_RB", "_TAG_TEAM", "_GOLD_METAL"])):
                        return True
                    if "ALTERNATIVE" in subs and ("_GOLD" in name and "_ALT" in name):
                        return True
                    if "BLACK GOLD" in subs and ("_BLACK_GOLD" in name or "_GOLD_BLACK" in name):
                        return True
                # GOLD simple (exclut BORDER GOLD)
                elif "_GOLD" in name and "_BORDER_GOLD" not in name:
                    return True
            elif style == "BORDER GOLD":
                if "_BORDER_GOLD" in name:
                    return True
            elif style == "MEGA-PRIMO":
                if "_MEGA-PRIMO" in name:
                    return True
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
            if style == "BORDER GOLD" and "_BORDER_GOLD" in name:
                return True
            if style == "MEGA-PRIMO" and "_MEGA-PRIMO" in name:
                return True
        return False

    résultats = []
    for chemin in cartes:
        name = os.path.basename(chemin).upper()
        path_upper = chemin.upper()

        # Filtrer Metal / No Metal
        if metal and "_METAL" not in name:
            continue
        if no_metal and "_METAL" in name:
            continue
        # Contraintes POSITIVES pour Full Art / Mega-Primo / Border Gold / Gold et toutes les options supplémentaires
        if opt_fullart and not ("_FA" in name or "_FULL" in name):
            continue
        if opt_megaprimo and "_MEGA-PRIMO" not in name:
            continue
        if opt_bordergold and "_BORDER_GOLD" not in name:
            continue
        # Cas "opt_gold" : inclure tous les GOLD sauf BORDER GOLD
        if opt_gold and ("_GOLD" not in name or "_BORDER_GOLD" in name):
            continue
        if opt_alternative and "_ALT" not in name:
            continue
        if opt_alternative_gold and not ("_ALT" in name and "_GOLD" in name):
            continue
        if opt_blackgold and not ("_BLACK_GOLD" in name or "_GOLD_BLACK" in name):
            continue
        if opt_characters and not ("/CSR/" in path_upper or "/CHR/" in path_upper):
            continue
        if opt_metal and "_METAL" not in name:
            continue
        if opt_rainbow and not ("_RB" in name and any(x in name for x in ["_V","_VMAX","_VSTAR","TRAINERS"])):
            continue
        if opt_shiny and "_SHINY" not in name:
            continue
        if opt_trainers and "TRAINERS" not in name:
            continue
        # Options supplémentaires d’EXCLUSION
        if no_fullart and "_FA" in name:
            continue
        if no_mega_primo and "_MEGA-PRIMO" in name:
            continue
        if no_border_gold and "_BORDER_GOLD" in name:
            continue
        if no_alternative_opt and "_ALT" in name:
            continue
        if no_blackgold and ("_BLACK_GOLD" in name or "_GOLD_BLACK" in name):
            continue
        if no_gold_metal and "_GOLD_METAL" in name:
            continue

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
            # if no_fullart and ("_FA" in name or "_FULL" in name):
            #     continue
            if no_shiny_opt and "_SHINY" in name:
                continue
            if no_gold_opt and "_GOLD" in name:
                continue
            # if no_alternative_opt and "_ALT" in name:
            #     continue

        # Détecter si c'est une carte VMAX
        is_vmax = "_VMAX" in name
        if "VMAX" in selected_types and is_vmax:
            if no_shiny_opt and "_SHINY" in name:
                continue
            if no_gold_opt and "_GOLD" in name:
                continue
            # Pour VMAX, exclure Rainbow ou Alternative si demandé
            if no_rainbow_opt and "_RB" in name:
                continue
            # if no_alternative_opt and "_ALT" in name:
            #     continue

        # Détecter si c'est une carte VSTAR
        is_vstar = "_VSTAR" in name
        if "VSTAR" in selected_types and is_vstar:
            if no_gold_opt and "_GOLD" in name:
                continue
            # Pour VSTAR, exclure Rainbow ou Alternative si demandé
            if no_rainbow_opt and "_RB" in name:
                continue
            # if no_alternative_opt and "_ALT" in name:
            #     continue

        # Exclure cartes holo/shiny "S" (simple shiny) si demandé
        if no_holo_shiny and "/S/" in name:
            continue
        # Exclure cartes "K" (Kagayaku) si demandé
        if no_k_shiny and "/K/" in name:
            continue
        # Exclure cartes "MEGA-PRIMO" si demandé
        if no_mega_primo and "_MEGA-PRIMO" in name:
            continue
        # Exclure cartes "BORDER GOLD" si demandé
        if no_border_gold and "_BORDER_GOLD" in name:
            continue

        # Nouveaux filtres "Options supplémentaires"
        if no_characters and ("/CSR/" in name or "/CHR/" in name):
            continue
        if no_trainers and "TRAINERS" in name:
            continue
        # Cas "no_gold_opt" : exclure tous les GOLD sauf BORDER GOLD
        if no_gold_opt and "_GOLD" in name and "_BORDER_GOLD" not in name:
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
        # Contraintes POSITIVES pour Full Art / Mega-Primo / Border Gold (AND)
        if opt_fullart and not ("_FA" in name or "_FULL" in name):
            continue
        if opt_megaprimo and "_MEGA-PRIMO" not in name:
            continue
        if opt_bordergold and "_BORDER_GOLD" not in name:
            continue
        # Options supplémentaires d’EXCLUSION
        if no_fullart and "_FA" in name:
            continue
        if no_mega_primo and "_MEGA-PRIMO" in name:
            continue
        if no_border_gold and "_BORDER_GOLD" in name:
            continue
        if no_alternative_opt and "_ALT" in name:
            continue
        # Ensuite, après toutes ces contraintes, on applique le filtre OR sur selected_styles
        if selected_styles and not matches_style_or(name, selected_styles, selected_substyles):
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

    # Construire une liste temporaire de cartes correspondant uniquement à l'ère/série/deck sélectionnés
    context_cards = []
    for chemin in toutes_les_cartes:
        path_upper = chemin.upper()
        # Si des séries ou decks sont cochés, respecter ces sélections
        if selected_series or selected_decks:
            match_series = any(path_upper.startswith(f"CARDS/{ERA_TO_FOLDER.get(era, era).upper()}/{ser}/") for ser in selected_series for era in selected_eras) if selected_series else False
            match_deck = any(path_upper.startswith(f"CARDS/{ERA_TO_FOLDER.get(era, era).upper()}/{deck}/") for deck in selected_decks for era in selected_eras) if selected_decks else False
            if not (match_series or match_deck):
                continue
        # Filtrer par ère si spécifié
        if selected_eras:
            if not any(f"/{ERA_TO_FOLDER.get(era, era).upper()}/" in path_upper for era in selected_eras):
                continue
        context_cards.append(chemin)

    # Déterminer les filtres disponibles dans le contexte actuel
    # Types disponibles
    all_types = ["CHARACTERS RARES","ARSTYLE","EX","TURBO","SEMI AR","V","VMAX","VSTAR","V-UNION","EX B&W","EX_PCG","EX XY","GX","TRAINERS","ENERGY"]
    available_types = []
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
            elif t == "ARSTYLE":
                if "/AR/" in name or "/ARSTYLE/" in name:
                    return True
            elif t == "V-UNION":
                if "V-UNION" in name:
                    return True
            elif t == "TURBO":
                if "_TURBO" in name:
                    return True
            elif t == "EX":
                # Cartes EX : contiennent "_EX" (par ex. EX_FA, EX_MEGA, EX_XY, etc.)
                if "_EX" in name:
                    return True
            elif t == "SEMI AR":
                if "_SEMI_AR" in name:
                    return True
            # REMOVED SECRET from here: now handled as style
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
    for t in all_types:
        for chemin in context_cards:
            name = os.path.basename(chemin).upper()
            if matches_type_with_substyle(name, [t], {}):
                available_types.append(t)
                break
    # Styles disponibles
    all_styles = ["BASE","FULL ART","ALTERNATIVE","RAINBOW","ESCOUADE","SHINY","GOLD","BORDER GOLD","MEGA-PRIMO"]
    available_styles = []
    def matches_style_included(name, styles, substyles):
        # Si aucun style sélectionné, on accepte tout
        if not styles:
            return True

        # Pour chaque style demandé, la carte doit correspondre à ce style (AND)
        for style in styles:
            if style == "FULL ART":
                if not ("_FA" in name or "_FULL" in name):
                    return False

            elif style == "ALTERNATIVE":
                if not ("_ALT" in name and any(x in name for x in ["_V", "_VMAX", "_VSTAR", "TRAINERS"])):
                    return False

            elif style == "RAINBOW":
                if not ("_RB" in name and any(x in name for x in ["_V", "_VMAX", "_VSTAR", "TRAINERS"])):
                    return False

            elif style == "ESCOUADE":
                if not ("_TAG_TEAM" in name and "GX" in name):
                    return False

            elif style == "SHINY":
                if not ("_SHINY" in name):
                    return False

            elif style == "GOLD":
                subs = substyles.get("GOLD", [])
                # Gold Metal
                if "GOLD METAL" in subs:
                    if not ("_GOLD_METAL" in name):
                        return False
                # Pokémon sans Trainer/Energy
                if "POKEMON" in subs:
                    if not ("_GOLD" in name and not any(x in name for x in ["TRAINERS", "ENERGY"])):
                        return False
                if subs:
                    if "BASE" in subs:
                        if not ("_GOLD" in name and not any(x in name for x in ["_BLACK", "_ALT", "_SHINY", "_RB", "_TAG_TEAM", "_GOLD_METAL"])):
                            return False
                    if "ALTERNATIVE" in subs:
                        if not ("_GOLD" in name and "_ALT" in name):
                            return False
                    if "BLACK GOLD" in subs:
                        if not ("_BLACK_GOLD" in name or "_GOLD_BLACK" in name):
                            return False
                else:
                    if not ("_GOLD" in name):
                        return False

            elif style == "BORDER GOLD":
                if not ("_BORDER_GOLD" in name):
                    return False

            elif style == "MEGA-PRIMO":
                if not ("_MEGA-PRIMO" in name):
                    return False

            # Si le style ne correspond à aucun cas, on le considère comme non-matching

        # Si on est arrivé ici, la carte a satisfait tous les styles demandés
        return True
    for s in all_styles:
        for chemin in context_cards:
            name = os.path.basename(chemin).upper()
            if matches_style_included(name, [s], {"GOLD": ["BASE","ALTERNATIVE","BLACK GOLD","GOLD METAL","POKEMON"], "FULL ART": ["BASE"]}):
                available_styles.append(s)
                break
    # Options supplémentaires disponibles (exemple: fullart, mega-primo, secret, alternative)
    available_extras = {
        'no_fullart': any("_FA" in os.path.basename(c).upper() for c in context_cards),
        'no_mega_primo': any("_MEGA-PRIMO" in os.path.basename(c).upper() for c in context_cards),
        'no_border_gold': any("_BORDER_GOLD" in os.path.basename(c).upper() for c in context_cards),
        'no_alternative': any("_ALT" in os.path.basename(c).upper() for c in context_cards)
    }

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
    no_mega_primo = 'no_mega_primo' in request.args
    no_border_gold = 'no_border_gold' in request.args
    metal = 'metal' in request.args
    no_metal = 'no_metal' in request.args
    bordergold = 'bordergold' in request.args
    no_blackgold = 'no_blackgold' in request.args
    no_gold_metal = 'no_gold_metal' in request.args
    opt_fullart = 'opt_fullart' in request.args
    opt_megaprimo = 'opt_megaprimo' in request.args
    opt_bordergold = 'opt_bordergold' in request.args
    opt_gold = 'opt_gold' in request.args
    opt_alternative = 'opt_alternative' in request.args
    opt_alternative_gold = 'opt_alternative_gold' in request.args
    opt_blackgold = 'opt_blackgold' in request.args
    opt_characters = 'opt_characters' in request.args
    opt_metal = 'opt_metal' in request.args
    opt_rainbow = 'opt_rainbow' in request.args
    opt_shiny = 'opt_shiny' in request.args
    opt_trainers = 'opt_trainers' in request.args

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
        no_holo_shiny,
        no_k_shiny,
        no_mega_primo,
        opt_fullart,
        opt_megaprimo,
        opt_bordergold,
        opt_gold,
        opt_alternative,
        opt_alternative_gold,
        opt_blackgold,
        opt_characters,
        opt_metal,
        opt_rainbow,
        opt_shiny,
        opt_trainers,
        metal,
        no_metal,
        no_border_gold,
        no_blackgold,
        no_gold_metal,
        selected_eras,
        selected_series,
        selected_decks
    )


    # Construction dynamique des listes 'series' et 'decks' en fonction des ères choisies
    if not selected_eras:
        # Si aucune ère sélectionnée, inclure toutes les séries/decks de chaque ère
        series_list = []
        deck_list = []
        # Pour chaque ère disponible, ajouter son ordre de séries et deck
        for era_key in ERA_TO_SERIES:
            if era_key == "XY":
                series_list.extend(XY_SERIES_ORDER)
                deck_list.extend(XY_DECK_ORDER)
            elif era_key == "SWORD_AND_SHIELD":
                series_list.extend(SERIES_ORDER)
                deck_list.extend(DECK_ORDER)
            # Si d'autres ères sont ajoutées ultérieurement, répéter ce schéma
    else:
        # Si une ou plusieurs ères cochées, combiner les listes pour chaque ère sélectionnée
        series_list = []
        deck_list = []
        for era in selected_eras:
            if era == "XY":
                series_list.extend(XY_SERIES_ORDER)
                deck_list.extend(XY_DECK_ORDER)
            elif era == "SWORD_AND_SHIELD":
                series_list.extend(SERIES_ORDER)
                deck_list.extend(DECK_ORDER)
            # Ajouter ici d'autres conditions si vous intégrez de nouvelles ères
    
    # Éviter les doublons au cas où une ère serait listée plusieurs fois
    # (optionnel, selon usage)
    # series_list = list(dict.fromkeys(series_list))
    # deck_list = list(dict.fromkeys(deck_list))

    # Trier les cartes : d'abord séries dynamiques, puis decks dynamiques, puis promos
    def sort_key_dynamic(path):
        name = os.path.basename(path).upper()
        parts = name.split('_')
        if len(parts) < 2:
            return (3, 0, 0)
        code = parts[0]  # ex. 'S1H', 'SF', 'XYP', etc.
        try:
            num = int(parts[1])
        except:
            num = 0
        # Série (priorité 0)
        if code in series_list:
            return (0, series_list.index(code), num)
        # Deck (priorité 1)
        if code in deck_list:
            return (1, deck_list.index(code), num)
        # Promo ou autres (priorité 2)
        if 'PROMO' in name or code == 'SPP':
            return (2, num, 0)
        # Tout le reste (priorité 3)
        return (3, 0, 0)

    cartes_filtrees.sort(key=sort_key_dynamic)

    # Pagination : decouper cartes_filtrees en pages de 150
    page = request.args.get('page', 1)
    try:
        current_page = int(page)
    except ValueError:
        current_page = 1
    if current_page < 1:
        current_page = 1
    total_cards = len(cartes_filtrees)
    total_pages = math.ceil(total_cards / 150) if total_cards > 0 else 1
    if current_page > total_pages:
        current_page = total_pages
    start_idx = (current_page - 1) * 150
    end_idx = start_idx + 150
    page_cards = cartes_filtrees[start_idx:end_idx]

    # Indicateurs pour la section Options Supplémentaires
    show_no_bordergold_for_megaprimo = "MEGA-PRIMO" in selected_styles
    show_fullart_for_bordergold = "BORDER GOLD" in selected_styles

    return render_template(
        'index.html',
        cartes=page_cards,
        rarities=["AR","CHR","CSR","A","K","S","DECK","HR","PROMO","RR","RRR","SAR","SR","SSR","UR","NORARITY"],
        types=["CHARACTERS RARES","ARSTYLE","EX","TURBO","SEMI AR","V","VMAX","VSTAR","V-UNION",
               "EX B&W","EX_PCG","EX XY","GX","TRAINERS","ENERGY"],
        styles=["BASE","FULL ART","ALTERNATIVE","RAINBOW","ESCOUADE","SHINY","GOLD","BORDER GOLD","MEGA-PRIMO"],
        substyles={"GOLD": ["BASE","ALTERNATIVE","BLACK GOLD","GOLD METAL","POKEMON"], "FULL ART": ["BASE"]},
        available_types=available_types,
        available_styles=available_styles,
        available_extras=available_extras,
        selected_rarities=selected_rarities,
        selected_types=selected_types,
        selected_styles=selected_styles,
        selected_substyles=selected_substyles,
        eras=list(ERA_TO_SERIES.keys()),
        series=series_list,
        decks=deck_list,
        selected_eras=selected_eras,
        selected_series=selected_series,
        selected_decks=selected_decks,
        allowed_series=allowed_series,
        show_no_bordergold_for_megaprimo=show_no_bordergold_for_megaprimo,
        show_fullart_for_bordergold=show_fullart_for_bordergold,
        total_cards=total_cards,
        current_page=current_page,
        total_pages=total_pages
    )

if __name__ == '__main__':
    app.run(debug=True)