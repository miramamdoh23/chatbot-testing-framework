"""
Context Handling Tests
Tests for chatbot's ability to maintain and use conversation context
Author: Mira Mamdoh
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.mock_chatbot import Conversation


class TestContextHandling:
    """Test suite for context management in conversations"""
    
    def test_name_context_storage(self):
        """Test that chatbot remembers user's name"""
        conv = Conversation()
        
        # Introduce name
        response1 = conv.send("My name is Mira")
        assert "mira" in response1.lower()
        
        # Check context
        context = conv.get_context()
        assert "user_name" in context
        assert context["user_name"] == "Mira"
        
        print("✅ Name Storage Test PASSED")
    
    def test_name_context_recall(self):
        """Test that chatbot can recall stored name"""
        conv = Conversation()
        
        # Store name
        conv.send("My name is Mira")
        
        # Ask for name
        response = conv.send("What's my name?")
        assert "mira" in response.lower()
        
        print("✅ Name Recall Test PASSED")
    
    def test_name_context_variations(self):
        """Test different ways of introducing name"""
        test_cases = [
            "My name is Ahmed",
            "I am Sara",
            "I'm John",
            "Call me Alex"
        ]
        
        for intro in test_cases:
            conv = Conversation()
            conv.send(intro)
            
            context = conv.get_context()
            assert "user_name" in context, f"Failed to store name from: {intro}"
            assert len(context["user_name"]) > 0
        
        print("✅ Name Variations Test PASSED")
    
    def test_booking_context_tracking(self):
        """Test booking context is maintained across turns"""
        conv = Conversation()
        
        # Start booking
        conv.send("I want to book a meeting")
        
        context = conv.get_context()
        assert "booking_started" in context
        assert context["booking_started"] == True
        
        # Provide time
        conv.send("Tomorrow at 2pm")
        
        context = conv.get_context()
        assert "booking_time" in context
        
        print("✅ Booking Context Tracking Test PASSED")
    
    def test_context_persistence_across_intents(self):
        """Test context persists when switching topics"""
        conv = Conversation()
        
        # Store name
        conv.send("My name is Mira")
        
        # Switch to different topic
        conv.send("What's the weather?")
        
        # Name should still be remembered
        response = conv.send("What's my name?")
        assert "mira" in response.lower()
        
        print("✅ Context Persistence Test PASSED")
    
    def test_context_reset_clears_data(self):
        """Test that reset clears all context"""
        conv = Conversation()
        
        # Build up context
        conv.send("My name is Mira")
        conv.send("I want to book a meeting")
        
        # Verify context exists
        assert len(conv.get_context()) > 0
        
        # Reset
        conv.reset()
        
        # Context should be empty
        assert len(conv.get_context()) == 0
        
        print("✅ Context Reset Test PASSED")
    
    def test_multiple_context_variables(self):
        """Test handling multiple context variables simultaneously"""
        conv = Conversation()
        
        # Set multiple context items
        conv.send("My name is Mira")
        conv.send("I want to book a meeting")
        
        context = conv.get_context()
        
        # Both should be present
        assert "user_name" in context
        assert "booking_started" in context
        assert context["user_name"] == "Mira"
        assert context["booking_started"] == True
        
        print("✅ Multiple Context Variables Test PASSED")
    
    def test_context_used_in_responses(self):
        """Test that context actually influences responses"""
        conv = Conversation()
        
        # Without name context
        response1 = conv.send("What's my name?")
        assert "don't know" in response1.lower() or "what should i call you" in response1.lower()
        
        # With name context
        conv.send("My name is Mira")
        response2 = conv.send("What's my name?")
        assert "mira" in response2.lower()
        assert response1 != response2
        
        print("✅ Context Influences Responses Test PASSED")
    
    def test_context_overwrites_correctly(self):
        """Test that new context overwrites old values"""
        conv = Conversation()
        
        # Set initial name
        conv.send("My name is Ahmed")
        assert conv.get_context()["user_name"] == "Ahmed"
        
        # Change name
        conv.send("Actually, my name is Sara")
        assert conv.get_context()["user_name"] == "Sara"
        
        print("✅ Context Overwrite Test PASSED")
    
    def test_context_isolation_between_conversations(self):
        """Test that different conversations have separate contexts"""
        conv1 = Conversation()
        conv2 = Conversation()
        
        # Set name in first conversation
        conv1.send("My name is Mira")
        
        # Second conversation should not have this context
        context2 = conv2.get_context()
        assert "user_name" not in context2
        
        print("✅ Context Isolation Test PASSED")
    
    def test_booking_flow_context_completion(self):
        """Test complete booking flow with context"""
        conv = Conversation()
        
        # Start booking
        conv.send("I want to book a meeting")
        assert conv.get_context()["booking_started"] == True
        
        # Complete booking
        conv.send("Tomorrow at 2pm")
        
        # Booking should be marked complete
        context = conv.get_context()
        assert "booking_time" in context
        # booking_started should be False after completion
        assert context.get("booking_started", False) == False
        
        print("✅ Booking Flow Completion Test PASSED")
    
    def test_context_with_complex_conversation(self):
        """Test context handling in complex multi-turn conversation"""
        conv = Conversation()
        
        # Complex flow
        conv.send("Hello")
        conv.send("My name is Mira")
        conv.send("I need help")
        conv.send("I want to book a meeting")
        conv.send("Tomorrow at 3pm")
        
        # Check final context
        context = conv.get_context()
        assert "user_name" in context
        assert context["user_name"] == "Mira"
        
        # History should be complete
        history = conv.get_history()
        assert len(history) == 10  # 5 user + 5 bot messages
        
        print("✅ Complex Conversation Context Test PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])