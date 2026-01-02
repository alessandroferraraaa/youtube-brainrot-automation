import os
import json
import requests
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips

def download_pexels_video():
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        raise ValueError("PEXELS_API_KEY not found")
    
    print("Searching for video...")
    headers = {'Authorization': api_key}
    params = {'query': 'minecraft parkour', 'orientation': 'portrait', 'per_page': 10}
    
    response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)
    data = response.json()
    
    if not data.get('videos'):
        raise Exception("No videos found")
    
    video_file = data['videos'][0]['video_files'][0]
    
    print("Downloading video...")
    video_data = requests.get(video_file['link']).content
    with open('background.mp4', 'wb') as f:
        f.write(video_data)
    
    print("Video downloaded")
    return 'background.mp4'

async def generate_voiceover_async(text):
    print("Generating voiceover...")
    communicate = edge_tts.Communicate(text, "en-US-GuyNeural", rate="+5%")
    await communicate.save("voiceover.mp3")
    print("Voiceover done")
    return 'voiceover.mp3'

def generate_voiceover(text):
    return asyncio.run(generate_voiceover_async(text))

def create_video():
    print("Starting video creation")
    
    with open('script.json', 'r') as f:
        script_data = json.load(f)
    
    voiceover_file = generate_voiceover(script_data['story'])
    background_file = download_pexels_video()
    
    print("Loading clips")
    background = VideoFileClip(background_file)
    audio = AudioFileClip(voiceover_file)
    
    duration = audio.duration
    print(f"Duration: {duration:.1f}s")
    
    # Loop video if needed (MoviePy 2.0 way)
    if background.duration < duration:
        loops = int(duration / background.duration) + 1
        clips = [background] * loops
        background = concatenate_videoclips(clips)
    
    # Trim to audio duration
    background = background.subclipped(0, duration)
    
    # Resize to 1080x1920
    background = background.resized(height=1920)
    
    # Crop to 1080 width
    w = background.w
    x1 = int(w/2 - 540)
    x2 = int(w/2 + 540)
    background = background.cropped(x1=x1, x2=x2, y1=0, y2=1920)
    
    # Add audio
    final = background.with_audio(audio)
    
    print("Exporting video")
    final.write_videofile(
        'final_video.mp4',
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='medium',
        threads=4
    )
    
    print("Video created successfully")
    background.close()
    audio.close()
    
    return 'final_video.mp4'

if __name__ == "__main__":
    create_video()
