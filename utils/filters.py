import os
import re

def filter_cards(cartes, selected_rarities, selected_types, selected_styles, selected_substyles, selected_excluded_styles,
                 no_fullart=False, no_characters=False, no_trainers=False, no_gold_opt=False, no_shiny_opt=False,
                 no_alternative_opt=False, no_rainbow_opt=False,
                 no_holo_shiny=False, no_k_shiny=False, no_mega_primo=False,
                 opt_fullart=False, opt_megaprimo=False, opt_bordergold=False, opt_gold=False,
                 opt_alternative=False, opt_alternative_gold=False, opt_blackgold=False, opt_characters=False,
                 opt_metal=False, opt_rainbow=False, opt_shiny=False, opt_trainers=False,
                 opt_tagteam=False, no_tagteam=False,
                 metal=False, no_metal=False, no_border_gold=False, no_blackgold=False, no_gold_metal=False,
                 plasma=False, no_plasma=False,
                 selected_eras=None, selected_series=None, selected_decks=None):
    from constants.eras import ERA_TO_FOLDER
    # Filtrage Era
    filtered_era = []
    for chemin in cartes:
        path_upper = chemin.upper()
        if selected_eras:
            match_era = False
            for era in selected_eras:
                folder = ERA_TO_FOLDER.get(era, era).upper()
                if f"/CARDS/{folder}/" in f"/{path_upper}":
                    match_era = True
                    break
            if not match_era:
                continue
        filtered_era.append(chemin)
    cartes = filtered_era
    # Filtrage Series/Decks (le code doit être le préfixe du nom de fichier)
    if selected_series or selected_decks:
        filtered_sd = []
        for chemin in cartes:
            filename = os.path.basename(chemin).upper()
            code = filename.split('_')[0]
            match_series = code in (selected_series or [])
            match_deck = code in (selected_decks or [])
            if match_series or match_deck:
                filtered_sd.append(chemin)
        cartes = filtered_sd

    def matches_rarity(path):
        if not selected_rarities:
            return True
        name = os.path.basename(path).upper()
        for rar in selected_rarities:
            if rar == "A":
                if "_A.JPEG" in name:
                    return True
            elif rar == "AR":
                if "_AR.JPEG" in name:
                    return True
            elif rar == "CHR":
                if "_CHR" in name:
                    return True
            elif rar == "CSR":
                if "_CSR" in name:
                    return True
            elif rar == "DECK":
                if "_DECK" in name:
                    return True
            elif rar == "HR":
                if "_HR" in name:
                    return True
            elif rar == "K":
                if "_K_" in name:
                    return True
            elif rar == "NORARITY":
                if "_NORARITY" in name:
                    return True
            elif rar == "PRISM STAR":
                if "_PR.JPEG" in name:
                    return True
            elif rar == "PROMO":
                if "_PROMO_" in name:
                    return True
            elif rar == "RR":
                if "_RR_" in name:
                    return True
            elif rar == "RRR":
                if "_RRR_" in name:
                    return True
            elif rar == "S":
                if "_S_" in name:
                    return True
            elif rar == "SAR":
                if "_SAR" in name:
                    return True
            elif rar == "SECRET":
                if "_SECRET" in name:
                    return True
            elif rar == "SR":
                if "_SR" in name:
                    return True
            elif rar == "SSR":
                if "_SSR" in name:
                    return True
            elif rar == "UR":
                if "_UR" in name:
                    return True
        return False

    def matches_type(path):
        if not selected_types:
            return True
        name = os.path.basename(path).upper()
        for t in selected_types:
            if t == "EX":
                if "_EX" in name:
                    return True
            elif t == "SHINING":
                if "_SHINING" in name:
                    return True
            elif t == "BREAK":
                if "_BREAK" in name:
                    return True
            elif t == "V":
                if "_V_" in name or "_V.JPEG" in name:
                    return True
            elif t == "VMAX":
                if "_VMAX" in name:
                    return True
            elif t == "VSTAR":
                if "_VSTAR" in name:
                    return True
            elif t == "V-UNION":
                if "_V-UNION" in name:
                    return True
            elif t == "GX":
                if "_GX" in name:
                    return True
            elif t == "TRAINERS":
                if "_TRAINERS" in name:
                    return True
            elif t == "ENERGY":
                if "_ENERGY" in name:
                    return True
            elif t == "PRIME":
                if "PRIME" in name:
                    return True
            elif t == "LEGEND":
                if "LEGEND" in name:
                    return True
        return False

    def matches_style(path):
        if not selected_styles:
            return True
        name = os.path.basename(path).upper()
        for style in selected_styles:
            if style == "ALTERNATIVE":
                if "_ALT" not in name:
                    return False
            elif style == "ARSTYLE":
                if "_ARSTYLE" not in name:
                    return False
            elif style == "BORDER GOLD":
                if "_BG" not in name:
                    return False
            elif style == "CHARACTERS RARES":
                if not ("_CHARACTER" in name or "_CSR" in name or "_CHR" in name):
                    return False
            elif style == "FULL ART":
                # Doit contenir _FA_ ou _FA. (et pas juste FA dans un mot)
                if not ("_FA_" in name or "_FA." in name):
                    return False
            elif style == "GOLD":
                # Doit contenir _GOLD_ ou _GOLD. (et pas juste GOLD dans un mot)
                if not ("_GOLD_" in name or "_GOLD." in name):
                    return False
            elif style == "MEGA-PRIMO":
                if "_MEGA-PRIMO" not in name:
                    return False
            elif style == "RAINBOW":
                if "_RB" not in name:
                    return False
            elif style == "SHINY":
                if "_SHINY" not in name:
                    return False
            elif style == "LEGENDARY":
                if "LGDRY" not in name:
                    return False
        return True

    def matches_excluded_style(path):
        if not selected_excluded_styles:
            return True
        name = os.path.basename(path).upper()
        for style in selected_excluded_styles:
            if style == "ALTERNATIVE":
                if "_ALT" in name:
                    return False
            elif style == "ARSTYLE":
                if "_ARSTYLE" in name:
                    return False
            elif style == "BORDER GOLD":
                if "_BG" in name:
                    return False
            elif style == "CHARACTERS RARES":
                if ("_CHARACTER" in name or "_CSR" in name or "_CHR" in name):
                    return False
            elif style == "FULL ART":
                if "_FA" in name:
                    return False
            elif style == "GOLD":
                if "_A.JPEG" in name:
                    return False
            elif style == "MEGA-PRIMO":
                if "_MEGA-PRIMO" in name:
                    return False
            elif style == "RAINBOW":
                if "_RB" in name:
                    return False
            elif style == "SHINY":
                if "_SHINY" in name:
                    return False
        return True

    def matches_options(path):
        name = os.path.basename(path).upper()
        # Filtres négatifs
        if no_fullart and ("_FA_" in name or "_FA." in name):
            return False
        if no_characters and ("_CHARACTER" in name or "_CSR" in name or "_CHR" in name):
            return False
        if no_trainers and ("_TRAINERS" in name):
            return False
        if no_gold_opt and ("_GOLD_" in name or "_GOLD." in name):
            return False
        if no_shiny_opt and ("_SHINY" in name):
            return False
        if no_alternative_opt and ("_ALT" in name):
            return False
        if no_rainbow_opt and ("_RB" in name):
            return False
        if no_mega_primo and ("_MEGA-PRIMO" in name):
            return False
        if no_border_gold and ("_BG" in name):
            return False
        if no_blackgold and ("_BLACK_GOLD" in name):
            return False
        if no_gold_metal and ("_GOLD_METAL" in name):
            return False
        if no_tagteam and ("_TAGTEAM" in name):
            return False
        if no_metal and ("_METAL" in name):
            return False
        if no_plasma and ("_PLASMA" in name):
            return False
        # Filtres positifs
        if opt_fullart and not ("_FA_" in name or "_FA." in name):
            return False
        if opt_megaprimo and not ("_MEGA-PRIMO" in name):
            return False
        if opt_bordergold and not ("_BG" in name):
            return False
        if opt_gold and not ("_GOLD_" in name or "_GOLD." in name):
            return False
        if opt_alternative and not ("_ALT" in name):
            return False
        if opt_alternative_gold and not ("_ALT" in name and "_GOLD" in name):
            return False
        if opt_blackgold and not ("_BLACK_GOLD" in name):
            return False
        if opt_characters and not ("_CHARACTER" in name or "_CSR" in name or "_CHR" in name):
            return False
        if opt_metal and not ("_METAL" in name):
            return False
        if opt_rainbow and not ("_RB" in name):
            return False
        if opt_shiny and not ("_SHINY" in name):
            return False
        if opt_trainers and not ("_TRAINERS" in name):
            return False
        if opt_tagteam and not ("_TAGTEAM" in name):
            return False
        if metal and not ("_METAL" in name):
            return False
        if plasma and not ("_PLASMA" in name):
            return False
        return True

    filtered = []
    for path in cartes:
        if not matches_rarity(path):
            continue
        if not matches_type(path):
            continue
        if not matches_style(path):
            continue
        if not matches_excluded_style(path):
            continue
        if not matches_options(path):
            continue
        filtered.append(path)
    return filtered
