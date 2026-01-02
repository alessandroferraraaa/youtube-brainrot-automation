import os
import json
import requests
import random

# Personaggi brainrot disponibili
CHARACTERS = {
    "Skibidi Toilet": {
        "description": "A creepy singing head in a toilet",
        "personality": "Mischievous and chaotic",
        "voice": "en-US-GuyNeural"
    },
    "Cappuccina": {
        "description": "A dancing coffee cup with big eyes",
        "personality": "Energetic and dramatic",
        "voice": "en-US-JennyNeural"
    },
    "Tung Tung Sahur": {
        "description": "A monkey inside a banana",
        "personality": "Silly and innocent",
        "voice": "en-US-ChristopherNeural"
    },
    "Mr Pen Pineapple": {
        "description": "A tall pineapple-pen hybrid character",
        "personality": "Mysterious and powerful",
        "voice": "en-GB-RyanNeural"
    }
}

def generate_brainrot_short():
    """Generate a dramatic brainrot short story script"""
    
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY not found")
    
    # Random 2-3 characters
    num_chars = random.choice([2, 3])
    selected = random.sample(list(CHARACTERS.keys()), num_chars)
    
    char_descriptions = "\n".join([
        f"- {name}: {CHARACTERS[name]['description']}, {CHARACTERS[name]['personality']}"
        for name in selected
    ])
    
    prompt = f"""Create a SHORT dramatic/dark/funny brainrot story (30-45 seconds when read aloud) featuring these characters:

{char_descriptions}

The story should:
- Be a conflict, betrayal, fight, or dramatic moment between them
- Include brainrot humor and internet culture references
- Have a surprising twist or chaotic ending
- Be suitable for YouTube Shorts (vertical video, fast-paced)

Return ONLY valid JSON with this EXACT structure:
{{
  "title": "Catchy clickbait title (max 60 chars)",
  "characters": {selected},
  "scenes": [
    {{
      "character": "character_name",
      "action": "what they're doing visually",
      "dialogue": "what they say",
      "duration": 3
    }}
  ],
  "total_duration": 40,
  "tags": ["brainrot", "shorts", "tag3"]
}}

Each scene should be 3-8 seconds. Total duration 30-50 seconds."""

    try:
        print("🎬 Generating brainrot short script...")
        
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a brainrot content creator. Generate chaotic, dramatic, internet-culture stories with JSON format only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 1.0,
            "max_tokens": 800
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")
        
        result = response.json()
        content = result['choices'][0]['message']['content'].strip()
        
        # Clean markdown
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        script_data = json.loads(content)
        
        # Add voice mapping
        for scene in script_data['scenes']:
            char = scene['character']
            if char in CHARACTERS:
                scene['voice'] = CHARACTERS[char]['voice']
        
        # Save
        with open('brainrot_short.json', 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Script generated!")
        print(f"📝 Title: {script_data['title']}")
        print(f"🎭 Characters: {', '.join(script_data['characters'])}")
        print(f"⏱️ Duration: {script_data['total_duration']}s")
        
        return script_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    generate_brainrot_short()
