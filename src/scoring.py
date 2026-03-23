"""This module contains functions to compute the final score for a location based on the extracted features and the defined quality metrics."""

from typing import Any

from .config import QUALITY_METRICS


def normalize_count(value: float, cap: float) -> float:
    """
    Higher is better.
    Maps 0..cap to 0..1, clipping above cap.
    """
    return min(value / cap, 1.0)


def normalize_distance(value: float, best: float, worst: float) -> float:
    """
    Lower is better.
    <= best   -> 1.0
    >= worst  -> 0.0
    linear in between
    """
    if value <= best:
        return 1.0
    if value >= worst:
        return 0.0
    return 1.0 - (value - best) / (worst - best)


def compute_subscores(features: dict[str, int | float]) -> dict[str, float]:
    return {
        'daily_needs': (
            0.6 * normalize_count(features['supermarket_count_1000m'], 3)
            + 0.4 * normalize_count(features['pharmacy_count_1000m'], 2)
        ),
        'leisure': (
            0.5 * normalize_count(features['park_count_1000m'], 3)
            + 0.3 * normalize_count(features['sports_centre_count_2000m'], 2)
            + 0.2 * normalize_count(features['swimming_pool_count_2000m'], 2)
        ),
        'convenience': (
            0.4 * normalize_distance(features['nearest_supermarket_m'], 100, 2000)
            + 0.3 * normalize_distance(features['nearest_pharmacy_m'], 100, 2000)
            + 0.3 * normalize_distance(features['nearest_park_m'], 150, 2500)
        ),
        'diversity': normalize_count(features['poi_diversity_1000m'], 6),
    }


def compute_final_score(
    subscores: dict[str, float],
    quality_metrics: dict[str, dict[str, float]] = QUALITY_METRICS,
) -> float:
    score_0_1 = 0.0

    for metric_name, metric_info in quality_metrics.items():
        weight = metric_info['weight']
        score_0_1 += weight * subscores[metric_name]

    return score_0_1 * 100.0


def score_location(features: dict[str, int | float]) -> dict[str, dict[str, Any] | Any]:
    subscores = compute_subscores(features)
    final_score = compute_final_score(subscores)

    return {
        'final_score': round(final_score, 2),
        'subscores': {k: round(v, 3) for k, v in subscores.items()},
        'features': features,
    }
