"""
ELIZA Chatbot Package
--------------------

A modern implementation of the ELIZA chatbot with context awareness
and natural language processing capabilities.
"""

from .core.chatbot import Eliza
from .core.response_patterns import ResponsePattern

__version__ = '1.0.0'
__author__ = 'Your Name'
__all__ = ['Eliza', 'ResponsePattern']
