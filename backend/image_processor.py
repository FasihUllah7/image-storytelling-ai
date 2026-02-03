"""
Image preprocessing utilities.
"""
import io
import base64
from PIL import Image
from config import Config

class ImageProcessor:
    """Handle image validation, preprocessing, and conversion."""
    
    @staticmethod
    def validate_image(file_data):
        """
        Validate image file.
        
        Args:
            file_data: File-like object or bytes
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Check file size
            if hasattr(file_data, 'seek'):
                file_data.seek(0, 2)  # Seek to end
                size = file_data.tell()
                file_data.seek(0)  # Reset
            else:
                size = len(file_data)
            
            if size > Config.MAX_IMAGE_SIZE_BYTES:
                return False, f"Image too large. Max size: {Config.MAX_IMAGE_SIZE_MB}MB"
            
            if size == 0:
                return False, "Empty file"
            
            # Try to open with PIL
            try:
                img = Image.open(file_data)
                img.verify()
                
                # CRITICAL FIX: verify() consumes the image and leaves file pointer in invalid state
                # We must reset the file pointer after verification
                if hasattr(file_data, 'seek'):
                    file_data.seek(0)
                
                return True, None
            except Exception as e:
                return False, f"Invalid image format: {str(e)}"
                
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def preprocess_image(file_data):
        """
        Preprocess image: resize if needed, convert to RGB.
        
        Args:
            file_data: File-like object or bytes
            
        Returns:
            PIL.Image: Processed image
        """
        # Reset file pointer if needed
        if hasattr(file_data, 'seek'):
            file_data.seek(0)
        
        # Open image
        img = Image.open(file_data)
        
        # Convert to RGB (handle RGBA, grayscale, etc.)
        if img.mode != 'RGB':
            # Handle transparency
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                img = background
            else:
                img = img.convert('RGB')
        
        # Resize if too large
        max_dim = Config.RESIZE_MAX_DIMENSION
        if max(img.size) > max_dim:
            ratio = max_dim / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        return img
    
    @staticmethod
    def image_to_bytes(img, format='JPEG'):
        """
        Convert PIL Image to bytes.
        
        Args:
            img: PIL.Image
            format: Output format (JPEG, PNG, etc.)
            
        Returns:
            bytes: Image data
        """
        buffer = io.BytesIO()
        img.save(buffer, format=format, quality=95)
        return buffer.getvalue()
    
    @staticmethod
    def base64_to_image(base64_string):
        """
        Convert base64 string to PIL Image.
        
        Args:
            base64_string: Base64 encoded image (with or without data URI prefix)
            
        Returns:
            PIL.Image: Decoded image
        """
        # Remove data URI prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode
        image_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_data))
    
    @staticmethod
    def image_to_base64(img, format='JPEG'):
        """
        Convert PIL Image to base64 string.
        
        Args:
            img: PIL.Image
            format: Output format
            
        Returns:
            str: Base64 encoded image
        """
        buffer = io.BytesIO()
        img.save(buffer, format=format, quality=95)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
