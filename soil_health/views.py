from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import (
    SoilTip, SoilTest, SoilTestResult, SoilHealthRecord,
    FertilizerRecommendation, SoilImprovement, SoilConservation,
    SoilMonitoringSchedule, SoilHealthAlert, SoilType
)


def soil_home(request):
    """Soil health home page"""
    featured_tips = SoilTip.objects.filter(is_featured=True, is_active=True)[:3]
    soil_types = SoilType.objects.all()[:5]
    recent_tests = SoilTest.objects.all()[:3] if request.user.is_authenticated else []
    
    context = {
        'featured_tips': featured_tips,
        'soil_types': soil_types,
        'recent_tests': recent_tests,
    }
    return render(request, 'soil_health/home.html', context)


def tip_list(request):
    """List soil health tips"""
    tips = SoilTip.objects.filter(is_active=True)
    context = {'tips': tips}
    return render(request, 'soil_health/tips.html', context)


def tip_detail(request, pk):
    """Soil tip detail"""
    tip = get_object_or_404(SoilTip, pk=pk, is_active=True)
    context = {'tip': tip}
    return render(request, 'soil_health/tip_detail.html', context)


@login_required
def soil_test_list(request):
    """List user's soil tests with enhanced analytics"""
    try:
        tests = SoilTest.objects.filter(user=request.user)
        
        # Calculate statistics
        completed_tests_count = tests.filter(is_completed=True).count()
        pending_tests_count = tests.filter(is_completed=False).count()
        
        # Calculate average health score from soil health records
        health_records = SoilHealthRecord.objects.filter(user=request.user)
        avg_health_score = 0
        if health_records.exists():
            total_score = sum(record.health_score or 0 for record in health_records)
            avg_health_score = total_score / health_records.count()
        
        # Get latest test for insights
        latest_test = tests.first()
        
        context = {
            'soil_tests': tests,
            'completed_tests_count': completed_tests_count,
            'pending_tests_count': pending_tests_count,
            'avg_health_score': avg_health_score,
            'latest_test': latest_test,
        }
        return render(request, 'soil_health/tests.html', context)
    except Exception as e:
        # Log the error for debugging
        print(f"Error in soil_test_list: {e}")
        # Return a simple error context
        context = {
            'soil_tests': [],
            'completed_tests_count': 0,
            'pending_tests_count': 0,
            'avg_health_score': 0,
            'latest_test': None,
            'error_message': 'An error occurred while loading soil tests.'
        }
        return render(request, 'soil_health/tests.html', context)


@login_required
def soil_test_detail(request, pk):
    """Soil test detail"""
    test = get_object_or_404(SoilTest, pk=pk, user=request.user)
    results = SoilTestResult.objects.filter(soil_test=test)
    context = {'test': test, 'results': results}
    return render(request, 'soil_health/test_detail.html', context)


@login_required
def soil_health_record(request):
    """User's soil health records"""
    records = SoilHealthRecord.objects.filter(user=request.user)
    context = {'records': records}
    return render(request, 'soil_health/records.html', context)


def soil_improvement_list(request):
    """List soil improvement methods"""
    if request.user.is_authenticated:
        improvements = SoilImprovement.objects.filter(user=request.user)
    else:
        improvements = SoilImprovement.objects.all()
    context = {'improvements': improvements}
    return render(request, 'soil_health/improvements.html', context)


def soil_conservation_list(request):
    """List soil conservation methods"""
    conservation_methods = SoilConservation.objects.filter(is_active=True)
    context = {'conservation_methods': conservation_methods}
    return render(request, 'soil_health/conservation.html', context)


@login_required
def soil_monitoring_schedule(request):
    """User's soil monitoring schedule"""
    schedules = SoilMonitoringSchedule.objects.filter(user=request.user, is_active=True)
    context = {'schedules': schedules}
    return render(request, 'soil_health/monitoring_schedule.html', context)


@login_required
def soil_health_alerts(request):
    """User's soil health alerts"""
    alerts = SoilHealthAlert.objects.filter(user=request.user, is_resolved=False)
    context = {'alerts': alerts}
    return render(request, 'soil_health/alerts.html', context)


def soil_type_list(request):
    """List soil types"""
    soil_types = SoilType.objects.all()
    context = {'soil_types': soil_types}
    return render(request, 'soil_health/soil_types.html', context)


def soil_type_detail(request, pk):
    """Soil type detail"""
    soil_type = get_object_or_404(SoilType, pk=pk)
    context = {'soil_type': soil_type}
    return render(request, 'soil_health/soil_type_detail.html', context)


def soil_recommendations(request):
    """Soil recommendations"""
    context = {}
    return render(request, 'soil_health/recommendations.html', context)


def soil_monitoring(request):
    """Soil monitoring"""
    context = {}
    return render(request, 'soil_health/monitoring.html', context)


@login_required
def schedule_soil_test(request):
    """Schedule a new soil test"""
    if request.method == 'POST':
        try:
            # Create new soil test
            test = SoilTest.objects.create(
                user=request.user,
                test_type=request.POST.get('test_type'),
                test_date=request.POST.get('test_date'),
                location=request.POST.get('location'),
                soil_depth=request.POST.get('soil_depth'),
                sample_weight=request.POST.get('sample_weight'),
                notes=request.POST.get('notes'),
                is_completed=False
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Soil test scheduled successfully',
                'test_id': test.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })
