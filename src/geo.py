"""This module provides geocoding functionality to resolve human-readable addresses to latitude and longitude coordinates."""

from typing import Optional

from geopy.geocoders import Nominatim


def geocode_address(address: str) -> Optional[tuple[float, float]]:
    """Resolve a human-readable address to (lat, lon)."""
    geolocator = Nominatim(user_agent='smls_gnn_project')

    try:
        location = geolocator.geocode(address, exactly_one=True, timeout=20)
        if location is None:
            print('Address could not be found.')
            return None

        print('Location confirmed')
        return (location.latitude, location.longitude)

    except Exception as e:
        print(f'Error during geocoding: {e}')
        return None
