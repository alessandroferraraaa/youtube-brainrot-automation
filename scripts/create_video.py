import os
import json
import requests
import asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip

def download_pexels_video():
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        raise ValueError("PEXELS_API_KEY not found")
    
    headers = {'Authorization': api_key}
    params = {
        'query': 'minecraft parkour gameplay',
        'orientation': 'portrait',
        'size': 'medium',
        'per_page': 15
    }
    
    print("Searching for background video...")
    response = requests.get(
        'https://api.pexels.com/videos/search',
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        raise Exception(f"Pexels API error: {response.status_code}")
    
    data = response.json()
    
    if not data.get('videos'):
        params['query'] = 'gaming'
        response = requests.get(
            'https://api.pexels.com/videos/search',
            headers=headers,
            params=params
        )
        data = response.json()
    
    if not data.get('videos'):
        raise Exception("No videos found")
    
    video = data['videos'][0]
    
    video_file = None
    for file in video['video_files']:
        if file['quality'] in ['hd', 'sd']:
            video_file = file
            break
    
    if not video_file:
        video_file = video['video_files'][0]
    
    print(f"Downloading video...")
    video_response = requests.get(video_file['link'], stream=True)
    
    with open('background.mp4', 'wb') as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print("Background video downloaded!")
    return 'background.mp4'

async def generate_voiceover_async(text):
    print("Generating voiceover with Edge TTS...")
    
    voice = "en-US-GuyNeural"
    
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate="+5%",
        pitch="+0Hz"
    )
    
    await communicate.save("voiceover.mp3")
    
    print(f"Voiceover generated!")
    return 'voiceover.mp3'

def generate_voiceover(text):
    return asyncio.run(generate_voiceover_async(text))

def create_video():
    print("Starting video creation...")
    
    with open('script.json', 'r', encoding='utf-8') as f:
        script_data = json.load(f)
    
    story_text = script_data['story']
    
    voiceover_file = generate_voiceover(story_text)
    background_file = download_pexels_video()
    
    print("Loading clips...")
    background = VideoFileClip(background_file)
    audio = AudioFileClip(voiceover_file)
    
    duration = audio.duration
    print(f"Duration: {duration:.1f}s")
    
    if background.duration < duration:
        n_loops = int(duration / background.duration) + 1
        background = background.loop(n=n_loops)
    
    background = background.subclip(0, duration)
    
    print("Resizing to 1080x1920...")
    background = background.resize(height=1920)
    
    w, h = background.size
    x_center = w / 2
    x1 = x_center - 540
    x2 = x_center + 540
    background = background.crop(x1=int(x1), x2=int(x2), y1=0, y2=1920)
    
    final_video = background.set_audio(audio)
    
    print("Exporting final video...")
    final_video.write_videofile(
        'final_video.mp4',
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='medium',
        threads=4
    )
    
    print("Video created successfully!")
    
    background.close()
    audio.close()
    
    return 'final_video.mp4'

if __name__ == "__main__":
    create_video()
