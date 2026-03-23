"""This module provides functions to interact with the Overpass API to fetch Points of Interest (POI) data based on geographic coordinates and specified categories."""

import requests
from typing import Any, Dict, Iterable, List, Optional
import json

def build_overpass_query(lat, lon, categories, radius):
    parts = []
    for cat in categories:
        key, value = cat.split("=", 1)
        parts.append(f'nwr["{key}"="{value}"](around:{radius},{lat},{lon});')

    return f"""
    [out:json][timeout:45];
    (
      {"".join(parts)}
    );
    out center tags;
    """.strip()


def fetch_poi_data(
    lat: float,
    lon: float,
    categories: Iterable[str],
    radius: int,
    overpass_url: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> List[Dict[str, Any]]:
    """Fetch POI data from Overpass. Always returns a list."""
    if not overpass_url:
        raise ValueError("Overpass URL is not provided.")

    query = build_overpass_query(lat, lon, categories, radius)
    http = session or requests.Session()

    try:
        response = http.post(
            overpass_url,
            data=query,
            headers={"Content-Type": "text/plain; charset=utf-8"},
            timeout=120,
        )

        # Raise on HTTP errors first
        response.raise_for_status()

        # Parse JSON explicitly and show a useful snippet if it fails
        try:
            payload = response.json()
        except json.JSONDecodeError:
            body_preview = response.text[:1000].strip()
            raise RuntimeError(
                "Overpass returned a non-JSON response.\n"
                f"URL: {overpass_url}\n"
                f"Status: {response.status_code}\n"
                f"Body preview:\n{body_preview}"
            )

        if "elements" not in payload:
            raise RuntimeError(
                "Overpass response JSON does not contain 'elements'. "
                f"Top-level keys: {list(payload.keys())}"
            )

        return payload["elements"]

    except requests.Timeout:
        raise RuntimeError("Overpass request timed out.")
    except requests.RequestException as e:
        raise RuntimeError(f"HTTP error during Overpass request: {e}") from e
