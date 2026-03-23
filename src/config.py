DEFAULT_OVERPASS_URL = "https://overpass-api.de/api/interpreter"

POINTS_OF_INTEREST = [
    "amenity=cafe",
    "shop=supermarket",
    "amenity=pharmacy",
    "leisure=park",
    "leisure=swimming_pool",
    "leisure=sports_centre",
]

QUALITY_METRICS = {
    "daily_needs": {"weight": 0.40},
    "leisure": {"weight": 0.25},
    "convenience": {"weight": 0.20},
    "diversity": {"weight": 0.15},
}
