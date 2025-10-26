from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime
import math
from .models import CropType, SoilType, YieldPrediction, YieldHistory, CropRecommendation
from .forms import YieldPredictionForm, YieldHistoryForm
from .utils import calculate_yield_prediction, get_crop_recommendations

def index(request):
    """Yield Prediction (Simple Calculator)"""
    result = None
    crop_name = ''
    area_acres = ''
    fertility_factor = ''
    # Season predictor state
    season_result = None
    month_input = ''
    # Water calculator state
    water_result = None
    water_crop = ''
    water_area = ''

    if request.method == 'POST':
        # Determine which form was submitted by hidden flags
        if request.POST.get('calc_form') == '1':
            crop_name = (request.POST.get('crop_name') or '').strip()
            try:
                area_acres = float(request.POST.get('area_acres') or 0)
            except ValueError:
                area_acres = 0.0
            try:
                fertility_factor = float(request.POST.get('fertility_factor') or 1)
            except ValueError:
                fertility_factor = 1.0

            raw_yield = area_acres * fertility_factor
            result = {
                'crop_name': crop_name,
                'area_acres': area_acres,
                'fertility_factor': fertility_factor,
                'raw_yield': raw_yield,
                'rounded_yield': math.floor(raw_yield),
            }
        elif request.POST.get('season_form') == '1':
            month_input = (request.POST.get('month') or '').strip()
            try:
                month_num = int(month_input)
            except ValueError:
                month_num = 0

            # Map month to season (India)
            season = None
            if 3 <= month_num <= 5:
                season = 'Summer'
            elif 6 <= month_num <= 9:
                season = 'Monsoon'
            elif month_num == 10 or month_num == 11 or month_num == 12 or month_num == 1 or month_num == 2:
                season = 'Winter'
            else:
                season = 'Invalid month'

            season_result = {
                'month': month_input,
                'season': season,
            }
        elif request.POST.get('water_form') == '1':
            # Simple water requirement calculator
            water_crop = (request.POST.get('water_crop') or '').strip()
            try:
                water_area = float(request.POST.get('water_area') or 0)
            except ValueError:
                water_area = 0.0

            crop_key = water_crop.lower()
            # Predefined constants: liters per acre per day (example values)
            rates = {
                'rice': 6000,
                'paddy': 6000,
                'wheat': 3500,
                'maize': 3000,
                'corn': 3000,
                'cotton': 4500,
                'sugarcane': 6500,
                'soybean': 2500,
                'groundnut': 2200,
            }
            rate = rates.get(crop_key, 3000)
            total = water_area * rate
            water_result = {
                'crop_display': water_crop or 'Unknown',
                'area_acres': water_area,
                'rate_liters_per_acre': rate,
                'total_liters_per_day': math.floor(total),
            }

    context = {
        'result': result,
        'crop_name': crop_name,
        'area_acres': area_acres,
        'fertility_factor': fertility_factor,
        'season_result': season_result,
        'month_input': month_input,
        'water_result': water_result,
        'water_crop': water_crop,
        'water_area': water_area,
    }
    return render(request, 'yield_prediction/home.html', context)

@login_required
def predict_yield(request):
    """Create a new yield prediction"""
    if request.method == 'POST':
        form = YieldPredictionForm(request.POST)
        if form.is_valid():
            # Get form data
            crop_type = form.cleaned_data['crop_type']
            soil_type = form.cleaned_data['soil_type']
            area_hectares = form.cleaned_data['area_hectares']
            season = form.cleaned_data['season']
            irrigation_type = form.cleaned_data['irrigation_type']
            fertilizer_type = form.cleaned_data['fertilizer_type']
            weather_condition = form.cleaned_data.get('weather_condition', '')
            pest_disease_risk = form.cleaned_data.get('pest_disease_risk', 'medium')
            
            # Calculate yield prediction
            prediction_result = calculate_yield_prediction(
                crop_type=crop_type,
                soil_type=soil_type,
                area_hectares=area_hectares,
                season=season,
                irrigation_type=irrigation_type,
                fertilizer_type=fertilizer_type,
                weather_condition=weather_condition,
                pest_disease_risk=pest_disease_risk
            )
            
            # Create prediction record
            prediction = YieldPrediction.objects.create(
                user=request.user,
                crop_type=crop_type,
                soil_type=soil_type,
                area_hectares=area_hectares,
                season=season,
                irrigation_type=irrigation_type,
                fertilizer_type=fertilizer_type,
                weather_condition=weather_condition,
                pest_disease_risk=pest_disease_risk,
                predicted_yield_min=prediction_result['yield_min'],
                predicted_yield_max=prediction_result['yield_max'],
                predicted_yield_avg=prediction_result['yield_avg'],
                confidence_level=prediction_result['confidence'],
                recommendations=prediction_result['recommendations'],
                notes=form.cleaned_data.get('notes', '')
            )
            
            messages.success(request, 'Yield prediction completed successfully!')
            return redirect('yield_prediction:prediction_detail', prediction_id=prediction.id)
    else:
        form = YieldPredictionForm()
    
    context = {
        'form': form,
        'crop_types': CropType.objects.filter(is_active=True),
        'soil_types': SoilType.objects.filter(is_active=True),
    }
    return render(request, 'yield_prediction/predict_yield.html', context)

