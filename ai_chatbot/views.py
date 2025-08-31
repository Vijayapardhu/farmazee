import json
import uuid
import time
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from .models import ChatSession, ChatMessage, FarmerQuery, AIKnowledgeBase


def ai_chat_home(request):
    """AI Chatbot home page"""
    if request.user.is_authenticated:
        # Get or create active chat session
        session, created = ChatSession.objects.get_or_create(
            user=request.user,
            is_active=True,
            defaults={'session_id': str(uuid.uuid4())}
        )
        
        # Get recent messages
        recent_messages = ChatMessage.objects.filter(session=session).order_by('timestamp')[:10]
        
        context = {
            'chat_session': session,
            'recent_messages': recent_messages,
        }
        return render(request, 'ai_chatbot/chat.html', context)
    else:
        return render(request, 'ai_chatbot/chat_guest.html')


@login_required
def chat_interface(request):
    """Main chat interface for authenticated users"""
    # Get or create active chat session
    session, created = ChatSession.objects.get_or_create(
        user=request.user,
        is_active=True,
        defaults={'session_id': str(uuid.uuid4())}
    )
    
    # Get chat history
    chat_messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    
    context = {
        'chat_session': session,
        'chat_messages': chat_messages,
    }
    return render(request, 'ai_chatbot/chat_interface.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Handle sending messages and getting AI responses"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        message_text = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message_text:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create chat session
        session, created = ChatSession.objects.get_or_create(
            user=request.user,
            session_id=session_id,
            defaults={'is_active': True}
        )
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message_text
        )
        
        # Get AI response
        start_time = time.time()
        ai_response = get_ai_response(message_text, request.user)
        response_time = time.time() - start_time
        
        # Save AI response
        ai_message = ChatMessage.objects.create(
            session=session,
            message_type='assistant',
            content=ai_response,
            response_time=response_time
        )
        
        # Store query for analytics
        FarmerQuery.objects.create(
            user=request.user,
            query_text=message_text,
            category=categorize_query(message_text),
            ai_response=ai_response
        )
        
        # Update session
        session.updated_at = timezone.now()
        session.save()
        
        return JsonResponse({
            'success': True,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'timestamp': user_message.timestamp.isoformat(),
            },
            'ai_response': {
                'id': ai_message.id,
                'content': ai_response,
                'timestamp': ai_message.timestamp.isoformat(),
            },
            'response_time': round(response_time, 2)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_ai_response(message, user):
    """Get AI response using OpenRouter API or fallback to knowledge base"""
    try:
        # Try OpenRouter API first
        if hasattr(settings, 'OPENROUTER_API_KEY') and settings.OPENROUTER_API_KEY:
            return get_openrouter_response(message, user)
        else:
            # Fallback to knowledge base
            return get_knowledge_base_response(message)
    except Exception as e:
        # Fallback to predefined responses
        return get_fallback_response(message)


def get_openrouter_response(message, user):
    """Get response from OpenRouter API (ChatGPT)"""
    try:
        # OpenRouter API endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Prepare the message with farming context
        system_prompt = f"""You are Farmazee AI, a helpful agricultural assistant for Indian farmers. 
        You provide practical, actionable advice for farming in Telugu states (Telangana and Andhra Pradesh).
        Focus on local farming practices, crop management, pest control, soil health, and government schemes.
        Keep responses concise, practical, and in simple language that farmers can understand.
        Always provide specific, actionable steps when possible."""
        
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "openai/gpt-3.5-turbo",  # Use GPT-3.5 for cost efficiency
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        return ai_response
        
    except Exception as e:
        # Fallback to knowledge base if API fails
        return get_knowledge_base_response(message)


def get_knowledge_base_response(message):
    """Get response from local knowledge base"""
    # Search knowledge base for relevant information
    keywords = message.lower().split()
    
    # Find relevant knowledge entries
    relevant_entries = AIKnowledgeBase.objects.filter(
        is_active=True
    ).filter(
        keywords__icontains=keywords[0]  # Simple keyword matching
    )[:3]
    
    if relevant_entries:
        response = "Based on our knowledge base:\n\n"
        for entry in relevant_entries:
            response += f"**{entry.title}**\n{entry.content[:200]}...\n\n"
        return response
    else:
        return get_fallback_response(message)


def get_fallback_response(message):
    """Get fallback response when AI is not available"""
    message_lower = message.lower()
    
    # Simple keyword-based responses
    if any(word in message_lower for word in ['rice', 'paddy', 'వరి']):
        return """For rice cultivation in Telugu states:
        • Best sowing time: June-July (Kharif)
        • Use certified seeds
        • Maintain 2-3 inches water level
        • Apply NPK fertilizers as recommended
        • Control weeds regularly
        • Protect from stem borer pests"""
    
    elif any(word in message_lower for word in ['pest', 'disease', 'bug', 'insect']):
        return """For pest and disease management:
        • Use integrated pest management (IPM)
        • Monitor crops regularly
        • Use neem-based products when possible
        • Follow recommended pesticide schedules
        • Maintain crop diversity
        • Contact local agricultural officer for specific issues"""
    
    elif any(word in message_lower for word in ['soil', 'fertilizer', 'nutrient']):
        return """For soil health improvement:
        • Test soil every 2-3 years
        • Use organic matter (compost, farmyard manure)
        • Apply balanced NPK fertilizers
        • Practice crop rotation
        • Use green manure crops
        • Maintain proper pH levels (6.0-7.5)"""
    
    elif any(word in message_lower for word in ['weather', 'rain', 'drought']):
        return """For weather-related farming:
        • Check local weather forecasts regularly
        • Use drought-resistant crop varieties
        • Practice water conservation techniques
        • Use mulching to retain soil moisture
        • Plan irrigation schedules
        • Consider crop insurance"""
    
    else:
        return """Thank you for your question! I'm here to help with farming advice.
        
        I can assist with:
        • Crop management and cultivation
        • Pest and disease control
        • Soil health and fertilizers
        • Weather and irrigation
        • Government schemes and subsidies
        • Market information
        
        Please ask your specific farming question and I'll provide detailed guidance."""


def categorize_query(message):
    """Categorize farmer query for analytics"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['crop', 'plant', 'sow', 'harvest']):
        return 'crop_management'
    elif any(word in message_lower for word in ['pest', 'disease', 'bug', 'insect']):
        return 'pest_control'
    elif any(word in message_lower for word in ['soil', 'fertilizer', 'nutrient']):
        return 'soil_health'
    elif any(word in message_lower for word in ['weather', 'rain', 'drought']):
        return 'weather'
    elif any(word in message_lower for word in ['market', 'price', 'sell']):
        return 'market_info'
    elif any(word in message_lower for word in ['scheme', 'subsidy', 'government']):
        return 'government_schemes'
    else:
        return 'general'


@login_required
def chat_history(request):
    """View chat history for authenticated users"""
    chat_sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
    
    context = {
        'chat_sessions': chat_sessions,
    }
    return render(request, 'ai_chatbot/chat_history.html', context)


@login_required
def query_analytics(request):
    """View query analytics for authenticated users"""
    user_queries = FarmerQuery.objects.filter(user=request.user).order_by('-created_at')
    
    # Basic analytics
    total_queries = user_queries.count()
    category_counts = {}
    for query in user_queries:
        category_counts[query.category] = category_counts.get(query.category, 0) + 1
    
    context = {
        'user_queries': user_queries,
        'total_queries': total_queries,
        'category_counts': category_counts,
    }
    return render(request, 'ai_chatbot/query_analytics.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def rate_response(request):
    """Rate AI response helpfulness"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        query_id = data.get('query_id')
        rating = data.get('rating')  # 1-5 scale
        is_helpful = data.get('is_helpful')  # boolean
        
        if query_id:
            query = FarmerQuery.objects.get(id=query_id, user=request.user)
            query.satisfaction_rating = rating
            query.is_helpful = is_helpful
            query.save()
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Query ID required'}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
