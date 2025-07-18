"""
Content filtering utilities for the GymPro chatbot
"""
import logging
from typing import Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)

class ContentFilter:
    """Service for filtering and categorizing user messages"""
    
    def __init__(self):
        self.gym_keywords = settings.GYM_KEYWORDS
    
    def is_gym_related(self, message: str) -> bool:
        """Check if the message is related to gym/fitness"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.gym_keywords)
    
    def get_fallback_response(self, message: str) -> str:
        """Provide a fallback response when RAG is not available"""
        if not self.is_gym_related(message):
            return """I'm GymPro AI, your dedicated fitness assistant! 🏋️‍♂️

I specialize in helping with:
• Exercise techniques and workout routines
• Gym equipment usage and safety
• Nutrition and fitness goals
• Training programs and progression
• Injury prevention and recovery

Please ask me something related to fitness, gym, or health topics, and I'll be happy to help!"""
        
        # Create a simple template for fallback responses
        fallback_template = """I'm GymPro AI, and I'd love to help with your fitness question! 💪

However, my advanced RAG system is currently unavailable. Here's some general guidance:

🏋️ **Essential Fitness Tips:**
• Always warm up before exercising (5-10 minutes)
• Focus on compound movements: squats, deadlifts, bench press, rows
• Prioritize proper form over heavy weights
• Stay hydrated throughout your workout
• Allow adequate rest between training sessions (48-72 hours for muscle groups)
• Get 7-9 hours of quality sleep for recovery

📝 **For Your Specific Question:** "{question}"
Please ensure your Google API key is properly configured to get detailed, personalized advice!

Feel free to ask about specific exercises, workout plans, or nutrition guidance! 🎯"""
        
        return fallback_template.format(question=message)
    
    def validate_message(self, message: str) -> Dict[str, Any]:
        """Validate and categorize a user message"""
        if not message or not message.strip():
            return {
                "valid": False,
                "gym_related": False,
                "error": "Message cannot be empty"
            }
        
        message = message.strip()
        if len(message) > 1000:
            return {
                "valid": False,
                "gym_related": False,
                "error": "Message too long (max 1000 characters)"
            }
        
        gym_related = self.is_gym_related(message)
        
        return {
            "valid": True,
            "gym_related": gym_related,
            "message": message
        }

# Create global content filter instance
content_filter = ContentFilter()
