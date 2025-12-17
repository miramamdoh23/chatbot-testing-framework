"""
Intent Recognition Tests
Tests for chatbot's ability to classify user intents correctly
Author: Mira Mamdoh
"""

import pytest
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.mock_chatbot import MockChatbot
from chatbot.intent_classifier import IntentClassifier


class TestIntentRecognition:
    """Test suite for intent classification"""
    
    def setup_method(self):
        """Setup for each test"""
        self.chatbot = MockChatbot()
        self.classifier = IntentClassifier()
    
    def test_greeting_intent(self):
        """Test recognition of greeting messages"""
        greetings = ["Hello", "Hi", "Hey", "Good morning", "Good evening"]
        
        for greeting in greetings:
            intent = self.chatbot.get_intent(greeting)
            assert intent == "greeting", f"Failed for: {greeting}"
        
        print("✅ Greeting Intent Test PASSED")
    
    def test_goodbye_intent(self):
        """Test recognition of goodbye messages"""
        goodbyes = ["Goodbye", "Bye", "See you", "Farewell"]
        
        for goodbye in goodbyes:
            intent = self.chatbot.get_intent(goodbye)
            assert intent == "goodbye", f"Failed for: {goodbye}"
        
        print("✅ Goodbye Intent Test PASSED")
    
    def test_thanks_intent(self):
        """Test recognition of thank you messages"""
        thanks_msgs = ["Thank you", "Thanks", "Thanks a lot", "I appreciate it"]
        
        for msg in thanks_msgs:
            intent = self.chatbot.get_intent(msg)
            assert intent == "thanks", f"Failed for: {msg}"
        
        print("✅ Thanks Intent Test PASSED")
    
    def test_help_intent(self):
        """Test recognition of help requests"""
        help_msgs = ["I need help", "Can you help me?", "I need assistance", "Support please"]
        
        for msg in help_msgs:
            intent = self.chatbot.get_intent(msg)
            assert intent == "help", f"Failed for: {msg}"
        
        print("✅ Help Intent Test PASSED")
    
    def test_booking_intent(self):
        """Test recognition of booking requests"""
        booking_msgs = [
            "I want to book a meeting",
            "Can I schedule an appointment?",
            "Book a slot please"
        ]
        
        for msg in booking_msgs:
            intent = self.chatbot.get_intent(msg)
            assert intent == "booking", f"Failed for: {msg}"
        
        print("✅ Booking Intent Test PASSED")
    
    def test_question_intent(self):
        """Test recognition of question patterns"""
        questions = [
            "What is AI?",
            "How does this work?",
            "Why is this happening?",
            "When can I start?",
            "Where is the location?"
        ]
        
        for question in questions:
            intent = self.chatbot.get_intent(question)
            assert intent == "question", f"Failed for: {question}"
        
        print("✅ Question Intent Test PASSED")
    
    def test_weather_intent(self):
        """Test recognition of weather queries"""
        weather_msgs = [
            "What's the weather?",
            "Weather forecast please",
            "Is it going to rain?"
        ]
        
        for msg in weather_msgs:
            intent = self.chatbot.get_intent(msg)
            assert intent == "weather", f"Failed for: {msg}"
        
        print("✅ Weather Intent Test PASSED")
    
    def test_unknown_intent(self):
        """Test handling of unrecognizable messages"""
        unknown_msgs = [
            "asdfghjkl",
            "xyz123",
            "random gibberish"
        ]
        
        for msg in unknown_msgs:
            intent = self.chatbot.get_intent(msg)
            assert intent == "unknown", f"Should be unknown for: {msg}"
        
        print("✅ Unknown Intent Test PASSED")
    
    def test_intent_confidence_scores(self):
        """Test confidence scores for intent classification"""
        # High confidence intents
        high_confidence_intents = ["greeting", "goodbye", "thanks"]
        for intent in high_confidence_intents:
            confidence = self.chatbot.calculate_confidence(intent)
            assert confidence >= 0.9, f"Low confidence for {intent}: {confidence}"
        
        # Medium confidence intents
        medium_confidence_intents = ["booking", "help", "question"]
        for intent in medium_confidence_intents:
            confidence = self.chatbot.calculate_confidence(intent)
            assert 0.7 <= confidence < 0.9, f"Unexpected confidence for {intent}: {confidence}"
        
        # Low confidence for unknown
        confidence = self.chatbot.calculate_confidence("unknown")
        assert confidence < 0.5, f"Too high confidence for unknown: {confidence}"
        
        print("✅ Intent Confidence Test PASSED")
    
    def test_case_insensitivity(self):
        """Test that intent recognition is case-insensitive"""
        messages = [
            ("HELLO", "greeting"),
            ("hello", "greeting"),
            ("HeLLo", "greeting"),
            ("THANK YOU", "thanks"),
            ("thank you", "thanks")
        ]
        
        for msg, expected_intent in messages:
            intent = self.chatbot.get_intent(msg)
            assert intent == expected_intent, f"Case sensitivity issue for: {msg}"
        
        print("✅ Case Insensitivity Test PASSED")
    
    @pytest.mark.parametrize("message,expected_intent", [
        ("Hi there!", "greeting"),
        ("I need help with booking", "help"),
        ("What's the weather like?", "weather"),
        ("Book a meeting for tomorrow", "booking"),
        ("Thanks for your help", "thanks")
    ])
    def test_intent_with_context(self, message, expected_intent):
        """Test intent recognition with additional context"""
        intent = self.chatbot.get_intent(message)
        assert intent == expected_intent
    
    def test_intent_accuracy_metrics(self):
        """Test overall intent classification accuracy"""
        # Load test data
        test_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_conversations.json')
        
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                data = json.load(f)
            
            predictions = []
            ground_truth = []
            
            for sample in data.get('intent_test_samples', []):
                predicted_intent = self.chatbot.get_intent(sample['text'])
                predictions.append(predicted_intent)
                ground_truth.append(sample['intent'])
            
            # Calculate accuracy
            accuracy = self.classifier.calculate_accuracy(predictions, ground_truth)
            
            # Expect >80% accuracy
            assert accuracy >= 0.8, f"Intent accuracy too low: {accuracy:.2%}"
            
            print(f"✅ Intent Accuracy Test PASSED: {accuracy:.2%}")
        else:
            pytest.skip("Test data file not found")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])