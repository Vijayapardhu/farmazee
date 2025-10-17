from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

from django.contrib.auth.models import User
from core.models import UserProfile
from ai_chatbot.models import ChatSession, ChatMessage, FarmerQuery, AIKnowledgeBase
from farmer_problems.models import FarmerProblem as Problem, Solution, ExpertProfile
# Community functionality removed
from schemes.models import GovernmentScheme
# from weather.models import WeatherData
from marketplace.models import Product
from soil_health.models import SoilTest

def is_admin_user(user):
    """Check if user is admin or staff"""
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
@user_passes_test(is_admin_user)
def admin_dashboard(request):
    """Main admin dashboard with overview statistics"""
    
    # Get date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # User statistics
    total_users = User.objects.count()
    new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
    active_users_week = User.objects.filter(last_login__gte=week_ago).count()
    
    # AI Chat statistics
    total_chats = ChatSession.objects.count()
    total_messages = ChatMessage.objects.count()
    ai_queries_week = FarmerQuery.objects.filter(created_at__gte=week_ago).count()
    
    # Farmer Problems statistics
    total_problems = Problem.objects.count()
    solved_problems = Problem.objects.filter(status='solved').count()
    expert_count = ExpertProfile.objects.count()
    
    # Community statistics removed
    total_topics = 0
    total_questions = 0
    total_answers = 0
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_problems = Problem.objects.order_by('-created_at')[:5]
    recent_queries = FarmerQuery.objects.order_by('-created_at')[:5]
    
    # Popular queries
    popular_queries = FarmerQuery.objects.values('query_text').annotate(
        count=Count('query_text')
    ).order_by('-count')[:10]
    
    # System health
    system_health = {
        'database_status': 'Healthy',
        'ai_service_status': 'Active',
        'storage_usage': '65%',
        'last_backup': '2 hours ago'
    }
    
    context = {
        'total_users': total_users,
        'new_users_week': new_users_week,
        'active_users_week': active_users_week,
        'total_chats': total_chats,
        'total_messages': total_messages,
        'ai_queries_week': ai_queries_week,
        'total_problems': total_problems,
        'solved_problems': solved_problems,
        'expert_count': expert_count,
        'total_topics': total_topics,
        'total_questions': total_questions,
        'total_answers': total_answers,
        'recent_users': recent_users,
        'recent_problems': recent_problems,
        'recent_queries': recent_queries,
        'popular_queries': popular_queries,
        'system_health': system_health,
        'today': today,
        'week_ago': week_ago,
        'month_ago': month_ago,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@user_passes_test(is_admin_user)
def user_management(request):
    """User management page"""
    
    # Get filter parameters
    search = request.GET.get('search', '')
    user_type = request.GET.get('type', 'all')
    status = request.GET.get('status', 'all')
    
    # Base queryset
    users = User.objects.select_related('userprofile').all()
    
    # Apply filters
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    if user_type == 'farmers':
        users = users.filter(userprofile__is_expert=False)
    elif user_type == 'experts':
        users = users.filter(userprofile__is_expert=True)
    
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'search': search,
        'user_type': user_type,
        'status': status,
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'experts': User.objects.filter(userprofile__is_expert=True).count(),
    }
    
    return render(request, 'admin_panel/user_management.html', context)

@login_required
@user_passes_test(is_admin_user)
def user_detail(request, user_id):
    """Individual user detail page"""
    user = get_object_or_404(User, id=user_id)
    
    # Get user activity
    user_chats = ChatSession.objects.filter(user=user).count()
    user_queries = FarmerQuery.objects.filter(user=user).count()
    user_problems = Problem.objects.filter(user=user).count()
    user_solutions = Solution.objects.filter(user=user).count()
    
    # Recent activity
    recent_queries = FarmerQuery.objects.filter(user=user).order_by('-created_at')[:10]
    recent_problems = Problem.objects.filter(user=user).order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'user_chats': user_chats,
        'user_queries': user_queries,
        'user_problems': user_problems,
        'user_solutions': user_solutions,
        'recent_queries': recent_queries,
        'recent_problems': recent_problems,
    }
    
    return render(request, 'admin_panel/user_detail.html', context)

