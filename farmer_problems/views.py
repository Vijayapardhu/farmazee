"""
Views for Farmer Problems & Solutions
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count, Prefetch
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
import json

from .models import (
    FarmerProblem, ProblemCategory, Solution, Comment,
    Vote, ProblemImage, SolutionImage, ExpertProfile, Tag
)
from .supabase_storage import get_storage_service


def problem_list(request):
    """List all problems with filtering and search"""
    # Get filter parameters
    category_slug = request.GET.get('category')
    status = request.GET.get('status')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Base queryset
    problems = FarmerProblem.objects.select_related('author', 'category').annotate(
        vote_count=Count('votes', filter=Q(votes__vote_type='up')) - Count('votes', filter=Q(votes__vote_type='down')),
        solution_count=Count('solutions')
    )
    
    # Apply filters
    if category_slug:
        problems = problems.filter(category__slug=category_slug)
    
    if status:
        problems = problems.filter(status=status)
    
    if search_query:
        problems = problems.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(crop_type__icontains=search_query)
        )
    
    # Sorting
    sort_options = {
        '-created_at': '-created_at',
        'oldest': 'created_at',
        'most_voted': '-vote_count',
        'most_solutions': '-solution_count',
    }
    problems = problems.order_by(sort_options.get(sort_by, '-created_at'))
    
    # Pagination
    paginator = Paginator(problems, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = ProblemCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'current_status': status,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'farmer_problems/problem_list.html', context)


def problem_detail(request, slug):
    """View single problem with all solutions"""
    problem = get_object_or_404(
        FarmerProblem.objects.select_related('author', 'category').prefetch_related(
            'images',
            'tags',
            Prefetch('solutions', queryset=Solution.objects.select_related('author').prefetch_related('images'))
        ),
        slug=slug
    )
    
    # Increment views
    problem.views_count += 1
    problem.save(update_fields=['views_count'])
    
    # Get user's vote if logged in
    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(user=request.user, problem=problem).first()
    
    # Get solutions with votes
    solutions = problem.solutions.annotate(
        vote_count=Count('votes', filter=Q(votes__vote_type='up')) - Count('votes', filter=Q(votes__vote_type='down'))
    )
    
    context = {
        'problem': problem,
        'solutions': solutions,
        'user_vote': user_vote,
    }
    
    return render(request, 'farmer_problems/problem_detail.html', context)


@login_required
def problem_create(request):
    """Create new problem"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            category_id = request.POST.get('category')
            location = request.POST.get('location', '')
            crop_type = request.POST.get('crop_type', '')
            
            # Create problem
            problem = FarmerProblem.objects.create(
                title=title,
                slug=slugify(title) + '-' + str(timezone.now().timestamp()).replace('.', ''),
                description=description,
                author=request.user,
                category_id=category_id if category_id else None,
                location=location,
                crop_type=crop_type,
            )
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            if images:
                storage_service = get_storage_service()
                for i, image in enumerate(images):
                    result = storage_service.upload_image(image, folder='problems')
                    if result['success']:
                        ProblemImage.objects.create(
                            problem=problem,
                            image_url=result['url'],
                            order=i
                        )
            
            # Handle tags
            tags_input = request.POST.get('tags', '')
            if tags_input:
                tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    problem.tags.add(tag)
            
            messages.success(request, 'Problem posted successfully!')
            return redirect('farmer_problems:detail', slug=problem.slug)
            
        except Exception as e:
            messages.error(request, f'Error creating problem: {str(e)}')
            return redirect('farmer_problems:create')
    
    # GET request
    categories = ProblemCategory.objects.all()
    context = {'categories': categories}
    return render(request, 'farmer_problems/problem_create.html', context)