@login_required
def prediction_detail(request, prediction_id):
    """View detailed yield prediction results"""
    prediction = get_object_or_404(YieldPrediction, id=prediction_id, user=request.user)
    history = YieldHistory.objects.filter(prediction=prediction).order_by('-harvest_date')
    
    context = {
        'prediction': prediction,
        'history': history,
    }
    return render(request, 'yield_prediction/prediction_detail.html', context)

@login_required
def prediction_list(request):
    """List all yield predictions for the user"""
    predictions = YieldPrediction.objects.filter(user=request.user).order_by('-created_at')
    
    # Filtering
    crop_filter = request.GET.get('crop')
    soil_filter = request.GET.get('soil')
    season_filter = request.GET.get('season')
    
    if crop_filter:
        predictions = predictions.filter(crop_type__name__icontains=crop_filter)
    if soil_filter:
        predictions = predictions.filter(soil_type__name__icontains=soil_filter)
    if season_filter:
        predictions = predictions.filter(season=season_filter)
    
    # Pagination
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'predictions': page_obj,
        'crop_types': CropType.objects.filter(is_active=True),
        'soil_types': SoilType.objects.filter(is_active=True),
        'seasons': YieldPrediction.SEASON_CHOICES,
    }
    return render(request, 'yield_prediction/prediction_list.html', context)

@login_required
def add_yield_history(request, prediction_id):
    """Add actual yield data to a prediction"""
    prediction = get_object_or_404(YieldPrediction, id=prediction_id, user=request.user)
    
    if request.method == 'POST':
        form = YieldHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.prediction = prediction
            history.save()
            
            messages.success(request, 'Yield history added successfully!')
            return redirect('yield_prediction:prediction_detail', prediction_id=prediction.id)
    else:
        form = YieldHistoryForm()
    
    context = {
        'form': form,
        'prediction': prediction,
    }
    return render(request, 'yield_prediction/add_history.html', context)

@login_required
def crop_recommendations(request):
    """Get crop recommendations based on soil and season"""
    soil_type_id = request.GET.get('soil_type')
    season = request.GET.get('season')
    
    recommendations = []
    if soil_type_id and season:
        try:
            soil_type = SoilType.objects.get(id=soil_type_id)
            recommendations = CropRecommendation.objects.filter(
                soil_type=soil_type,
                season=season,
                is_active=True
            ).first()
            if recommendations:
                recommendations = recommendations.recommended_crops.all()
        except SoilType.DoesNotExist:
            pass
    
    context = {
        'recommendations': recommendations,
        'soil_types': SoilType.objects.filter(is_active=True),
        'seasons': YieldPrediction.SEASON_CHOICES,
        'selected_soil': soil_type_id,
        'selected_season': season,
    }
    return render(request, 'yield_prediction/crop_recommendations.html', context)

@login_required
def delete_prediction(request, prediction_id):
    """Delete a yield prediction"""
    prediction = get_object_or_404(YieldPrediction, id=prediction_id, user=request.user)
    
    if request.method == 'POST':
        prediction.delete()
        messages.success(request, 'Yield prediction deleted successfully!')
        return redirect('yield_prediction:prediction_list')
    
    context = {'prediction': prediction}
    return render(request, 'yield_prediction/delete_prediction.html', context)

# API Views
@login_required
@require_http_methods(["GET"])
def get_crop_details_api(request, crop_id):
    """API endpoint to get crop details"""
    try:
        crop = CropType.objects.get(id=crop_id, is_active=True)
        data = {
            'id': crop.id,
            'name': crop.name,
            'category': crop.category,
            'base_yield_min': crop.base_yield_min,
            'base_yield_max': crop.base_yield_max,
            'average_yield': crop.average_yield,
            'growing_season': crop.growing_season,
            'maturity_days': crop.maturity_days,
            'water_requirement': crop.water_requirement,
            'preferred_soil_types': crop.preferred_soil_types,
            'ph_range_min': crop.ph_range_min,
            'ph_range_max': crop.ph_range_max,
        }
        return JsonResponse(data)
    except CropType.DoesNotExist:
        return JsonResponse({'error': 'Crop not found'}, status=404)

@login_required
@require_http_methods(["GET"])
def get_soil_details_api(request, soil_id):
    """API endpoint to get soil details"""
    try:
        soil = SoilType.objects.get(id=soil_id, is_active=True)
        data = {
            'id': soil.id,
            'name': soil.name,
            'fertility_level': soil.fertility_level,
            'water_retention': soil.water_retention,
            'drainage': soil.drainage,
            'yield_multiplier': soil.yield_multiplier,
        }
        return JsonResponse(data)
    except SoilType.DoesNotExist:
        return JsonResponse({'error': 'Soil type not found'}, status=404)

@login_required
@require_http_methods(["POST"])
def quick_predict_api(request):
    """API endpoint for quick yield prediction"""
    try:
        data = request.POST
        crop_id = data.get('crop_id')
        soil_id = data.get('soil_id')
        area = float(data.get('area', 1))
        
        crop = CropType.objects.get(id=crop_id, is_active=True)
        soil = SoilType.objects.get(id=soil_id, is_active=True)
        
        # Quick calculation
        base_yield = crop.average_yield
        soil_multiplier = soil.yield_multiplier
        predicted_yield = base_yield * soil_multiplier * area
        
        return JsonResponse({
            'success': True,
            'predicted_yield': round(predicted_yield, 2),
            'yield_per_hectare': round(predicted_yield / area, 2),
            'crop_name': crop.name,
            'soil_name': soil.name
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)