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
from . import rule_based
from django.utils import timezone
from .models import ChatSession, ChatMessage, FarmerQuery, AIKnowledgeBase
from .gemini_service import get_gemini_service
import datetime


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
        
        # Estimate tokens (rough estimate for tracking)
        tokens_used = len(message_text.split()) + len(ai_response.split())
        
        # Save AI response
        ai_message = ChatMessage.objects.create(
            session=session,
            message_type='assistant',
            content=ai_response,
            response_time=response_time,
            tokens_used=tokens_used
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


@login_required
@require_http_methods(["GET", "POST"])
def start_trial(request):
    """Start a 14-day farmer trial stored in the user's session."""
    try:
        now = timezone.now()
        expires_at = now + datetime.timedelta(days=14)

        request.session['trial_active'] = True
        request.session['trial_started_at'] = now.isoformat()
        request.session['trial_expires_at'] = expires_at.isoformat()

        return JsonResponse({
            'success': True,
            'trial_active': True,
            'trial_started_at': now.isoformat(),
            'trial_expires_at': expires_at.isoformat(),
            'message': 'Your 14-day farmer trial has started.'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_ai_response(message, user):
    """Get AI response using Gemini AI or fallback to knowledge base"""
    try:
        # Use deterministic rule-based mode if enabled (no AI/ML, offline-friendly)
        if getattr(settings, 'USE_RULE_BASED', False):
            rb = rule_based.reply(message, session_id="")
            return rb.get('content', 'I can show topics with /menu')
        
        # Try Gemini AI first
        if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
            return get_gemini_response(message, user)
        # Fallback to OpenRouter if Gemini is not available
        elif hasattr(settings, 'OPENROUTER_API_KEY') and settings.OPENROUTER_API_KEY:
            return get_openrouter_response(message, user)
        else:
            # Fallback to knowledge base
            return get_knowledge_base_response(message)
    except Exception as e:
        # Fallback to predefined responses
        return get_fallback_response(message)


def get_gemini_response(message, user):
    """Get response from Gemini AI"""
    try:
        # Get conversation history for context
        active_session = ChatSession.objects.filter(
            user=user, 
            is_active=True
        ).first()
        
        conversation_history = []
        if active_session:
            recent_messages = ChatMessage.objects.filter(
                session=active_session
            ).order_by('-timestamp')[:10]
            
            for msg in reversed(recent_messages):
                conversation_history.append({
                    'type': msg.message_type,
                    'content': msg.content
                })
        
        # Get Gemini service and generate response
        gemini_service = get_gemini_service()
        result = gemini_service.get_farming_response(
            message=message,
            user=user,
            conversation_history=conversation_history
        )
        
        if result['success']:
            return result['content']
        else:
            # If Gemini fails, try fallback
            return get_knowledge_base_response(message)
            
    except Exception as e:
        # Fallback to knowledge base if Gemini fails
        return get_knowledge_base_response(message)


def get_openrouter_response(message, user):
    """Get response from OpenRouter API (ChatGPT) - Legacy fallback"""
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
    
    # Trial onboarding intent
    if any(phrase in message_lower for phrase in [
        'free trial',
        'trial',
        'start trial',
        'take a trial',
        'trial as a farmer',
        'try as a farmer'
    ]):
        return (
            "Great! You can start your Farmazee Farmer Trial (14 days).\n\n"
            "Steps:\n"
            "• Click the link below to start your trial\n"
            "• Explore AI chatbot, weather, soil tips and more\n"
            "• You can upgrade anytime\n\n"
            "Start your trial: /ai-chatbot/start-trial/\n"
            "If the link doesn’t work, type: Start trial"
        )

    # Simple keyword-based responses
    if any(word in message_lower for word in ['machine learning', 'ml ', ' ml', 'build model', 'build a model', 'roadmap', 'chatbot', 'ai model']):
        return """🧭 Step-by-Step Roadmap to Build a Machine Learning Model

---

🪜 Step 1: Understand What ML Means

Machine Learning = teaching computers to learn from data and make predictions without hardcoding rules.

For example:

> You give past crop data (rainfall, soil, yield).
The ML model learns the pattern.
Then, for new data, it predicts the expected yield. 🌾

---

🧰 Step 2: Set Up Your Tools

Install these locally (or use Google Colab online):

```bash
pip install numpy pandas matplotlib scikit-learn
```

Optional but helpful:
- Jupyter Notebook → for testing ML code
- VS Code or Cursor → for project development
- Google Colab → for free GPU and cloud notebook

---

📚 Step 3: Learn the Basics

Concept           | Why It’s Important
------------------|-------------------
Data (CSV files)  | Your model learns from data
Features & Labels | Input (X) → Output (Y)
Train & Test      | Model learns, then is tested
Accuracy          | Measures how good your model is

👉 Example (yield prediction):
- Features: area, soil fertility, rainfall
- Label: predicted yield

---

🧪 Step 4: Build Your First Model

Example: Predict crop yield

```python
# Step 1: Import libraries
import pandas as pd
from sklearn.linear_model import LinearRegression

# Step 2: Prepare data
data = {
    'area': [1, 2, 3, 4, 5],
    'fertility': [1.2, 1.5, 1.7, 2.0, 2.2],
    'yield': [1.3, 2.5, 3.0, 4.1, 4.8]
}
df = pd.DataFrame(data)

# Step 3: Train model
X = df[['area', 'fertility']]   # inputs
y = df['yield']                 # output

model = LinearRegression()
model.fit(X, y)

# Step 4: Predict yield for new data
new_data = [[2.5, 1.8]]
prediction = model.predict(new_data)

print("Predicted Yield:", prediction[0])
```

✅ This small program trains a machine learning model and predicts output.

---

📊 Step 5: Try Different Models

After LinearRegression, explore:
- DecisionTreeClassifier (for categories)
- KNeighborsClassifier (pattern matching)
- RandomForestRegressor (advanced predictions)

All are available in scikit-learn.

---

🔍 Step 6: Work With Real Data

Practice using datasets from:
- Kaggle.com
- UCI Machine Learning Repository
- Government portals (crop, weather, etc.)

---

🚀 Step 7: Create a Real Project

Ideas:
1. 🌾 Crop Yield Prediction (soil, rainfall, area)
2. 🌧 Rainfall Prediction (past weather data)
3. 🧑‍🎓 Student Score Prediction (study hours)
4. 🏠 House Price Prediction (classic project)

---

🧠 Step 8: Advance to Deep Learning (Optional)

When ready:
- Learn TensorFlow or PyTorch
- Study Neural Networks

If you want, I can generate a starter notebook or Django view to integrate a simple ML demo into your app."""

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
        # Provide specific answers based on common questions
        message_lower = message.lower()
        
        if 'summer' in message_lower and 'crop' in message_lower:
            return """Great question about summer crops! Here are crops you can harvest in summer:

**Summer Crops for Harvest:**
• **Rice** - Main crop in Telangana/AP, harvest May-July
• **Cotton** - Harvest from October to February (planted in summer)
• **Maize** - Harvest 90-100 days after planting
• **Sunflower** - Harvest 90-110 days, good for oil
• **Groundnut** - Harvest 100-120 days, excellent for oil
• **Sesame** - Quick crop, 80-90 days
• **Red Gram (Toor Dal)** - 120-140 days
• **Green Gram (Moong)** - 65-75 days
• **Black Gram (Urad)** - 80-90 days

**Best for Telangana/AP:**
- Rice varieties: BPT 5204, RNR 15048, MTU 1010
- Cotton: Bt cotton varieties
- Maize: Hybrid varieties for better yield

**Planting Time:** March-April for summer crops
**Harvest Time:** May-October depending on crop

Need specific advice on any crop? Ask me about planting, fertilizers, or pest control!"""
        
        elif 'winter' in message_lower and 'crop' in message_lower:
            return """Winter crops you can plant and harvest:

**Rabi Season Crops (Winter):**
• **Wheat** - Plant Oct-Nov, harvest Mar-Apr
• **Chickpea (Bengal Gram)** - Plant Oct-Nov, harvest Feb-Mar
• **Mustard** - Plant Oct-Nov, harvest Feb-Mar
• **Barley** - Plant Oct-Nov, harvest Mar-Apr
• **Lentil (Masoor)** - Plant Oct-Nov, harvest Feb-Mar
• **Fenugreek** - Quick crop, 90-100 days
• **Onion** - Plant Oct-Nov, harvest Mar-Apr
• **Tomato** - Plant Oct-Nov, harvest Dec-Mar

**Best for Telangana/AP:**
- Wheat: HD 2967, HD 3086
- Chickpea: JG 11, JG 14
- Mustard: Pusa Bold, Varuna

**Planting:** October-November
**Harvest:** February-April

Need specific cultivation tips for any winter crop?"""
        
        elif 'pest' in message_lower or 'disease' in message_lower:
            return """I can help with pest and disease control! Common issues:

**Major Pests:**
• **Aphids** - Use neem oil or imidacloprid
• **Stem Borer** - Use cartap hydrochloride
• **Whitefly** - Use thiamethoxam
• **Thrips** - Use spinosad

**Common Diseases:**
• **Blast (Rice)** - Use tricyclazole
• **Rust (Wheat)** - Use propiconazole
• **Wilt (Cotton)** - Use carbendazim

**Organic Solutions:**
- Neem oil spray (2ml per liter)
- Cow urine spray (10%)
- Trichoderma for soil diseases

What specific pest or disease are you facing? Share crop name and symptoms for detailed treatment!"""
        
        else:
            return """I'm your farming expert! I can help with:

**Crop Management:**
• Seasonal crops and planting times
• Variety selection for Telangana/AP
• Fertilizer recommendations
• Irrigation scheduling

**Problem Solving:**
• Pest and disease identification
• Treatment recommendations
• Soil health improvement
• Weather-based decisions

**Practical Advice:**
• Government schemes and subsidies
• Market prices and selling tips
• Cost-effective farming methods
• Organic farming techniques

Ask me anything specific about your crops, soil, pests, or farming challenges!"""


def categorize_query(message):
    """Categorize farmer query for analytics"""
    try:
        # Use Gemini service for more accurate categorization
        gemini_service = get_gemini_service()
        category = gemini_service.categorize_query(message)
        
        # Map to FarmerQuery category choices
        category_map = {
            'crop_management': 'crop_management',
            'pest_control': 'pest_control',
            'soil_health': 'soil_health',
            'weather': 'weather',
            'market_info': 'market_info',
            'government_schemes': 'government_schemes',
            'irrigation': 'technical',
            'general': 'general'
        }
        
        return category_map.get(category, 'general')
    except:
        # Fallback to simple categorization
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