@login_required
@require_http_methods(["POST"])
def solution_create(request, problem_slug):
    """Add solution to a problem"""
    problem = get_object_or_404(FarmerProblem, slug=problem_slug)
    
    try:
        content = request.POST.get('content')
        
        # Check if user is expert
        is_expert = hasattr(request.user, 'farming_expert_profile') and request.user.farming_expert_profile.is_verified
        expert_badge = ''
        if is_expert:
            expert_badge = request.user.farming_expert_profile.get_expert_type_display()
        
        # Create solution
        solution = Solution.objects.create(
            problem=problem,
            author=request.user,
            content=content,
            is_expert=is_expert,
            expert_badge=expert_badge
        )
        
        # Handle image uploads
        images = request.FILES.getlist('images')
        if images:
            storage_service = get_storage_service()
            for i, image in enumerate(images):
                result = storage_service.upload_image(image, folder='solutions')
                if result['success']:
                    SolutionImage.objects.create(
                        solution=solution,
                        image_url=result['url'],
                        order=i
                    )
        
        # Update expert stats if applicable
        if is_expert:
            expert_profile = request.user.farming_expert_profile
            expert_profile.solutions_count += 1
            expert_profile.save(update_fields=['solutions_count'])
        
        messages.success(request, 'Solution added successfully!')
        
    except Exception as e:
        messages.error(request, f'Error adding solution: {str(e)}')
    
    return redirect('farmer_problems:detail', slug=problem_slug)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def vote(request):
    """Handle upvote/downvote"""
    try:
        data = json.loads(request.body)
        content_type = data.get('content_type')  # 'problem' or 'solution'
        content_id = data.get('content_id')
        vote_type = data.get('vote_type')  # 'up' or 'down'
        
        if content_type == 'problem':
            problem = get_object_or_404(FarmerProblem, id=content_id)
            vote_obj, created = Vote.objects.get_or_create(
                user=request.user,
                problem=problem,
                defaults={'content_type': 'problem', 'vote_type': vote_type}
            )
            if not created:
                if vote_obj.vote_type == vote_type:
                    # Remove vote if clicking same button
                    vote_obj.delete()
                    return JsonResponse({'success': True, 'action': 'removed'})
                else:
                    # Change vote
                    vote_obj.vote_type = vote_type
                    vote_obj.save()
            
            # Get new vote count
            vote_count = problem.votes.filter(vote_type='up').count() - problem.votes.filter(vote_type='down').count()
            
        elif content_type == 'solution':
            solution = get_object_or_404(Solution, id=content_id)
            vote_obj, created = Vote.objects.get_or_create(
                user=request.user,
                solution=solution,
                defaults={'content_type': 'solution', 'vote_type': vote_type}
            )
            if not created:
                if vote_obj.vote_type == vote_type:
                    vote_obj.delete()
                    return JsonResponse({'success': True, 'action': 'removed'})
                else:
                    vote_obj.vote_type = vote_type
                    vote_obj.save()
            
            # Get new vote count
            vote_count = solution.votes.filter(vote_type='up').count() - solution.votes.filter(vote_type='down').count()
        
        else:
            return JsonResponse({'success': False, 'error': 'Invalid content type'}, status=400)
        
        return JsonResponse({
            'success': True,
            'vote_count': vote_count,
            'action': 'voted'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def accept_solution(request, solution_id):
    """Mark solution as accepted (only problem author can do this)"""
    solution = get_object_or_404(Solution, id=solution_id)
    problem = solution.problem
    
    if request.user != problem.author:
        return JsonResponse({'success': False, 'error': 'Only problem author can accept solutions'}, status=403)
    
    # Unaccept all other solutions
    problem.solutions.update(is_accepted=False)
    
    # Accept this solution
    solution.is_accepted = True
    solution.save()
    
    # Update problem status
    problem.status = 'solved'
    problem.solved_at = timezone.now()
    problem.save()
    
    # Update expert stats
    if solution.is_expert and hasattr(solution.author, 'farming_expert_profile'):
        expert_profile = solution.author.farming_expert_profile
        expert_profile.accepted_solutions_count += 1
        expert_profile.reputation_score += 10
        expert_profile.save()
    
    return JsonResponse({'success': True})


def expert_list(request):
    """List all verified experts"""
    experts = ExpertProfile.objects.filter(is_verified=True).select_related('user')
    
    context = {'experts': experts}
    return render(request, 'farmer_problems/expert_list.html', context)


@login_required
def become_expert(request):
    """Application to become an expert"""
    if hasattr(request.user, 'farming_expert_profile'):
        messages.info(request, 'You already have an expert profile')
        return redirect('farmer_problems:list')
    
    if request.method == 'POST':
        try:
            expert_type = request.POST.get('expert_type')
            qualification = request.POST.get('qualification')
            institution = request.POST.get('institution', '')
            years_of_experience = int(request.POST.get('years_of_experience', 0))
            specialization = request.POST.get('specialization', '')
            bio = request.POST.get('bio', '')
            
            # Create expert profile
            expert_profile = ExpertProfile.objects.create(
                user=request.user,
                expert_type=expert_type,
                qualification=qualification,
                institution=institution,
                years_of_experience=years_of_experience,
                specialization=specialization,
                bio=bio,
            )
            
            # Handle verification document
            if 'verification_document' in request.FILES:
                storage_service = get_storage_service()
                result = storage_service.upload_image(
                    request.FILES['verification_document'],
                    folder='expert_verifications'
                )
                if result['success']:
                    expert_profile.verification_document_url = result['url']
                    expert_profile.save()
            
            messages.success(request, 'Expert application submitted! Awaiting verification.')
            return redirect('farmer_problems:list')
            
        except Exception as e:
            messages.error(request, f'Error submitting application: {str(e)}')
    
    return render(request, 'farmer_problems/become_expert.html')


def category_list(request):
    """List all categories"""
    categories = ProblemCategory.objects.annotate(
        problem_count=Count('problems')
    )
    
    context = {'categories': categories}
    return render(request, 'farmer_problems/category_list.html', context)