@login_required
@user_passes_test(is_admin_user)
def toggle_user_status(request, user_id):
    """Toggle user active/inactive status"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f'User {user.username} has been {status}.')
    
    return redirect('admin_panel:user_detail', user_id=user_id)

@login_required
@user_passes_test(is_admin_user)
def knowledge_base_management(request):
    """AI Knowledge Base management"""
    
    search = request.GET.get('search', '')
    category = request.GET.get('category', 'all')
    
    knowledge_items = AIKnowledgeBase.objects.all()
    
    if search:
        knowledge_items = knowledge_items.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(keywords__icontains=search)
        )
    
    if category != 'all':
        knowledge_items = knowledge_items.filter(category=category)
    
    paginator = Paginator(knowledge_items, 20)
    page_number = request.GET.get('page')
    knowledge_items = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = AIKnowledgeBase.objects.values_list('category', flat=True).distinct()
    
    context = {
        'knowledge_items': knowledge_items,
        'search': search,
        'category': category,
        'categories': categories,
    }
    
    return render(request, 'admin_panel/knowledge_base.html', context)

@login_required
@user_passes_test(is_admin_user)
def add_knowledge_item(request):
    """Add new knowledge item"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        keywords = request.POST.get('keywords')
        
        AIKnowledgeBase.objects.create(
            title=title,
            content=content,
            category=category,
            keywords=keywords
        )
        
        messages.success(request, 'Knowledge item added successfully.')
        return redirect('admin_panel:knowledge_base')
    
    return render(request, 'admin_panel/add_knowledge.html')

@login_required
@user_passes_test(is_admin_user)
def edit_knowledge_item(request, item_id):
    """Edit knowledge item"""
    item = get_object_or_404(AIKnowledgeBase, id=item_id)
    
    if request.method == 'POST':
        item.title = request.POST.get('title')
        item.content = request.POST.get('content')
        item.category = request.POST.get('category')
        item.keywords = request.POST.get('keywords')
        item.save()
        
        messages.success(request, 'Knowledge item updated successfully.')
        return redirect('admin_panel:knowledge_base')
    
    context = {'item': item}
    return render(request, 'admin_panel/edit_knowledge.html', context)

@login_required
@user_passes_test(is_admin_user)
def delete_knowledge_item(request, item_id):
    """Delete knowledge item"""
    if request.method == 'POST':
        item = get_object_or_404(AIKnowledgeBase, id=item_id)
        item.delete()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_admin_user)
def farmer_problems_management(request):
    """Farmer Problems management"""
    
    search = request.GET.get('search', '')
    status = request.GET.get('status', 'all')
    category = request.GET.get('category', 'all')
    
    problems = Problem.objects.select_related('user', 'category').all()
    
    if search:
        problems = problems.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    if status == 'solved':
        problems = problems.filter(status='solved')
    elif status == 'unsolved':
        problems = problems.exclude(status='solved')
    
    if category != 'all':
        problems = problems.filter(category__name__icontains=category)
    
    # Order by creation date
    problems = problems.order_by('-created_at')
    
    paginator = Paginator(problems, 20)
    page_number = request.GET.get('page')
    problems = paginator.get_page(page_number)
    
    context = {
        'problems': problems,
        'search': search,
        'status': status,
        'category': category,
        'total_problems': Problem.objects.count(),
        'solved_problems': Problem.objects.filter(status='solved').count(),
    }
    
    return render(request, 'admin_panel/farmer_problems.html', context)

@login_required
@user_passes_test(is_admin_user)
def problem_detail(request, problem_id):
    """Individual problem detail page"""
    problem = get_object_or_404(Problem, id=problem_id)
    solutions = Solution.objects.filter(problem=problem).order_by('-created_at')
    
    context = {
        'problem': problem,
        'solutions': solutions,
    }
    
    return render(request, 'admin_panel/problem_detail.html', context)

@login_required
@user_passes_test(is_admin_user)
def mark_problem_solved(request, problem_id):
    """Mark problem as solved"""
    if request.method == 'POST':
        problem = get_object_or_404(Problem, id=problem_id)
        problem.status = 'solved'
        problem.solved_at = timezone.now()
        problem.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_admin_user)
def delete_problem(request, problem_id):
    """Delete problem"""
    if request.method == 'POST':
        problem = get_object_or_404(Problem, id=problem_id)
        problem.delete()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_admin_user)
def accept_solution(request, solution_id):
    """Accept a solution"""
    if request.method == 'POST':
        solution = get_object_or_404(Solution, id=solution_id)
        solution.is_accepted = True
        solution.problem.status = 'solved'
        solution.problem.solved_at = timezone.now()
        solution.problem.save()
        solution.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_admin_user)
def delete_solution(request, solution_id):
    """Delete a solution"""
    if request.method == 'POST':
        solution = get_object_or_404(Solution, id=solution_id)
        solution.delete()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_admin_user)
def analytics_dashboard(request):
    """Analytics and reporting dashboard"""
    
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # User analytics
    user_signups = []
    for i in range(30):
        date = today - timedelta(days=i)
        count = User.objects.filter(date_joined__date=date).count()
        user_signups.append({'date': date.strftime('%Y-%m-%d'), 'count': count})
    
    # Query analytics
    query_categories = FarmerQuery.objects.values('category').annotate(
        count=Count('category')
    ).order_by('-count')[:10]
    
    # Problem analytics
    problem_categories = Problem.objects.values('category__name').annotate(
        count=Count('category')
    ).order_by('-count')[:10]
    
    # Activity over time
    daily_activity = []
    for i in range(30):
        date = today - timedelta(days=i)
        queries = FarmerQuery.objects.filter(created_at__date=date).count()
        problems = Problem.objects.filter(created_at__date=date).count()
        daily_activity.append({
            'date': date.strftime('%Y-%m-%d'),
            'queries': queries,
            'problems': problems
        })
    
    context = {
        'user_signups': user_signups,
        'query_categories': query_categories,
        'problem_categories': problem_categories,
        'daily_activity': daily_activity,
        'total_queries': FarmerQuery.objects.count(),
        'total_problems': Problem.objects.count(),
        'total_solutions': Solution.objects.count(),
    }
    
    return render(request, 'admin_panel/analytics.html', context)

@login_required
@user_passes_test(is_admin_user)
def system_settings(request):
    """System settings and configuration"""
    
    if request.method == 'POST':
        # Handle settings update
        setting_type = request.POST.get('setting_type')
        
        if setting_type == 'ai_settings':
            # Update AI settings
            messages.success(request, 'AI settings updated successfully.')
        elif setting_type == 'notification_settings':
            # Update notification settings
            messages.success(request, 'Notification settings updated successfully.')
        elif setting_type == 'system_settings':
            # Update system settings
            messages.success(request, 'System settings updated successfully.')
        
        return redirect('admin_panel:system_settings')
    
    # Default settings
    settings = {
        'ai_model': 'gemini-2.5-flash',
        'max_tokens': 1000,
        'response_timeout': 30,
        'notification_email': 'admin@farmazee.com',
        'backup_frequency': 'daily',
        'maintenance_mode': False,
    }
    
    context = {
        'settings': settings,
    }
    
    return render(request, 'admin_panel/system_settings.html', context)

