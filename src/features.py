"""This module contains functions to extract features from the POI data for a given location."""

import numpy as np
import pandas as pd


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return float(R * c)


def extract_location_features(
    lat: float, lon: float, poi_df: pd.DataFrame
) -> dict[str, int | float]:
    df = poi_df.copy()
    df = df.dropna(subset=['lat', 'lon', 'category_value']).copy()

    df['distance_m'] = haversine_distance(lat, lon, df['lat'].values, df['lon'].values)

    def count_within(category: str, radius: int) -> int:
        return int(
            ((df['category_value'] == category) & (df['distance_m'] <= radius)).sum()
        )

    def nearest_distance(category: str) -> float:
        cat_df = df[df['category_value'] == category]
        if cat_df.empty:
            return 99999.0
        return float(cat_df['distance_m'].min())

    return {
        'supermarket_count_1000m': count_within('supermarket', 1000),
        'pharmacy_count_1000m': count_within('pharmacy', 1000),
        'park_count_1000m': count_within('park', 1000),
        'sports_centre_count_2000m': count_within('sports_centre', 2000),
        'swimming_pool_count_2000m': count_within('swimming_pool', 2000),
        'nearest_supermarket_m': nearest_distance('supermarket'),
        'nearest_pharmacy_m': nearest_distance('pharmacy'),
        'nearest_park_m': nearest_distance('park'),
        'poi_diversity_1000m': int(
            df.loc[df['distance_m'] <= 1000, 'category_value'].nunique()
        ),
    }
