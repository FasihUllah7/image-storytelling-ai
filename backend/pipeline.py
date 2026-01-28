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
        Process image through complete pipeline.
        
        Args:
            image_data: File-like object, bytes, or PIL.Image
            
        Returns:
            dict: Analysis results with all five outputs
        """
        # Validate and preprocess
        is_valid, error = self.processor.validate_image(image_data)
        if not is_valid:
            raise ValueError(error)
        
        image = self.processor.preprocess_image(image_data)
        
        # Initialize results
        results = {
            'caption': '',
            'summary': '',
            'objects': '',
            'mood': '',
            'story': '',
            'metadata': {
                'image_size': image.size,
                'image_mode': image.mode
            }
        }
        
        try:
            # Stage 1: Generate caption
            print("Generating caption...")
            caption_prompt = prompts.get_caption_prompt()
            results['caption'] = self.client.analyze_with_retry(image, caption_prompt)
            
            # Stage 2: Generate summary
            print("Generating summary...")
            summary_prompt = prompts.get_summary_prompt(results['caption'])
            results['summary'] = self.client.analyze_with_retry(image, summary_prompt)
            
            # Stage 3: Detect objects
            print("Detecting objects...")
            objects_prompt = prompts.get_objects_prompt()
            results['objects'] = self.client.analyze_with_retry(image, objects_prompt)
            
            # Stage 4: Analyze mood
            print("Analyzing mood...")
            mood_prompt = prompts.get_mood_prompt(results['caption'], results['summary'])
            results['mood'] = self.client.analyze_with_retry(image, mood_prompt)
            
            # Stage 5: Generate story
            print("Generating story...")
            story_prompt = prompts.get_story_prompt(
                results['caption'],
                results['summary'],
                results['objects'],
                results['mood']
            )
            results['story'] = self.client.analyze_with_retry(image, story_prompt)
            
            return results
            
        except Exception as e:
            # Include partial results if available
            results['error'] = str(e)
            return results
    
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
