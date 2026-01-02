import os
import json
import requests
from elevenlabs import generate, set_api_key
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import time

def download_pexels_video():
    """Download a Minecraft/gameplay video from Pexels"""
    
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        raise ValueError("PEXELS_API_KEY not found")
    
    # Search for Minecraft gameplay
    headers = {'Authorization': api_key}
    params = {
        'query': 'minecraft gameplay',
        'orientation': 'portrait',
        'size': 'medium',
        'per_page': 10
    }
    
    print("🎮 Searching for background video on Pexels...")
    response = requests.get(
        'https://api.pexels.com/videos/search',
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        raise Exception(f"Pexels API error: {response.status_code}")
    
    data = response.json()
    
    if not data.get('videos'):
        # Fallback to parkour if no Minecraft found
        params['query'] = 'parkour gameplay'
        response = requests.get(
            'https://api.pexels.com/videos/search',
            headers=headers,
            params=params
        )
        data = response.json()
    
    # Get first video
    video = data['videos'][0]
    
    # Find HD video file
    video_file = None
    for file in video['video_files']:
        if file['quality'] == 'hd' or file['quality'] == 'sd':
            video_file = file
            break
    
    if not video_file:
        video_file = video['video_files'][0]
    
    # Download video
    print(f"⬇️  Downloading video: {video_file['link']}")
    video_response = requests.get(video_file['link'])
    
    with open('background.mp4', 'wb') as f:
        f.write(video_response.content)
    
    print("✅ Background video downloaded!")
    return 'background.mp4'

def generate_voiceover(text):
    """Generate voiceover using ElevenLabs"""
    
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found")
    
    set_api_key(api_key)
    
    print("🎙️  Generating voiceover with ElevenLabs...")
    
    # Generate audio
    audio = generate(
        text=text,
        voice="Adam",  # Default voice
        model="eleven_monolingual_v1"
    )
    
    # Save audio
    with open('voiceover.mp3', 'wb') as f:
        f.write(audio)
    
    print("✅ Voiceover generated!")
    return 'voiceover.mp3'

def create_video():
    """Create the final video with background, voiceover, and text"""
    
    print("🎬 Starting video creation...")
    
    # Load script
    with open('script.json', 'r', encoding='utf-8') as f:
        script_data = json.load(f)
    
    story_text = script_data['story']
    title = script_data['title']
    
    # Generate voiceover
    voiceover_file = generate_voiceover(story_text)
    
    # Download background video
    background_file = download_pexels_video()
    
    # Load clips
    print("🎞️  Loading video and audio clips...")
    background = VideoFileClip(background_file)
    audio = AudioFileClip(voiceover_file)
    
    # Get audio duration
    duration = audio.duration
    
    # Trim or loop background to match audio duration
    if background.duration < duration:
        # Loop video
        n_loops = int(duration / background.duration) + 1
        background = background.loop(n=n_loops)
    
    background = background.subclip(0, duration)
    
    # Resize to 1080x1920 (9:16 portrait for Shorts)
    background = background.resize(height=1920)
    
    # Center crop to 1080 width
    w, h = background.size
    x_center = w / 2
    x1 = x_center - 540
    x2 = x_center + 540
    background = background.crop(x1=x1, x2=x2, y1=0, y2=1920)
    
    # Add audio
    final_video = background.set_audio(audio)
    
    # Export
    print("💾 Exporting final video...")
    final_video.write_videofile(
        'final_video.mp4',
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='medium',
        threads=4
    )
    
    print("✅ Video created successfully: final_video.mp4")
    
    # Cleanup
    background.close()
    audio.close()
    
    return 'final_video.mp4'

if __name__ == "__main__":
    create_video()