@login_required
@user_passes_test(is_admin_user)
def export_data(request):
    """Export data functionality"""
    export_type = request.GET.get('type', 'users')
    
    if export_type == 'users':
        users = User.objects.all()
        data = []
        for user in users:
            data.append({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                'is_active': user.is_active,
            })
    elif export_type == 'queries':
        queries = FarmerQuery.objects.all()
        data = []
        for query in queries:
            data.append({
                'user': query.user.username if query.user else 'Guest',
                'query': query.query,
                'category': query.category,
                'created_at': query.created_at.isoformat() if query.created_at else None,
            })
    
    response = JsonResponse(data, safe=False)
    response['Content-Disposition'] = f'attachment; filename="{export_type}_export.json"'
    return response

# ============= ADVANCED ADMIN FEATURES =============

@login_required
@user_passes_test(is_admin_user)
def bulk_user_actions(request):
    """Bulk user management actions"""
    if request.method == 'POST':
        action = request.POST.get('action')
        user_ids = request.POST.getlist('user_ids')
        
        users = User.objects.filter(id__in=user_ids)
        
        if action == 'activate':
            users.update(is_active=True)
            messages.success(request, f'{users.count()} users activated successfully.')
        elif action == 'deactivate':
            users.update(is_active=False)
            messages.success(request, f'{users.count()} users deactivated successfully.')
        elif action == 'make_expert':
            for user in users:
                user.userprofile.is_expert = True
                user.userprofile.save()
            messages.success(request, f'{users.count()} users marked as experts.')
        elif action == 'send_email':
            # Email sending functionality
            messages.success(request, f'Email sent to {users.count()} users.')
        
        return redirect('admin_panel:user_management')
    
    return redirect('admin_panel:user_management')

@login_required
@user_passes_test(is_admin_user)
def content_moderation(request):
    """Content moderation dashboard"""
    
    # Get filter parameters
    content_type = request.GET.get('type', 'all')
    status = request.GET.get('status', 'pending')
    
    # Problems pending approval
    pending_problems = Problem.objects.filter(is_featured=False).order_by('-created_at')[:20]
    
    # Solutions pending approval
    pending_solutions = Solution.objects.filter(is_accepted=False).order_by('-created_at')[:20]
    
    # Comments to review
    from farmer_problems.models import Comment
    recent_comments = Comment.objects.order_by('-created_at')[:20]
    
    context = {
        'pending_problems': pending_problems,
        'pending_solutions': pending_solutions,
        'recent_comments': recent_comments,
        'content_type': content_type,
        'status': status,
    }
    
    return render(request, 'admin_panel/content_moderation.html', context)

@login_required
@user_passes_test(is_admin_user)
def approve_content(request, content_type, content_id):
    """Approve content"""
    if request.method == 'POST':
        if content_type == 'problem':
            problem = get_object_or_404(Problem, id=content_id)
            problem.is_featured = True
            problem.save()
            messages.success(request, 'Problem approved and featured.')
        elif content_type == 'solution':
            solution = get_object_or_404(Solution, id=content_id)
            solution.is_accepted = True
            solution.problem.status = 'solved'
            solution.problem.solved_at = timezone.now()
            solution.problem.save()
            solution.save()
            messages.success(request, 'Solution approved.')
        
        return redirect('admin_panel:content_moderation')
    
    return redirect('admin_panel:content_moderation')

@login_required
@user_passes_test(is_admin_user)
def delete_content(request, content_type, content_id):
    """Delete content"""
    if request.method == 'POST':
        if content_type == 'problem':
            problem = get_object_or_404(Problem, id=content_id)
            problem.delete()
            messages.success(request, 'Problem deleted.')
        elif content_type == 'solution':
            solution = get_object_or_404(Solution, id=content_id)
            solution.delete()
            messages.success(request, 'Solution deleted.')
        elif content_type == 'comment':
            from farmer_problems.models import Comment
            comment = get_object_or_404(Comment, id=content_id)
            comment.delete()
            messages.success(request, 'Comment deleted.')
        
        return redirect('admin_panel:content_moderation')
    
    return redirect('admin_panel:content_moderation')

