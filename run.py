from flask import Flask, render_template, request, url_for, jsonify
import os
import math
from constants.series_orders import *
from constants.eras import ERA_TO_SERIES, ERA_TO_FOLDER, ERA_LABELS
from constants.rarities import RARITY_ORDER
from utils.card_utils import lister_toutes_les_cartes, extract_card_name
from utils.filters import filter_cards, card_belongs_to_eras

app = Flask(__name__)

# Racine des cartes : chaque sous-dossier de static/cards/ est une série
CARDS_ROOT = os.path.join(app.static_folder, 'cards')

@app.route('/', methods=['GET'])
def index():
    toutes_les_cartes = lister_toutes_les_cartes()

    # Récupération des filtres depuis l'URL
    selected_rarities = [r.upper() for r in request.args.getlist('rarity')]
    selected_types = [t.upper() for t in request.args.getlist('type')]
    selected_styles = [s.upper() for s in request.args.getlist('style')]
    selected_excluded_styles = [s.upper() for s in request.args.getlist('exclude_style')]
    selected_eras = [e.upper() for e in request.args.getlist('era')]
    selected_series = [s.upper() for s in request.args.getlist('series')]
    selected_decks = [d.upper() for d in request.args.getlist('deck')]

    # Nouvelle gestion des substyles pour LV.X, BlackStar et nouveaux substyles
    substyle_lvx_sp = request.args.get('substyle_lvx_sp') == '1'
    substyle_no_lvx_sp = request.args.get('substyle_no_lvx_sp') == '1'
    substyle_blackstar = request.args.get('substyle_blackstar') == '1'
    substyle_no_blackstar = request.args.get('substyle_no_blackstar') == '1'
    substyle_delta = request.args.get('substyle_delta') == '1'
    substyle_no_delta = request.args.get('substyle_no_delta') == '1'
    substyle_rocket = request.args.get('substyle_rocket') == '1'
    substyle_no_rocket = request.args.get('substyle_no_rocket') == '1'
    substyle_ex_holo = request.args.get('substyle_ex_holo') == '1'
    substyle_no_ex_holo = request.args.get('substyle_no_ex_holo') == '1'

    # Construction de la liste des séries autorisées pour l'accordéon
    allowed_series = []
    for era in selected_eras:
        allowed_series.extend(ERA_TO_SERIES.get(era, []))

    context_cards = toutes_les_cartes
    search_query = request.args.get('search', '').strip().upper()

    # Détermination des types disponibles dans le contexte
    all_types = [
        "EX", "SHINING", "BREAK", "V", "VMAX", "VSTAR", "V-UNION", "GX",
        "LV.X", "GOLDSTAR", "TRAINERS", "ENERGY", "PRIME", "LEGEND", "HOLO"
    ]
    available_types = []
    def matches_type_with_substyle(name, types, substyles):
        for t in types:
            if t == "EX" and "_EX" in name:
                return True
            elif t == "SHINING" and "_SHINING" in name:
                return True
            elif t == "BREAK" and "_BREAK" in name:
                return True
            elif t == "V" and ("_V_" in name or "_V.JPEG" in name):
                return True
            elif t == "VMAX" and "_VMAX" in name:
                return True
            elif t == "VSTAR" and "_VSTAR" in name:
                return True
            elif t == "V-UNION" and "_V-UNION" in name:
                return True
            elif t == "GX" and "_GX" in name:
                return True
            elif t == "TRAINERS" and "_TRAINERS" in name:
                return True
            elif t == "ENERGY" and "_ENERGY" in name:
                return True
            elif t == "PRIME" and "PRIME" in name:
                return True
            elif t == "LEGEND" and "LEGEND" in name:
                return True
            # Pour HOLO, nous vérifions séparément les ères
            elif t == "HOLO" and "_HOLO" in name:
                for chemin in context_cards:
                    if os.path.basename(chemin).upper() == name:
                        # Vérifier si la carte appartient à VS, WEB ou E-Series Era
                        if card_belongs_to_eras(chemin, ["VS", "WEB", "E_SERIES"]):
                            return True
                return False
        return False
    for t in all_types:
        for chemin in context_cards:
            name = os.path.basename(chemin).upper()
            if matches_type_with_substyle(name, [t], {}):
                available_types.append(t)
                break

    # Détermination des styles disponibles dans le contexte
    all_styles = [
        "ALTERNATIVE", "ARSTYLE", "BORDER GOLD", "CHARACTERS RARES", "FULL ART", "GOLD", "MEGA-PRIMO", "RAINBOW", "SHINY", "LEGENDARY", "DELTA SPECIES"
    ]
    available_styles = []
    def matches_style_included(name, styles, substyles):
        if not styles:
            return True
        for style in styles:
            if style == "ALTERNATIVE" and "_ALT" not in name:
                return False
            elif style == "ARSTYLE" and "_ARSTYLE" not in name:
                return False
            elif style == "BORDER GOLD" and "_BG" not in name:
                return False
            elif style == "CHARACTERS RARES" and not ("_CHARACTER" in name or "_CSR" in name or "_CHR" in name):
                return False
            elif style == "FULL ART" and "_FA" not in name:
                return False
            elif style == "GOLD" and "_A.JPEG" not in name:
                return False
            elif style == "MEGA-PRIMO" and "_MEGA-PRIMO" not in name:
                return False
            elif style == "RAINBOW" and "_RB" not in name:
                return False
            elif style == "SHINY" and "_SHINY" not in name:
                return False
            elif style == "LEGENDARY" and "LGDRY" not in name:
                return False
            elif style == "DELTA SPECIES" and "_DELTA" not in name:
                return False
        return True
    for s in all_styles:
        for chemin in context_cards:
            name = os.path.basename(chemin).upper()
            if matches_style_included(name, [s], {}):
                available_styles.append(s)
                break

    # Options supplémentaires disponibles (présence de certains styles dans le contexte)
    available_extras = {
        'alternatives': any("_ALT" in os.path.basename(c).upper() for c in context_cards),
        'black_gold': any("_BLACK_GOLD" in os.path.basename(c).upper() for c in context_cards),
        'border_gold': any("_BG" in os.path.basename(c).upper() for c in context_cards),
        'characters_rares': any("_CHARACTER" in os.path.basename(c).upper() or "_CSR" in os.path.basename(c).upper() or "_CHR" in os.path.basename(c).upper() for c in context_cards),
        'full_art': any("_FA" in os.path.basename(c).upper() for c in context_cards),
        'gold': any("_GOLD" in os.path.basename(c).upper() for c in context_cards),
        'gold_metal': any("_GOLD_METAL" in os.path.basename(c).upper() for c in context_cards),
        'mega_primo': any("_MEGA-PRIMO" in os.path.basename(c).upper() for c in context_cards),
        'metal': any("_METAL" in os.path.basename(c).upper() for c in context_cards),
        'plasma': any("_PLASMA" in os.path.basename(c).upper() for c in context_cards),
        'rainbow': any("_RB" in os.path.basename(c).upper() for c in context_cards),
        'shiny': any("_SHINY" in os.path.basename(c).upper() for c in context_cards),
        'tagteam': any("_TAGTEAM" in os.path.basename(c).upper() for c in context_cards),
        'trainers': any("_TRAINERS" in os.path.basename(c).upper() for c in context_cards),
        'lvx_sp': any("_LV.X_SP" in os.path.basename(c).upper() for c in context_cards),
        'no_lvx_sp': any("_LV.X" in os.path.basename(c).upper() and "_SP" not in os.path.basename(c).upper() for c in context_cards),
        'delta': any("_DELTA" in os.path.basename(c).upper() for c in context_cards),
        'no_delta': any("_DELTA" in os.path.basename(c).upper() for c in context_cards),
        'rocket': any("_ROCKET" in os.path.basename(c).upper() for c in context_cards),
        'no_rocket': any("_ROCKET" in os.path.basename(c).upper() for c in context_cards),
        'ex_holo': any("_EX_HOLO" in os.path.basename(c).upper() for c in context_cards),
        'no_ex_holo': any("_EX_HOLO" in os.path.basename(c).upper() for c in context_cards),
        'blackstar': any("_BLACKSTAR" in os.path.basename(c).upper() for c in context_cards),
        'no_blackstar': any("_BLACKSTAR" in os.path.basename(c).upper() for c in context_cards),
        # Options négatives
        'no_alternatives': any("_ALT" in os.path.basename(c).upper() for c in context_cards),
        'no_black_gold': any("_BLACK_GOLD" in os.path.basename(c).upper() for c in context_cards),
        'no_border_gold': any("_BG" in os.path.basename(c).upper() for c in context_cards),
        'no_characters_rares': any("_CHARACTER" in os.path.basename(c).upper() or "_CSR" in os.path.basename(c).upper() or "_CHR" in os.path.basename(c).upper() for c in context_cards),
        'no_full_art': any("_FA" in os.path.basename(c).upper() for c in context_cards),
        'no_gold': any("_GOLD" in os.path.basename(c).upper() for c in context_cards),
        'no_gold_metal': any("_GOLD_METAL" in os.path.basename(c).upper() for c in context_cards),
        'no_mega_primo': any("_MEGA-PRIMO" in os.path.basename(c).upper() for c in context_cards),
        'no_metal': any("_METAL" in os.path.basename(c).upper() for c in context_cards),
        'no_plasma': any("_PLASMA" in os.path.basename(c).upper() for c in context_cards),
        'no_rainbow': any("_RB" in os.path.basename(c).upper() for c in context_cards),
        'no_shiny': any("_SHINY" in os.path.basename(c).upper() for c in context_cards),
        'no_tagteam': any("_TAGTEAM" in os.path.basename(c).upper() for c in context_cards),
        'no_trainers': any("_TRAINERS" in os.path.basename(c).upper() for c in context_cards),
    }

    # Options supplémentaires (cases à cocher)
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
    plasma = ('plasma' in request.args) or ('opt_plasma' in request.args)
    no_plasma = 'no_plasma' in request.args
    opt_dark = 'opt_dark' in request.args
    no_dark = 'no_dark' in request.args
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
    opt_tagteam = 'opt_tagteam' in request.args
    no_tagteam = 'no_tagteam' in request.args

    # Sous-catégories pour certains types/styles
    selected_substyles = {}
    for t in ['V', 'VMAX', 'VSTAR']:
        key = f"sub_{t}"
        values = [v.upper() for v in request.args.getlist(key) if v]
        if values:
            selected_substyles[t] = values
    values_fa = [v.upper() for v in request.args.getlist('sub_FULL_ART') if v]
    if values_fa:
        selected_substyles["FULL ART"] = values_fa
    for sub in ["BASE", "ALTERNATIVE", "BLACK GOLD", "GOLD METAL", "POKEMON"]:
        key = f"sub_{sub}"
        values = [v.upper() for v in request.args.getlist(key) if v]
        if values:
            selected_substyles.setdefault("GOLD", []).extend(values)

    # Filtrage principal
    cartes_filtrees = filter_cards(
        toutes_les_cartes,
        selected_rarities=selected_rarities,
        selected_types=selected_types,
        selected_styles=selected_styles,
        selected_excluded_styles=selected_excluded_styles,
        substyle_blackstar=substyle_blackstar,
        substyle_no_blackstar=substyle_no_blackstar,
        substyle_lvx_sp=substyle_lvx_sp,
        substyle_no_lvx_sp=substyle_no_lvx_sp,
        substyle_delta=substyle_delta,
        substyle_no_delta=substyle_no_delta,
        substyle_rocket=substyle_rocket,
        substyle_no_rocket=substyle_no_rocket,
        substyle_ex_holo=substyle_ex_holo,
        substyle_no_ex_holo=substyle_no_ex_holo,
        no_fullart=no_fullart,
        no_characters=no_characters,
        no_trainers=no_trainers,
        no_gold_opt=no_gold_opt,
        no_shiny_opt=no_shiny_opt,
        no_alternative_opt=no_alternative_opt,
        no_rainbow_opt=no_rainbow_opt,
        no_dark=no_dark,
        no_holo_shiny=no_holo_shiny,
        no_k_shiny=no_k_shiny,
        no_mega_primo=no_mega_primo,
        opt_fullart=opt_fullart,
        opt_megaprimo=opt_megaprimo,
        opt_bordergold=opt_bordergold,
        opt_gold=opt_gold,
        opt_alternative=opt_alternative,
        opt_alternative_gold=opt_alternative_gold,
        opt_blackgold=opt_blackgold,
        opt_characters=opt_characters,
        opt_metal=opt_metal,
        opt_rainbow=opt_rainbow,
        opt_shiny=opt_shiny,
        opt_trainers=opt_trainers,
        opt_dark=opt_dark,
        opt_tagteam=opt_tagteam,
        no_tagteam=no_tagteam,
        metal=metal,
        no_metal=no_metal,
        no_border_gold=no_border_gold,
        no_blackgold=no_blackgold,
        no_gold_metal=no_gold_metal,
        plasma=plasma,
        no_plasma=no_plasma,
        selected_eras=selected_eras,
        selected_series=selected_series,
        selected_decks=selected_decks
    )

    # Recherche par nom (appliquée après tous les autres filtres)
    if search_query:
        filtered = [c for c in cartes_filtrees if search_query in extract_card_name(os.path.basename(c))]
        if not filtered:
            filtered = [c for c in cartes_filtrees if search_query in os.path.basename(c).upper()]
        cartes_filtrees = filtered

    # Construction dynamique des listes 'series' et 'decks' selon les ères choisies
    if not selected_eras:
        series_list = []
        deck_list = []
        for era_key in ERA_TO_SERIES:
            if era_key == "VS":
                series_list.extend(VS_SERIES_ORDER)
                deck_list.extend(VS_DECK_ORDER)
            elif era_key == "WEB":
                series_list.extend(PW_SERIES_ORDER)
                deck_list.extend(PW_DECK_ORDER)
            elif era_key == "E_SERIES":
                series_list.extend(ES_SERIES_ORDER)
                deck_list.extend(ES_DECK_ORDER)
            elif era_key == "ADV":
                series_list.extend(ADV_SERIES_ORDER)
                deck_list.extend(ADV_DECK_ORDER)
            elif era_key == "PCG":
                series_list.extend(PCG_SERIES_ORDER)
                deck_list.extend(PCG_DECK_ORDER)
            elif era_key == "DIAMOND_AND_PEARL":
                series_list.extend(DP_SERIES_ORDER)
                deck_list.extend(DP_DECK_ORDER)
            elif era_key == "PLATINUM":
                series_list.extend(DPT_SERIES_ORDER)
                deck_list.extend(DPT_DECK_ORDER)
            elif era_key == "HGSS":
                series_list.extend(HGSS_SERIES_ORDER)
                deck_list.extend(HGSS_DECK_ORDER)
            elif era_key == "BLACK_AND_WHITE":
                series_list.extend(BW_SERIES_ORDER)
                deck_list.extend(BW_DECK_ORDER)
            elif era_key == "XY":
                series_list.extend(XY_SERIES_ORDER)
                deck_list.extend(XY_DECK_ORDER)
            elif era_key == "SUN_AND_MOON":
                series_list.extend(SM_SERIES_ORDER)
                deck_list.extend(SM_DECK_ORDER)
            elif era_key == "SWORD_AND_SHIELD":
                series_list.extend(SS_SERIES_ORDER)
                deck_list.extend(SS_DECK_ORDER)
    else:
        series_list = []
        deck_list = []
        for era in selected_eras:
            if era == "VS":
                series_list.extend(VS_SERIES_ORDER)
                deck_list.extend(VS_DECK_ORDER)
            elif era == "WEB":
                series_list.extend(PW_SERIES_ORDER)
                deck_list.extend(PW_DECK_ORDER)
            elif era == "E_SERIES":
                series_list.extend(ES_SERIES_ORDER)
                deck_list.extend(ES_DECK_ORDER)
            elif era == "ADV":
                series_list.extend(ADV_SERIES_ORDER)
                deck_list.extend(ADV_DECK_ORDER)
            elif era == "PCG":
                series_list.extend(PCG_SERIES_ORDER)
                deck_list.extend(PCG_DECK_ORDER)
            elif era == "DIAMOND_AND_PEARL":
                series_list.extend(DP_SERIES_ORDER)
                deck_list.extend(DP_DECK_ORDER)
            elif era == "PLATINUM":
                series_list.extend(DPT_SERIES_ORDER)
                deck_list.extend(DPT_DECK_ORDER)
            elif era == "HGSS":
                series_list.extend(HGSS_SERIES_ORDER)
                deck_list.extend(HGSS_DECK_ORDER)
            elif era == "BLACK_AND_WHITE":
                series_list.extend(BW_SERIES_ORDER)
                deck_list.extend(BW_DECK_ORDER)
            elif era == "XY":
                series_list.extend(XY_SERIES_ORDER)
                deck_list.extend(XY_DECK_ORDER)
            elif era == "SUN_AND_MOON":
                series_list.extend(SM_SERIES_ORDER)
                deck_list.extend(SM_DECK_ORDER)
            elif era == "SWORD_AND_SHIELD":
                series_list.extend(SS_SERIES_ORDER)
                deck_list.extend(SS_DECK_ORDER)

    # Tri des cartes : groupement par ère, puis promos, séries, decks pour chaque ère
    def sort_key_dynamic(path):
        name = os.path.basename(path).upper()
        parts = name.split('_')
        try:
            num = int(parts[1])
        except (IndexError, ValueError):
            num = 0
        era_folder = path.upper().split('/')[1]
        era_keys = list(ERA_TO_FOLDER.keys())
        era_idx = 0
        for idx, era in enumerate(era_keys):
            if ERA_TO_FOLDER[era].upper() == era_folder:
                era_idx = idx
                break
        code = parts[0]
        if 'PROMO' in name or code == 'SPP':
            subgroup = 0
            sub_idx = 0
        elif code in series_list:
            subgroup = 1
            sub_idx = series_list.index(code)
        elif code in deck_list:
            subgroup = 2
            sub_idx = deck_list.index(code)
        else:
            subgroup = 3
            sub_idx = 0
        return (era_idx, subgroup, sub_idx, num)

    cartes_filtrees.sort(key=sort_key_dynamic)

    # Pagination : découpe cartes_filtrees en pages modulables
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 150)
    try:
        current_page = int(page)
    except ValueError:
        current_page = 1
    try:
        per_page = int(per_page)
        if per_page not in [50, 100, 150, 200, 250, 300]:
            per_page = 150  # Valeur par défaut si invalide
    except ValueError:
        per_page = 150
        
    if current_page < 1:
        current_page = 1
    total_cards = len(cartes_filtrees)
    total_pages = math.ceil(total_cards / per_page) if total_cards > 0 else 1
    if current_page > total_pages:
        current_page = total_pages
    start_idx = (current_page - 1) * per_page
    end_idx = start_idx + per_page
    page_cards = cartes_filtrees[start_idx:end_idx]

    # Extraire les noms des cartes pour l'affichage
    cards_with_names = []
    for card_path in page_cards:
        card_name = extract_card_name(os.path.basename(card_path))
        cards_with_names.append({
            'path': card_path,
            'name': card_name
        })

    # Indicateurs pour la section Options Supplémentaires
    show_no_bordergold_for_megaprimo = "MEGA-PRIMO" in selected_styles
    show_fullart_for_bordergold = "BORDER GOLD" in selected_styles

    return render_template(
        'index.html',
        cartes=cards_with_names,
        rarities=RARITY_ORDER,
        types=[
            "EX", "SHINING", "BREAK", "V", "VMAX", "VSTAR", "V-UNION", "GX", "TRAINERS", "ENERGY", "PRIME", "LEGEND", "LV.X", "GOLDSTAR", "HOLO"
        ],
        styles=[
            "ALTERNATIVE", "ARSTYLE", "BORDER GOLD", "CHARACTERS RARES", "FULL ART", "GOLD", "MEGA-PRIMO", "RAINBOW", "SHINY", "LEGENDARY", "DELTA SPECIES"
        ],
        substyles={},
        available_types=available_types,
        available_styles=available_styles,
        available_extras=available_extras,
        selected_rarities=selected_rarities,
        selected_types=selected_types,
        selected_styles=selected_styles,
        selected_substyles=selected_substyles,
        eras=list(ERA_TO_SERIES.keys()),
        era_labels=ERA_LABELS,
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
        total_pages=total_pages,
        per_page=per_page,
        search_query=search_query,
    )

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '').strip().upper()
    toutes_les_cartes = lister_toutes_les_cartes()
    noms = set()
    for c in toutes_les_cartes:
        nom = extract_card_name(os.path.basename(c))
        if nom:
            noms.add(nom)
    if query:
        suggestions = [n for n in noms if n.startswith(query)]
    else:
        suggestions = []
    suggestions = sorted(suggestions)[:10]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True, port=5001)