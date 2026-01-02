import os
import json
import requests
import asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from moviepy.video.fx.all import crop

def download_pexels_video():
    """Download a Minecraft/gameplay video from Pexels"""
    
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        raise ValueError("PEXELS_API_KEY not found")
    
    # Search for background video
    headers = {'Authorization': api_key}
    params = {
        'query': 'minecraft parkour',
        'orientation': 'portrait',
        'size': 'medium',
        'per_page': 15
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
        # Fallback to gameplay
        params['query'] = 'gaming gameplay'
        response = requests.get(
            'https://api.pexels.com/videos/search',
            headers=headers,
            params=params
        )
        data = response.json()
    
    if not data.get('videos'):
        raise Exception("No videos found on Pexels")
    
    # Get first video
    video = data['videos'][0]
    
    # Find best quality video file
    video_file = None
    for file in video['video_files']:
        if file['quality'] in ['hd', 'sd']:
            video_file = file
            break
    
    if not video_file:
        video_file = video['video_files'][0]
    
    # Download video
    print(f"⬇️  Downloading: {video_file['link']}")
    video_response = requests.get(video_file['link'], stream=True)
    
    with open('background.mp4', 'wb') as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print("✅ Background video downloaded!")
    return 'background.mp4'

async def generate_voiceover_async(text):
    """Generate voiceover using Edge TTS (FREE & UNLIMITED)"""
    
    print("🎙️  Generating voiceover with Edge TTS (FREE)...")
    
    # Best male voices for storytelling
    voices = [
        "en-US-GuyNeural",        # Deep, engaging
        "en-US-ChristopherNeural", # Smooth narrator
        "en-GB-RyanNeural",        # British, clear
        "en-US-EricNeural"         # Calm, friendly
    ]
    
    voice = voices[0]  # Default: Guy (best for drama)
    
    # Generate audio with natural prosody
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate="+5%",    # Slightly faster for engagement
        pitch="+0Hz"    # Natural pitch
    )
    
    await communicate.save("voiceover.mp3")
    
    print(f"✅ Voiceover generated! (Voice: {voice})")
    return 'voiceover.mp3'

def generate_voiceover(text):
    """Wrapper to run async Edge TTS"""
    return asyncio.run(generate_voiceover_async(text))

def create_video():
    """Create the final video with background, voiceover"""
    
    print("🎬 Starting video creation...")
    
    # Load script
    with open('script.json', 'r', encoding='utf-8') as f:
        script_data = json.load(f)
    
    story_text = script_data['story']
    title = script_data['title']
    
    # Generate voiceover (FREE with Edge TTS!)
    voiceover_file = generate_voiceover(story_text)
    
    # Download background video
    background_file = download_pexels_video()
    
    # Load clips
    print("🎞️  Loading video and audio clips...")
    background = VideoFileClip(background_file)
    audio = AudioFileClip(voiceover_file)
    
    # Get audio duration
    duration = audio.duration
    print(f"⏱️  Video duration: {duration:.1f} seconds")
    
    # Trim or loop background to match audio duration
    if background.duration < duration:
        # Loop video if too short
        n_loops = int(duration / background.duration) + 1
        background = background.loop(n=n_loops)
    
    background = background.subclip(0, duration)
    
    # Resize to 1080x1920 (9:16 portrait for YouTube Shorts)
    print("📐 Resizing to 1080x1920 (Shorts format)...")
    background = background.resize(height=1920)
    
    # Center crop to 1080 width
    w, h = background.size
    x_center = w / 2
    x1 = x_center - 540
    x2 = x_center + 540
    background = background.crop(x1=int(x1), x2=int(x2), y1=0, y2=1920)
    
    # Add audio to video
    final_video = background.set_audio(audio)
    
    # Export final video
    print("💾 Exporting final video...")
    final_video.write_videofile(
        'final_video.mp4',
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='medium',
        threads=4,
        bitrate='8000k'
    )
    
    print("✅ Video created successfully: final_video.mp4")
    print(f"📊 Duration: {duration:.1f}s | Resolution: 1080x1920")
    
    # Cleanup
    background.close()
    audio.close()
    
    return 'final_video.mp4'

if __name__ == "__main__":
    create_video()
