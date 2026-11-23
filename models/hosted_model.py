"""Convenience wrapper around the local/Jetstream2-hosted model configuration."""
from models.model_factory import get_model

def load_hosted_model():
    return get_model('HOSTED')