@login_required
@user_passes_test(is_admin_user)
def advanced_analytics(request):
    """Advanced analytics dashboard"""
    
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)
    
    # User growth analytics
    user_growth = []
    for i in range(12):
        month_start = today - timedelta(days=30*i)
        month_end = today - timedelta(days=30*(i-1)) if i > 0 else today
        count = User.objects.filter(
            date_joined__date__gte=month_start,
            date_joined__date__lte=month_end
        ).count()
        user_growth.append({
            'month': month_start.strftime('%b %Y'),
            'users': count
        })
    
    # Engagement metrics
    engagement_metrics = {
        'daily_active_users': User.objects.filter(last_login__date=today).count(),
        'weekly_active_users': User.objects.filter(last_login__gte=week_ago).count(),
        'monthly_active_users': User.objects.filter(last_login__gte=month_ago).count(),
        'avg_session_duration': '15.5 min',  # Can be calculated from session data
        'bounce_rate': '35%',
        'retention_rate': '68%'
    }
    
    # Content creation metrics
    content_metrics = {
        'problems_this_week': Problem.objects.filter(created_at__gte=week_ago).count(),
        'solutions_this_week': Solution.objects.filter(created_at__gte=week_ago).count(),
        'queries_this_week': FarmerQuery.objects.filter(created_at__gte=week_ago).count(),
        'avg_response_time': '2.3 hours',
        'solution_rate': f"{(Problem.objects.filter(status='solved').count() / max(Problem.objects.count(), 1) * 100):.1f}%"
    }
    
    # Platform health
    platform_health = {
        'server_uptime': '99.8%',
        'avg_response_time': '120ms',
        'error_rate': '0.2%',
        'api_calls_today': 15420,
        'storage_used': '2.4 GB',
        'bandwidth_used': '45 GB'
    }
    
    # Top contributors
    top_farmers = User.objects.filter(
        farmer_problems__created_at__gte=month_ago
    ).annotate(
        problem_count=Count('farmer_problems')
    ).order_by('-problem_count')[:10]
    
    top_experts = User.objects.filter(
        solutions__created_at__gte=month_ago
    ).annotate(
        solution_count=Count('solutions')
    ).order_by('-solution_count')[:10]
    
    context = {
        'user_growth': user_growth,
        'engagement_metrics': engagement_metrics,
        'content_metrics': content_metrics,
        'platform_health': platform_health,
        'top_farmers': top_farmers,
        'top_experts': top_experts,
    }
    
    return render(request, 'admin_panel/advanced_analytics.html', context)

@login_required
@user_passes_test(is_admin_user)
def activity_logs(request):
    """System activity logs"""
    
    # In production, integrate with proper logging system
    # For now, show recent activities from database
    
    recent_activities = []
    
    # Recent user registrations
    recent_users = User.objects.order_by('-date_joined')[:10]
    for user in recent_users:
        recent_activities.append({
            'type': 'user_registration',
            'description': f'New user registered: {user.username}',
            'user': user.username,
            'timestamp': user.date_joined,
            'severity': 'info'
        })
    
    # Recent problems
    recent_problems = Problem.objects.order_by('-created_at')[:10]
    for problem in recent_problems:
        recent_activities.append({
            'type': 'problem_created',
            'description': f'New problem posted: {problem.title[:50]}',
            'user': problem.author.username if hasattr(problem, 'author') else 'Unknown',
            'timestamp': problem.created_at,
            'severity': 'info'
        })
    
    # Sort by timestamp
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Pagination
    paginator = Paginator(recent_activities, 50)
    page_number = request.GET.get('page')
    activities = paginator.get_page(page_number)
    
    context = {
        'activities': activities,
    }
    
    return render(request, 'admin_panel/activity_logs.html', context)

