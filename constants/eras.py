# Regroupement des séries par ères (inclut codes de séries, decks et promos)
from .series_orders import (
    BW_SERIES_ORDER, XY_SERIES_ORDER, SM_SERIES_ORDER, SS_SERIES_ORDER, 
    HGSS_SERIES_ORDER, DP_SERIES_ORDER, DPT_SERIES_ORDER, PCG_SERIES_ORDER, ADV_SERIES_ORDER,
    ES_SERIES_ORDER, PW_SERIES_ORDER, VS_SERIES_ORDER
)

ERA_TO_SERIES = {
    "VS": VS_SERIES_ORDER,
    "WEB": PW_SERIES_ORDER,
    "E_SERIES": ES_SERIES_ORDER,
    "ADV": ADV_SERIES_ORDER,
    "PCG": PCG_SERIES_ORDER,
    "DIAMOND_AND_PEARL": DP_SERIES_ORDER,
    "PLATINUM": DPT_SERIES_ORDER,
    "LEGEND": HGSS_SERIES_ORDER,
    "BLACK_AND_WHITE": BW_SERIES_ORDER,
    "XY": XY_SERIES_ORDER,
    "SUN_AND_MOON": SM_SERIES_ORDER,
    "SWORD_AND_SHIELD": SS_SERIES_ORDER,
}

ERA_TO_FOLDER = {
    "VS": "VS",
    "WEB": "WEB",
    "E_SERIES": "ES",
    "ADV": "ADV",
    "PCG": "PCG",
    "DIAMOND_AND_PEARL": "DP",
    "PLATINUM": "DPT",
    "LEGEND": "HGSS",
    "BLACK_AND_WHITE": "B&W",
    "XY": "XY",
    "SUN_AND_MOON": "S&M",
    "SWORD_AND_SHIELD": "S&S",
}

ERA_LABELS = {
    "VS": "VS Era",
    "WEB": "WEB Era",
    "E_SERIES": "E-Series Era",
    "ADV": "ADV Era",
    "PCG": "PCG Era",
    "DIAMOND_AND_PEARL": "Diamond & Pearl Era",
    "PLATINUM": "Platinum Era",
    "LEGEND": "LEGEND Era",
    "BLACK_AND_WHITE": "Black & White Era",
    "XY": "XY Era",
    "SUN_AND_MOON": "Sun & Moon Era",
    "SWORD_AND_SHIELD": "Sword & Shield Era",
}
