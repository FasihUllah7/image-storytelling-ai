"""
Main processing pipeline for multimodal image analysis.
"""
from openai_client import OpenAIClient
from image_processor import ImageProcessor
import prompts

class AnalysisPipeline:
    """Orchestrate the five-stage analysis pipeline."""
    
    def __init__(self):
        """Initialize pipeline with OpenAI client."""
        self.client = OpenAIClient()
        self.processor = ImageProcessor()
    
    def process_image(self, image_data):
        """
        Process image through complete pipeline in a single request.
        
        Args:
            image_data: File-like object, bytes, or PIL.Image
            
        Returns:
            dict: Analysis results with all five outputs
        """
        import json
        import re

        # Validate and preprocess
        is_valid, error = self.processor.validate_image(image_data)
        if not is_valid:
            raise ValueError(error)
        
        image = self.processor.preprocess_image(image_data)
        
        try:
            # Single stage: Consolidated Analysis
            print("Running consolidated image analysis...")
            prompt = prompts.get_analysis_prompt()
            response_text = self.client.analyze_with_retry(image, prompt)
            
            # Extract JSON from response (handling potential markdown blocks)
            json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            if json_match:
                results = json.loads(json_match.group(1))
            else:
                # Fallback if no JSON structure found
                results = json.loads(response_text)
            
            # Ensure metadata is added
            results['metadata'] = {
                'image_size': image.size,
                'image_mode': image.mode
            }
            
            return results
            
        except Exception as e:
            print(f"Pipeline error: {str(e)}")
            return {
                'error': str(e),
                'caption': 'Error analyzing image',
                'summary': 'Could not generate summary due to an error.',
                'objects': '- Error',
                'mood': 'Error',
                'story': 'Error'
            }

    
    def process_base64_image(self, base64_string):
        """
        Process base64 encoded image.
        
        Args:
            base64_string: Base64 encoded image data
            
        Returns:
            dict: Analysis results
        """
        image = self.processor.base64_to_image(base64_string)
        
        # Convert to bytes for processing
        import io
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        
        return self.process_image(buffer)
