"""
Routes initialization
"""
from .disease import disease_bp
from .skincare import skincare_bp
from .chatbot_route import chatbot_bp

__all__ = ['disease_bp', 'skincare_bp', 'chatbot_bp']