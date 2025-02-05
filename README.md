# Modern ELIZA Chatbot 🤖

A modern, context-aware implementation of the classic ELIZA chatbot, featuring both a sleek web interface and command-line interaction. This version combines the original pattern-matching approach with enhanced natural language processing and emotional intelligence.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[View Demo](#) | [Report Bug](#) | [Request Feature](#)

![ELIZA Demo](docs/images/eliza-demo.gif)

## ✨ Features

- **🎯 Context-Aware Conversations**
  - Tracks emotional state and conversation topics
  - Maintains conversation history
  - Provides contextually relevant responses

- **🌐 Modern Web Interface**
  - ChatGPT-style UI
  - Real-time responses
  - Mobile-responsive design
  - Typing indicators
  - Session persistence

- **🧠 Advanced NLP Capabilities**
  - Emotion detection
  - Pattern matching with regular expressions
  - Subject-object extraction
  - N-gram analysis

- **📊 Analysis Tools**
  - Conversation history tracking
  - Emotion tracking
  - Response pattern usage statistics
  - Perplexity calculation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ELIZA.git
cd ELIZA
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux:
python -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

### Running ELIZA

#### Web Interface
```bash
# Start the Flask server
python -m eliza.web.app

# Open your browser and navigate to:
# http://localhost:5000
```

#### Command Line Interface
```bash
python -m eliza.cli

# Or with session file specification:
python -m eliza.cli --session-file my_session.json
```

## 📁 Project Structure

```
ELIZA/
├── eliza/                  # Main package directory
│   ├── core/              # Core chatbot functionality
│   │   ├── chatbot.py     # Main ELIZA implementation
│   │   └── patterns.py    # Response patterns
│   ├── utils/             # Utility functions
│   │   └── text.py       # Text processing utilities
│   └── web/              # Web interface
│       ├── static/       # Static assets
│       └── templates/    # HTML templates
├── tests/                # Test suite
├── docs/                 # Documentation
├── README.md            # This file
├── LICENSE              # MIT License
└── setup.py            # Package configuration
```

## 💡 Usage Examples

### Web Interface

1. Start a conversation:
```python
from eliza.web.app import main
main()
```

2. Open your browser to `http://localhost:5000`
3. Start chatting!

### Command Line

```python
from eliza.core.chatbot import Eliza

# Initialize ELIZA
eliza = Eliza()

# Get a response
response = eliza.respond("I've been feeling sad lately")
print(response)
# Output: "I hear that you're feeling down. Would you like to tell me more about what's been making you feel this way?"
```

### Custom Response Patterns

```python
from eliza.core.patterns import ResponsePattern
import re

# Create a custom pattern
custom_pattern = ResponsePattern(
    pattern=re.compile(r'I love (.*)', re.IGNORECASE),
    responses=[
        "Tell me more about your feelings towards {}",
        "What makes you love {} so much?",
        "Since when have you felt this way about {}?"
    ]
)

# Add to ELIZA's patterns
eliza = Eliza()
eliza.responses.append(custom_pattern)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:
```env
FLASK_ENV=development
DEBUG=True
SESSION_FILE=eliza_session.json
```

### Response Patterns

Patterns are defined in `eliza/core/patterns.py`. Each pattern includes:
- Regular expression for matching user input
- List of possible responses
- Placeholders for captured groups

## 📊 Analysis Tools

### Emotion Tracking

```python
from eliza.utils.text import detect_emotion

emotion = detect_emotion("I'm feeling really anxious about this")
print(emotion)  # Output: "anxious"
```

### Session Analysis

```python
# Load a session file
with open('eliza_session.json', 'r') as f:
    session = json.load(f)

# Analyze emotions over time
emotions = [msg['emotion'] for msg in session if 'emotion' in msg]
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Code style
- Development process
- Submitting pull requests
- Adding new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original ELIZA by Joseph Weizenbaum
- Modern UI inspired by ChatGPT
- Contributors and maintainers

## 📫 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/ELIZA](https://github.com/yourusername/ELIZA)

## 🔜 Roadmap

- [ ] Add support for multiple languages
- [ ] Implement more sophisticated NLP techniques
- [ ] Add voice interaction
- [ ] Create a mobile app
- [ ] Add support for plugins

## 📚 Additional Resources

- [Original ELIZA Paper](link-to-paper)
- [Documentation](link-to-docs)
- [API Reference](link-to-api-docs)
- [Tutorial Videos](link-to-videos)
