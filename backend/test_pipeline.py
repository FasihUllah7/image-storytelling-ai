"""
Test script for the multimodal image analysis pipeline.
Usage: python test_pipeline.py <image_path>
"""
import sys
import os
from pipeline import AnalysisPipeline

def print_separator(char='-', length=70):
    """Print a separator line."""
    print(char * length)

def test_image(image_path):
    """
    Test the pipeline with a sample image.
    
    Args:
        image_path: Path to the image file
    """
    # Validate file exists
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found: {image_path}")
        sys.exit(1)
    
    print(f"\n🖼️  Testing Multimodal AI Pipeline")
    print_separator('=')
    print(f"Image: {image_path}")
    print(f"Size: {os.path.getsize(image_path) / 1024:.2f} KB")
    print_separator('=')
    
    # Initialize pipeline
    print("\n⚙️  Initializing pipeline...")
    try:
        pipeline = AnalysisPipeline()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file")
        print("2. Added your GEMINI_API_KEY")
        sys.exit(1)
    
    # Process image
    print("🔄 Processing image through 5-stage pipeline...\n")
    
    try:
        with open(image_path, 'rb') as f:
            results = pipeline.process_image(f)
        
        # Check for errors
        if 'error' in results:
            print(f"❌ Pipeline error: {results['error']}\n")
            print("Partial results:")
            for key, value in results.items():
                if key != 'error' and value:
                    print(f"  {key}: {value[:100]}...")
            sys.exit(1)
        
        # Display results
        print_separator()
        print("✅ ANALYSIS COMPLETE")
        print_separator()
        
        print("\n📝 1. FACTUAL CAPTION")
        print_separator('-', 50)
        print(results['caption'])
        
        print("\n\n📄 2. DESCRIPTIVE SUMMARY")
        print_separator('-', 50)
        print(results['summary'])
        
        print("\n\n🔍 3. DETECTED OBJECTS")
        print_separator('-', 50)
        print(results['objects'])
        
        print("\n\n😊 4. MOOD & EMOTION")
        print_separator('-', 50)
        print(results['mood'])
        
        print("\n\n📖 5. CREATIVE STORY")
        print_separator('-', 50)
        print(results['story'])
        
        print("\n")
        print_separator('=')
        print("✨ All outputs generated successfully!")
        print_separator('=')
        
        # Metadata
        if 'metadata' in results:
            print(f"\nImage metadata:")
            print(f"  Size: {results['metadata']['image_size']}")
            print(f"  Mode: {results['metadata']['image_mode']}")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python test_pipeline.py <image_path>")
        print("\nExample:")
        print("  python test_pipeline.py sample.jpg")
        print("  python test_pipeline.py C:\\Users\\Photos\\vacation.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_image(image_path)

if __name__ == '__main__':
    main()
