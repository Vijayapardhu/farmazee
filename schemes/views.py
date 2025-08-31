from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GovernmentScheme, SchemeApplication


def scheme_list(request):
    """List all government schemes"""
    schemes = GovernmentScheme.objects.filter(is_active=True)
    featured_schemes = GovernmentScheme.objects.filter(is_featured=True, is_active=True)[:3]
    
    # Handle search and filtering
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    state = request.GET.get('state', '')
    
    if search:
        schemes = schemes.filter(name__icontains=search) | schemes.filter(description__icontains=search)
    
    if category:
        schemes = schemes.filter(category=category)
    
    if state:
        schemes = schemes.filter(state=state)
    
    context = {
        'schemes': schemes,
        'featured_schemes': featured_schemes,
        'search': search,
        'category': category,
        'state': state,
    }
    return render(request, 'schemes/list.html', context)


def scheme_detail(request, pk):
    """Scheme detail view"""
    scheme = get_object_or_404(GovernmentScheme, pk=pk, is_active=True)
    context = {'scheme': scheme}
    return render(request, 'schemes/detail.html', context)


@login_required
def scheme_apply(request, pk):
    """Apply for a scheme"""
    scheme = get_object_or_404(GovernmentScheme, pk=pk, is_active=True)
    context = {'scheme': scheme}
    return render(request, 'schemes/apply.html', context)


@login_required
def application_list(request):
    """User's application list"""
    applications = SchemeApplication.objects.filter(applicant_email=request.user.email)
    context = {'applications': applications}
    return render(request, 'schemes/applications.html', context)


def scheme_dashboard(request):
    """User's scheme dashboard"""
    if not request.user.is_authenticated:
        return redirect('account_login')
    
    applications = SchemeApplication.objects.filter(applicant_email=request.user.email)
    context = {'applications': applications}
    return render(request, 'schemes/dashboard.html', context)


def scheme_eligibility(request):
    """Check scheme eligibility"""
    context = {}
    return render(request, 'schemes/eligibility.html', context)


def scheme_calculator(request):
    """Subsidy calculator"""
    context = {}
    return render(request, 'schemes/calculator.html', context)


def scheme_guidelines(request):
    """Scheme guidelines"""
    context = {}
    return render(request, 'schemes/guidelines.html', context)

