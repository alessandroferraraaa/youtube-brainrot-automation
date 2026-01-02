import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_brainrot_script():
    """Generate a Reddit-style brainrot story using ChatGPT"""
    
    prompt = """Create a short, engaging story (60-90 seconds when read aloud) in the style of Reddit brainrot content. 
    The story should be dramatic, surprising, and attention-grabbing. 
    Include elements like: unexpected plot twists, relatable scenarios, internet culture references.
    
    Format the output as a JSON object with these fields:
    - title: A catchy title
    - story: The full story text (should take 60-90 seconds to read)
    - tags: Array of relevant tags
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative storyteller specialized in engaging Reddit-style content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        # Parse response
        content = response.choices[0].message.content
        script_data = json.loads(content)
        
        # Save to file
        with open('script.json', 'w') as f:
            json.dump(script_data, f, indent=2)
        
        print("✅ Script generated successfully!")
        return script_data
        
    except Exception as e:
        print(f"❌ Error generating script: {e}")
        raise

if __name__ == "__main__":
    generate_brainrot_script()
