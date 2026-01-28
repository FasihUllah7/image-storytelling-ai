# Multimodal Image Understanding & Storytelling AI

An end-to-end AI system that analyzes images and generates five semantically consistent outputs:
1. **Factual Caption** - One-sentence description
2. **Descriptive Summary** - 3-5 line detailed summary
3. **Object Detection** - List of detected entities
4. **Mood Analysis** - Emotional tone and atmosphere
5. **Creative Story** - 5-10 line narrative inspired by the image

## 🎯 Features

- **Real-time Image Analysis** - Upload images or capture from camera
- **Multimodal AI** - Powered by Google Gemini 2.0 Flash
- **Semantic Consistency** - All outputs are contextually related
- **Modern Web UI** - Beautiful, responsive interface with dark mode
- **Live Demo Ready** - Minimal setup, robust error handling

## 🏗️ Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (Frontend UI)  │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  Flask Server   │
│   (Backend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ Image Processor │──────│  Gemini Vision   │
│   (Pipeline)    │      │      API         │
└─────────────────┘      └──────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Sequential Analysis Pipeline:      │
│  1. Caption → 2. Summary →          │
│  3. Objects → 4. Mood → 5. Story    │
└─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google AI Studio API key ([Get one free](https://makersuite.google.com/app/apikey))
- Modern web browser with camera support (optional)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "e:\Crowd Pleaser"
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure API key**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Start the backend server**
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:5000`

5. **Open the frontend**
   
   Open `frontend/index.html` in your web browser, or use a simple HTTP server:
   ```bash
   cd ../frontend
   python -m http.server 8000
   ```
   
   Then visit `http://localhost:8000`

## 📖 Usage

### Web Interface

1. **Upload an Image**
   - Drag & drop an image onto the dropzone
   - Or click "Browse Files" to select from your computer
   - Supports: JPG, PNG, WebP, GIF (max 10MB)

2. **Camera Capture** (Optional)
   - Switch to "Camera Capture" tab
   - Click "Start Camera" and allow camera access
   - Click "Capture Photo" to take a picture

3. **Analyze**
   - Click "Analyze Image" button
   - Wait 10-20 seconds for AI processing
   - View all five outputs in organized cards

4. **New Analysis**
   - Click "Analyze Another Image" to start over

### API Usage

**Endpoint:** `POST /api/analyze`

**Request (multipart/form-data):**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@path/to/image.jpg"
```

**Request (JSON with base64):**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image_data"}'
```

**Response:**
```json
{
  "success": true,
  "results": {
    "caption": "A golden retriever playing in a sunny park.",
    "summary": "The image shows a happy golden retriever...",
    "objects": "- Golden retriever dog\n- Green grass\n- Trees...",
    "mood": "The scene conveys joy and playfulness...",
    "story": "Max had been waiting all morning for this moment...",
    "metadata": {
      "image_size": [1920, 1080],
      "image_mode": "RGB"
    }
  }
}
```

## 🧪 Testing

### Manual Testing

Test with various image types:
- **Portraits** - People, faces, expressions
- **Landscapes** - Nature scenes, cityscapes
- **Objects** - Products, still life
- **Action** - Sports, movement
- **Abstract** - Art, patterns

### Sample Test Script

```python
# test_pipeline.py
import sys
from pipeline import AnalysisPipeline

def test_image(image_path):
    """Test the pipeline with a sample image."""
    print(f"\nTesting with: {image_path}")
    print("-" * 60)
    
    pipeline = AnalysisPipeline()
    
    with open(image_path, 'rb') as f:
        results = pipeline.process_image(f)
    
    print(f"\n📝 CAPTION:\n{results['caption']}\n")
    print(f"📄 SUMMARY:\n{results['summary']}\n")
    print(f"🔍 OBJECTS:\n{results['objects']}\n")
    print(f"😊 MOOD:\n{results['mood']}\n")
    print(f"📖 STORY:\n{results['story']}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_pipeline.py <image_path>")
        sys.exit(1)
    
    test_image(sys.argv[1])
```

Run with:
```bash
cd backend
python test_pipeline.py path/to/test/image.jpg
```

## 🔧 Configuration

Edit `backend/config.py` to customize:

```python
# Model Selection
MODEL_NAME = 'gemini-2.0-flash-exp'  # Fast and cost-effective

# Image Constraints
MAX_IMAGE_SIZE_MB = 10
RESIZE_MAX_DIMENSION = 2048

# Generation Parameters
GENERATION_CONFIG = {
    'temperature': 0.7,      # Creativity (0.0-1.0)
    'top_p': 0.95,
    'top_k': 40,
    'max_output_tokens': 2048
}
```

## 🎨 Model Choices

### Current: Google Gemini 2.0 Flash
- ✅ Native multimodal (vision + language)
- ✅ Fast inference (~10-15 seconds)
- ✅ Cost-effective
- ✅ High-quality outputs
- ✅ Free tier available

### Alternatives

**OpenAI GPT-4 Vision**
```python
# Requires: pip install openai
# Change in gemini_client.py to use OpenAI API
```

**Anthropic Claude 3.5 Sonnet**
```python
# Requires: pip install anthropic
# Excellent reasoning, similar pricing to Gemini
```

**Open-Source (LLaVA, BLIP-2)**
```python
# Requires: Local GPU, transformers library
# Free but needs powerful hardware
```

## 📁 Project Structure

```
Crowd Pleaser/
├── backend/
│   ├── app.py              # Flask REST API server
│   ├── pipeline.py         # Main processing pipeline
│   ├── gemini_client.py    # Gemini API integration
│   ├── image_processor.py  # Image preprocessing
│   ├── prompts.py          # Structured prompts
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   └── .env               # Your API key (create this)
│
├── frontend/
│   ├── index.html         # Main HTML structure
│   ├── styles.css         # Premium dark mode design
│   └── app.js             # Frontend application logic
│
└── README.md              # This file
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- Create `.env` file in `backend/` directory
- Add your API key: `GEMINI_API_KEY=your_key_here`

### "Backend not available"
- Make sure Flask server is running: `python backend/app.py`
- Check console for error messages
- Verify port 5000 is not in use

### "Failed to access camera"
- Grant camera permissions in browser
- Use HTTPS or localhost (required for camera access)
- Check if camera is already in use

### "Image too large"
- Maximum size: 10MB
- Try compressing the image
- Or increase `MAX_IMAGE_SIZE_MB` in `config.py`

### Slow processing
- Normal: 10-20 seconds for all 5 outputs
- Check internet connection (API calls)
- Consider using faster model tier

## 🔒 Security Notes

- Never commit `.env` file with API keys
- Use environment variables in production
- Implement rate limiting for public deployments
- Validate and sanitize all user inputs

## 📊 Performance

- **Average Processing Time:** 10-20 seconds
- **Concurrent Requests:** Supported (API rate limits apply)
- **Image Size Limit:** 10MB (configurable)
- **Supported Formats:** JPG, PNG, WebP, GIF

## 🎯 Verification Checklist

- [x] Accepts uploaded images
- [x] Supports camera capture
- [x] Generates factual caption (1 sentence)
- [x] Generates descriptive summary (3-5 lines)
- [x] Detects objects/entities
- [x] Analyzes mood/emotion
- [x] Creates creative story (5-10 lines)
- [x] Outputs are semantically consistent
- [x] No hardcoded outputs
- [x] Runs live during evaluation
- [x] Error handling and validation
- [x] Responsive UI design

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation: [Google AI Studio](https://ai.google.dev/)
3. Open an issue on the repository

---

**Built with ❤️ using Google Gemini 2.0 Flash, Flask, and Modern Web Technologies**
