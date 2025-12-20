# Chatbot Testing Framework

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Testing-Pytest-green.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Comprehensive testing framework for GenAI chatbots with focus on conversation flow, intent recognition, response quality, and context handling.

---

## Purpose

This framework demonstrates professional testing practices for conversational AI systems, including:

- **Conversation Flow Testing**: Multi-turn dialogue validation
- **Intent Recognition**: NLP classification accuracy
- **Response Quality Assessment**: Relevance, tone, and grammar
- **Context Handling**: Memory and state management
- **Error Scenario Testing**: Edge cases and failure modes

---

## Technologies Used

- **Python 3.9+**: Core programming language
- **Pytest**: Testing framework
- **Mock Chatbot**: Simulated GenAI assistant
- **JSON**: Test data management

---

## Installation
```bash
# Clone the repository
git clone https://github.com/miramamdoh23/chatbot-testing-framework.git
cd chatbot-testing-framework

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Quick Start
```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_intent_recognition.py -v

# Generate HTML report
pytest --html=reports/test_report.html tests/

# Run with coverage
pytest --cov=chatbot --cov=tests tests/
```

---

## Test Results

**Latest Test Run**: All tests passing
```bash
======================== test passed ========================
```

### Test Categories

| Category | Tests | Description |
|----------|-------|-------------|
| **Intent Recognition** | 12 | Classification accuracy, confidence scores |
| **Conversation Flow** | 10 | Multi-turn dialogues, flow management |
| **Response Quality** | 11 | Length, relevance, tone, grammar |
| **Context Handling** | 12 | Memory, state persistence, recall |

**Total: 45+ comprehensive test cases**

---

## Test Coverage Breakdown

### 1. Intent Recognition Tests

Tests the chatbot's ability to correctly classify user intents:

- Greeting intent (Hello, Hi, Good morning)
- Goodbye intent (Bye, Farewell)
- Help requests
- Booking requests
- Questions (What, How, Why)
- Weather queries
- Thank you messages
- Unknown intent handling
- Confidence scoring
- Case insensitivity
- Overall accuracy metrics (>80% target)

**Example**:
```python
def test_greeting_intent():
    """Test recognition of greeting messages"""
    assert chatbot.get_intent("Hello") == "greeting"
    assert chatbot.get_intent("Good morning") == "greeting"
```

### 2. Conversation Flow Tests

Tests multi-turn conversation handling:

- Simple greeting flows
- Multi-turn booking flows
- Intent switching (Help → Booking)
- Complete conversations (Greeting → Help → Thanks → Goodbye)
- Conversation history tracking
- Reset functionality
- Interrupted flows
- Rapid intent switching
- Empty message handling
- Extended conversations (10+ turns)

**Example**:
```python
def test_multi_turn_booking_flow():
    """Test complete booking conversation"""
    conv = Conversation()
    conv.send("I want to book a meeting")
    response = conv.send("Tomorrow at 2pm")
    assert "confirm" in response.lower()
```

### 3. Response Quality Tests

Tests the quality and appropriateness of chatbot responses:

- Non-empty responses
- Reasonable length (3-50 words)
- No error indicators
- Relevance to user intent
- Friendly tone
- Proper grammar (capitalization, punctuation)
- Fast response time (<0.1s)
- Consistency
- Word count distribution
- No repetitive responses

**Example**:
```python
def test_response_tone_friendly():
    """Test friendly tone in responses"""
    response = chatbot.generate_response("Hello")
    assert any(word in response.lower() 
               for word in ["!", "help", "happy"])
```

### 4. Context Handling Tests

Tests the chatbot's memory and context management:

- Name storage and recall
- Name introduction variations
- Booking context tracking
- Context persistence across intents
- Context reset
- Multiple context variables
- Context influence on responses
- Context overwriting
- Conversation isolation
- Complex multi-turn context

**Example**:
```python
def test_name_context_recall():
    """Test chatbot remembers user's name"""
    conv.send("My name is Mira")
    response = conv.send("What's my name?")
    assert "mira" in response.lower()
