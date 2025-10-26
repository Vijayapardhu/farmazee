from django import forms
from .models import YieldPrediction, YieldHistory


class YieldPredictionForm(forms.ModelForm):
    class Meta:
        model = YieldPrediction
        fields = [
            'crop_type',
            'soil_type',
            'area_hectares',
            'season',
            'irrigation_type',
            'fertilizer_type',
            'weather_condition',
            'pest_disease_risk',
            'notes',
        ]


class YieldHistoryForm(forms.ModelForm):
    class Meta:
        model = YieldHistory
        fields = [
            'harvest_date',
            'actual_yield',
            'weather_conditions',
            'notes',
        ]

