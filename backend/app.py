"""
Flask REST API server for multimodal image analysis.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import AnalysisPipeline
from config import Config
import traceback

app = Flask(__name__)

# Simplified CORS for Vercel deployment
CORS(app) 

# Initialize pipeline
pipeline = None

def get_pipeline():
    """Lazy initialization of pipeline."""
    global pipeline
    if pipeline is None:
        pipeline = AnalysisPipeline()
    return pipeline

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model': Config.MODEL_NAME,
        'version': '1.0.0'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """
    Main endpoint for image analysis.
    
    Accepts:
        - multipart/form-data with 'image' file
        - application/json with 'image' as base64 string
        
    Returns:
        JSON with all five analysis outputs
    """
    try:
        # Check if API key is configured
        if not Config.OPENAI_API_KEY:
            return jsonify({
                'error': 'API key not configured. Please set OPENAI_API_KEY in .env file'
            }), 500
        
        # Get pipeline instance
        pipe = get_pipeline()
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Process image
            results = pipe.process_image(file)
            
        # Handle base64 data
        elif request.is_json and 'image' in request.json:
            base64_data = request.json['image']
            results = pipe.process_base64_image(base64_data)
            
        else:
            return jsonify({
                'error': 'No image provided. Send as multipart file or base64 JSON'
            }), 400
        
        # Check for errors in results
        if 'error' in results:
            return jsonify({
                'error': results['error'],
                'partial_results': {k: v for k, v in results.items() if k != 'error'}
            }), 500
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print(f"Starting server on port {Config.PORT}...")
    print(f"Using model: {Config.MODEL_NAME}")
    
    if not Config.OPENAI_API_KEY:
        print("\n⚠️  WARNING: OPENAI_API_KEY not set!")
        print("Please create a .env file with your API key.")
        print("Get your API key from: https://platform.openai.com/api-keys")
        print("See .env.example for template.\n")
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
