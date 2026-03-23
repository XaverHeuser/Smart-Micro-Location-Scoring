"""This module provides functions to process raw Points of Interest (POI) data fetched from the Overpass API and normalize it into a structured format suitable for analysis and scoring."""

import pandas as pd

def normalize_pois(raw_data):
    rows = []

    for el in raw_data:
        tags = el.get("tags", {})
        lat = el.get("lat")
        lon = el.get("lon")

        if lat is None or lon is None:
            center = el.get("center", {})
            lat = center.get("lat")
            lon = center.get("lon")

        category_group = None
        category_value = None
        for key in ["amenity", "shop", "leisure"]:
            if key in tags:
                category_group = key
                category_value = tags[key]
                break

        rows.append({
            "osm_id": el.get("id"),
            "osm_type": el.get("type"),
            "lat": lat,
            "lon": lon,
            "name": tags.get("name"),
            "category_group": category_group,
            "category_value": category_value,
            "tags": tags,
        })

    return pd.DataFrame(rows)
