from typing import Dict

from .models import CropType, SoilType


def calculate_yield_prediction(
    crop_type: CropType,
    soil_type: SoilType,
    area_hectares: float,
    season: str,
    irrigation_type: str,
    fertilizer_type: str,
    weather_condition: str = "",
    pest_disease_risk: str = "medium",
) -> Dict[str, object]:
    # Baseline from crop
    base_avg = crop_type.average_yield

    # Soil multiplier
    soil_mult = soil_type.yield_multiplier

    # Season adjustment (simple heuristic)
    season_mult = 1.0
    if season != crop_type.growing_season and crop_type.growing_season != 'year_round':
        season_mult = 0.9

    # Irrigation adjustment
    irrigation_mult = {
        'rainfed': 0.95,
        'irrigated': 1.05,
        'drip': 1.08,
        'sprinkler': 1.03,
    }.get(irrigation_type, 1.0)

    # Fertilizer adjustment
    fertilizer_mult = {
        'organic': 1.0,
        'chemical': 1.05,
        'mixed': 1.07,
        'none': 0.9,
    }.get(fertilizer_type, 1.0)

    # Weather adjustment
    weather_mult = 1.0
    if weather_condition:
        text = weather_condition.lower()
        if 'drought' in text or 'dry' in text:
            weather_mult = 0.9
        elif 'excess' in text or 'flood' in text:
            weather_mult = 0.92
        elif 'favorable' in text or 'good' in text:
            weather_mult = 1.05

    # Pest/disease risk
    pest_mult = {'low': 1.02, 'medium': 1.0, 'high': 0.95}.get(pest_disease_risk, 1.0)

    per_hectare = base_avg * soil_mult * season_mult * irrigation_mult * fertilizer_mult * weather_mult * pest_mult
    yield_avg = per_hectare * area_hectares
    yield_min = yield_avg * 0.9
    yield_max = yield_avg * 1.1

    # Confidence heuristic
    total_mult = soil_mult * season_mult * irrigation_mult * fertilizer_mult * weather_mult * pest_mult
    if total_mult >= 1.05:
        confidence = 'high'
    elif total_mult >= 1.0:
        confidence = 'medium'
    else:
        confidence = 'low'

    recommendations = (
        "Use mulching to conserve soil moisture; schedule irrigation early morning; monitor for pests weekly."
    )

    return {
        'yield_min': round(yield_min, 2),
        'yield_max': round(yield_max, 2),
        'yield_avg': round(yield_avg, 2),
        'confidence': confidence,
        'recommendations': recommendations,
    }


def get_crop_recommendations(soil_type: SoilType, season: str):
    # Placeholder: recommendations resolved in views via model relations
    return []







