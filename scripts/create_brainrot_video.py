import os
import json
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ColorClip
import requests

def download_character_video(character_name):
    """Download stock video for character from Pexels"""
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print(f"Warning: PEXELS_API_KEY not found, using solid color background")
        return None
    
    queries = {
        "Skibidi Toilet": "toilet funny",
        "Cappuccina": "coffee cup animated",
        "Tung Tung Sahur": "monkey banana funny",
        "Mr Pen Pineapple": "pineapple cartoon"
    }
    
    query = queries.get(character_name, "animated character")
    
    try:
        headers = {'Authorization': api_key}
        params = {'query': query, 'orientation': 'portrait', 'per_page': 5}
        
        response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params, timeout=10)
        data = response.json()
        
        if data.get('videos'):
            video_file = data['videos'][0]['video_files'][0]
            video_data = requests.get(video_file['link'], timeout=30).content
            
            filename = f"{character_name.replace(' ', '_')}.mp4"
            with open(filename, 'wb') as f:
                f.write(video_data)
            return filename
    except Exception as e:
        print(f"Warning: Could not download video for {character_name}: {e}")
    
    return None

async def generate_voiceover_async(text, voice, output_file):
    """Generate voiceover using Edge TTS"""
    communicate = edge_tts.Communicate(text, voice, rate="+15%")
    await communicate.save(output_file)
    return output_file

def create_scene_clip(scene, scene_num):
    """Create video clip for a scene"""
    
    character = scene['character']
    dialogue = scene['dialogue']
    action = scene.get('action', '')
    voice = scene.get('voice', 'en-US-GuyNeural')
    
    print(f"  Scene {scene_num}: {character} - {dialogue[:40]}...")
    
    # Generate voiceover
    voice_file = f"scene_{scene_num}.mp3"
    asyncio.run(generate_voiceover_async(dialogue, voice, voice_file))
    
    audio = AudioFileClip(voice_file)
    duration = audio.duration
    
    # Try to get character video
    video_file = download_character_video(character)
    
    if video_file and os.path.exists(video_file):
        print(f"    Using video: {video_file}")
        video = VideoFileClip(video_file)
        if video.duration < duration:
            loops = int(duration / video.duration) + 1
            clips_to_loop = [video] * loops
            video = concatenate_videoclips(clips_to_loop)
        video = video.subclipped(0, duration)
    else:
        # Fallback: colored background
        print(f"    Using solid color background")
        colors = {
            "Skibidi Toilet": (30, 30, 30),
            "Cappuccina": (139, 69, 19),
            "Tung Tung Sahur": (255, 215, 0),
            "Mr Pen Pineapple": (255, 165, 0)
        }
        color = colors.get(character, (50, 50, 50))
        video = ColorClip(size=(1080, 1920), color=color, duration=duration)
    
    # Resize and crop to 1080x1920
    video = video.resized(height=1920)
    w = video.w
    if w > 1080:
        x1 = int(w/2 - 540)
        x2 = int(w/2 + 540)
        video = video.cropped(x1=x1, x2=x2, y1=0, y2=1920)
    elif w < 1080:
        video = video.resized(width=1080)
    
    # Add text overlay with Ubuntu-compatible font
    try:
        txt = TextClip(
            text=f"{character}:\n{dialogue[:80]}",
            font='DejaVu-Sans-Bold',  # Ubuntu default font
            font_size=50,
            color='white',
            stroke_color='black',
            stroke_width=2,
            size=(1000, None),
            method='caption'
        )
    except Exception as e:
        print(f"    Warning: Could not create text overlay: {e}")
        # Fallback: try without stroke
        txt = TextClip(
            text=f"{character}:\n{dialogue[:80]}",
            font='DejaVu-Sans-Bold',
            font_size=50,
            color='white',
            size=(1000, None),
            method='caption'
        )
    
    txt = txt.with_position(('center', 1600)).with_duration(duration)
    
    final = CompositeVideoClip([video, txt])
    final = final.with_audio(audio)
    
    return final

def create_brainrot_video():
    """Create brainrot short video from script"""
    
    print("Creating brainrot short video...")
    
    if not os.path.exists('brainrot_short.json'):
        raise FileNotFoundError("brainrot_short.json not found. Run generate_brainrot_short.py first")
    
    with open('brainrot_short.json', 'r') as f:
        script = json.load(f)
    
    print(f"Title: {script['title']}")
    print(f"Characters: {', '.join(script['characters'])}")
    print(f"Scenes: {len(script['scenes'])}")
    
    clips = []
    
    for i, scene in enumerate(script['scenes'], 1):
        print(f"\n🎬 Creating scene {i}/{len(script['scenes'])}...")
        try:
            clip = create_scene_clip(scene, i)
            clips.append(clip)
        except Exception as e:
            print(f"❌ Error creating scene {i}: {e}")
            print(f"   Skipping scene...")
            continue
    
    if not clips:
        raise Exception("No clips were created successfully")
    
    print("\n🎞️ Combining all scenes...")
    final = concatenate_videoclips(clips, method="compose")
    
    print("💾 Exporting video...")
    final.write_videofile(
        'brainrot_short.mp4',
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='fast',
        threads=4
    )
    
    print("✅ Video created successfully!")
    print(f"📹 Output: brainrot_short.mp4")
    print(f"⏱️ Duration: {final.duration:.1f}s")
    
    for clip in clips:
        clip.close()
    final.close()
    
    return 'brainrot_short.mp4'

if __name__ == "__main__":
    create_brainrot_video()
