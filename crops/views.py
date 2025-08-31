from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import (
    Crop, CropPlan, CropActivity, CropMonitoring, 
    PestDisease, CropCalendar, CropAdvice, YieldRecord
)
from datetime import date, timedelta


def crop_list(request):
    """List all crops with filtering and search"""
    crops = Crop.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        crops = crops.filter(
            Q(name__icontains=search_query) |
            Q(scientific_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category = request.GET.get('category', '')
    if category:
        crops = crops.filter(category=category)
    
    # Season filter
    season = request.GET.get('season', '')
    if season:
        crops = crops.filter(season=season)
    
    # Featured crops
    featured_crops = Crop.objects.filter(is_featured=True, is_active=True)[:6]
    
    context = {
        'crops': crops,
        'featured_crops': featured_crops,
        'categories': Crop.CROP_CATEGORIES,
        'seasons': Crop.SEASONS,
        'search_query': search_query,
        'selected_category': category,
        'selected_season': season,
    }
    return render(request, 'crops/list.html', context)


def crop_detail(request, pk):
    """Crop detail view with comprehensive information"""
    crop = get_object_or_404(Crop, pk=pk, is_active=True)
    
    # Get related data
    related_crops = Crop.objects.filter(
        category=crop.category,
        is_active=True
    ).exclude(pk=crop.pk)[:4]
    
    # Get crop advice
    crop_advice = CropAdvice.objects.filter(
        crop=crop,
        is_active=True
    )[:3]
    
    # Get pest and diseases affecting this crop
    pests_diseases = crop.pests_diseases.filter(is_active=True)[:5]
    
    context = {
        'crop': crop,
        'related_crops': related_crops,
        'crop_advice': crop_advice,
        'pests_diseases': pests_diseases,
    }
    return render(request, 'crops/detail.html', context)


@login_required
def crop_plan(request, pk):
    """Crop plan view for authenticated users"""
    crop = get_object_or_404(Crop, pk=pk, is_active=True)
    
    if request.method == 'POST':
        # Handle crop plan creation
        title = request.POST.get('title')
        land_area = request.POST.get('land_area')
        planned_sowing_date = request.POST.get('planned_sowing_date')
        expected_harvest_date = request.POST.get('expected_harvest_date')
        budget = request.POST.get('budget')
        notes = request.POST.get('notes')
        
        if title and land_area and planned_sowing_date and expected_harvest_date:
            CropPlan.objects.create(
                user=request.user,
                crop=crop,
                title=title,
                land_area=land_area,
                planned_sowing_date=planned_sowing_date,
                expected_harvest_date=expected_harvest_date,
                budget=budget or None,
                notes=notes,
                status='draft'
            )
            messages.success(request, 'Crop plan created successfully!')
            return redirect('crops:plan', pk=pk)
        else:
            messages.error(request, 'Please fill all required fields.')
    
    # Get user's crop plans for this crop
    user_plans = CropPlan.objects.filter(
        user=request.user,
        crop=crop
    ).order_by('-created_at')
    
    context = {
        'crop': crop,
        'plans': user_plans,
    }
    return render(request, 'crops/plan.html', context)


@login_required
def crop_activities(request, pk):
    """Crop activities view for authenticated users"""
    crop = get_object_or_404(Crop, pk=pk, is_active=True)
    
    if request.method == 'POST':
        # Handle activity creation
        activity_type = request.POST.get('activity_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        scheduled_date = request.POST.get('scheduled_date')
        cost = request.POST.get('cost')
        notes = request.POST.get('notes')
        
        if activity_type and title and description and scheduled_date:
            # Get the first crop plan for this crop and user
            crop_plan = CropPlan.objects.filter(
                user=request.user,
                crop=crop
            ).first()
            
            if crop_plan:
                CropActivity.objects.create(
                    crop_plan=crop_plan,
                    activity_type=activity_type,
                    title=title,
                    description=description,
                    scheduled_date=scheduled_date,
                    cost=cost or None,
                    notes=notes
                )
                messages.success(request, 'Activity created successfully!')
                return redirect('crops:activities', pk=pk)
            else:
                messages.error(request, 'Please create a crop plan first.')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    # Get user's activities for this crop
    user_activities = []
    crop_plans = CropPlan.objects.filter(user=request.user, crop=crop)
    for plan in crop_plans:
        activities = CropActivity.objects.filter(crop_plan=plan).order_by('-scheduled_date')
        user_activities.extend(activities)
    
    # Sort by scheduled date
    user_activities.sort(key=lambda x: x.scheduled_date, reverse=True)
    
    context = {
        'crop': crop,
        'activities': user_activities,
    }
    return render(request, 'crops/activities.html', context)


@login_required
def crop_monitoring(request, pk):
    """Crop monitoring view for authenticated users"""
    crop = get_object_or_404(Crop, pk=pk, is_active=True)
    
    if request.method == 'POST':
        # Handle monitoring record creation
        monitoring_date = request.POST.get('monitoring_date')
        growth_stage = request.POST.get('growth_stage')
        health_status = request.POST.get('health_status')
        height = request.POST.get('height')
        observations = request.POST.get('observations')
        issues_found = request.POST.get('issues_found')
        recommendations = request.POST.get('recommendations')
        
        if monitoring_date and growth_stage and health_status and observations:
            # Get the first crop plan for this crop and user
            crop_plan = CropPlan.objects.filter(
                user=request.user,
                crop=crop
            ).first()
            
            if crop_plan:
                CropMonitoring.objects.create(
                    crop_plan=crop_plan,
                    monitoring_date=monitoring_date,
                    growth_stage=growth_stage,
                    health_status=health_status,
                    height=height or None,
                    observations=observations,
                    issues_found=issues_found,
                    recommendations=recommendations
                )
                messages.success(request, 'Monitoring record created successfully!')
                return redirect('crops:monitoring', pk=pk)
            else:
                messages.error(request, 'Please create a crop plan first.')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    # Get user's monitoring records for this crop
    user_monitoring = []
    crop_plans = CropPlan.objects.filter(user=request.user, crop=crop)
    for plan in crop_plans:
        monitoring = CropMonitoring.objects.filter(crop_plan=plan).order_by('-monitoring_date')
        user_monitoring.extend(monitoring)
    
    # Sort by monitoring date
    user_monitoring.sort(key=lambda x: x.monitoring_date, reverse=True)
    
    context = {
        'crop': crop,
        'monitoring_records': user_monitoring,
    }
    return render(request, 'crops/monitoring.html', context)


def crop_calendar(request):
    """Crop calendar view"""
    # Get current month and year
    current_date = date.today()
    current_month = current_date.month
    current_year = current_date.year
    
    # Get calendar entries for current month
    calendar_entries = CropCalendar.objects.filter(
        event_date__month=current_month,
        event_date__year=current_year
    ).order_by('event_date')
    
    # Get upcoming events
    upcoming_events = CropCalendar.objects.filter(
        event_date__gte=current_date
    ).order_by('event_date')[:10]
    
    context = {
        'calendar_entries': calendar_entries,
        'upcoming_events': upcoming_events,
        'current_month': current_month,
        'current_year': current_year,
    }
    return render(request, 'crops/calendar.html', context)


def pest_disease_list(request):
    """List crop pests and diseases with search and filtering"""
    pest_diseases = PestDisease.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        pest_diseases = pest_diseases.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(symptoms__icontains=search_query)
        )
    
    # Type filter
    pest_type = request.GET.get('type', '')
    if pest_type:
        pest_diseases = pest_diseases.filter(type=pest_type)
    
    # Severity filter
    severity = request.GET.get('severity', '')
    if severity:
        pest_diseases = pest_diseases.filter(severity=severity)
    
    context = {
        'pest_diseases': pest_diseases,
        'search_query': search_query,
        'selected_type': pest_type,
        'selected_severity': severity,
        'type_choices': PestDisease.TYPE_CHOICES,
        'severity_choices': PestDisease.SEVERITY_LEVELS,
    }
    return render(request, 'crops/pest_diseases.html', context)


def crop_advice(request):
    """Crop advice view with search and filtering"""
    advice_list = CropAdvice.objects.filter(is_active=True).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        advice_list = advice_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Season filter
    season = request.GET.get('season', '')
    if season:
        advice_list = advice_list.filter(season=season)
    
    # Featured advice
    featured_advice = CropAdvice.objects.filter(
        is_featured=True,
        is_active=True
    ).order_by('-created_at')[:5]
    
    context = {
        'advice_list': advice_list,
        'featured_advice': featured_advice,
        'search_query': search_query,
        'selected_season': season,
        'seasons': Crop.SEASONS,
    }
    return render(request, 'crops/advice.html', context)


@login_required
def my_crops(request):
    """User's crop plans and activities dashboard"""
    user_plans = CropPlan.objects.filter(user=request.user).order_by('-created_at')
    
    # Get upcoming activities
    upcoming_activities = []
    for plan in user_plans:
        activities = CropActivity.objects.filter(
            crop_plan=plan,
            scheduled_date__gte=date.today(),
            is_completed=False
        ).order_by('scheduled_date')[:5]
        upcoming_activities.extend(activities)
    
    # Sort by scheduled date
    upcoming_activities.sort(key=lambda x: x.scheduled_date)
    
    # Get recent monitoring records
    recent_monitoring = []
    for plan in user_plans:
        monitoring = CropMonitoring.objects.filter(
            crop_plan=plan
        ).order_by('-monitoring_date')[:3]
        recent_monitoring.extend(monitoring)
    
    # Sort by monitoring date
    recent_monitoring.sort(key=lambda x: x.monitoring_date, reverse=True)
    
    context = {
        'user_plans': user_plans,
        'upcoming_activities': upcoming_activities,
        'recent_monitoring': recent_monitoring,
    }
    return render(request, 'crops/my_crops.html', context)


@login_required
def crop_yield_tracking(request, pk):
    """Crop yield tracking for authenticated users"""
    crop = get_object_or_404(Crop, pk=pk, is_active=True)
    
    if request.method == 'POST':
        # Handle yield record creation
        harvest_date = request.POST.get('harvest_date')
        quantity_harvested = request.POST.get('quantity_harvested')
        quality_grade = request.POST.get('quality_grade')
        market_price = request.POST.get('market_price')
        notes = request.POST.get('notes')
        
        if harvest_date and quantity_harvested:
            # Get the first crop plan for this crop and user
            crop_plan = CropPlan.objects.filter(
                user=request.user,
                crop=crop
            ).first()
            
            if crop_plan:
                # Calculate total value
                total_value = None
                if quantity_harvested and market_price:
                    try:
                        total_value = float(quantity_harvested) * float(market_price)
                    except (ValueError, TypeError):
                        pass
                
                YieldRecord.objects.create(
                    crop_plan=crop_plan,
                    harvest_date=harvest_date,
                    quantity_harvested=quantity_harvested,
                    quality_grade=quality_grade,
                    market_price=market_price or None,
                    total_value=total_value,
                    notes=notes
                )
                messages.success(request, 'Yield record created successfully!')
                return redirect('crops:yield_tracking', pk=pk)
            else:
                messages.error(request, 'Please create a crop plan first.')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    # Get user's yield records for this crop
    user_yields = []
    crop_plans = CropPlan.objects.filter(user=request.user, crop=crop)
    for plan in crop_plans:
        yields = YieldRecord.objects.filter(crop_plan=plan).order_by('-harvest_date')
        user_yields.extend(yields)
    
    # Sort by harvest date
    user_yields.sort(key=lambda x: x.harvest_date, reverse=True)
    
    context = {
        'crop': crop,
        'yield_records': user_yields,
    }
    return render(request, 'crops/yield_tracking.html', context)

