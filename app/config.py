import os
# Replace these placeholders with actual credentials or set via environment variables.
class Config:
    # Configuration loaded from environment variables with defaults
    ARGILLA_API_KEY = os.environ.get('ARGILLA_API_KEY', 'argilla.apikey')
    ARGILLA_API_URL = os.environ.get('ARGILLA_API_URL', 'http://localhost:6900')
    ARGILLA_DATASET = os.environ.get('ARGILLA_DATASET', 'feedback-ai')
    ARGILLA_WORKSPACE = os.environ.get('ARGILLA_WORKSPACE', 'rh-argilla')
