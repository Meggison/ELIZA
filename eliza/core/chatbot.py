import re
import random
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Pattern

@dataclass
class ResponsePattern:
    pattern: Pattern
    responses: List[str]
    last_used: str = ""
    usage_count: int = 0

class Eliza:
    def __init__(self):
        self.session_history = []
        self.context = {
            "current_emotion": None,
            "current_topic": None,
            "mentioned_family": False,
            "mentioned_feelings": False
        }
        
        self.responses = [
            ResponsePattern(
                re.compile(r'.*\b(sad|depressed|unhappy|down)\b.*', re.IGNORECASE),
                [
                    "I hear that you're feeling down. Would you like to tell me more about what's been making you feel this way?",
                    "It sounds like you're going through a difficult time. How long have you been feeling this way?",
                    "I'm sorry you're feeling this way. What do you think triggered these feelings?"
                ]
            ),
            ResponsePattern(
                re.compile(r'.*\b(angry|mad|pissed|furious)\b.*', re.IGNORECASE),
                [
                    "I can hear the anger in your words. What specifically made you feel this way?",
                    "Your anger seems very present. When did you start feeling this intense emotion?",
                    "It's okay to feel angry. Can you tell me more about what's causing these strong feelings?"
                ]
            ),
            ResponsePattern(
                re.compile(r'.*\b(family|mother|father|sister|brother|parent)\b.*\b(sucks|terrible|awful|bad)\b.*', re.IGNORECASE),
                [
                    "It sounds like you're having some difficult feelings about your family. Could you tell me more about what's been happening?",
                    "Family relationships can be really challenging. What aspects of your family situation are most difficult for you?",
                    "I can hear that you're struggling with your family. How long has this been affecting you?"
                ]
            ),
            ResponsePattern(
                re.compile(r'.*\b(feel|feeling|felt)\b.*', re.IGNORECASE),
                [
                    "Thank you for sharing your feelings with me. Could you tell me more about what led to these emotions?",
                    "It's important to acknowledge our feelings. How do these emotions affect your daily life?",
                    "I appreciate you opening up about your feelings. What do you think triggered these emotions?"
                ]
            ),
            ResponsePattern(
                re.compile(r'I need (.*)', re.IGNORECASE),
                [
                    "I understand that you need {}. Could you tell me more about why this is important to you?",
                    "What makes you feel that you need {} right now?",
                    "How long have you felt that you need {}?"
                ]
            ),
            ResponsePattern(
                re.compile(r'.*\b(anxious|worried|scared|afraid)\b.*', re.IGNORECASE),
                [
                    "Anxiety can be really overwhelming. What specifically has been causing you to feel this way?",
                    "It's natural to feel anxious sometimes. Can you tell me more about what's worrying you?",
                    "I hear that you're feeling anxious. When did these feelings start?"
                ]
            ),
            ResponsePattern(
                re.compile(r'.*\b(lonely|alone|isolated)\b.*', re.IGNORECASE),
                [
                    "Feeling lonely can be really difficult. How long have you been feeling this way?",
                    "I hear that you're feeling isolated. What do you think has contributed to these feelings?",
                    "It must be hard feeling so alone. Have you felt able to reach out to anyone about this?"
                ]
            ),
            ResponsePattern(
                re.compile(r'Hello|Hi|Hey', re.IGNORECASE),
                [
                    "Hello! I'm here to listen and support you. How are you feeling today?",
                    "Hi there! Thank you for reaching out. What's been on your mind lately?",
                    "Hello! I'm here to help. Would you like to tell me what brings you here today?"
                ]
            ),
            ResponsePattern(
                re.compile(r'Yes', re.IGNORECASE),
                [
                    "I appreciate you confirming that. Could you elaborate more on your thoughts?",
                    "Thank you for being open. Would you like to tell me more about that?",
                    "I see. What other thoughts or feelings come up for you about this?"
                ]
            ),
            ResponsePattern(
                re.compile(r'No', re.IGNORECASE),
                [
                    "I understand that you don't agree. Could you tell me more about your perspective?",
                    "That's completely fine. What are your thoughts on this?",
                    "I appreciate your honesty. What makes you feel that way?"
                ]
            ),
            ResponsePattern(
                re.compile(r'.*\b(help|support)\b.*', re.IGNORECASE),
                [
                    "I'm here to support you. What kind of help would be most useful right now?",
                    "I want to help you in the best way I can. Could you tell me more about what you need?",
                    "You're taking a positive step by asking for help. What's been the hardest part?"
                ]
            ),
            ResponsePattern(
                re.compile(r'.*\b(thank|thanks)\b.*', re.IGNORECASE),
                [
                    "You're welcome. I'm here to listen and support you.",
                    "I appreciate you sharing your thoughts and feelings with me.",
                    "I'm glad I could help. Is there anything else you'd like to discuss?"
                ]
            ),
            ResponsePattern(
                re.compile(r'(.*)\?', re.IGNORECASE),
                [
                    "That's a thoughtful question. What are your own thoughts about this?",
                    "I sense this is something important to you. What makes you ask about this?",
                    "This seems to be weighing on your mind. What led you to this question?"
                ]
            ),
            ResponsePattern(
                re.compile(r'quit|goodbye|bye', re.IGNORECASE),
                [
                    "Thank you for sharing with me today. Take care of yourself.",
                    "I appreciate you opening up to me. Remember that it's okay to reach out for support when you need it.",
                    "Thank you for trusting me with your thoughts and feelings. Take care, and feel free to return anytime."
                ]
            ),
            ResponsePattern(
                re.compile(r'(.*)', re.IGNORECASE),
                [
                    "I'm listening. Could you tell me more about that?",
                    "That sounds important to you. Could you elaborate on what you mean?",
                    "I'd like to understand better. Could you share more about your experience?",
                    "Your feelings are valid. Would you like to explore this further?",
                    "Thank you for sharing that. How does this situation affect you?"
                ]
            )
        ]

    def respond(self, user_input: str) -> str:
        """Generate a response to user input with context awareness."""
        try:
            # Update context based on user input
            self._update_context(user_input.lower())
            
            # Record user input in session history
            self.session_history.append({
                "timestamp": datetime.now().isoformat(),
                "speaker": "user",
                "text": user_input
            })

            # Generate response
            for pattern in self.responses:
                match = pattern.pattern.match(user_input)
                if match:
                    groups = match.groups()
                    
                    # Filter responses based on context
                    available_responses = self._filter_responses_by_context(pattern.responses)
                    if not available_responses:
                        available_responses = pattern.responses
                    
                    response = random.choice(available_responses)
                    pattern.last_used = response
                    
                    try:
                        if groups:
                            final_response = response.format(*groups)
                        else:
                            final_response = response
                    except (IndexError, KeyError):
                        final_response = self._get_contextual_fallback_response()
                    
                    # Record ELIZA's response
                    self.session_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "speaker": "eliza",
                        "text": final_response
                    })
                    
                    return final_response
            
            # If no pattern matches, use contextual default response
            default_response = self._get_contextual_fallback_response()
            self.session_history.append({
                "timestamp": datetime.now().isoformat(),
                "speaker": "eliza",
                "text": default_response
            })
            return default_response
            
        except Exception as e:
            print(f"Error in respond method: {e}")
            return "I want to understand better. Could you rephrase that?"

    def _update_context(self, user_input: str):
        """Update conversation context based on user input."""
        # Track emotions
        if any(word in user_input for word in ['sad', 'depressed', 'unhappy', 'down']):
            self.context['current_emotion'] = 'sad'
        elif any(word in user_input for word in ['angry', 'mad', 'pissed', 'furious']):
            self.context['current_emotion'] = 'angry'
        elif any(word in user_input for word in ['anxious', 'worried', 'scared']):
            self.context['current_emotion'] = 'anxious'
        
        # Track topics
        if any(word in user_input for word in ['family', 'mother', 'father', 'sister', 'brother']):
            self.context['current_topic'] = 'family'
            self.context['mentioned_family'] = True
        
        if 'feel' in user_input:
            self.context['mentioned_feelings'] = True

    def _filter_responses_by_context(self, responses: List[str]) -> List[str]:
        """Filter responses based on current context."""
        if not self.context['current_emotion'] and not self.context['current_topic']:
            return responses
            
        filtered = []
        for response in responses:
            # Avoid asking about feelings if already discussing them
            if self.context['mentioned_feelings'] and 'feel' in response.lower():
                continue
            # Avoid changing topic if currently discussing something important
            if self.context['current_topic'] and 'change focus' in response.lower():
                continue
            filtered.append(response)
            
        return filtered or responses

    def _get_contextual_fallback_response(self) -> str:
        """Generate a context-aware fallback response."""
        if self.context['current_emotion'] == 'sad':
            return "I hear that you're going through a difficult time. Would you like to tell me more about what's troubling you?"
        elif self.context['current_emotion'] == 'angry':
            return "I can sense that this is really frustrating for you. Could you help me understand what's making you feel this way?"
        elif self.context['current_emotion'] == 'anxious':
            return "It sounds like you're dealing with a lot of anxiety. What do you think is contributing to these feelings?"
        elif self.context['current_topic'] == 'family':
            return "Family situations can be complex. How are you coping with these challenges?"
        else:
            return "I'm here to listen. Could you tell me more about what's on your mind?"

    def save_session(self, filepath: str = "eliza_session.json"):
        """Save the current session history to a file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.session_history, f, indent=2)
        except Exception as e:
            print(f"Error saving session: {e}")
