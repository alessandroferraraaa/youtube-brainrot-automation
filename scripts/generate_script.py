import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_brainrot_script():
    """Genera script per video brainrot virale"""
    
    prompt = """
    Generate a viral 45-second Reddit story for Gen Alpha audience.
    Include:
    - Shocking hook in first 3 seconds
    - Dramatic plot twist
    - Gen Alpha slang (skibidi, rizz, sigma, etc.)
    - Fast pacing with emotional peaks
    
    Format: Just the narration script, no descriptions.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    
    script = response.choices[0].message.content
    
    # Salva script
    with open('video_script.txt', 'w', encoding='utf-8') as f:
        f.write(script)
    
    print(f"✅ Script generato: {len(script)} caratteri")
    return script

if __name__ == "__main__":
    generate_brainrot_script()