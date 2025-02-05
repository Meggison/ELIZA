"""
Response pattern definitions for the ELIZA chatbot.
"""

from dataclasses import dataclass
from typing import List, Pattern
import re

@dataclass
class ResponsePattern:
    """
    A dataclass representing a response pattern with its associated responses.
    
    Attributes:
        pattern (Pattern): Compiled regex pattern for matching user input
        responses (List[str]): List of possible response templates
        last_used (str): The last response used from this pattern
        usage_count (int): Number of times this pattern has been used
    """
    pattern: Pattern
    responses: List[str]
    last_used: str = ""
    usage_count: int = 0

# Common regex patterns
EMOTION_PATTERNS = {
    'sad': r'.*\b(sad|depressed|unhappy|down)\b.*',
    'angry': r'.*\b(angry|mad|pissed|furious)\b.*',
    'anxious': r'.*\b(anxious|worried|scared|afraid)\b.*',
    'lonely': r'.*\b(lonely|alone|isolated)\b.*'
}

TOPIC_PATTERNS = {
    'family': r'.*\b(family|mother|father|sister|brother|parent)\b.*',
    'work': r'.*\b(work|job|career|boss|colleague)\b.*',
    'health': r'.*\b(health|sick|illness|doctor)\b.*',
    'relationships': r'.*\b(relationship|partner|spouse|boyfriend|girlfriend)\b.*'
}
