"""
Gemini AI Service for Farmazee Chatbot
Handles all interactions with Google's Gemini AI API
"""

import google.generativeai as genai
from django.conf import settings
import time
import logging

logger = logging.getLogger(__name__)


class GeminiAIService:
    """Service class for Gemini AI integration"""
    
    def __init__(self):
        """Initialize Gemini AI with API key"""
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use Gemini 2.5 Flash - fast, efficient, and stable
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            raise ValueError("GEMINI_API_KEY not found in settings")
    
    def get_farming_response(self, message, user=None, conversation_history=None):
        """
        Get AI response for farming-related queries
        
        Args:
            message (str): User's message/query
            user: Django User object (optional)
            conversation_history (list): Previous conversation messages (optional)
        
        Returns:
            dict: Response with content, response_time, and tokens_used
        """
        try:
            start_time = time.time()
            
            # Build the context and prompt
            system_context = self._build_system_context(user)
            full_prompt = self._build_prompt(message, system_context, conversation_history)
            
            # Configure generation settings
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
            
            # Safety settings to filter harmful content
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]
            
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            response_time = time.time() - start_time
            
            # Extract response text
            if response.text:
                ai_response = response.text
            else:
                ai_response = "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
            
            # Get token count if available
            tokens_used = 0
            if hasattr(response, 'usage_metadata'):
                tokens_used = (
                    response.usage_metadata.prompt_token_count + 
                    response.usage_metadata.candidates_token_count
                )
            
            return {
                'content': ai_response,
                'response_time': round(response_time, 2),
                'tokens_used': tokens_used,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Gemini AI Error: {str(e)}")
            return {
                'content': self._get_fallback_response(message),
                'response_time': 0,
                'tokens_used': 0,
                'success': False,
                'error': str(e)
            }
    
    def _build_system_context(self, user=None):
        """Build system context for the AI"""
        context = """You are Farmazee AI, an expert agricultural assistant specializing in farming practices in India, 
        particularly in Telugu states (Telangana and Andhra Pradesh).
        
        Your expertise includes:
        - Crop management and cultivation techniques
        - Pest and disease identification and control
        - Soil health management and fertilization
        - Weather-based farming advice
        - Government agricultural schemes and subsidies
        - Market prices and selling strategies
        - Sustainable and organic farming practices
        - Water management and irrigation
        - Farm equipment and machinery guidance
        
        CRITICAL RESPONSE GUIDELINES:
        1. ALWAYS ANSWER THE SPECIFIC QUESTION ASKED - Never give generic responses
        2. Provide detailed, practical advice with specific crop names, varieties, and timing
        3. Include step-by-step instructions with quantities and methods
        4. Mention specific varieties suitable for Telangana/AP
        5. Give actionable steps farmers can follow immediately
        6. Use simple, clear language avoiding complex technical jargon
        7. Consider local climate, soil conditions, and farming practices
        8. Include safety warnings when discussing pesticides or chemicals
        9. Provide specific examples and crop details
        10. Be encouraging and supportive of farmers' efforts
        
        EXAMPLE: If asked "which crops can I harvest in summer" → List specific summer crops with harvest times, varieties, and cultivation details
        10. Keep responses concise but comprehensive (2-4 paragraphs typically)
        
        Regional focus:
        - Climate: Tropical to semi-arid
        - Major crops: Rice, cotton, maize, chili, turmeric, groundnut
        - Seasons: Kharif (June-Oct), Rabi (Nov-Mar), Summer (Apr-May)
        """
        
        if user and hasattr(user, 'profile'):
            # Add user-specific context if available
            context += f"\n\nUser information: Farmer from the region, interested in personalized farming advice."
        
        return context
    
    def _build_prompt(self, message, system_context, conversation_history=None):
        """Build the complete prompt for Gemini"""
        prompt = f"{system_context}\n\n"
        
        # Add conversation history if available
        if conversation_history and len(conversation_history) > 0:
            prompt += "Previous conversation:\n"
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = "Farmer" if msg['type'] == 'user' else "Farmazee AI"
                prompt += f"{role}: {msg['content']}\n"
            prompt += "\n"
        
        # Add current query
        prompt += f"Farmer's current question: {message}\n\n"
        prompt += "Please provide a helpful, practical response:"
        
        return prompt
    
    def _get_fallback_response(self, message):
        """Fallback response when AI fails"""
        message_lower = message.lower()
        
        # Simple keyword-based responses
        if any(word in message_lower for word in ['rice', 'paddy', 'వరి', 'dhaan']):
            return """**Rice Cultivation Guide:**

For successful rice cultivation in our region:

**Best Practices:**
• Sowing time: June-July (Kharif season)
• Use certified high-yield varieties like BPT-5204, MTU-1010
• Maintain 2-3 inches water level in fields
• Apply balanced NPK fertilizers (120:60:40 kg/ha)
• Control weeds within first 45 days

**Common Issues:**
• Stem borer: Use Cartap Hydrochloride
• Leaf folder: Apply Chlorantraniliprole
• Blast disease: Use Tricyclazole fungicide

For specific issues, please contact your local agricultural extension officer."""
        
        elif any(word in message_lower for word in ['pest', 'disease', 'bug', 'insect', 'రోగాలు']):
            return """**Pest & Disease Management:**

**Integrated Pest Management (IPM) approach:**
• Regular field monitoring (2-3 times per week)
• Use pheromone traps for early detection
• Apply neem-based organic pesticides first
• Use chemical pesticides only when threshold exceeded
• Rotate pesticide families to prevent resistance

**Preventive Measures:**
• Maintain crop diversity
• Use resistant varieties
• Proper field sanitation
• Balanced fertilization
• Adequate spacing between plants

**Emergency Contact:**
For severe infestations, immediately contact your local agricultural officer or call the farmer helpline: 1800-180-1551"""
        
        elif any(word in message_lower for word in ['soil', 'fertilizer', 'nutrient', 'manure']):
            return """**Soil Health Management:**

**Soil Testing & Improvement:**
• Test soil every 2-3 years (available at govt. labs)
• Optimal pH range: 6.0-7.5 for most crops
• Apply organic matter regularly (5-10 tons/ha)

**Fertilization Strategy:**
• Use balanced NPK based on soil test results
• Apply organic manure (FYM/compost) before sowing
• Consider vermicompost for better soil structure
• Use green manure crops (dhaincha, sunhemp)

**Soil Conservation:**
• Practice crop rotation
• Use cover crops
• Avoid over-irrigation
• Maintain soil organic content above 0.5%"""
        
        elif any(word in message_lower for word in ['weather', 'rain', 'drought', 'climate']):
            return """**Weather-Based Farming:**

**Weather Monitoring:**
• Check weather forecasts regularly (IMD Meghdoot app)
• Plan sowing based on monsoon predictions
• Use weather-based agro-advisories

**Climate Adaptation:**
• Choose drought-resistant varieties for uncertain rainfall
• Practice water conservation techniques
• Use drip irrigation where possible
• Apply mulching to retain soil moisture
• Consider rainwater harvesting

**Risk Management:**
• Enroll in Pradhan Mantri Fasal Bima Yojana (crop insurance)
• Diversify crops to reduce risk
• Maintain emergency irrigation arrangements"""
        
        elif any(word in message_lower for word in ['market', 'price', 'sell', 'mandi']):
            return """**Market Information & Selling:**

**Getting Best Prices:**
• Check daily mandi prices on eNAM portal/app
• Consider direct marketing through FPOs
• Grade and clean produce before selling
• Time your sales to avoid glut periods

**Market Channels:**
• Local APMC mandis
• eNAM electronic platform
• Direct to retailers/processors
• Farmer Producer Organizations (FPOs)
• Online platforms (if available)

**Value Addition:**
• Proper grading and packaging
• Storage to sell in off-season
• Processing (if facilities available)
• Organic certification for premium prices"""
        
        elif any(word in message_lower for word in ['scheme', 'subsidy', 'government', 'yojana']):
            return """**Government Schemes for Farmers:**

**Major Schemes:**
1. **PM-KISAN**: ₹6,000/year direct benefit transfer
2. **Pradhan Mantri Fasal Bima Yojana**: Crop insurance
3. **Soil Health Card Scheme**: Free soil testing
4. **Pradhan Mantri Krishi Sinchai Yojana**: Irrigation support
5. **KCC (Kisan Credit Card)**: Easy farm loans

**State Schemes (Telangana/AP):**
• Rythu Bandhu/Bharosa: Investment support
• Free electricity for agriculture
• Input subsidies

**How to Apply:**
Visit your nearest Agriculture Office or check the official government agriculture portal for your state."""
        
        else:
            return """**Welcome to Farmazee AI!**

I'm here to help you with all your farming questions. I can assist with:

* **Crop Management** - Cultivation techniques, varieties, timing
* **Pest & Disease Control** - Identification and treatment
* **Soil Health** - Testing, fertilization, improvement
* **Weather & Irrigation** - Water management, climate adaptation
* **Market Information** - Prices, selling strategies
* **Government Schemes** - Subsidies, insurance, benefits
* **Best Practices** - Sustainable and organic farming

Please ask me your specific farming question, and I'll provide detailed, practical guidance!

**Example questions:**
- "How to control leaf curl in cotton?"
- "When should I sow maize in Rabi season?"
- "What fertilizers for chili crop?"
- "How to apply for PM-KISAN scheme?" """
    
    def categorize_query(self, message):
        """Categorize the farming query"""
        message_lower = message.lower()
        
        categories = {
            'crop_management': ['crop', 'plant', 'sow', 'harvest', 'cultivation', 'variety', 'seed'],
            'pest_control': ['pest', 'disease', 'bug', 'insect', 'fungus', 'virus', 'infection'],
            'soil_health': ['soil', 'fertilizer', 'nutrient', 'manure', 'compost', 'ph'],
            'weather': ['weather', 'rain', 'drought', 'climate', 'monsoon', 'temperature'],
            'market_info': ['market', 'price', 'sell', 'mandi', 'buyer', 'trade'],
            'government_schemes': ['scheme', 'subsidy', 'government', 'yojana', 'kisan', 'support'],
            'irrigation': ['water', 'irrigation', 'drip', 'sprinkler', 'pump'],
        }
        
        for category, keywords in categories.items():
            if any(keyword in message_lower for keyword in keywords):
                return category
        
        return 'general'


# Singleton instance
_gemini_service = None

def get_gemini_service():
    """Get or create Gemini service instance"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiAIService()
    return _gemini_service

