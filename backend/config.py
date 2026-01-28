"""
Configuration settings for the multimodal AI system.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration."""
    
    # Analysis Settings
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Image Processing
    MAX_IMAGE_SIZE_MB = 10
    MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    RESIZE_MAX_DIMENSION = 2048  # Max width or height
    
    # Model Configuration

    GENERATION_CONFIG = {
        'temperature': 0.7,
        'max_tokens': 2048,
    }
