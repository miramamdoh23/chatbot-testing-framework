"""
Mock Chatbot for Testing
Simulates a GenAI chatbot with intent recognition and context handling
Author: Mira Mamdoh
"""

from typing import List, Dict, Optional
import re


class MockChatbot:
    """
    A mock chatbot that simulates GenAI conversation capabilities
    Supports: Intent recognition, Context tracking, Multi-turn conversations
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.context: Dict[str, any] = {}
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "goodbye": ["bye", "goodbye", "see you", "farewell"],
            "thanks": ["thank you", "thanks", "appreciate"],
            "help": ["help", "assist", "support"],
            "booking": ["book", "schedule", "appointment", "meeting"],
            "status": ["status", "update", "progress"],
            "cancel": ["cancel", "stop", "abort"],
            "question": ["what", "how", "why", "when", "where", "who"],
            "name_query": ["my name", "what's my name", "who am i"],
            "weather": ["weather", "forecast", "temperature", "rain"]
        }
        
        self.responses = {
            "greeting": "Hello! How can I help you today?",
            "goodbye": "Goodbye! Have a great day!",
            "thanks": "You're welcome! Happy to help!",
            "help": "I can help you with bookings, questions, and general inquiries. What do you need?",
            "booking": "I'd be happy to help you book. When would you like to schedule?",
            "status": "Let me check the status for you.",
            "cancel": "Your request has been cancelled.",
            "question": "That's a great question. Let me help you with that.",
            "weather": "The weather today is sunny with a high of 25°C.",
            "unknown": "I'm not sure I understand. Could you rephrase that?"
        }
    
    def get_intent(self, message: str) -> str:
        """
        Classify the intent of a user message
        
        Args:
            message: User input text
            
        Returns:
            Intent classification string
        """
        message_lower = message.lower().strip()
        
        # Check for name storage
        if "my name is" in message_lower or ("i am" in message_lower and len(message_lower.split()) <= 3) or "i'm" in message_lower or "call me" in message_lower:
            return "name_introduction"
        
        # Check for name query
        if any(phrase in message_lower for phrase in self.intents["name_query"]):
            return "name_query"
        
        # Priority order for overlapping keywords
        # 1. Thanks (check first before help because "thanks for your help")
        if "thank" in message_lower or ("thanks" in message_lower and "help" not in message_lower.split("thanks")[0]) or "appreciate" in message_lower:
            return "thanks"
        
        # 2. Help (specific when mentioned)
        if ("help" in message_lower or "assist" in message_lower or "support" in message_lower) and "thank" not in message_lower:
            return "help"
        
        # 3. Goodbye (check "good" in context)
        if message_lower.startswith("good") and ("bye" in message_lower or message_lower == "goodbye"):
            return "goodbye"
        if any(word in message_lower for word in ["bye", "farewell", "see you"]):
            return "goodbye"
        
        # 4. Weather (specific)
        if any(keyword in message_lower for keyword in self.intents["weather"]):
            return "weather"
        
        # 5. Booking
        if any(keyword in message_lower for keyword in self.intents["booking"]):
            return "booking"
        
        # 6. Greeting (check start of message)
        if message_lower.startswith("hi") or message_lower.startswith("hello") or message_lower.startswith("hey"):
            return "greeting"
        if message_lower.startswith("good") and ("morning" in message_lower or "evening" in message_lower or "afternoon" in message_lower):
            return "greeting"
        
        # 7. Question words at start
        if any(message_lower.startswith(q) for q in ["what", "how", "why", "when", "where", "who"]):
            return "question"
        
        # 8. Other intents
        for intent in ["status", "cancel"]:
            if any(keyword in message_lower for keyword in self.intents[intent]):
                return intent
        
        return "unknown"
    
    def extract_name(self, message: str) -> Optional[str]:
        """Extract name from introduction message"""
        patterns = [
            r"my name is (\w+)",
            r"i am (\w+)",
            r"i'm (\w+)",
            r"call me (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1).capitalize()
        return None
    
    def generate_response(self, message: str) -> str:
        """
        Generate a response based on user message and context
        
        Args:
            message: User input text
            
        Returns:
            Chatbot response string
        """
        # Check if we're in booking mode and message looks like a time
        in_booking_mode = self.context.get("booking_started", False)
        time_indicators = ["tomorrow", "today", "monday", "tuesday", "wednesday", 
                          "thursday", "friday", "saturday", "sunday", "pm", "am", 
                          "morning", "afternoon", "evening", "at ", " at", "1pm", "2pm", 
                          "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm", "12pm",
                          "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12am"]
        # Only treat as time if doesn't start with question words
        is_question = any(message.lower().startswith(q) for q in ["what", "how", "why", "when", "where", "who"])
        looks_like_time = in_booking_mode and any(word in message.lower() for word in time_indicators) and not is_question
        
        # If in booking mode and looks like time, treat as booking continuation
        if looks_like_time:
            intent = "booking_time"
        else:
            intent = self.get_intent(message)
        
        # Store message in history
        self.conversation_history.append({
            "role": "user",
            "content": message,
            "intent": intent
        })
        
        # Handle name introduction
        if intent == "name_introduction":
            name = self.extract_name(message)
            if name:
                self.context["user_name"] = name
                response = f"Nice to meet you, {name}! How can I help you today?"
            else:
                response = "Nice to meet you! What's your name?"
        
        # Handle name query
        elif intent == "name_query":
            if "user_name" in self.context:
                response = f"Your name is {self.context['user_name']}!"
            else:
                response = "I don't know your name yet. What should I call you?"
        
        # Handle booking time (continuation of booking)
        elif intent == "booking_time":
            self.context["booking_time"] = message
            response = "Great! Your booking is confirmed. You'll receive a confirmation email shortly."
            self.context["booking_started"] = False
        
        # Handle booking with context
        elif intent == "booking":
            if not self.context.get("booking_started", False):
                self.context["booking_started"] = True
                response = "I'd be happy to help you book. When would you like to schedule?"
            else:
                response = "Please specify when you'd like to book (e.g., 'tomorrow at 2pm')"
        
        # Handle weather with specific response
        elif intent == "weather":
            response = "The weather today is sunny with a high of 25°C."
        
        # Default responses
        else:
            response = self.responses.get(intent, self.responses["unknown"])
        
        # Store response in history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "intent": intent
        })
        
        return response
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get full conversation history"""
        return self.conversation_history
    
    def get_context(self) -> Dict[str, any]:
        """Get current conversation context"""
        return self.context
    
    def reset(self):
        """Reset conversation history and context"""
        self.conversation_history = []
        self.context = {}
    
    def get_response_length(self, response: str) -> int:
        """Get word count of response"""
        return len(response.split())
    
    def calculate_confidence(self, intent: str) -> float:
        """
        Mock confidence score for intent classification
        In real chatbot, this would come from ML model
        """
        if intent == "unknown":
            return 0.3
        elif intent in ["greeting", "goodbye", "thanks"]:
            return 0.95
        else:
            return 0.85


class Conversation:
    """Helper class to manage multi-turn conversations"""
    
    def __init__(self):
        self.chatbot = MockChatbot()
        self.last_response = ""
    
    def send(self, message: str) -> str:
        """Send a message and get response"""
        self.last_response = self.chatbot.generate_response(message)
        return self.last_response
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.chatbot.get_conversation_history()
    
    def get_context(self) -> Dict[str, any]:
        """Get current context"""
        return self.chatbot.get_context()
    
    def reset(self):
        """Reset conversation"""
        self.chatbot.reset()
        self.last_response = ""