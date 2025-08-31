from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ForumCategory, ForumTopic, Question, Expert, CommunityEvent


def community_home(request):
    """Community home page"""
    recent_topics = ForumTopic.objects.filter(is_active=True)[:5]
    recent_questions = Question.objects.filter(status='open')[:5]
    upcoming_events = CommunityEvent.objects.filter(is_active=True)[:3]
    
    # Get community stats
    total_members = 1234  # Placeholder - should come from User model
    total_discussions = ForumTopic.objects.filter(is_active=True).count()
    total_questions = Question.objects.count()
    total_events = CommunityEvent.objects.filter(is_active=True).count()
    
    context = {
        'recent_topics': recent_topics,
        'recent_questions': recent_questions,
        'upcoming_events': upcoming_events,
        'total_members': total_members,
        'total_discussions': total_discussions,
        'total_questions': total_questions,
        'total_events': total_events,
    }
    return render(request, 'community/home.html', context)


def forum_list(request):
    """Forum categories list"""
    categories = ForumCategory.objects.filter(is_active=True)
    context = {'categories': categories}
    return render(request, 'community/forum_list.html', context)


def forum_detail(request, pk):
    """Forum category detail with topics"""
    category = get_object_or_404(ForumCategory, pk=pk, is_active=True)
    topics = category.topics.filter(is_active=True)
    context = {'category': category, 'topics': topics}
    return render(request, 'community/forum_detail.html', context)


def topic_detail(request, pk):
    """Topic detail view"""
    topic = get_object_or_404(ForumTopic, pk=pk, is_active=True)
    context = {'topic': topic}
    return render(request, 'community/topic_detail.html', context)


def qa_list(request):
    """Q&A list"""
    questions = Question.objects.all().order_by('-created_at')
    context = {'questions': questions}
    return render(request, 'community/qa_list.html', context)


def qa_detail(request, pk):
    """Q&A detail"""
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    context = {'question': question, 'answers': answers}
    return render(request, 'community/qa_detail.html', context)


def question_detail(request, pk):
    """Question detail view"""
    question = get_object_or_404(Question, pk=pk)
    context = {'question': question}
    return render(request, 'community/question_detail.html', context)


@login_required
def ask_question(request):
    """Ask a new question"""
    if request.method == 'POST':
        # Handle form submission
        pass
    context = {}
    return render(request, 'community/ask_question.html', context)


def expert_list(request):
    """Expert list"""
    experts = Expert.objects.filter(is_active=True)
    context = {'experts': experts}
    return render(request, 'community/experts.html', context)


def expert_detail(request, pk):
    """Expert detail view"""
    expert = get_object_or_404(Expert, pk=pk, is_active=True)
    context = {'expert': expert}
    return render(request, 'community/expert_detail.html', context)


def event_list(request):
    """Community events list"""
    events = CommunityEvent.objects.filter(is_active=True)
    context = {'events': events}
    return render(request, 'community/events.html', context)


def event_detail(request, pk):
    """Event detail"""
    event = get_object_or_404(CommunityEvent, pk=pk, is_active=True)
    context = {'event': event}
    return render(request, 'community/event_detail.html', context)


def topics_list(request):
    """Topics list"""
    topics = ForumTopic.objects.filter(is_active=True).order_by('-created_at')
    context = {'topics': topics}
    return render(request, 'community/topics.html', context)


def questions_list(request):
    """Questions list"""
    questions = Question.objects.all().order_by('-created_at')
    context = {'questions': questions}
    return render(request, 'community/questions.html', context)
