import os
import json
import requests

def generate_brainrot_script():
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY not found")
    
    prompt = """Create a short, engaging story (60-90 seconds when read aloud) in the style of Reddit brainrot content. 
    The story should be dramatic, surprising, and attention-grabbing with a twist ending.
    
    Return ONLY a valid JSON object with these exact fields:
    {"title": "A catchy title", "story": "The full story (200-300 words)", "tags": ["tag1", "tag2", "tag3"]}"""
    
    try:
        print("Generating script with Perplexity API...")
        
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "You are a creative storyteller. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 600
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        result = response.json()
        content = result['choices'][0]['message']['content'].strip()
        
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        script_data = json.loads(content)
        
        required_fields = ["title", "story", "tags"]
        for field in required_fields:
            if field not in script_data:
                raise ValueError(f"Missing field: {field}")
        
        with open('script.json', 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2, ensure_ascii=False)
        
        print(f"Script generated!")
        print(f"Title: {script_data['title']}")
        print(f"Length: {len(script_data['story'])} characters")
        
        return script_data
        
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        print(f"Content: {content[:200]}...")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    generate_brainrot_script()
