import os
import json
from openai import OpenAI

def generate_brainrot_script():
    """Generate a Reddit-style brainrot story using ChatGPT"""
    
    # Initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = OpenAI(api_key=api_key)
    
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
        print("🤖 Generating script with GPT-3.5-turbo...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a creative storyteller. Always respond with valid JSON only, no markdown formatting."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.9,
            max_tokens=600
        )
        
        # Get response content
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        # Parse JSON
        script_data = json.loads(content)
        
        # Validate required fields
        required_fields = ["title", "story", "tags"]
        for field in required_fields:
            if field not in script_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Save to file
        with open('script.json', 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Script generated successfully!")
        print(f"📝 Title: {script_data['title']}")
        print(f"📊 Story length: {len(script_data['story'])} characters")
        
        return script_data
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response content: {content[:200]}...")
        raise
    except Exception as e:
        print(f"❌ Error generating script: {e}")
        raise

if __name__ == "__main__":
    generate_brainrot_script()
