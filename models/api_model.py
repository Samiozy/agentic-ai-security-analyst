"""Convenience wrapper around a paid API model configuration."""
from models.model_factory import get_model

def load_api_model():
    return get_model('API')
