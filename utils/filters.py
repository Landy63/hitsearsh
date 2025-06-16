import os
import re

def filter_cards(cartes, selected_rarities, selected_types, selected_styles, selected_excluded_styles,
                 substyle_lvx_sp=False, substyle_no_lvx_sp=False, substyle_blackstar=False, substyle_no_blackstar=False,
                 substyle_delta=False, substyle_no_delta=False, substyle_rocket=False, substyle_no_rocket=False,
                 substyle_ex_holo=False, substyle_no_ex_holo=False,
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
            # Cas spécial pour PRISM STAR qui est codé comme PR dans les fichiers
            if rar == "PRISM STAR":
                if "_PR_" in name or "_PR." in name:
                    return True
            else:
                # Vérification précise pour chaque rareté : _RARITY. ou _RARITY_
                if f"_{rar}_" in name or f"_{rar}." in name:
                    return True
        return False

    def matches_type(path):
        if not selected_types:
            return True
        name = os.path.basename(path).upper()
        for t in selected_types:
            if t == "EX":
                if "_EX_" in name or "_EX." in name:
                    return True
            elif t == "SHINING":
                if "_SHINING_" in name or "_SHINING." in name:
                    return True
            elif t == "BREAK":
                if "_BREAK_" in name or "_BREAK." in name:
                    return True
            elif t == "V":
                if "_V_" in name or "_V." in name:
                    return True
            elif t == "VMAX":
                if "_VMAX_" in name or "_VMAX." in name:
                    return True
            elif t == "VSTAR":
                if "_VSTAR_" in name or "_VSTAR." in name:
                    return True
            elif t == "V-UNION":
                if "_V-UNION_" in name or "_V-UNION." in name:
                    return True
            elif t == "GX":
                if "_GX_" in name or "_GX." in name:
                    return True
            elif t == "TRAINERS":
                if "_TRAINERS_" in name or "_TRAINERS." in name:
                    return True
            elif t == "ENERGY":
                if "_ENERGY_" in name or "_ENERGY." in name:
                    return True
            elif t == "PRIME":
                if "_PRIME_" in name or "_PRIME." in name:
                    return True
            elif t == "LEGEND":
                if "_LEGEND_" in name or "_LEGEND." in name:
                    return True
            elif t == "BLACKSTAR":
                if "_BLACKSTAR_" in name or "_BLACKSTAR." in name:
                    return True
            elif t == "LV.X":
                if "_LV.X_" in name or "_LV.X." in name:
                    return True
                    return True
            elif t == "GOLDSTAR":
                if "_GOLDSTAR_" in name or "_GOLDSTAR." in name:
                    return True
        return False

    def matches_style(path):
        if not selected_styles:
            return True
        name = os.path.basename(path).upper()
        for style in selected_styles:
            if style == "ALTERNATIVE":
                if "_ALT_" in name or "_ALT." in name:
                    return True
            elif style == "ARSTYLE":
                if "_ARSTYLE_" in name or "_ARSTYLE." in name:
                    return True
            elif style == "BORDER GOLD":
                if "_BG_" in name or "_BG." in name:
                    return True
            elif style == "CHARACTERS RARES":
                if ("_CHARACTER_" in name or "_CHARACTER." in name or 
                    "_CSR_" in name or "_CSR." in name or 
                    "_CHR_" in name or "_CHR." in name):
                    return True
            elif style == "FULL ART":
                if "_FA_" in name or "_FA." in name:
                    return True
            elif style == "GOLD":
                if "_GOLD_" in name or "_GOLD." in name:
                    return True
            elif style == "MEGA-PRIMO":
                if "_MEGA-PRIMO_" in name or "_MEGA-PRIMO." in name:
                    return True
            elif style == "RAINBOW":
                if "_RB_" in name or "_RB." in name:
                    return True
            elif style == "SHINY":
                if "_SHINY_" in name or "_SHINY." in name:
                    return True
            elif style == "LEGENDARY":
                if "_LGDRY_" in name or "_LGDRY." in name:
                    return True
            elif style == "DELTA SPECIES":
                if "_DELTA_" in name or "_DELTA." in name:
                    return True
        return False

    def matches_excluded_style(path):
        if not selected_excluded_styles:
            return True
        name = os.path.basename(path).upper()
        for style in selected_excluded_styles:
            if style == "ALTERNATIVE":
                if "_ALT_" in name or "_ALT." in name:
                    return False
            elif style == "ARSTYLE":
                if "_ARSTYLE_" in name or "_ARSTYLE." in name:
                    return False
            elif style == "BORDER GOLD":
                if "_BG_" in name or "_BG." in name:
                    return False
            elif style == "CHARACTERS RARES":
                if ("_CHARACTER_" in name or "_CHARACTER." in name or 
                    "_CSR_" in name or "_CSR." in name or 
                    "_CHR_" in name or "_CHR." in name):
                    return False
            elif style == "FULL ART":
                if "_FA_" in name or "_FA." in name:
                    return False
            elif style == "GOLD":
                if "_GOLD_" in name or "_GOLD." in name:
                    return False
            elif style == "MEGA-PRIMO":
                if "_MEGA-PRIMO_" in name or "_MEGA-PRIMO." in name:
                    return False
            elif style == "RAINBOW":
                if "_RB_" in name or "_RB." in name:
                    return False
            elif style == "SHINY":
                if "_SHINY_" in name or "_SHINY." in name:
                    return False
            elif style == "LEGENDARY":
                if "_LGDRY_" in name or "_LGDRY." in name:
                    return False
            elif style == "DELTA SPECIES":
                if "_DELTA_" in name or "_DELTA." in name:
                    return False
        return True

    def matches_options(path):
        name = os.path.basename(path).upper()
        
        # Filtres positifs pour les nouveaux substyles
        if substyle_delta and not ("_DELTA_" in name or "_DELTA." in name):
            return False
        if substyle_rocket and not ("_ROCKET_" in name or "_ROCKET." in name):
            return False
        if substyle_ex_holo and not ("_EX_HOLO_" in name or "_EX_HOLO." in name):
            return False
        if substyle_blackstar and not ("_BLACKSTAR_" in name or "_BLACKSTAR." in name):
            return False
        if substyle_lvx_sp and not ("_LV.X_SP_" in name or "_LV.X_SP." in name):
            return False
        
        # Filtres négatifs pour les nouveaux substyles
        if substyle_no_delta and ("_DELTA_" in name or "_DELTA." in name):
            return False
        if substyle_no_rocket and ("_ROCKET_" in name or "_ROCKET." in name):
            return False
        if substyle_no_ex_holo and ("_EX_HOLO_" in name or "_EX_HOLO." in name):
            return False
        if substyle_no_blackstar and ("_BLACKSTAR_" in name or "_BLACKSTAR." in name):
            return False
        if substyle_no_lvx_sp and ("_LV.X_SP_" in name or "_LV.X_SP." in name):
            return False
        
        # Filtres négatifs
        if no_fullart and ("_FA_" in name or "_FA." in name):
            return False
        if no_characters and ("_CHARACTER_" in name or "_CHARACTER." in name or "_CSR_" in name or "_CSR." in name or "_CHR_" in name or "_CHR." in name):
            return False
        if no_trainers and ("_TRAINERS_" in name or "_TRAINERS." in name):
            return False
        if no_gold_opt and ("_GOLD_" in name or "_GOLD." in name):
            return False
        if no_shiny_opt and ("_SHINY_" in name or "_SHINY." in name):
            return False
        if no_alternative_opt and ("_ALT_" in name or "_ALT." in name):
            return False
        if no_rainbow_opt and ("_RB_" in name or "_RB." in name):
            return False
        if no_mega_primo and ("_MEGA-PRIMO_" in name or "_MEGA-PRIMO." in name):
            return False
        if no_border_gold and ("_BG_" in name or "_BG." in name):
            return False
        if no_blackgold and ("_BLACK_GOLD_" in name or "_BLACK_GOLD." in name):
            return False
        if no_gold_metal and ("_GOLD_METAL_" in name or "_GOLD_METAL." in name):
            return False
        if no_tagteam and ("_TAGTEAM_" in name or "_TAGTEAM." in name):
            return False
        if no_metal and ("_METAL_" in name or "_METAL." in name):
            return False
        if no_plasma and ("_PLASMA_" in name or "_PLASMA." in name):
            return False
        
        # Filtres positifs
        if opt_fullart and not ("_FA_" in name or "_FA." in name):
            return False
        if opt_megaprimo and not ("_MEGA-PRIMO_" in name or "_MEGA-PRIMO." in name):
            return False
        if opt_bordergold and not ("_BG_" in name or "_BG." in name):
            return False
        if opt_gold and not ("_GOLD_" in name or "_GOLD." in name):
            return False
        if opt_alternative and not ("_ALT_" in name or "_ALT." in name):
            return False
        if opt_alternative_gold and not (("_ALT_" in name or "_ALT." in name) and ("_GOLD_" in name or "_GOLD." in name)):
            return False
        if opt_blackgold and not ("_BLACK_GOLD_" in name or "_BLACK_GOLD." in name):
            return False
        if opt_characters and not ("_CHARACTER_" in name or "_CHARACTER." in name or "_CSR_" in name or "_CSR." in name or "_CHR_" in name or "_CHR." in name):
            return False
        if opt_metal and not ("_METAL_" in name or "_METAL." in name):
            return False
        if opt_rainbow and not ("_RB_" in name or "_RB." in name):
            return False
        if opt_shiny and not ("_SHINY_" in name or "_SHINY." in name):
            return False
        if opt_trainers and not ("_TRAINERS_" in name or "_TRAINERS." in name):
            return False
        if opt_tagteam and not ("_TAGTEAM_" in name or "_TAGTEAM." in name):
            return False
        if metal and not ("_METAL_" in name or "_METAL." in name):
            return False
        if plasma and not ("_PLASMA_" in name or "_PLASMA." in name):
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