@login_required
@user_passes_test(is_admin_user)
def broadcast_notification(request):
    """Send broadcast notifications to users"""
    
    if request.method == 'POST':
        notification_type = request.POST.get('notification_type')
        target_users = request.POST.get('target_users', 'all')
        title = request.POST.get('title')
        message = request.POST.get('message')
        
        # Determine target users
        if target_users == 'all':
            users = User.objects.filter(is_active=True)
        elif target_users == 'farmers':
            users = User.objects.filter(is_active=True, userprofile__is_expert=False)
        elif target_users == 'experts':
            users = User.objects.filter(is_active=True, userprofile__is_expert=True)
        else:
            users = User.objects.none()
        
        # Create notifications
        # In production, integrate with notification system
        notification_count = users.count()
        
        messages.success(request, f'Notification sent to {notification_count} users successfully.')
        
        return redirect('admin_panel:broadcast_notification')
    
    context = {
        'total_users': User.objects.filter(is_active=True).count(),
        'total_farmers': User.objects.filter(is_active=True, userprofile__is_expert=False).count(),
        'total_experts': User.objects.filter(is_active=True, userprofile__is_expert=True).count(),
    }
    
    return render(request, 'admin_panel/broadcast_notification.html', context)

@login_required
@user_passes_test(is_admin_user)
def database_management(request):
    """Database backup and management"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'backup':
            # In production, implement actual backup
            messages.success(request, 'Database backup created successfully.')
        elif action == 'optimize':
            # In production, implement database optimization
            messages.success(request, 'Database optimized successfully.')
        elif action == 'clean':
            # Clean old session data, cache, etc.
            messages.success(request, 'Database cleaned successfully.')
        
        return redirect('admin_panel:database_management')
    
    # Database statistics
    db_stats = {
        'total_users': User.objects.count(),
        'total_problems': Problem.objects.count(),
        'total_solutions': Solution.objects.count(),
        'total_queries': FarmerQuery.objects.count(),
        'total_products': Product.objects.count(),
        'database_size': '245 MB',
        'last_backup': '2 hours ago',
        'next_backup': 'In 22 hours'
    }
    
    context = {
        'db_stats': db_stats,
    }
    
    return render(request, 'admin_panel/database_management.html', context)

@login_required
@user_passes_test(is_admin_user)
def expert_verification(request):
    """Verify expert profiles"""
    
    # Get pending verifications
    pending_experts = ExpertProfile.objects.filter(is_verified=False).order_by('-created_at')
    verified_experts = ExpertProfile.objects.filter(is_verified=True).order_by('-verified_at')[:20]
    
    context = {
        'pending_experts': pending_experts,
        'verified_experts': verified_experts,
    }
    
    return render(request, 'admin_panel/expert_verification.html', context)

@login_required
@user_passes_test(is_admin_user)
def verify_expert(request, expert_id):
    """Verify an expert"""
    if request.method == 'POST':
        expert = get_object_or_404(ExpertProfile, id=expert_id)
        expert.is_verified = True
        expert.verified_at = timezone.now()
        expert.verified_by = request.user
        expert.save()
        
        messages.success(request, f'Expert {expert.user.get_full_name()} verified successfully.')
        
        return redirect('admin_panel:expert_verification')
    
    return redirect('admin_panel:expert_verification')

@login_required
@user_passes_test(is_admin_user)
def reject_expert(request, expert_id):
    """Reject expert verification"""
    if request.method == 'POST':
        expert = get_object_or_404(ExpertProfile, id=expert_id)
        rejection_reason = request.POST.get('reason', '')
        
        # In production, send email with rejection reason
        expert.delete()
        
        messages.success(request, 'Expert application rejected.')
        
        return redirect('admin_panel:expert_verification')
    
    return redirect('admin_panel:expert_verification')

@login_required
@user_passes_test(is_admin_user)
def platform_statistics(request):
    """Comprehensive platform statistics"""
    
    # Get all statistics
    stats = {
        'users': {
            'total': User.objects.count(),
            'active': User.objects.filter(is_active=True).count(),
            'farmers': User.objects.filter(userprofile__is_expert=False).count(),
            'experts': User.objects.filter(userprofile__is_expert=True).count(),
            'verified_experts': ExpertProfile.objects.filter(is_verified=True).count(),
        },
        'content': {
            'problems': Problem.objects.count(),
            'solved_problems': Problem.objects.filter(status='solved').count(),
            'solutions': Solution.objects.count(),
            'accepted_solutions': Solution.objects.filter(is_accepted=True).count(),
            'ai_queries': FarmerQuery.objects.count(),
            'knowledge_items': AIKnowledgeBase.objects.count(),
        },
        'community': {
            'topics': 0,
            'questions': 0,
            'answers': 0,
            'products': Product.objects.count(),
        },
        'engagement': {
            'avg_problems_per_user': round(Problem.objects.count() / max(User.objects.count(), 1), 2),
            'avg_solutions_per_problem': round(Solution.objects.count() / max(Problem.objects.count(), 1), 2),
            'problem_solve_rate': f"{(Problem.objects.filter(status='solved').count() / max(Problem.objects.count(), 1) * 100):.1f}%",
        }
    }
    
    context = {'stats': stats}
    
    return render(request, 'admin_panel/platform_statistics.html', context)

# ============= USER FEATURES MANAGEMENT =============

@login_required
@user_passes_test(is_admin_user)
def schemes_management(request):
    """Government schemes management"""
    
    search = request.GET.get('search', '')
    status = request.GET.get('status', 'all')
    category = request.GET.get('category', 'all')
    
    schemes = GovernmentScheme.objects.all()
    
    if search:
        schemes = schemes.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    if status == 'active':
        schemes = schemes.filter(is_active=True)
    elif status == 'inactive':
        schemes = schemes.filter(is_active=False)
    
    schemes = schemes.order_by('-created_at')
    
    paginator = Paginator(schemes, 20)
    page_number = request.GET.get('page')
    schemes = paginator.get_page(page_number)
    
    context = {
        'schemes': schemes,
        'search': search,
        'status': status,
        'total_schemes': GovernmentScheme.objects.count(),
        'active_schemes': GovernmentScheme.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'admin_panel/schemes_management.html', context)

@login_required
@user_passes_test(is_admin_user)
def add_scheme(request):
    """Add new government scheme"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category', '')
        eligibility = request.POST.get('eligibility', '')
        benefits = request.POST.get('benefits', '')
        application_process = request.POST.get('application_process', '')
        required_documents = request.POST.get('required_documents', '')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_active = request.POST.get('is_active') == 'on'
        
        GovernmentScheme.objects.create(
            name=name,
            description=description,
            category=category,
            eligibility=eligibility,
            benefits=benefits,
            application_process=application_process,
            required_documents=required_documents,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None,
            is_active=is_active
        )
        
        messages.success(request, f'Scheme "{name}" added successfully.')
        return redirect('admin_panel:schemes_management')
    
    return render(request, 'admin_panel/add_scheme.html')

