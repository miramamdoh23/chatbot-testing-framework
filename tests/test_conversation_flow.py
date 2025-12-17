"""
Conversation Flow Tests
Tests for multi-turn conversation handling and flow logic
Author: Mira Mamdoh
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.mock_chatbot import Conversation


class TestConversationFlow:
    """Test suite for conversation flow management"""
    
    def test_simple_greeting_flow(self):
        """Test basic greeting conversation"""
        conv = Conversation()
        
        response = conv.send("Hello")
        assert "help" in response.lower() or "hello" in response.lower()
        
        print("✅ Simple Greeting Flow Test PASSED")
    
    def test_multi_turn_booking_flow(self):
        """Test complete booking conversation flow"""
        conv = Conversation()
        
        # Step 1: Initial booking request
        response1 = conv.send("I want to book a meeting")
        assert "when" in response1.lower() or "schedule" in response1.lower()
        
        # Step 2: Provide time
        response2 = conv.send("Tomorrow at 2pm")
        assert "confirm" in response2.lower() or "booking" in response2.lower()
        
        # Verify conversation has 4 messages (2 user, 2 bot)
        history = conv.get_history()
        assert len(history) == 4
        
        print("✅ Multi-turn Booking Flow Test PASSED")
    
    def test_help_then_booking_flow(self):
        """Test transitioning from help to booking"""
        conv = Conversation()
        
        # Ask for help
        response1 = conv.send("I need help")
        assert "help" in response1.lower() or "assist" in response1.lower()
        
        # Then book
        response2 = conv.send("I want to book a meeting")
        assert "when" in response2.lower() or "schedule" in response2.lower()
        
        print("✅ Help to Booking Flow Test PASSED")
    
    def test_greeting_help_goodbye_flow(self):
        """Test complete conversation from greeting to goodbye"""
        conv = Conversation()
        
        # Greeting
        response1 = conv.send("Hi")
        assert len(response1) > 0
        
        # Help request
        response2 = conv.send("Can you help me?")
        assert "help" in response2.lower() or "assist" in response2.lower()
        
        # Thanks
        response3 = conv.send("Thank you")
        assert "welcome" in response3.lower() or "happy" in response3.lower()
        
        # Goodbye
        response4 = conv.send("Bye")
        assert "bye" in response4.lower() or "goodbye" in response4.lower()
        
        # Check history length (8 messages: 4 user + 4 bot)
        history = conv.get_history()
        assert len(history) == 8
        
        print("✅ Complete Conversation Flow Test PASSED")
    
    def test_conversation_history_tracking(self):
        """Test that conversation history is properly tracked"""
        conv = Conversation()
        
        conv.send("Hello")
        conv.send("I need help")
        conv.send("Thanks")
        
        history = conv.get_history()
        
        # Should have 6 entries (3 user + 3 bot)
        assert len(history) == 6
        
        # Check alternating user/assistant
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"
        assert history[2]["role"] == "user"
        assert history[3]["role"] == "assistant"
        
        print("✅ Conversation History Test PASSED")
    
    def test_conversation_reset(self):
        """Test conversation reset functionality"""
        conv = Conversation()
        
        # Have a conversation
        conv.send("Hello")
        conv.send("I need help")
        
        # Verify history exists
        assert len(conv.get_history()) > 0
        
        # Reset
        conv.reset()
        
        # Verify history is cleared
        assert len(conv.get_history()) == 0
        assert conv.last_response == ""
        
        print("✅ Conversation Reset Test PASSED")
    
    def test_interrupted_booking_flow(self):
        """Test handling of interrupted booking flow"""
        conv = Conversation()
        
        # Start booking
        conv.send("I want to book a meeting")
        
        # Interrupt with different intent
        response = conv.send("What's the weather?")
        assert "weather" in response.lower() or "sunny" in response.lower()
        
        # Continue booking
        conv.send("Book a meeting")
        response = conv.send("Tomorrow at 3pm")
        assert "confirm" in response.lower()
        
        print("✅ Interrupted Booking Flow Test PASSED")
    
    def test_rapid_intent_switching(self):
        """Test handling rapid changes in conversation topic"""
        conv = Conversation()
        
        intents_to_test = [
            ("Hello", "greeting"),
            ("What's the weather?", "weather"),
            ("Book a meeting", "booking"),
            ("Cancel", "cancel"),
            ("Thanks", "thanks")
        ]
        
        for message, expected_intent in intents_to_test:
            response = conv.send(message)
            assert len(response) > 0, f"No response for: {message}"
        
        # Should have 10 messages (5 user + 5 bot)
        assert len(conv.get_history()) == 10
        
        print("✅ Rapid Intent Switching Test PASSED")
    
    def test_empty_message_handling(self):
        """Test handling of empty or whitespace messages"""
        conv = Conversation()
        
        # Empty string
        response1 = conv.send("")
        assert len(response1) > 0
        
        # Whitespace only
        response2 = conv.send("   ")
        assert len(response2) > 0
        
        print("✅ Empty Message Handling Test PASSED")
    
    def test_very_long_conversation(self):
        """Test handling of extended conversation"""
        conv = Conversation()
        
        # Simulate 10 turns
        for i in range(10):
            response = conv.send(f"Message {i}")
            assert len(response) > 0
        
        # Should have 20 messages
        history = conv.get_history()
        assert len(history) == 20
        
        print("✅ Long Conversation Test PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])