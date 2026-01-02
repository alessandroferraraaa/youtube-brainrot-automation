import os
import json
import requests

def generate_brainrot_script():
    """Generate a Reddit-style brainrot story using Perplexity API"""
    
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
    
    prompt = """Create a short, engaging story (60-90 seconds when read aloud) in the style of Reddit brainrot content. 
    The story should be dramatic, surprising, and attention-grabbing with a twist ending.
    Include elements like: unexpected plot twists, relatable scenarios, dramatic revelations.
    
    Keep it suitable for all audiences (no explicit content).
    
    Return ONLY a valid JSON object (no markdown, no extra text) with these exact fields:
    {
      "title": "A catchy, attention-grabbing title",
      "story": "The full story text (200-300 words, takes 60-90 seconds to read aloud)",
      "tags": ["tag1", "tag2", "tag3"]
    }
    """
    
    try:
        print("🤖 Generating script with Perplexity Sonar API...")
        
        url = "https://api.perplexity.ai/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data
