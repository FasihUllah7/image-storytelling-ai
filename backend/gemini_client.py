"""
Gemini API client for vision-language tasks.
"""
import google.generativeai as genai
from config import Config
import time

class GeminiClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client."""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            generation_config=Config.GENERATION_CONFIG,
            safety_settings=Config.SAFETY_SETTINGS
        )
    
    def analyze_image(self, image, prompt):
        """
        Analyze image with given prompt.
        
        Args:
            image: PIL.Image object
            prompt: Text prompt for analysis
            
        Returns:
            str: Generated text response
        """
        try:
            # Generate content
            response = self.model.generate_content([prompt, image])
            
            # Handle blocked responses
            if not response.text:
                if hasattr(response, 'prompt_feedback'):
                    return f"[Response blocked: {response.prompt_feedback}]"
                return "[No response generated]"
            
            return response.text.strip()
            
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def analyze_with_retry(self, image, prompt, max_retries=3):
        """
        Analyze image with retry logic.
        
        Args:
            image: PIL.Image object
            prompt: Text prompt
            max_retries: Maximum number of retry attempts
            
        Returns:
            str: Generated response
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                return self.analyze_image(image, prompt)
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = (2 ** attempt) * 1
                    time.sleep(wait_time)
                    continue
                else:
                    raise last_error