```

---

## Project Structure
```
chatbot-testing-framework/
│
├── chatbot/                          # Chatbot implementation
│   ├── __init__.py                   
│   ├── mock_chatbot.py               # Mock GenAI chatbot
│   └── intent_classifier.py          # Intent classification utilities
│
├── tests/                            # Test suites
│   ├── __init__.py
│   ├── test_conversation_flow.py     # Conversation flow tests
│   ├── test_intent_recognition.py    # Intent classification tests
│   ├── test_response_quality.py      # Response quality tests
│   └── test_context_handling.py      # Context management tests
│
├── data/                             # Test data
│   └── test_conversations.json       # Test conversation scenarios
│
├── reports/                          # Test reports
│   └── test_report.html              # HTML test results
│
├── requirements.txt                  # Dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # Documentation
```

---

## Skills Demonstrated

This project showcases expertise in:

| Skill | Implementation |
|-------|----------------|
| **GenAI Testing** | Conversational AI validation |
| **NLP Concepts** | Intent, Entity, Context understanding |
| **Test Automation** | Pytest framework, fixtures |
| **Quality Assurance** | Comprehensive test coverage |
| **Python Programming** | Clean, modular code |
| **Mock Design** | Simulated AI for testing |
| **Conversation Design** | UX for chatbots |
| **Performance Testing** | Response time validation |
| **Context Management** | State tracking and memory |
| **Documentation** | Clear, professional README |

---

## Key Features

### Mock Chatbot Implementation
- Simulates GenAI chatbot behavior
- 10+ intent classifications
- Context tracking and memory
- Multi-turn conversation support
- Confidence scoring

### Comprehensive Test Coverage
- 45+ test cases across 4 categories
- Parametrized testing for efficiency
- Edge case validation
- Performance benchmarks

### Professional Reporting
- HTML test reports with pytest-html
- Coverage analysis
- Detailed test documentation

---

## Use Cases

This framework can be adapted for testing:

- **Customer Service Chatbots**: Support automation
- **Virtual Assistants**: Task completion bots
- **Educational Chatbots**: Learning companions
- **Healthcare Chatbots**: Medical information systems
- **E-commerce Chatbots**: Shopping assistants

---

## Customization

### Adding New Intents

Edit `chatbot/mock_chatbot.py`:
```python
self.intents = {
    "greeting": ["hello", "hi"],
    "your_new_intent": ["keyword1", "keyword2"]  # Add here
}

self.responses = {
    "your_new_intent": "Your response here"  # Add here
}
```

### Adding New Tests

Create new test file in `tests/`:
```python
import pytest
from chatbot.mock_chatbot import MockChatbot

class TestNewFeature:
    def test_new_functionality(self):
        chatbot = MockChatbot()
        # Your test logic here
        assert True
```

---

## Performance Metrics

- **Intent Classification Accuracy**: >80%
- **Response Time**: <0.1 seconds
- **Test Execution Time**: <5 seconds for all tests
- **Test Pass Rate**: 100%

---

## Testing Strategy

### 1. Happy Path Testing
- Standard conversation flows
- Expected user inputs
- Typical use cases

### 2. Edge Case Testing
- Empty messages
- Very long conversations
- Rapid topic switching
- Interrupted flows

### 3. Error Handling
- Unknown intents
- Malformed inputs
- Context conflicts

### 4. Performance Testing
- Response time benchmarks
- Conversation length limits
- Context memory efficiency

---

## Future Enhancements

- Integration with real GenAI APIs (OpenAI, Claude)
- Entity extraction testing
- Sentiment analysis validation
- Multi-language support testing
- Load testing for concurrent conversations
- A/B testing framework
- Response diversity metrics

---

## Author

**Mira Mamdoh Yousef Mossad**  
AI QA Engineer | GenAI Testing Specialist

**Specializing in**:
- AI/ML Quality Assurance
- GenAI Application Testing
- Conversational AI Validation
- Test Automation & CI/CD

**Connect**:
- Email: miramamdoh10@gmail.com
- LinkedIn: [linkedin.com/in/mira-mamdoh-a9aa78224](https://www.linkedin.com/in/mira-mamdoh-a9aa78224)
- GitHub: [github.com/miramamdoh23](https://github.com/miramamdoh23)

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

Built to demonstrate professional GenAI testing methodologies and best practices for conversational AI quality assurance.

---

## Contact

For questions, suggestions, or collaboration opportunities, feel free to reach out via:
- GitHub Issues
- Email: miramamdoh10@gmail.com
- LinkedIn: [Mira Mamdoh](https://www.linkedin.com/in/mira-mamdoh-a9aa78224)

---

**Built by Mira Mamdoh**
