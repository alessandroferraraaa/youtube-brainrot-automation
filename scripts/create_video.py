import os
import requests
from elevenlabs import generate, save
from moviepy.editor import VideoFileClip, AudioFileClip

def create_voiceover(script_file='video_script.txt'):
    """Genera voiceover con ElevenLabs"""
    
    with open(script_file, 'r', encoding='utf-8') as f:
        script = f.read()
    
    # ElevenLabs API
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    
    audio = generate(
        text=script,
        voice="Adam",
        api_key=api_key
    )
    
    save(audio, 'voiceover.mp3')
    print("✅ Voiceover creato")
    return 'voiceover.mp3'

def download_background():
    """Scarica video background da Pexels"""
    
    api_key = os.environ.get('PEXELS_API_KEY')
    
    # Cerca "minecraft parkour"
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": api_key}
    params = {"query": "minecraft parkour", "per_page": 1}
    
    response = requests.get(url, headers=headers, params=params)
    video_url = response.json()['videos'][0]['video_files'][0]['link']
    
    # Download video
    video_data = requests.get(video_url).content
    with open('background.mp4', 'wb') as f:
        f.write(video_data)
    
    print("✅ Background scaricato")
    return 'background.mp4'

def assemble_video():
    """Assembla video finale"""
    
    # Carica componenti
    audio = AudioFileClip('voiceover.mp3')
    background = VideoFileClip('background.mp4').subclip(0, audio.duration)
    
    # Combina
    final = background.set_audio(audio)
    
    # Export
    final.write_videofile(
        'final_video.mp4',
        fps=30,
        codec='libx264',
        audio_codec='aac'
    )
    
    print("✅ Video creato: final_video.mp4")
    return 'final_video.mp4'

if __name__ == "__main__":
    create_voiceover()
    download_background()
    assemble_video()