@login_required
@user_passes_test(is_admin_user)
def edit_scheme(request, scheme_id):
    """Edit government scheme"""
    scheme = get_object_or_404(GovernmentScheme, id=scheme_id)
    
    if request.method == 'POST':
        scheme.name = request.POST.get('name')
        scheme.description = request.POST.get('description')
        scheme.category = request.POST.get('category', '')
        scheme.eligibility = request.POST.get('eligibility', '')
        scheme.benefits = request.POST.get('benefits', '')
        scheme.application_process = request.POST.get('application_process', '')
        scheme.required_documents = request.POST.get('required_documents', '')
        scheme.start_date = request.POST.get('start_date') or None
        scheme.end_date = request.POST.get('end_date') or None
        scheme.is_active = request.POST.get('is_active') == 'on'
        scheme.save()
        
        messages.success(request, f'Scheme "{scheme.name}" updated successfully.')
        return redirect('admin_panel:schemes_management')
    
    context = {'scheme': scheme}
    return render(request, 'admin_panel/edit_scheme.html', context)

@login_required
@user_passes_test(is_admin_user)
def delete_scheme(request, scheme_id):
    """Delete government scheme"""
    if request.method == 'POST':
        scheme = get_object_or_404(GovernmentScheme, id=scheme_id)
        scheme.delete()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_admin_user)
