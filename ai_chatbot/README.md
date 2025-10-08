# Farmazee AI Chatbot - Gemini Integration

## Overview

The Farmazee AI Chatbot uses Google's Gemini AI to provide intelligent, context-aware responses to farmers' questions about agriculture, crop management, pest control, soil health, and more.

## Features

✅ **Gemini AI Integration** - Powered by Google's Gemini 1.5 Flash model  
✅ **Conversation History** - Maintains context across chat sessions  
✅ **Smart Categorization** - Automatically categorizes queries for analytics  
✅ **Multi-layer Fallback** - Falls back gracefully when AI is unavailable  
✅ **Query Analytics** - Track and analyze farming queries  
✅ **Response Rating** - Farmers can rate AI responses  
✅ **Multilingual Support** - Handles English and Telugu queries  

## Architecture

### Core Components

1. **GeminiAIService** (`gemini_service.py`)
   - Manages all Gemini AI interactions
   - Handles conversation context
   - Provides fallback responses
   - Categorizes queries

2. **Views** (`views.py`)
   - Chat interface and message handling
   - Session management
   - Analytics and history

3. **Models** (`models.py`)
   - ChatSession - User chat sessions
   - ChatMessage - Individual messages
   - FarmerQuery - Query analytics
   - AIKnowledgeBase - Fallback knowledge

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

Or update `farmazee/settings.py` directly (not recommended for production).

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Test the Integration

#### From Django Shell:
```python
python manage.py shell

>>> from ai_chatbot.tests import manual_test_gemini
>>> manual_test_gemini()
```

#### Run Unit Tests:
```bash
python manage.py test ai_chatbot
```

## Usage

### Basic Chat Flow

1. **User visits chat page** → Creates/retrieves chat session
2. **User sends message** → Saved to database
3. **Gemini AI processes** → Generates contextual response
4. **Response saved** → Stored with metrics (time, tokens)
5. **Analytics recorded** → Query categorized and stored

### API Endpoints

- `GET /ai-chat/` - Chat home page
- `GET /ai-chat/chat/` - Chat interface
- `POST /ai-chat/send-message/` - Send message and get AI response
- `GET /ai-chat/history/` - View chat history
- `GET /ai-chat/analytics/` - View query analytics
- `POST /ai-chat/rate-response/` - Rate AI response

### Example API Request

```javascript
fetch('/ai-chat/send-message/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
        message: 'How to grow rice in Telangana?',
        session_id: 'current-session-id'
    })
})
.then(response => response.json())
.then(data => {
    console.log('AI Response:', data.ai_response.content);
    console.log('Response time:', data.response_time);
});
```

## Gemini AI Configuration

### Model Selection

Currently using **Gemini 1.5 Flash** for:
- Fast response times
- Cost efficiency
- Good quality responses
- Lower token usage

### Generation Settings

```python
generation_config = {
    "temperature": 0.7,      # Balanced creativity
    "top_p": 0.95,           # Nucleus sampling
    "top_k": 40,             # Token selection diversity
    "max_output_tokens": 1024 # Max response length
}
```

### Safety Settings

Configured to block:
- Harassment
- Hate speech
- Sexually explicit content
- Dangerous content

## Conversation Context

The chatbot maintains conversation history:

- Last 10 messages used for context
- Session-based conversation tracking
- User-specific personalization (if profile available)

## Fallback Strategy

1. **Gemini AI** (Primary)
2. **Knowledge Base** (Secondary)
3. **Predefined Responses** (Tertiary)

Each layer provides farming-specific responses even when AI is unavailable.

## Query Categories

Automatically categorizes queries into:

- **crop_management** - Crop cultivation, varieties, timing
- **pest_control** - Pest/disease identification and treatment
- **soil_health** - Soil testing, fertilization, improvement
- **weather** - Weather-based farming advice
- **market_info** - Market prices, selling strategies
- **government_schemes** - Subsidies, insurance, benefits
- **technical** - Irrigation, equipment
- **general** - Other farming queries

## Analytics

Track and analyze:

- Query categories distribution
- Response satisfaction ratings
- Most common farming issues
- Response times and token usage
- User engagement patterns

## Customization

### Modify System Context

Edit `GeminiAIService._build_system_context()` to customize the AI's expertise and response style.

### Add Knowledge Base Entries

```python
from ai_chatbot.models import AIKnowledgeBase

AIKnowledgeBase.objects.create(
    title="Rice Cultivation Guide",
    content="Detailed rice cultivation information...",
    knowledge_type="crop_info",
    keywords="rice,paddy,cultivation,telangana,andhra",
    source="Agriculture Department"
)
```

### Customize Fallback Responses

Edit `GeminiAIService._get_fallback_response()` to add more keyword-based responses.

## Performance Optimization

1. **Session caching** - Reuse chat sessions
2. **Conversation history limit** - Only last 10 messages
3. **Token optimization** - Concise prompts and responses
4. **Async processing** - Consider Celery for background processing

## Troubleshooting

### API Key Issues
```
Error: GEMINI_API_KEY not found in settings
```
**Solution:** Add `GEMINI_API_KEY` to `.env` file or settings.py

### Response Quality Issues
- Adjust `temperature` (0.7 = balanced, lower = more focused)
- Modify system context for better domain expertise
- Add more examples to knowledge base

### Slow Responses
- Check internet connection
- Consider using Gemini 1.5 Flash (faster)
- Implement response caching for common queries

### Safety Filters Triggered
- Adjust safety settings thresholds
- Rephrase sensitive queries
- Add content moderation layer

## Testing

### Unit Tests
```bash
python manage.py test ai_chatbot.tests.GeminiServiceTestCase
python manage.py test ai_chatbot.tests.ChatbotViewsTestCase
python manage.py test ai_chatbot.tests.ChatModelsTestCase
```

### Manual Testing
```python
# Django shell
from ai_chatbot.tests import manual_test_gemini
manual_test_gemini()
```

### Integration Testing
1. Start development server: `python manage.py runserver`
2. Visit: `http://localhost:8000/ai-chat/`
3. Login and test chat functionality
4. Check analytics: `http://localhost:8000/ai-chat/analytics/`

## Best Practices

1. ✅ Always handle API failures gracefully
2. ✅ Store queries for analytics and improvement
3. ✅ Rate-limit API calls in production
4. ✅ Monitor token usage and costs
5. ✅ Collect user feedback on responses
6. ✅ Regularly update knowledge base
7. ✅ Test with real farmer queries
8. ✅ Use environment variables for API keys

## Security

- Never commit API keys to version control
- Use `.env` files for local development
- Use environment variables in production
- Implement rate limiting for API endpoints
- Validate and sanitize user inputs
- Monitor for abuse patterns

## Future Enhancements

- [ ] Voice input/output support
- [ ] Image recognition for crop/pest identification
- [ ] Regional language support (Telugu, Hindi)
- [ ] Offline mode with cached responses
- [ ] Integration with other farm data (soil tests, weather)
- [ ] Personalized recommendations based on farmer's location/crops
- [ ] Multi-turn conversation improvements
- [ ] Response caching for common queries

## Support

For issues or questions:
1. Check troubleshooting section
2. Review test cases
3. Check Django logs: `logs/farmazee.log`
4. Consult Gemini AI documentation: https://ai.google.dev/

## License

Part of the Farmazee agricultural platform.

