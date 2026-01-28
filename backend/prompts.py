def get_analysis_prompt():
    """Generate a consolidated prompt for all five analysis tasks in one request."""
    return """Analyze this image in detail and provide the following five outputs in a JSON format:

1. "caption": A single factual sentence describing the main subject and action.
2. "summary": A 3-5 line descriptive summary including visual details (colors, lighting, atmosphere).
3. "objects": A bulleted list of all visible objects, people, and entities.
4. "mood": A 2-3 sentence analysis of the emotional tone and atmosphere.
5. "story": A creative 5-10 line short story inspired by the image.

Requirements for JSON format:
- Use precisely these keys: "caption", "summary", "objects", "mood", "story"
- Ensure the JSON is valid and well-formatted.
- Provide only the JSON object, nothing else."""

