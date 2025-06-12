# Regroupement des séries par ères (inclut codes de séries, decks et promos)
from .series_orders import BW_SERIES_ORDER, XY_SERIES_ORDER, SM_SERIES_ORDER, SS_SERIES_ORDER, HGSS_SERIES_ORDER

ERA_TO_SERIES = {
    "HGSS": HGSS_SERIES_ORDER,
    "BLACK_AND_WHITE": BW_SERIES_ORDER,
    "XY": XY_SERIES_ORDER,
    "SUN_AND_MOON": SM_SERIES_ORDER,
    "SWORD_AND_SHIELD": SS_SERIES_ORDER,
}

ERA_TO_FOLDER = {
    "HGSS": "HGSS",
    "BLACK_AND_WHITE": "B&W",
    "XY": "XY",
    "SUN_AND_MOON": "S&M",
    "SWORD_AND_SHIELD": "S&S",
}

ERA_LABELS = {
    "HGSS": "HeartGold & SoulSilver",
    "BLACK_AND_WHITE": "Black & White",
    "XY": "XY",
    "SUN_AND_MOON": "Sun & Moon",
    "SWORD_AND_SHIELD": "Sword & Shield",
}
