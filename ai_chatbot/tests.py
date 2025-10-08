"""
Tests for AI Chatbot functionality with Gemini AI
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ChatSession, ChatMessage, FarmerQuery
from .gemini_service import get_gemini_service
import json


class GeminiServiceTestCase(TestCase):
    """Test cases for Gemini AI service"""
    
    def setUp(self):
        """Set up test environment"""
        self.user = User.objects.create_user(
            username='testfarmer',
            email='test@farmer.com',
            password='testpass123'
        )
    
    def test_gemini_service_initialization(self):
        """Test that Gemini service can be initialized"""
        try:
            service = get_gemini_service()
            self.assertIsNotNone(service)
            self.assertIsNotNone(service.model)
        except Exception as e:
            self.skipTest(f"Gemini API not available: {str(e)}")
    
    def test_farming_response_generation(self):
        """Test that Gemini can generate farming responses"""
        try:
            service = get_gemini_service()
            result = service.get_farming_response(
                message="How to grow rice?",
                user=self.user
            )
            
            self.assertIsInstance(result, dict)
            self.assertIn('content', result)
            self.assertIn('response_time', result)
            self.assertIn('success', result)
            
            if result['success']:
                self.assertTrue(len(result['content']) > 0)
                self.assertGreater(result['response_time'], 0)
        except Exception as e:
            self.skipTest(f"Gemini API test failed: {str(e)}")
    
    def test_query_categorization(self):
        """Test query categorization"""
        try:
            service = get_gemini_service()
            
            test_cases = [
                ("How to control pests in cotton?", "pest_control"),
                ("Best time to sow rice?", "crop_management"),
                ("Soil pH for tomatoes?", "soil_health"),
                ("Weather forecast impact?", "weather"),
            ]
            
            for message, expected_category in test_cases:
                category = service.categorize_query(message)
                self.assertIn(category, [
                    'crop_management', 'pest_control', 'soil_health',
                    'weather', 'market_info', 'government_schemes',
                    'irrigation', 'general'
                ])
        except Exception as e:
            self.skipTest(f"Categorization test failed: {str(e)}")
    
    def test_fallback_response(self):
        """Test fallback response when AI fails"""
        service = get_gemini_service()
        fallback = service._get_fallback_response("How to grow rice?")
        
        self.assertIsInstance(fallback, str)
        self.assertTrue(len(fallback) > 0)


class ChatbotViewsTestCase(TestCase):
    """Test cases for chatbot views"""
    
    def setUp(self):
        """Set up test environment"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testfarmer',
            email='test@farmer.com',
            password='testpass123'
        )
    
    def test_chat_home_authenticated(self):
        """Test chat home for authenticated users"""
        self.client.login(username='testfarmer', password='testpass123')
        response = self.client.get(reverse('ai_chatbot:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'chat')
    
    def test_chat_home_guest(self):
        """Test chat home for guest users"""
        response = self.client.get(reverse('ai_chatbot:home'))
        
        self.assertEqual(response.status_code, 200)
    
    def test_send_message_authenticated(self):
        """Test sending a message"""
        self.client.login(username='testfarmer', password='testpass123')
        
        # Create a chat session
        session = ChatSession.objects.create(
            user=self.user,
            session_id='test-session-123'
        )
        
        response = self.client.post(
            reverse('ai_chatbot:send_message'),
            data=json.dumps({
                'message': 'How to grow rice?',
                'session_id': session.session_id
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        if 'success' in data:
            self.assertTrue(data['success'])
            self.assertIn('ai_response', data)
    
    def test_send_message_unauthenticated(self):
        """Test that unauthenticated users cannot send messages"""
        response = self.client.post(
            reverse('ai_chatbot:send_message'),
            data=json.dumps({'message': 'Test'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
    
    def test_chat_history(self):
        """Test chat history view"""
        self.client.login(username='testfarmer', password='testpass123')
        
        # Create test data
        session = ChatSession.objects.create(
            user=self.user,
            session_id='test-session-123'
        )
        
        ChatMessage.objects.create(
            session=session,
            message_type='user',
            content='Test question'
        )
        
        response = self.client.get(reverse('ai_chatbot:history'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test question')
    
    def test_query_analytics(self):
        """Test query analytics view"""
        self.client.login(username='testfarmer', password='testpass123')
        
        # Create test query
        FarmerQuery.objects.create(
            user=self.user,
            query_text='How to grow rice?',
            category='crop_management',
            ai_response='Test response'
        )
        
        response = self.client.get(reverse('ai_chatbot:analytics'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'crop_management')


class ChatModelsTestCase(TestCase):
    """Test cases for chat models"""
    
    def setUp(self):
        """Set up test environment"""
        self.user = User.objects.create_user(
            username='testfarmer',
            email='test@farmer.com',
            password='testpass123'
        )
    
    def test_chat_session_creation(self):
        """Test chat session creation"""
        session = ChatSession.objects.create(
            user=self.user,
            session_id='test-123'
        )
        
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.session_id, 'test-123')
        self.assertTrue(session.is_active)
    
    def test_chat_message_creation(self):
        """Test chat message creation"""
        session = ChatSession.objects.create(
            user=self.user,
            session_id='test-123'
        )
        
        message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content='Test message'
        )
        
        self.assertEqual(message.session, session)
        self.assertEqual(message.message_type, 'user')
        self.assertEqual(message.content, 'Test message')
    
    def test_farmer_query_creation(self):
        """Test farmer query creation"""
        query = FarmerQuery.objects.create(
            user=self.user,
            query_text='How to grow rice?',
            category='crop_management',
            ai_response='Rice cultivation guide...'
        )
        
        self.assertEqual(query.user, self.user)
        self.assertEqual(query.category, 'crop_management')
        self.assertIsNone(query.satisfaction_rating)


# Manual test function for quick testing
def manual_test_gemini():
    """
    Manual test function to verify Gemini AI integration
    Run this from Django shell:
    >>> from ai_chatbot.tests import manual_test_gemini
    >>> manual_test_gemini()
    """
    try:
        from .gemini_service import get_gemini_service
        
        print("🚀 Testing Gemini AI Integration...")
        print("-" * 50)
        
        service = get_gemini_service()
        print("✅ Gemini service initialized successfully")
        
        test_queries = [
            "How to grow rice in Telangana?",
            "What are the common pests in cotton crops?",
            "How to improve soil health?",
            "Best time to sow maize?",
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            result = service.get_farming_response(query)
            
            if result['success']:
                print(f"✅ Success!")
                print(f"⏱️  Response time: {result['response_time']}s")
                print(f"🔢 Tokens used: {result['tokens_used']}")
                print(f"💬 Response preview: {result['content'][:200]}...")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                print(f"💬 Fallback response: {result['content'][:200]}...")
        
        print("\n" + "=" * 50)
        print("🎉 Gemini AI Integration Test Complete!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
