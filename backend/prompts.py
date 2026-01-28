"""
Structured prompts for each analysis task.
"""

def get_caption_prompt():
    """Generate prompt for one-sentence factual caption."""
    return """Analyze this image and provide a single factual sentence that describes what you see.
Be concise and objective. Focus on the main subject and action.
Format: Return ONLY the caption sentence, nothing else."""

def get_summary_prompt(caption):
    """Generate prompt for 3-5 line descriptive summary."""
    return f"""Based on this image (Caption: "{caption}"), provide a detailed descriptive summary.

Requirements:
- Write 3-5 lines
- Include visual details (colors, composition, lighting, atmosphere)
- Describe spatial relationships and context
- Be descriptive but factual

Format: Return ONLY the summary text, nothing else."""

def get_objects_prompt():
    """Generate prompt for object/entity detection."""
    return """Identify and list all visible objects, people, animals, and entities in this image.

Requirements:
- List each item on a new line with a bullet point (-)
- Include both prominent and background elements
- Be specific (e.g., "red sports car" not just "car")
- Order by prominence (most prominent first)

Format: Return ONLY the bulleted list, nothing else."""

def get_mood_prompt(caption, summary):
    """Generate prompt for mood/emotion analysis."""
    return f"""Analyze the emotional tone and mood of this image.

Context:
- Caption: "{caption}"
- Summary: "{summary}"

Requirements:
- Identify the overall mood/atmosphere (e.g., peaceful, energetic, melancholic, joyful)
- Explain what visual elements contribute to this mood
- Consider lighting, colors, composition, and subject expressions
- Write 2-3 sentences

Format: Return ONLY the mood analysis, nothing else."""

def get_story_prompt(caption, summary, objects, mood):
    """Generate prompt for creative story generation."""
    return f"""Write a creative short story inspired by this image.

Context:
- Caption: "{caption}"
- Summary: "{summary}"
- Objects present: {objects}
- Mood: "{mood}"

Requirements:
- Write 5-10 lines
- Create a narrative that fits the scene
- Include sensory details and emotions
- Stay grounded in what's visible in the image
- Make it engaging and imaginative

Format: Return ONLY the story text, nothing else."""
