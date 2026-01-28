"""
OpenAI API client for vision-language tasks.
"""
from openai import OpenAI
from config import Config
import base64
from io import BytesIO
import time

class OpenAIClient:
    """Client for interacting with OpenAI GPT-4 Vision API."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.MODEL_NAME
    
    def _image_to_base64(self, image):
        """
        Convert PIL Image to base64 string.
        
        Args:
            image: PIL.Image object
            
        Returns:
            str: Base64 encoded image
        """
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=95)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def analyze_image(self, image, prompt):
        """
        Analyze image with given prompt using GPT-4 Vision.
        
        Args:
            image: PIL.Image object
            prompt: Text prompt for analysis
            
        Returns:
            str: Generated text response
        """
        try:
            # Convert image to base64
            base64_image = self._image_to_base64(image)
            
            # Create message with image and prompt
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=Config.GENERATION_CONFIG['max_tokens'],
                temperature=Config.GENERATION_CONFIG['temperature']
            )
            
            # Extract text from response
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
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
                    print(f"Retry attempt {attempt + 1} after {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise last_error
