# Quick Start Guide - Gemini AI Chatbot

## 🚀 Your chatbot is now powered by Gemini AI!

### What Just Happened?

Your Farmazee AI Chatbot now uses **Google's Gemini 2.5 Flash** model to provide intelligent, context-aware responses to farmers' questions.

### Test It Right Now!

1. **Start the Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Open your browser:**
   ```
   http://localhost:8000/ai-chat/
   ```

3. **Login and ask a question:**
   - "How to grow rice in Telangana?"
   - "What are the best fertilizers for cotton?"
   - "How to control pests in tomato crops?"

### How It Works

```
User Question
     ↓
Gemini AI (2.5 Flash) ←── Conversation History
     ↓                    ←── Farming Context
AI Response
     ↓
Saved to Database ──→ Analytics
```

### Key Features

✅ **Real-time AI Responses** - 10-20 second response times
✅ **Conversation Memory** - Remembers your last 10 messages
✅ **Smart Categorization** - Auto-categorizes queries
✅ **Multi-language** - Handles English and Telugu
✅ **Intelligent Fallback** - Works even if AI fails
✅ **Safety Filters** - Blocks harmful content

### API Endpoints

#### Get Chat Interface
```
GET /ai-chat/
```

#### Send Message
```javascript
POST /ai-chat/send-message/

Body:
{
  "message": "Your farming question",
  "session_id": "your-session-id"
}

Response:
{
  "success": true,
  "ai_response": {
    "content": "Detailed farming advice...",
    "timestamp": "2025-10-08T12:00:00Z"
  },
  "response_time": 11.6
}
```

#### View Chat History
```
GET /ai-chat/history/
```

#### View Analytics
```
GET /ai-chat/analytics/
```

### Configuration

Your API key is already configured:
```python
# farmazee/settings.py
GEMINI_API_KEY = 'AIzaSyDFCmoQCjp6qbUp_rDErGCgFQoBsJblMVQ'
```

**Model:** gemini-2.5-flash (latest stable version)

### Testing

Run the test suite:
```bash
python manage.py test ai_chatbot
```

Or test manually in Django shell:
```python
python manage.py shell

>>> from ai_chatbot.gemini_service import get_gemini_service
>>> service = get_gemini_service()
>>> result = service.get_farming_response("How to grow rice?")
>>> print(result['content'])
```

### What Was Changed?

1. **Added Gemini AI Package**
   - `google-generativeai>=0.3.0` in requirements.txt

2. **Created Gemini Service**
   - `ai_chatbot/gemini_service.py` - Complete AI integration

3. **Updated Views**
   - `ai_chatbot/views.py` - Now uses Gemini AI

4. **Added Tests**
   - `ai_chatbot/tests.py` - Comprehensive test suite

5. **Updated Configuration**
   - `farmazee/settings.py` - Added GEMINI_API_KEY
   - `env.example` - Added API key placeholder

### Troubleshooting

**If responses are slow:**
- Normal: 10-20 seconds (Gemini AI processing)
- Check your internet connection
- Response times will vary based on question complexity

**If you get errors:**
1. Make sure the server is running
2. Check that you're logged in
3. Verify internet connectivity
4. Check logs: `logs/farmazee.log`

**If you see fallback responses:**
- Some queries may trigger safety filters
- System automatically provides relevant fallback content
- This is normal and expected behavior

### Example Queries to Try

**Crop Management:**
- "When should I plant rice in Telangana?"
- "Best cotton varieties for black soil"
- "Crop rotation strategies for maize"

**Pest Control:**
- "How to control aphids in cotton?"
- "Natural pest control methods"
- "Symptoms of stem borer in rice"

**Soil Health:**
- "How to improve soil fertility?"
- "What is the ideal pH for tomatoes?"
- "Organic fertilizers for vegetables"

**Government Schemes:**
- "How to apply for PM-KISAN?"
- "What subsidies are available for farmers?"
- "Crop insurance schemes"

### Admin Access

Monitor chatbot usage:
```
http://localhost:8000/admin/ai_chatbot/
```

View analytics:
- Chat sessions
- Messages
- Farmer queries
- Query categories
- Response ratings

### Production Deployment

When deploying to production:

1. **Move API key to environment variable:**
   ```bash
   export GEMINI_API_KEY='your-api-key'
   ```

2. **Enable rate limiting** (optional but recommended)

3. **Set up monitoring** for response times and errors

4. **Configure logging** for production environment

### Documentation

- **Full Documentation:** `ai_chatbot/README.md`
- **Integration Summary:** `GEMINI_INTEGRATION_SUMMARY.md`
- **Gemini API Docs:** https://ai.google.dev/

### Support

- Test Suite: `python manage.py test ai_chatbot`
- Django Logs: `logs/farmazee.log`
- Gemini Status: https://status.cloud.google.com/

### Next Steps (Optional)

1. ✅ **Test the chatbot** - Try different queries
2. ✅ **Check analytics** - View query patterns
3. ✅ **Customize responses** - Edit system context in `gemini_service.py`
4. ✅ **Add knowledge base** - Create AIKnowledgeBase entries
5. ✅ **Collect feedback** - Enable response ratings
6. ✅ **Deploy to production** - Follow deployment guide

---

## 🎉 You're All Set!

Your AI chatbot is ready to help farmers with intelligent, context-aware advice.

**Start the server and give it a try!**

```bash
python manage.py runserver
```

Then visit: http://localhost:8000/ai-chat/

Happy farming! 🌾
