# Regroupement des séries par ères (inclut codes de séries, decks et promos)
from .series_orders import (
    BW_SERIES_ORDER, XY_SERIES_ORDER, SM_SERIES_ORDER, SS_SERIES_ORDER, 
    HGSS_SERIES_ORDER, DP_SERIES_ORDER, DPT_SERIES_ORDER, PCG_SERIES_ORDER, ADV_SERIES_ORDER
)

ERA_TO_SERIES = {
    "ADV": ADV_SERIES_ORDER,
    "PCG": PCG_SERIES_ORDER,
    "DIAMOND_AND_PEARL": DP_SERIES_ORDER,
    "PLATINUM": DPT_SERIES_ORDER,
    "HGSS": HGSS_SERIES_ORDER,
    "BLACK_AND_WHITE": BW_SERIES_ORDER,
    "XY": XY_SERIES_ORDER,
    "SUN_AND_MOON": SM_SERIES_ORDER,
    "SWORD_AND_SHIELD": SS_SERIES_ORDER,
}

ERA_TO_FOLDER = {
    "ADV": "ADV",
    "PCG": "PCG",
    "DIAMOND_AND_PEARL": "DP",
    "PLATINUM": "DPT",
    "HGSS": "HGSS",
    "BLACK_AND_WHITE": "B&W",
    "XY": "XY",
    "SUN_AND_MOON": "S&M",
    "SWORD_AND_SHIELD": "S&S",
}

ERA_LABELS = {
    "ADV": "ADV",
    "PCG": "PCG",
    "DIAMOND_AND_PEARL": "Diamond & Pearl",
    "PLATINUM": "Platinum",
    "HGSS": "HeartGold & SoulSilver",
    "BLACK_AND_WHITE": "Black & White",
    "XY": "XY",
    "SUN_AND_MOON": "Sun & Moon",
    "SWORD_AND_SHIELD": "Sword & Shield",
}
