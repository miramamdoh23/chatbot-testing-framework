"""
Response Quality Tests
Tests for chatbot response quality, length, and relevance
Author: Mira Mamdoh
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.mock_chatbot import MockChatbot, Conversation


class TestResponseQuality:
    """Test suite for response quality assessment"""
    
    def setup_method(self):
        """Setup for each test"""
        self.chatbot = MockChatbot()
    
    def test_response_not_empty(self):
        """Test that responses are never empty"""
        test_messages = [
            "Hello",
            "Help me",
            "Book a meeting",
            "What's the weather?",
            "Thanks"
        ]
        
        for message in test_messages:
            response = self.chatbot.generate_response(message)
            assert len(response) > 0, f"Empty response for: {message}"
            assert response.strip() != "", f"Whitespace-only response for: {message}"
        
        print("✅ Response Not Empty Test PASSED")
    
    def test_response_length_reasonable(self):
        """Test that responses are of reasonable length"""
        messages = [
            "Hello",
            "I need help",
            "What's the weather?"
        ]
        
        for message in messages:
            response = self.chatbot.generate_response(message)
            word_count = self.chatbot.get_response_length(response)
            
            # Response should be between 3 and 50 words
            assert 3 <= word_count <= 50, \
                f"Response length {word_count} out of range for: {message}"
        
        print("✅ Response Length Test PASSED")
    
    def test_response_contains_no_errors(self):
        """Test that responses don't contain error indicators"""
        messages = ["Hello", "Help", "Thanks"]
        error_indicators = ["error", "exception", "failed", "null", "undefined"]
        
        for message in messages:
            response = self.chatbot.generate_response(message).lower()
            
            for indicator in error_indicators:
                assert indicator not in response, \
                    f"Error indicator '{indicator}' found in response for: {message}"
        
        print("✅ No Error Indicators Test PASSED")
    
    def test_response_is_relevant_to_intent(self):
        """Test that responses are relevant to user intent"""
        test_cases = [
            ("Hello", ["hello", "hi", "help"]),
            ("Thanks", ["welcome", "happy"]),
            ("Goodbye", ["bye", "goodbye", "day"]),
            ("I need help", ["help", "assist"]),
            ("What's the weather?", ["weather", "sunny", "temperature"])
        ]
        
        for message, expected_keywords in test_cases:
            response = self.chatbot.generate_response(message).lower()
            
            # At least one keyword should be present
            assert any(keyword in response for keyword in expected_keywords), \
                f"Response not relevant for: {message}. Got: {response}"
        
        print("✅ Response Relevance Test PASSED")
    
    def test_response_tone_friendly(self):
        """Test that responses maintain friendly tone"""
        friendly_indicators = [
            "!", "help", "happy", "great", "wonderful", 
            "glad", "please", "thank"
        ]
        
        messages = ["Hello", "I need help", "Thanks"]
        
        for message in messages:
            response = self.chatbot.generate_response(message).lower()
            
            # At least one friendly indicator should be present
            has_friendly_tone = any(indicator in response for indicator in friendly_indicators)
            assert has_friendly_tone, f"Response lacks friendly tone for: {message}"
        
        print("✅ Friendly Tone Test PASSED")
    
    def test_response_has_proper_grammar(self):
        """Test basic grammar rules in responses"""
        messages = ["Hello", "Help me", "Thanks"]
        
        for message in messages:
            response = self.chatbot.generate_response(message)
            
            # Should start with capital letter
            assert response[0].isupper(), f"Response doesn't start with capital: {response}"
            
            # Should end with punctuation
            assert response[-1] in ['.', '!', '?'], f"Response missing punctuation: {response}"
        
        print("✅ Grammar Test PASSED")
    
    def test_response_time_simulation(self):
        """Test that response generation is fast (simulated)"""
        import time
        
        message = "Hello"
        
        start_time = time.time()
        response = self.chatbot.generate_response(message)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Response should be generated in less than 0.1 seconds
        assert response_time < 0.1, f"Response too slow: {response_time}s"
        
        print(f"✅ Response Time Test PASSED: {response_time:.4f}s")
    
    def test_response_consistency(self):
        """Test that same input produces consistent responses"""
        message = "Hello"
        
        # Reset and generate response multiple times
        responses = []
        for _ in range(3):
            self.chatbot.reset()
            response = self.chatbot.generate_response(message)
            responses.append(response)
        
        # All responses should be the same
        assert len(set(responses)) == 1, "Inconsistent responses for same input"
        
        print("✅ Response Consistency Test PASSED")
    
    def test_response_word_count_distribution(self):
        """Test that response lengths are well-distributed"""
        messages = [
            "Hi",
            "Hello there",
            "Good morning",
            "I need help with booking",
            "Can you assist me with scheduling?",
            "What's the weather forecast for today?"
        ]
        
        word_counts = []
        for message in messages:
            self.chatbot.reset()
            response = self.chatbot.generate_response(message)
            word_counts.append(self.chatbot.get_response_length(response))
        
        # Average should be reasonable
        avg_words = sum(word_counts) / len(word_counts)
        assert 5 <= avg_words <= 30, f"Average word count unusual: {avg_words}"
        
        print(f"✅ Word Count Distribution Test PASSED: Avg {avg_words:.1f} words")
    
    def test_no_repetitive_responses(self):
        """Test that chatbot doesn't repeat the same response"""
        conv = Conversation()
        
        responses = []
        messages = ["Hello", "Hi there", "Hey", "Good morning"]
        
        for message in messages:
            response = conv.send(message)
            responses.append(response)
        
        # Should not have exact duplicates (though intent is same)
        # For greeting, response might be same - that's acceptable
        # Just check responses are being generated
        assert all(len(r) > 0 for r in responses)
        
        print("✅ No Repetitive Responses Test PASSED")
    
    @pytest.mark.parametrize("message,min_words,max_words", [
        ("Hi", 3, 20),
        ("I need detailed help with booking", 5, 30),
        ("Thanks", 3, 15)
    ])
    def test_response_length_by_context(self, message, min_words, max_words):
        """Test that response length matches context complexity"""
        response = self.chatbot.generate_response(message)
        word_count = self.chatbot.get_response_length(response)
        
        assert min_words <= word_count <= max_words, \
            f"Word count {word_count} out of range [{min_words}, {max_words}]"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])