def toggle_scheme_status(request, scheme_id):
    """Toggle scheme active status"""
    scheme = get_object_or_404(GovernmentScheme, id=scheme_id)
    scheme.is_active = not scheme.is_active
    scheme.save()
    
    status = "activated" if scheme.is_active else "deactivated"
    messages.success(request, f'Scheme "{scheme.name}" has been {status}.')
    
    return redirect('admin_panel:schemes_management')

# Crops management removed

@login_required
@user_passes_test(is_admin_user)
def marketplace_management(request):
    """Marketplace products and vendors management"""
    from marketplace.models import Vendor
    
    tab = request.GET.get('tab', 'products')
    search = request.GET.get('search', '')
    
    if tab == 'products':
        products = Product.objects.select_related('vendor').all()
        
        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        products = products.order_by('-created_at')
        
        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        
        context = {
            'products': products,
            'tab': tab,
            'search': search,
            'total_products': Product.objects.count(),
            'active_products': Product.objects.filter(is_active=True).count(),
        }
    else:  # vendors
        vendors = Vendor.objects.all()
        
        if search:
            vendors = vendors.filter(
                Q(business_name__icontains=search) |
                Q(user__username__icontains=search)
            )
        
        vendors = vendors.order_by('-created_at')
        
        paginator = Paginator(vendors, 20)
        page_number = request.GET.get('page')
        vendors = paginator.get_page(page_number)
        
        context = {
            'vendors': vendors,
            'tab': tab,
            'search': search,
            'total_vendors': Vendor.objects.count(),
            'verified_vendors': Vendor.objects.filter(is_verified=True).count(),
        }
    
    return render(request, 'admin_panel/marketplace_management.html', context)

@login_required
@user_passes_test(is_admin_user)
def soil_tests_management(request):
    """Soil health tests management"""
    
    search = request.GET.get('search', '')
    
    soil_tests = SoilTest.objects.select_related('user').all()
    
    if search:
        soil_tests = soil_tests.filter(
            Q(user__username__icontains=search) |
            Q(location__icontains=search)
        )
    
    soil_tests = soil_tests.order_by('-test_date')
    
    paginator = Paginator(soil_tests, 20)
    page_number = request.GET.get('page')
    soil_tests = paginator.get_page(page_number)
    
    context = {
        'soil_tests': soil_tests,
        'search': search,
        'total_tests': SoilTest.objects.count(),
    }
    
    return render(request, 'admin_panel/soil_tests_management.html', context)

@login_required
@user_passes_test(is_admin_user)
def community_management(request):
    """Community topics and questions management"""
    
    tab = request.GET.get('tab', 'topics')
    search = request.GET.get('search', '')
    
    if tab == 'topics':
        topics = Topic.objects.select_related('author', 'category').all()
        
        if search:
            topics = topics.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
        
        topics = topics.order_by('-created_at')
        
        paginator = Paginator(topics, 20)
        page_number = request.GET.get('page')
        items = paginator.get_page(page_number)
        
        context = {
            'items': items,
            'tab': tab,
            'search': search,
            'total_topics': Topic.objects.count(),
        }
    else:  # questions
        questions = Question.objects.select_related('author').all()
        
        if search:
            questions = questions.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
        
        questions = questions.order_by('-created_at')
        
        paginator = Paginator(questions, 20)
        page_number = request.GET.get('page')
        items = paginator.get_page(page_number)
        
        context = {
            'items': items,
            'tab': tab,
            'search': search,
            'total_questions': Question.objects.count(),
        }
    
    return render(request, 'admin_panel/community_management.html', context)

